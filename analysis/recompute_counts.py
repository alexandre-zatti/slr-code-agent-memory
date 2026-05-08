#!/usr/bin/env python3
"""Recompute search post-extraction summary counts.

This script is intentionally conservative. It only computes counts directly
supported by `extraction/extracted-data.tsv` and surfaces fields that still
need manual recomputation instead of inferring final methodological labels.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "extraction" / "extracted-data.tsv"
OUT_MD = ROOT / "analysis" / "post-extraction-recompute.md"
OUT_TSV = ROOT / "analysis" / "post-extraction-recompute-records.tsv"

MISSING = {"", "NR", "NA", "nao_reportado", "not reported", "not_applicable_contextual"}

BENCHMARK_PATTERNS = [
    ("SWE-bench Verified", r"swe[- ]?bench[- ]?verified|swe[- ]?bench v\."),
    ("SWE-Bench Pro", r"swe[- ]?bench[- ]?pro"),
    ("SWE-bench Lite", r"swe[- ]?bench[- ]?lite"),
    ("SWE-Bench-CL", r"swe[- ]?bench[- ]?cl"),
    ("HumanEval", r"humaneval"),
    ("MBPP", r"\bmbpp\b"),
    ("BigCodeBench", r"bigcodebench"),
    ("LiveCodeBench", r"livecodebench"),
    ("WebArena", r"webarena"),
    ("OSWorld", r"osworld"),
    ("AppWorld", r"appworld"),
    ("DS-1000", r"ds[- ]?1000"),
    ("MATH", r"\bmath\b"),
    ("MLE-Bench", r"mle[- ]?bench"),
    ("ALE-Bench", r"ale[- ]?bench"),
    ("PaperBench", r"paperbench"),
    ("ResearchCodeBench", r"researchcodebench"),
    ("ScienceAgentBench", r"scienceagentbench"),
    ("SUPER", r"\bsuper\b"),
    ("KernelBench", r"kernelbench"),
    ("NKIBench", r"nkibench"),
    ("CodeIF-Bench", r"codeif[- ]?bench"),
    ("CoderEval", r"codereval"),
    ("Terminal-Bench", r"terminal[- ]?bench"),
    ("CyberGym", r"cybergym"),
    ("DevOps-Gym", r"devops[- ]?gym"),
    ("DafnyBench", r"dafnybench"),
    ("HumanEvalDafny", r"humanevaldafny"),
    ("tau2-bench", r"tau2[- ]?bench"),
    ("LoCoMo", r"locomo"),
]


def load_rows() -> list[dict[str, str]]:
    with IN_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def is_reported(value: str) -> bool:
    return value.strip() not in MISSING


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "NA"
    return f"{(100 * numerator / denominator):.1f}%"


def count_field(rows: list[dict[str, str]], field: str) -> Counter[str]:
    return Counter(row[field].strip() or "NR" for row in rows)


def markdown_count_table(counter: Counter[str], denominator: int) -> list[str]:
    lines = ["| Value | N | % |", "| --- | ---: | ---: |"]
    for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} | {pct(count, denominator)} |")
    return lines


def benchmark_hits(rows: list[dict[str, str]]) -> Counter[str]:
    hits: Counter[str] = Counter()
    for row in rows:
        haystack = row["benchmarks_utilizados"].lower()
        for label, pattern in BENCHMARK_PATTERNS:
            if re.search(pattern, haystack):
                hits[label] += 1
    return hits


def evaluation_category(value: str) -> str:
    lowered = value.lower()
    if "benchmark" in lowered:
        return "benchmark"
    if "misto" in lowered or "mixed" in lowered:
        return "mixed"
    if "estudo_caso" in lowered or "case" in lowered:
        return "case_study"
    if "study" in lowered or "evaluation" in lowered:
        return "empirical_nonstandard"
    if value.strip() in MISSING:
        return "NR"
    return "other"


def numeric_quality(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def write_record_flags(rows: list[dict[str, str]]) -> None:
    fields = [
        "included_id",
        "id",
        "titulo",
        "study_role",
        "architecture_denominator_decision",
        "architecture_status",
        "tipo_arquitetura",
        "controlled_comparison_status",
        "has_baseline_text",
        "quality_score",
        "quality_status",
        "cost_reporting",
        "negative_result",
        "benchmark_markers",
    ]
    with OUT_TSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for row in rows:
            markers = [
                label
                for label, pattern in BENCHMARK_PATTERNS
                if re.search(pattern, row["benchmarks_utilizados"].lower())
            ]
            score = row["pontuacao_qualidade"].strip()
            writer.writerow(
                {
                    "included_id": row["included_id"],
                    "id": row["id"],
                    "titulo": row["titulo"],
                    "study_role": row["study_role"],
                    "architecture_denominator_decision": row[
                        "architecture_denominator_decision"
                    ],
                    "architecture_status": row["architecture_status"],
                    "tipo_arquitetura": row["tipo_arquitetura"],
                    "controlled_comparison_status": row[
                        "controlled_comparison_status"
                    ],
                    "has_baseline_text": "yes"
                    if is_reported(row["baseline_comparado"])
                    else "no",
                    "quality_score": score,
                    "quality_status": "numeric"
                    if numeric_quality(score) is not None
                    else "needs_manual_score",
                    "cost_reporting": row["reporta_dados_custo"],
                    "negative_result": row["resultado_negativo"],
                    "benchmark_markers": ";".join(markers) if markers else "NR",
                }
            )


def main() -> None:
    rows = load_rows()
    architecture = [
        row
        for row in rows
        if row["architecture_denominator_decision"] == "include_architecture"
    ]
    contextual = [
        row
        for row in rows
        if row["architecture_denominator_decision"] != "include_architecture"
    ]

    pending_control = [
        row
        for row in architecture
        if row["controlled_comparison_status"] == "pending_extraction"
    ]
    strict_control = [
        row
        for row in architecture
        if row["controlled_comparison_status"]
        == "yes_no_persistence_or_memory_ablation"
    ]
    external_control = [
        row
        for row in architecture
        if row["controlled_comparison_status"]
        == "yes_nonmemory_external_baseline"
    ]
    boundary_control = [
        row
        for row in architecture
        if row["controlled_comparison_status"] == "boundary_needs_pdf_review"
    ]
    pending_quality = [
        row for row in architecture if numeric_quality(row["pontuacao_qualidade"]) is None
    ]
    baseline_text = [row for row in architecture if is_reported(row["baseline_comparado"])]
    numeric_quality_rows = [
        row for row in architecture if numeric_quality(row["pontuacao_qualidade"]) is not None
    ]
    quality_values = sorted(
        numeric_quality(row["pontuacao_qualidade"]) for row in numeric_quality_rows
    )
    quality_counter = Counter(
        f"{numeric_quality(row['pontuacao_qualidade']):.1f}"
        for row in numeric_quality_rows
    )

    write_record_flags(rows)

    lines: list[str] = [
        "# Search Post-Extraction Recomputed Counts",
        "",
        "Date: 2026-04-29",
        "",
        "## Scope",
        "",
        "This report recomputes deterministic counts from `extraction/extracted-data.tsv`.",
        "It does not infer final controlled-comparison or quality labels where the extraction",
        "TSV still marks those fields as pending or `NR`.",
        "",
        "## Denominators",
        "",
        f"- Included search records with extraction rows: {len(rows)}.",
        f"- Architecture denominator: {len(architecture)}.",
        f"- Contextual/boundary records outside the architecture denominator: {len(contextual)}.",
        "",
        "## Architecture Taxonomy",
        "",
        "### Architecture Status",
        "",
        *markdown_count_table(count_field(architecture, "architecture_status"), len(architecture)),
        "",
        "### Legacy Architecture Type",
        "",
        *markdown_count_table(count_field(architecture, "tipo_arquitetura"), len(architecture)),
        "",
        "### Temporal Scope",
        "",
        *markdown_count_table(count_field(architecture, "escopo_temporal"), len(architecture)),
        "",
        "### Representational Substrate",
        "",
        *markdown_count_table(count_field(architecture, "substrato_representacional"), len(architecture)),
        "",
        "### Control Policy",
        "",
        *markdown_count_table(count_field(architecture, "politica_controle"), len(architecture)),
        "",
        "### Retrieval Method",
        "",
        *markdown_count_table(count_field(architecture, "metodo_recuperacao"), len(architecture)),
        "",
        "### Memory Granularity",
        "",
        *markdown_count_table(count_field(architecture, "granularidade_memoria"), len(architecture)),
        "",
        "### Cross-Agent Sharing",
        "",
        *markdown_count_table(
            count_field(architecture, "compartilhamento_entre_agentes"),
            len(architecture),
        ),
        "",
        "## Evaluation And Benchmarks",
        "",
        "### Evaluation Method Category",
        "",
        *markdown_count_table(
            Counter(evaluation_category(row["metodo_avaliacao"]) for row in architecture),
            len(architecture),
        ),
        "",
        "### Benchmark Markers",
        "",
        *markdown_count_table(benchmark_hits(architecture), len(architecture)),
        "",
        "## Controlled-Comparison Recode Status",
        "",
        *markdown_count_table(
            count_field(architecture, "controlled_comparison_status"),
            len(architecture),
        ),
        "",
        f"- Strict no-persistence or memory-ablation comparators: {len(strict_control)} of {len(architecture)} ({pct(len(strict_control), len(architecture))}).",
        f"- External/non-memory architecture comparators: {len(external_control)} of {len(architecture)} ({pct(len(external_control), len(architecture))}).",
        f"- Broad controlled-comparison candidates: {len(strict_control) + len(external_control)} of {len(architecture)} ({pct(len(strict_control) + len(external_control), len(architecture))}).",
        f"- Boundary records needing PDF review before final denominator use: {len(boundary_control)}.",
        f"- Architecture records still marked `pending_extraction` for controlled-comparison status: {len(pending_control)}.",
        "",
        "Use the strict denominator when the claim requires a same-system",
        "no-memory/no-persistence or memory-ablation comparator. Use the broad",
        "candidate denominator only if external non-memory architecture baselines",
        "are accepted in the target synthesis. Boundary records are excluded until",
        "PDF review resolves them.",
        "",
        "## Cost And Efficiency",
        "",
        *markdown_count_table(count_field(architecture, "reporta_dados_custo"), len(architecture)),
        "",
        "## Negative Or Adverse Results",
        "",
        *markdown_count_table(count_field(architecture, "resultado_negativo"), len(architecture)),
        "",
        "## Quality Score Distribution",
        "",
        f"- Architecture records with numeric quality scores: {len(numeric_quality_rows)}.",
        f"- Architecture records needing manual quality scoring: {len(pending_quality)}.",
        f"- Median quality score: {median(quality_values):.1f} of 6.0."
        if quality_values
        else "- Median quality score: NA.",
        f"- Records below 3.0/6.0 for sensitivity exclusion: {sum(value < 3.0 for value in quality_values)}.",
        "",
        *markdown_count_table(quality_counter, len(architecture)),
        "",
        "Quality scores are final only when `analysis/quality-assessment.tsv`",
        "contains Q1-Q6 values and `final_score` for every architecture record.",
        "",
        "## Record-Level Flag File",
        "",
        "- `analysis/post-extraction-recompute-records.tsv` records per-study",
        "  flags for controlled-comparison status, baseline text, quality-score status,",
        "  cost reporting, adverse-result reporting, and benchmark markers.",
        "",
        "## Next Manual Pass",
        "",
        "1. Rebuild benchmark, cost, adverse-result, and performance-delta synthesis tables.",
        "2. Create the search synthesis matrix from the finalized extraction TSV.",
        "3. Update PRISMA and manuscript claims only from saved search artifacts.",
        "",
    ]

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    print(f"wrote {OUT_TSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
