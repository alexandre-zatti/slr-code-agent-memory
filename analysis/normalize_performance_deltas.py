#!/usr/bin/env python3
"""Normalize representative search performance evidence for SQ3.

This script produces a synthesis scaffold, not a meta-analysis. Each broad
controlled record receives one representative effect statement. When possible,
the representative effect favors an explicit no-memory/no-persistence ablation;
otherwise it uses the clearest external-baseline comparison already recorded in
the extraction table. Heterogeneous metrics are preserved through unit and
metric-family fields instead of being pooled.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path
from typing import TypedDict


ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "analysis" / "performance-delta-candidates.tsv"
OUT_TSV = ROOT / "analysis" / "performance-normalized.tsv"
OUT_MD = ROOT / "analysis" / "performance-normalized-summary.md"


class NormalizedEffect(TypedDict):
    metric_family: str
    comparison_scope: str
    normalized_delta_type: str
    normalized_delta_value: str
    normalized_delta_unit: str
    direction: str
    normalization_status: str
    manual_note: str


def effect(
    metric_family: str,
    comparison_scope: str,
    normalized_delta_type: str,
    normalized_delta_value: str,
    normalized_delta_unit: str,
    direction: str,
    normalization_status: str,
    manual_note: str,
) -> NormalizedEffect:
    return {
        "metric_family": metric_family,
        "comparison_scope": comparison_scope,
        "normalized_delta_type": normalized_delta_type,
        "normalized_delta_value": normalized_delta_value,
        "normalized_delta_unit": normalized_delta_unit,
        "direction": direction,
        "normalization_status": normalization_status,
        "manual_note": manual_note,
    }


OVERRIDES: dict[str, NormalizedEffect] = {
    "I002": effect(
        "task_success_or_quality",
        "self_improvement_transfer",
        "qualitative_outperformance",
        "NR",
        "qualitative",
        "positive",
        "qualitative_only",
        "Table-level transfer improvement is reported, but the extracted text lacks a comparable numeric delta.",
    ),
    "I012": effect(
        "optimization_score",
        "memory_ablation",
        "absolute_score_delta",
        "4.3",
        "score_points",
        "positive",
        "normalized_manual",
        "Removing refinement reduces out-of-distribution macro from 74.8 to 70.5; effect recorded as full minus ablated.",
    ),
    "I015": effect(
        "preference_or_judge_score",
        "external_nonmemory_baseline",
        "absolute_proportion_delta",
        "0.24",
        "proportion_points",
        "positive",
        "normalized_manual",
        "Representative A/B preference delta uses accuracy: 0.50 vs 0.26.",
    ),
    "I017": effect(
        "task_success_or_accuracy",
        "self_improvement_baseline",
        "absolute_percentage_point_delta",
        "16.5",
        "percentage_points",
        "positive",
        "normalized_manual",
        "Polyglot improves from 14.2% to 30.7%; SWE-bench comparison remains qualitative in extracted text.",
    ),
    "I019": effect(
        "program_discovery_score",
        "external_nonmemory_baseline",
        "qualitative_outperformance",
        "NR",
        "qualitative",
        "positive",
        "insufficient_numeric_baseline",
        "Baseline scores are recorded, but the EvoLattice absolute score is not in the extracted text.",
    ),
    "I020": effect(
        "task_success_or_accuracy",
        "external_nonmemory_baseline",
        "absolute_percentage_point_delta",
        "17.8",
        "percentage_points",
        "positive",
        "normalized_manual",
        "Claude Compilation@1 improves from 57.9% to 75.7%.",
    ),
    "I021": effect(
        "task_success_or_accuracy",
        "memory_ablation",
        "absolute_percentage_point_delta",
        "6.4",
        "percentage_points",
        "positive",
        "normalized_manual",
        "Removing the experience module drops resolved rate from 47.7% to 41.3%.",
    ),
    "I024": effect(
        "efficiency_or_resource_use",
        "self_improvement_external_baseline",
        "resource_reduction",
        "58.0",
        "percent_reduction",
        "positive",
        "normalized_manual",
        "CPU-hour reduction on SWE-Verified-60: 517 vs DGM 1231, computed as (1231-517)/1231.",
    ),
    "I025": effect(
        "task_success_or_accuracy",
        "external_nonmemory_baseline",
        "reported_absolute_delta",
        "4.9",
        "percentage_points_reported_as_percent",
        "positive",
        "normalized_manual",
        "Extraction labels +4.9% Acc@5 absolute versus LocAgent; unit retained as reported.",
    ),
    "I027": effect(
        "task_success_or_accuracy",
        "external_nonmemory_baseline",
        "absolute_percentage_point_delta",
        "4.2",
        "percentage_points",
        "positive",
        "normalized_manual",
        "Claude 4 Sonnet Lingxi reports 74.60% versus OpenHands/Augment at 70.40%.",
    ),
    "I030": effect(
        "benchmark_score",
        "memory_ablation",
        "absolute_score_delta",
        "1.85",
        "score_points",
        "positive",
        "normalized_manual",
        "IaC-Eval full MACOG 74.02 versus -Memory Curator 72.17.",
    ),
    "I031": effect(
        "task_success_or_accuracy",
        "memory_ablation",
        "absolute_percentage_point_delta",
        "4.6",
        "percentage_points",
        "positive",
        "normalized_manual",
        "Gemini-2.5-flash SWE-bench Verified: 38.8% versus 34.2% No Memory.",
    ),
    "I033": effect(
        "security_or_safety_rate",
        "memory_ablation",
        "reported_score_delta",
        "11.2",
        "points",
        "mixed",
        "normalized_manual",
        "Largest reported security-rate gain is +11.2; pass rate can decrease for qwen3-coder-plus.",
    ),
    "I035": effect(
        "code_quality_score",
        "memory_ablation",
        "absolute_score_delta",
        "0.66",
        "score_points",
        "positive",
        "normalized_manual",
        "Qwen3-Coder code-quality score improves from 4.23 to 4.89.",
    ),
    "I038": effect(
        "task_success_or_accuracy",
        "external_nonmemory_baseline",
        "absolute_score_delta",
        "19.5",
        "points",
        "positive",
        "normalized_manual",
        "Representative EESR gain: Finance GPT-4o-mini VALID from 41.5 to 61.0.",
    ),
    "I041": effect(
        "task_success_or_accuracy",
        "memory_ablation",
        "absolute_percentage_point_delta",
        "9.0",
        "percentage_points",
        "positive",
        "normalized_manual",
        "Removing experience drops Exact-Match from 97% to 88%.",
    ),
    "I043": effect(
        "optimization_success_rate",
        "memory_ablation",
        "absolute_percentage_point_delta",
        "15.0",
        "percentage_points",
        "positive",
        "normalized_manual",
        "Removing cross-task skill memory drops Fast@1.2 from 71% to 56%.",
    ),
    "I044": effect(
        "task_success_or_accuracy",
        "initial_agent_baseline",
        "absolute_percentage_point_delta",
        "11.0",
        "percentage_points",
        "positive",
        "normalized_manual",
        "SWE-bench Lite AgentDevel 22.0% versus base 11.0%.",
    ),
    "I045": effect(
        "preference_or_win_rate",
        "initial_agent_baseline",
        "absolute_percentage_point_delta",
        "36.5",
        "percentage_points",
        "positive",
        "normalized_manual",
        "Parent-conditioned operators win 48.7% of tournaments versus Initial proposals at 12.2%.",
    ),
    "I047": effect(
        "optimization_gap",
        "external_nonmemory_baseline",
        "absolute_gap_reduction",
        "0.95",
        "score_points",
        "positive_lower_is_better",
        "normalized_manual",
        "BBOB average gap is 0.007 versus ReEvo 0.957; lower gap is better.",
    ),
    "I048": effect(
        "repair_success_count",
        "memory_guided_baseline",
        "absolute_success_count_delta",
        "3",
        "bugs_of_6",
        "positive",
        "normalized_manual",
        "Memory-guided repair succeeds on 4/6 bugs versus baseline 1/6.",
    ),
    "I049": effect(
        "security_or_repair_success",
        "memory_ablation",
        "absolute_percentage_point_delta",
        "9.1",
        "percentage_points",
        "positive",
        "normalized_manual",
        "Removing memory drops Gemini-2.5-pro CyBench from 59.1% to 50.0%.",
    ),
    "I050": effect(
        "quality_efficiency_tradeoff",
        "external_nonmemory_baseline",
        "quality_retention",
        "90",
        "percent_of_baseline_quality",
        "near_parity_with_efficiency_gain",
        "normalized_manual",
        "MCP Agent reaches 90% of Explorer quality while using 10 times fewer tokens.",
    ),
    "I052": effect(
        "aggregate_task_score",
        "memory_ablation",
        "absolute_score_delta",
        "0.04",
        "score_points",
        "positive",
        "normalized_manual",
        "Complementary RL with experience averages 0.82 versus 0.78 without experience.",
    ),
    "I053": effect(
        "optimization_score",
        "memory_ablation",
        "absolute_score_delta",
        "5.02",
        "points",
        "positive",
        "normalized_manual",
        "GPT-5 full CSE MI 68.10% versus 63.08% without memory.",
    ),
    "I054": effect(
        "optimization_cost_or_objective",
        "knowledge_ablation",
        "lower_is_better_delta",
        "251",
        "cycles_reduced",
        "positive_lower_is_better",
        "normalized_manual",
        "Knowledge ablation worsens Kernel Engineering from 1350 to 1601 cycles; effect recorded as cycles avoided.",
    ),
    "I055": effect(
        "model_training_metric",
        "memory_ablation",
        "reported_relative_delta",
        "3",
        "relative_percent",
        "positive",
        "low_confidence",
        "Removing persistent memory produced about 3% worse performance; authors caution the result is not statistically meaningful.",
    ),
    "I056": effect(
        "task_success_or_quality",
        "memory_ablation",
        "qualitative_outperformance",
        "NR",
        "qualitative",
        "positive",
        "qualitative_only",
        "Lesson-based context consistently outperforms raw trajectories and vanilla context-free agents in extracted text.",
    ),
    "I058": effect(
        "task_success_or_accuracy",
        "retrieval_ablation",
        "absolute_percentage_point_delta",
        "57.02",
        "percentage_points",
        "positive",
        "normalized_manual",
        "Truck CAN Signal Qwen2.5-7B pass@1 improves from 39.62% to 96.64%.",
    ),
    "I059": effect(
        "task_success_or_accuracy",
        "memory_ablation",
        "reported_absolute_delta",
        "2.7",
        "percentage_points_reported_as_percent",
        "positive",
        "normalized_manual",
        "Average resolve-rate gain is reported as +2.7% versus agents without EET.",
    ),
    "I060": effect(
        "optimization_score",
        "external_nonmemory_baseline",
        "qualitative_outperformance",
        "NR",
        "qualitative",
        "positive",
        "insufficient_numeric_baseline",
        "The extracted text says EffiSkill outperforms listed baselines but does not include a comparable baseline value.",
    ),
    "I061": effect(
        "task_success_or_accuracy",
        "external_nonmemory_baseline",
        "absolute_percentage_point_delta",
        "3.7",
        "percentage_points",
        "positive",
        "normalized_manual",
        "Representative SWE-bench Multimodal gain: GPT-5.1 33.1% versus GUIRepair 29.4%.",
    ),
    "I064": effect(
        "efficiency_speedup",
        "memory_ablation",
        "multiplicative_speedup",
        "1.67",
        "x_speedup",
        "positive",
        "normalized_manual",
        "KernelBlaster reports 1.67x versus no_mem_agent.",
    ),
    "I065": effect(
        "efficiency_speedup",
        "external_nonmemory_baseline",
        "relative_speedup_delta",
        "79.5",
        "percent",
        "positive",
        "normalized_manual",
        "Compared with STARK, KernelSkill improves average speedup by 79.5% on Level 1.",
    ),
    "I067": effect(
        "coding_benchmark_score",
        "memory_ablation",
        "absolute_score_delta",
        "18.45",
        "points",
        "positive",
        "normalized_manual",
        "KodCode gains range up to +18.45 points.",
    ),
    "I068": effect(
        "repository_change_quality",
        "memory_ablation",
        "absolute_percentage_point_delta",
        "19.0",
        "percentage_points",
        "positive",
        "normalized_manual",
        "File IoU improves from 61% to 80% in seq-all.",
    ),
    "I069": effect(
        "task_success_or_accuracy",
        "memory_ablation",
        "absolute_score_delta",
        "25.32",
        "pass_at_1_points",
        "positive",
        "normalized_manual",
        "NdonnxEval Pass@1 with Qwen2.5-Coder: 52.54 versus Naive RAG 27.22.",
    ),
    "I070": effect(
        "task_success_or_accuracy",
        "memory_ablation",
        "absolute_score_delta",
        "14.5",
        "accuracy_points",
        "positive",
        "normalized_manual",
        "Qwen2.5-7B average accuracy improves from 57.1 to 71.6.",
    ),
    "I073": effect(
        "task_success_or_accuracy",
        "memory_transfer",
        "absolute_proportion_delta",
        "0.037",
        "pass_at_3_proportion_points",
        "positive",
        "normalized_manual",
        "GPT-5-mini zero-shot average Pass@3 0.523 versus MTL Insight 0.560.",
    ),
    "I074": effect(
        "task_success_or_accuracy",
        "experience_variant_comparison",
        "reported_absolute_delta",
        "6.35",
        "pass_at_1_points",
        "positive",
        "normalized_manual",
        "External Experience improves over Internal Experience by 6.35 Pass@1 points.",
    ),
    "I076": effect(
        "game_generation_quality",
        "external_nonmemory_baseline",
        "absolute_score_delta",
        "6.2",
        "points",
        "positive",
        "normalized_manual",
        "OpenGame with Claude Sonnet 4.6 improves Intent Alignment by 6.2 points over Cursor.",
    ),
    "I077": effect(
        "task_success_or_accuracy",
        "memory_ablation",
        "absolute_score_delta",
        "2.8",
        "points",
        "positive",
        "normalized_manual",
        "OpenSage memory ablation: 59.0 versus NoMem 56.2 on SWE-Bench Pro.",
    ),
    "I078": effect(
        "task_success_or_accuracy",
        "external_nonmemory_baseline",
        "absolute_percentage_point_delta",
        "10.4",
        "percentage_points",
        "positive",
        "normalized_manual",
        "GPT-4o Pass@1 improves over Agentless from 27.3% to 37.7%.",
    ),
    "I079": effect(
        "task_success_or_accuracy",
        "retrieval_ablation",
        "absolute_score_delta",
        "0.066",
        "accuracy_points",
        "positive",
        "normalized_manual",
        "LiveCodeBench V1-4: Reasoning Memory 0.471 versus Length Scaling 0.405.",
    ),
    "I080": effect(
        "task_success_or_accuracy",
        "external_nonmemory_baseline",
        "lower_bound_score_delta",
        "7.0",
        "points",
        "positive",
        "lower_bound",
        "Extracted text states ReCreate improves over ADAS/AgentSquare averages by more than seven points.",
    ),
    "I081": effect(
        "research_workflow_score",
        "memory_ablation",
        "absolute_score_delta",
        "18.7",
        "score_points",
        "positive",
        "normalized_manual",
        "Removing the full Global Training Context drops SUPER Overall from 34.7 to 16.0.",
    ),
    "I082": effect(
        "efficiency_speedup",
        "external_nonmemory_baseline",
        "multiplicative_speedup",
        "4.3",
        "x_speedup",
        "positive",
        "normalized_manual",
        "RuleFlow reaches a maximum speedup of 4.3x over DIAS.",
    ),
    "I083": effect(
        "multi_agent_task_score",
        "memory_topology_ablation",
        "absolute_score_delta",
        "2.89",
        "score_points",
        "positive",
        "normalized_manual",
        "Coding topology ablation: local memory TS 49.68 versus shared 46.79.",
    ),
    "I085": effect(
        "task_success_or_accuracy",
        "external_nonmemory_baseline",
        "absolute_percentage_point_delta",
        "21.3",
        "percentage_points",
        "positive",
        "normalized_manual",
        "SEVerA exceeds the best constrained-decoding method on GSM-Symbolic by 21.3 percentage points.",
    ),
    "I086": effect(
        "task_success_or_accuracy",
        "external_nonmemory_baseline",
        "absolute_percentage_point_delta",
        "61.8",
        "percentage_points",
        "positive",
        "normalized_manual",
        "SelfEvolve reaches 92.7% Pass@1 versus AutoGen at 30.9%; TDD ablation is noted separately in raw evidence.",
    ),
    "I090": effect(
        "task_success_or_accuracy",
        "case_base_ablation",
        "absolute_score_delta",
        "6.67",
        "pass_score_points",
        "positive",
        "normalized_manual",
        "HumanEval-Hard TextBFGS 97.78 versus without case base 91.11.",
    ),
    "I091": effect(
        "research_workflow_score",
        "memory_ablation",
        "absolute_score_delta",
        "6.41",
        "points",
        "positive",
        "normalized_manual",
        "Removing File-as-Bus drops PaperBench by 6.41 points.",
    ),
    "I093": effect(
        "benchmark_faithfulness_or_guardrail",
        "memory_or_specification_ablation",
        "count_improved_cases",
        "15/20",
        "cases",
        "positive",
        "count_only",
        "ProjectGuard improves Claude IF50 on 15 of 20 papers; single-shot comparison remains a boundary adverse result.",
    ),
    "I095": effect(
        "research_workflow_score",
        "memory_ablation",
        "absolute_score_delta",
        "18.7",
        "score_points",
        "positive",
        "normalized_manual",
        "Ablating Global Training Context drops SUPER overall from 34.7 to 16.0.",
    ),
}


def load_rows() -> list[dict[str, str]]:
    with IN_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def default_scope(row: dict[str, str]) -> str:
    status = row["controlled_comparison_status"]
    if status == "yes_no_persistence_or_memory_ablation":
        return "memory_ablation_or_no_memory_baseline"
    if status == "yes_nonmemory_external_baseline":
        return "external_nonmemory_baseline"
    return "other_controlled_comparison"


def infer_metric_family(text: str) -> str:
    lower = text.lower()
    if any(token in lower for token in ["security", "unsafe", "violation"]):
        return "security_or_safety_rate"
    if any(
        token in lower
        for token in [
            "pass@",
            "pass rate",
            "resolve",
            "resolved",
            "accuracy",
            "compilation",
            "success",
            "exact-match",
        ]
    ):
        return "task_success_or_accuracy"
    if any(token in lower for token in ["speedup", "faster", "cpu-hour", "tokens", "tool calls"]):
        return "efficiency_or_resource_use"
    if any(token in lower for token in ["quality", "judge", "preference", "win"]):
        return "preference_or_quality_score"
    if any(token in lower for token in ["score", "bleu", "elo", "eesr", "mi "]):
        return "benchmark_score"
    return "task_success_or_accuracy"


def parse_signed_number(value: str) -> float | None:
    match = re.search(r"([+-]?)\s*(\d+(?:\.\d+)?)", value)
    if not match:
        return None
    sign = -1.0 if match.group(1) == "-" else 1.0
    return sign * float(match.group(2))


def auto_effect(row: dict[str, str]) -> NormalizedEffect:
    primary_type = row["primary_delta_type"]
    primary = row["primary_delta_candidate"]
    text = row["desempenho_vs_baseline"]
    metric_family = infer_metric_family(text)
    scope = default_scope(row)

    if primary_type == "signed_percentage_points":
        value = parse_signed_number(primary)
        if value is not None:
            return effect(
                metric_family,
                scope,
                "reported_signed_delta",
                f"{value:g}",
                "percentage_points",
                "positive" if value > 0 else "negative" if value < 0 else "neutral",
                "normalized_candidate",
                f"Representative signed percentage-point candidate retained from extraction: {primary}.",
            )
    if primary_type == "signed_percent":
        value = parse_signed_number(primary)
        if value is not None:
            return effect(
                metric_family,
                scope,
                "reported_signed_percent",
                f"{value:g}",
                "percent",
                "positive" if value > 0 else "negative" if value < 0 else "neutral",
                "normalized_candidate",
                f"Representative signed percent candidate retained from extraction: {primary}.",
            )
    if primary_type == "multiplicative":
        value = parse_signed_number(primary)
        if value is not None:
            return effect(
                metric_family,
                scope,
                "multiplicative_speedup",
                f"{value:g}",
                "x_speedup",
                "positive",
                "normalized_candidate",
                f"Representative multiplicative candidate retained from extraction: {primary}.",
            )

    return effect(
        metric_family,
        scope,
        "not_normalized",
        "NR",
        "NR",
        "unknown",
        "needs_manual_normalization",
        f"Primary candidate `{primary_type}: {primary}` needs manual interpretation before use.",
    )


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    normalized = OVERRIDES.get(row["included_id"], auto_effect(row))
    return {
        "included_id": row["included_id"],
        "id": row["id"],
        "title": row["title"],
        "controlled_comparison_status": row["controlled_comparison_status"],
        "benchmark_markers": row["benchmark_markers"],
        "metric_family": normalized["metric_family"],
        "comparison_scope": normalized["comparison_scope"],
        "normalized_delta_type": normalized["normalized_delta_type"],
        "normalized_delta_value": normalized["normalized_delta_value"],
        "normalized_delta_unit": normalized["normalized_delta_unit"],
        "direction": normalized["direction"],
        "normalization_status": normalized["normalization_status"],
        "manual_note": normalized["manual_note"],
        "raw_delta_candidates": row["all_delta_candidates"],
        "raw_evidence": row["desempenho_vs_baseline"],
    }


def write_tsv(rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "included_id",
        "id",
        "title",
        "controlled_comparison_status",
        "benchmark_markers",
        "metric_family",
        "comparison_scope",
        "normalized_delta_type",
        "normalized_delta_value",
        "normalized_delta_unit",
        "direction",
        "normalization_status",
        "manual_note",
        "raw_delta_candidates",
        "raw_evidence",
    ]
    with OUT_TSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_summary(rows: list[dict[str, str]]) -> None:
    status_counter = Counter(row["normalization_status"] for row in rows)
    direction_counter = Counter(row["direction"] for row in rows)
    unit_counter = Counter(row["normalized_delta_unit"] for row in rows)
    family_counter = Counter(row["metric_family"] for row in rows)
    scope_counter = Counter(row["comparison_scope"] for row in rows)
    numeric_rows = [
        row
        for row in rows
        if row["normalized_delta_value"] != "NR"
        and row["normalization_status"] not in {"count_only"}
        and "/" not in row["normalized_delta_value"]
    ]

    lines = [
        "# Search Performance Normalization Summary",
        "",
        "Generated from `analysis/performance-delta-candidates.tsv` on 2026-04-29.",
        "This artifact supports SQ3 synthesis only. It selects one representative effect per broad controlled record and preserves heterogeneous units instead of pooling effects.",
        "",
        "## Coverage",
        "",
        f"- Broad controlled records: {len(rows)}",
        f"- Records with a numeric representative value: {len(numeric_rows)}",
        f"- Records without a scalar numeric representative value: {len(rows) - len(numeric_rows)}",
        "",
        "## Normalization Status",
        "",
        "| Status | N |",
        "| --- | ---: |",
    ]
    for value, count in sorted(status_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} |")

    lines.extend(["", "## Direction", "", "| Direction | N |", "| --- | ---: |"])
    for value, count in sorted(direction_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} |")

    lines.extend(["", "## Metric Family", "", "| Metric family | N |", "| --- | ---: |"])
    for value, count in sorted(family_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} |")

    lines.extend(["", "## Comparison Scope", "", "| Comparison scope | N |", "| --- | ---: |"])
    for value, count in sorted(scope_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} |")

    lines.extend(["", "## Unit", "", "| Unit | N |", "| --- | ---: |"])
    for value, count in sorted(unit_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} |")

    lines.extend(
        [
            "",
            "## Use Notes",
            "",
            "- Do not pool `normalized_delta_value` across rows; metric families and units are heterogeneous.",
            "- For strict controlled rows, representative effects prefer explicit memory/no-persistence ablations when available.",
            "- Negative and mixed evidence is retained rather than filtered out.",
            "- `qualitative_only`, `insufficient_numeric_baseline`, `count_only`, `lower_bound`, and `low_confidence` rows require prose-level handling in SQ3.",
        ]
    )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_rows = load_rows()
    output_rows = [normalize_row(row) for row in source_rows]
    missing = sorted(
        row["included_id"]
        for row in output_rows
        if row["normalization_status"] == "needs_manual_normalization"
    )
    if missing:
        raise SystemExit(f"manual normalization still required for: {', '.join(missing)}")
    write_tsv(output_rows)
    write_summary(output_rows)
    print(f"wrote {OUT_TSV.relative_to(ROOT)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
