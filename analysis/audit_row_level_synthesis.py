#!/usr/bin/env python3
"""Audit search row-level synthesis scaffolds before Results prose."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "analysis" / "row-level-synthesis-audit.md"
SAMPLES = ROOT / "analysis" / "row-level-synthesis-audit-samples.tsv"


class Gate:
    def __init__(self) -> None:
        self.checks: list[tuple[str, str, str]] = []

    @staticmethod
    def _stable_repr(value) -> str:
        if isinstance(value, set):
            return repr(sorted(value))
        if isinstance(value, dict):
            return repr({key: value[key] for key in sorted(value)})
        return repr(value)

    def expect(self, label: str, actual, expected) -> None:
        status = "PASS" if actual == expected else "FAIL"
        actual_text = self._stable_repr(actual)
        expected_text = self._stable_repr(expected)
        self.checks.append((status, label, f"actual `{actual_text}`, expected `{expected_text}`"))

    def pass_note(self, label: str, detail: str) -> None:
        self.checks.append(("PASS", label, detail))

    def warn(self, label: str, detail: str) -> None:
        self.checks.append(("WARN", label, detail))

    @property
    def fail_count(self) -> int:
        return sum(1 for status, _, _ in self.checks if status == "FAIL")

    @property
    def warn_count(self) -> int:
        return sum(1 for status, _, _ in self.checks if status == "WARN")

    @property
    def pass_count(self) -> int:
        return sum(1 for status, _, _ in self.checks if status == "PASS")


def read_tsv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def by_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["id"]: row for row in rows}


def split_classes(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def evidence_snippet(*values: str, max_chars: int = 320) -> str:
    text = " | ".join(v.strip() for v in values if v and v.strip() not in {"NR", "NA"})
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        return text[: max_chars - 3].rstrip() + "..."
    return text or "NR"


def add_sample(
    samples: list[dict[str, str]],
    section: str,
    label: str,
    row: dict[str, str],
    evidence: str,
    status: str = "reviewed",
) -> None:
    samples.append(
        {
            "audit_section": section,
            "label": label,
            "included_id": row.get("included_id", ""),
            "id": row.get("id", ""),
            "title": row.get("title") or row.get("titulo", ""),
            "audit_status": status,
            "evidence_snippet": evidence,
        }
    )


def first_n(rows: list[dict[str, str]], n: int = 3) -> list[dict[str, str]]:
    return sorted(rows, key=lambda r: (r.get("included_id", ""), r.get("id", "")))[:n]


def is_float(value: str) -> bool:
    try:
        float(value)
    except ValueError:
        return False
    return True


def main() -> int:
    gate = Gate()
    samples: list[dict[str, str]] = []

    extracted = read_tsv("extraction/extracted-data.tsv")
    arch = [
        row
        for row in extracted
        if row["architecture_denominator_decision"] == "include_architecture"
    ]
    arch_ids = {row["id"] for row in arch}
    extraction_by_id = by_id(extracted)

    controlled = read_tsv("analysis/controlled-comparison-recode.tsv")
    performance = read_tsv("analysis/performance-normalized.tsv")
    benchmark_records = read_tsv("analysis/benchmark-records.tsv")
    benchmark_inventory = read_tsv("analysis/benchmark-inventory.tsv")
    cost = read_tsv("analysis/cost-evidence-classification.tsv")
    adverse = read_tsv("analysis/adverse-mechanism-classification.tsv")
    certainty = read_tsv("analysis/certainty-sensitivity-records.tsv")

    controlled_by_id = by_id(controlled)
    cost_by_id = by_id(cost)
    adverse_by_id = by_id(adverse)
    certainty_arch = [
        row
        for row in certainty
        if row["architecture_denominator_decision"] == "include_architecture"
    ]
    certainty_by_id = by_id(certainty_arch)

    strict_ids = {
        row["id"]
        for row in controlled
        if row["final_status"] == "yes_no_persistence_or_memory_ablation"
    }
    external_ids = {
        row["id"]
        for row in controlled
        if row["final_status"] == "yes_nonmemory_external_baseline"
    }
    no_comparator_ids = {
        row["id"]
        for row in controlled
        if row["final_status"] == "no_no_persistence_or_nonmemory_baseline"
    }
    broad_ids = strict_ids | external_ids

    gate.expect("architecture rows in extraction", len(arch), 85)
    gate.expect("controlled recode rows", len(controlled), 85)
    gate.expect("controlled recode ID set equals architecture ID set", set(controlled_by_id), arch_ids)
    gate.expect("strict controlled rows", len(strict_ids), 56)
    gate.expect("external/non-memory baseline rows", len(external_ids), 20)
    gate.expect("no-comparator rows", len(no_comparator_ids), 9)
    gate.expect("broad controlled rows", len(broad_ids), 76)

    status_mismatches = [
        row["id"]
        for row in arch
        if row["controlled_comparison_status"] != controlled_by_id[row["id"]]["final_status"]
    ]
    gate.expect("controlled status mismatches between extraction and recode", status_mismatches, [])

    for status in [
        "yes_no_persistence_or_memory_ablation",
        "yes_nonmemory_external_baseline",
        "no_no_persistence_or_nonmemory_baseline",
    ]:
        rows = [row for row in controlled if row["final_status"] == status]
        for row in first_n(rows):
            add_sample(
                samples,
                "controlled_comparison",
                status,
                row,
                evidence_snippet(row["baseline_evidence"], row["performance_evidence"], row["manual_rationale"]),
            )

    performance_ids = {row["id"] for row in performance}
    gate.expect("performance-normalized rows", len(performance), 76)
    gate.expect("performance ID set equals broad controlled ID set", performance_ids, broad_ids)
    gate.expect(
        "performance rows with no-comparator status",
        sorted(performance_ids & no_comparator_ids),
        [],
    )
    status_counts = Counter(row["normalization_status"] for row in performance)
    gate.expect(
        "performance normalization-status counts",
        dict(status_counts),
        {
            "normalized_manual": 47,
            "normalized_candidate": 22,
            "qualitative_only": 2,
            "insufficient_numeric_baseline": 2,
            "low_confidence": 1,
            "lower_bound": 1,
            "count_only": 1,
        },
    )
    scalar_rows = [row for row in performance if is_float(row["normalized_delta_value"])]
    gate.expect("performance scalar numeric rows", len(scalar_rows), 71)
    gate.expect("performance non-scalar rows", len(performance) - len(scalar_rows), 5)
    for label in sorted(status_counts):
        rows = [row for row in performance if row["normalization_status"] == label]
        for row in first_n(rows, 2):
            add_sample(
                samples,
                "performance_normalization",
                label,
                row,
                evidence_snippet(row["manual_note"], row["raw_evidence"], row["raw_delta_candidates"]),
            )

    benchmark_ids = {row["id"] for row in benchmark_records}
    inventory_counts = {row["benchmark_label"]: int(row["n_studies"]) for row in benchmark_inventory}
    gate.expect("benchmark record links", len(benchmark_records), 185)
    gate.expect("benchmark inventory labels", len(benchmark_inventory), 114)
    gate.expect("architecture records without benchmark label", sorted(arch_ids - benchmark_ids), [])
    gate.expect("benchmark records outside architecture denominator", sorted(benchmark_ids - arch_ids), [])
    gate.expect("SWE-bench Verified count", inventory_counts.get("SWE-bench Verified"), 22)
    gate.expect("SWE-bench Lite count", inventory_counts.get("SWE-bench Lite"), 8)
    for label in ["SWE-bench Verified", "SWE-bench Lite", "HumanEval", "MBPP"]:
        rows = [row for row in benchmark_records if row["benchmark_label"] == label]
        for row in first_n(rows, 3):
            add_sample(
                samples,
                "benchmark_normalization",
                label,
                row,
                evidence_snippet(row["raw_benchmarks"]),
            )

    gate.expect("cost classification rows", len(cost), 85)
    gate.expect("cost ID set equals architecture ID set", set(cost_by_id), arch_ids)
    cost_class_counts: Counter[str] = Counter()
    bad_no_cost: list[str] = []
    monetary_without_money: list[str] = []
    token_without_token_evidence: list[str] = []
    for row in cost:
        classes = split_classes(row["cost_evidence_classes"])
        cost_class_counts.update(classes)
        if "no_cost_evidence" in classes and len(classes) > 1:
            bad_no_cost.append(row["id"])
        if "no_cost_evidence" in classes and row["reporta_dados_custo"] != "nao":
            bad_no_cost.append(row["id"])
        money_text = evidence_snippet(row["custo_por_tarefa"], row["custo_vs_baseline"], max_chars=1000)
        if "monetary_cost" in classes and not re.search(r"\$|USD|dollar|cost", money_text, re.I):
            monetary_without_money.append(row["id"])
        token_text = evidence_snippet(
            row["tokens_entrada_por_tarefa"],
            row["tokens_saida_por_tarefa"],
            row["reducao_tokens"],
            row["custo_vs_baseline"],
            max_chars=1000,
        )
        if "token_usage" in classes and not re.search(
            r"\b(token|tokens|prompt|completion|cached|context window|context length)\b",
            token_text,
            re.I,
        ):
            token_without_token_evidence.append(row["id"])
    gate.expect(
        "cost evidence class counts",
        dict(cost_class_counts),
        {
            "cost_reduction_or_tradeoff": 46,
            "token_usage": 27,
            "no_cost_evidence": 26,
            "monetary_cost": 25,
            "runtime_or_latency": 26,
            "compute_or_resource": 14,
        },
    )
    gate.expect("invalid no-cost cost-class rows", sorted(set(bad_no_cost)), [])
    gate.expect("monetary-cost rows lacking monetary/cost evidence text", sorted(monetary_without_money), [])
    gate.expect("token-usage rows lacking token/context evidence text", sorted(token_without_token_evidence), [])
    for label in sorted(cost_class_counts):
        rows = [row for row in cost if label in split_classes(row["cost_evidence_classes"])]
        for row in first_n(rows, 3):
            add_sample(
                samples,
                "cost_classification",
                label,
                row,
                evidence_snippet(
                    row["tokens_entrada_por_tarefa"],
                    row["tokens_saida_por_tarefa"],
                    row["custo_por_tarefa"],
                    row["reducao_tokens"],
                    row["custo_vs_baseline"],
                ),
            )

    gate.expect("adverse mechanism rows", len(adverse), 85)
    gate.expect("adverse ID set equals architecture ID set", set(adverse_by_id), arch_ids)
    adverse_class_counts: Counter[str] = Counter()
    bad_no_adverse: list[str] = []
    for row in adverse:
        classes = split_classes(row["adverse_mechanism_classes"])
        adverse_class_counts.update(classes)
        if "no_adverse_evidence" in classes and len(classes) > 1:
            bad_no_adverse.append(row["id"])
        if "no_adverse_evidence" in classes and row["resultado_negativo"] != "nao":
            bad_no_adverse.append(row["id"])
    gate.expect(
        "adverse mechanism class counts",
        dict(adverse_class_counts),
        {
            "benchmark_or_domain_generalization": 54,
            "model_or_provider_dependence": 54,
            "cost_or_runtime_overhead": 53,
            "evaluation_or_judge_validity": 31,
            "verification_or_correctness_failure": 31,
            "human_or_workflow_dependence": 28,
            "no_adverse_evidence": 26,
            "memory_growth_or_context_pressure": 22,
            "retrieval_or_memory_noise": 21,
            "hardware_or_platform_dependence": 16,
            "safety_or_security_risk": 9,
        },
    )
    gate.expect("invalid no-adverse rows", sorted(set(bad_no_adverse)), [])
    for label in sorted(adverse_class_counts):
        rows = [row for row in adverse if label in split_classes(row["adverse_mechanism_classes"])]
        for row in first_n(rows, 3):
            add_sample(
                samples,
                "adverse_mechanism",
                label,
                row,
                evidence_snippet(row["limitacoes"], row["ameacas_validade"], row["custo_vs_baseline"]),
            )

    gate.expect("certainty architecture rows", len(certainty_arch), 85)
    gate.expect("certainty architecture ID set equals architecture ID set", set(certainty_by_id), arch_ids)
    publication_counts = Counter(row["publication_group"] for row in certainty_arch)
    gate.expect("certainty architecture publication counts", dict(publication_counts), {"preprint": 76, "peer_reviewed": 9})
    quality_threshold_counts = {
        ">=3.0": sum(row["retained_quality_ge_3_0"] == "yes" for row in certainty_arch),
        ">=4.0": sum(row["retained_quality_ge_4_0"] == "yes" for row in certainty_arch),
        ">=4.5": sum(row["retained_quality_ge_4_5"] == "yes" for row in certainty_arch),
        ">=5.0": sum(row["retained_quality_ge_5_0"] == "yes" for row in certainty_arch),
    }
    gate.expect("certainty quality-threshold counts", quality_threshold_counts, {">=3.0": 85, ">=4.0": 83, ">=4.5": 78, ">=5.0": 56})
    controlled_group_counts = Counter(row["controlled_group"] for row in certainty_arch)
    gate.expect(
        "certainty controlled-group counts for architecture rows",
        dict(controlled_group_counts),
        {
            "strict_no_persistence_or_memory_ablation": 56,
            "broad_external_nonmemory_baseline": 20,
            "no_suitable_controlled_comparison": 9,
        },
    )
    for label in sorted(publication_counts):
        rows = [row for row in certainty_arch if row["publication_group"] == label]
        for row in first_n(rows, 3):
            add_sample(
                samples,
                "certainty_sensitivity",
                label,
                row,
                evidence_snippet(row["tipo_venue"], row["venue"], row["quality_band"], row["controlled_group"]),
            )

    sample_fields = [
        "audit_section",
        "label",
        "included_id",
        "id",
        "title",
        "audit_status",
        "evidence_snippet",
    ]
    with SAMPLES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=sample_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(samples)

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    verdict = "FAIL" if gate.fail_count else "PASS"
    lines = [
        "# Search Row-Level Synthesis Audit",
        "",
        f"Generated: {now}",
        "",
        "Scope: row-level gate before writing final search Results and Discussion prose.",
        "",
        f"Verdict: {verdict}",
        "",
        "## Summary",
        "",
        f"- PASS: {gate.pass_count}",
        f"- WARN: {gate.warn_count}",
        f"- FAIL: {gate.fail_count}",
        f"- Stratified reviewed sample rows: {len(samples)}",
        f"- Sample ledger: `{SAMPLES.relative_to(ROOT)}`",
        "",
        "## Checks",
        "",
        "| Status | Check | Detail |",
        "| --- | --- | --- |",
    ]
    for status, label, detail in gate.checks:
        lines.append(f"| {status} | {label.replace('|', '\\|')} | {detail.replace('|', '\\|')} |")

    lines.extend(
        [
            "",
            "## Prose Constraints After This Gate",
            "",
            "- Controlled-effectiveness claims must distinguish strict controlled records (`n=56`) from broad controlled records (`n=76`).",
            "- Performance values are heterogeneous descriptive evidence, not pooled effect sizes.",
            "- Cost and adverse-mechanism classes are nonexclusive; class counts must not be summed to the architecture denominator.",
            "- Benchmark variant aggregation must be named explicitly when used.",
            "- Certainty and sensitivity labels qualify findings; they do not redefine the main corpus.",
            "",
        ]
    )
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {REPORT.relative_to(ROOT)}")
    print(f"wrote {SAMPLES.relative_to(ROOT)}")
    print(f"summary: PASS={gate.pass_count} WARN={gate.warn_count} FAIL={gate.fail_count}")
    return 1 if gate.fail_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
