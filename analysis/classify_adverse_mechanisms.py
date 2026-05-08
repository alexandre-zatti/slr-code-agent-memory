#!/usr/bin/env python3
"""Classify search adverse/degradation evidence mechanisms."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "extraction" / "extracted-data.tsv"
OUT_CLASSIFICATION = ROOT / "analysis" / "adverse-mechanism-classification.tsv"
OUT_SUMMARY = ROOT / "analysis" / "adverse-mechanism-summary.md"

MECHANISM_PATTERNS = {
    "retrieval_or_memory_noise": r"noise|noisy|irrelevant|retrieval|mismatch|negative transfer|misapplied|distract|contaminat|pollut|interference|conflict",
    "memory_growth_or_context_pressure": r"memory growth|context|window|prompt growth|large memory|size|scalability|scaling|too many|k>|retrieved.*too",
    "cost_or_runtime_overhead": r"cost|token|latency|runtime|wall[- ]?clock|overhead|expensive|compute|gpu|resource|time",
    "benchmark_or_domain_generalization": r"benchmark|subset|domain|dataset|task selection|representative|generaliz|external validity|proprietary|internal|single repository|small",
    "evaluation_or_judge_validity": r"llm[- ]?as[- ]?judge|judge|scorer|grader|evaluation|metric|manual|human evaluation|subjectiv|rubric|annotation",
    "model_or_provider_dependence": r"model|backbone|llm|gpt|claude|qwen|deepseek|gemini|provider|temperature",
    "safety_or_security_risk": r"safety|security|sandbox|vulnerab|attack|red[- ]?team|exploit|constraint|violation|harm|jailbreak",
    "verification_or_correctness_failure": r"correctness|incorrect|fail|failure|regression|compile|test|verifier|verification|bug|unresolved|pass[- ]?to[- ]?fail",
    "human_or_workflow_dependence": r"human|manual|operator|engineer|intervention|review|workflow|domain expert",
    "hardware_or_platform_dependence": r"gpu|cuda|nvidia|a100|h100|a40|a6000|trainium|hardware|platform|browser|android|kernel|docker",
}


def load_architecture_rows() -> list[dict[str, str]]:
    with IN_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return [
        row
        for row in rows
        if row["architecture_denominator_decision"] == "include_architecture"
    ]


def evidence_text(row: dict[str, str]) -> str:
    fields = [
        "limitacoes",
        "ameacas_validade",
        "custo_vs_baseline",
        "desempenho_vs_baseline",
        "resultado_principal",
    ]
    return " ".join(row[field] for field in fields)


def classify(row: dict[str, str]) -> list[str]:
    if row["resultado_negativo"] != "sim":
        return ["no_adverse_evidence"]
    text = evidence_text(row).lower()
    labels = [
        label
        for label, pattern in MECHANISM_PATTERNS.items()
        if re.search(pattern, text)
    ]
    return labels or ["other_adverse_evidence"]


def main() -> None:
    rows = load_architecture_rows()
    output_rows = []
    class_counter: Counter[str] = Counter()
    grouped: dict[str, list[str]] = defaultdict(list)

    for row in rows:
        labels = classify(row)
        for label in labels:
            class_counter[label] += 1
            grouped[label].append(f"{row['included_id']} {row['id']}")
        output_rows.append(
            {
                "included_id": row["included_id"],
                "id": row["id"],
                "title": row["titulo"],
                "resultado_negativo": row["resultado_negativo"],
                "adverse_mechanism_classes": ";".join(labels),
                "controlled_comparison_status": row["controlled_comparison_status"],
                "architecture_status": row["architecture_status"],
                "limitacoes": row["limitacoes"],
                "ameacas_validade": row["ameacas_validade"],
                "custo_vs_baseline": row["custo_vs_baseline"],
            }
        )

    with OUT_CLASSIFICATION.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "included_id",
            "id",
            "title",
            "resultado_negativo",
            "adverse_mechanism_classes",
            "controlled_comparison_status",
            "architecture_status",
            "limitacoes",
            "ameacas_validade",
            "custo_vs_baseline",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(output_rows)

    lines = [
        "# Search Adverse Mechanism Summary",
        "",
        "Generated from `extraction/extracted-data.tsv` on 2026-04-29.",
        "Classes are non-exclusive except `no_adverse_evidence`.",
        "",
        "| Class | N | Studies |",
        "| --- | ---: | --- |",
    ]
    for value, count in sorted(class_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} | {'; '.join(sorted(grouped[value]))} |")

    OUT_SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_CLASSIFICATION.relative_to(ROOT)}")
    print(f"wrote {OUT_SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
