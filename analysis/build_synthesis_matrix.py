#!/usr/bin/env python3
"""Build search synthesis matrix artifacts from finalized extraction data."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

from build_benchmark_inventory import (
    OUT_INVENTORY as BENCHMARK_INVENTORY_TSV,
    OUT_RECORDS as BENCHMARK_RECORDS_TSV,
    normalized_benchmarks,
    write_outputs as write_benchmark_outputs,
)
from recompute_counts import evaluation_category, pct


ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "extraction" / "extracted-data.tsv"
OUT_MD = ROOT / "analysis" / "synthesis-matrix.md"
CONTROLLED_TSV = ROOT / "analysis" / "controlled-evidence-table.tsv"
COST_TSV = ROOT / "analysis" / "cost-evidence-table.tsv"
ADVERSE_TSV = ROOT / "analysis" / "adverse-evidence-table.tsv"
COST_CLASSIFICATION_TSV = ROOT / "analysis" / "cost-evidence-classification.tsv"
COST_SUMMARY_MD = ROOT / "analysis" / "cost-evidence-summary.md"
ADVERSE_CLASSIFICATION_TSV = ROOT / "analysis" / "adverse-mechanism-classification.tsv"
ADVERSE_SUMMARY_MD = ROOT / "analysis" / "adverse-mechanism-summary.md"
PERFORMANCE_DELTA_TSV = ROOT / "analysis" / "performance-delta-candidates.tsv"
PERFORMANCE_DELTA_SUMMARY_MD = ROOT / "analysis" / "performance-delta-summary.md"
PERFORMANCE_NORMALIZED_TSV = ROOT / "analysis" / "performance-normalized.tsv"
PERFORMANCE_NORMALIZED_SUMMARY_MD = ROOT / "analysis" / "performance-normalized-summary.md"
CERTAINTY_SENSITIVITY_TSV = ROOT / "analysis" / "certainty-sensitivity-records.tsv"
CERTAINTY_SENSITIVITY_MD = ROOT / "analysis" / "certainty-sensitivity-summary.md"

MISSING = {"", "NR", "NA", "nao_reportado", "not_applicable_contextual"}


def load_rows() -> list[dict[str, str]]:
    with IN_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_optional_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def reported(value: str) -> bool:
    return value.strip() not in MISSING


def short_title(row: dict[str, str]) -> str:
    title = row["titulo"]
    if len(title) <= 72:
        return title
    return f"{title[:69]}..."


def study_ref(row: dict[str, str]) -> str:
    return f"{row['included_id']} {row['id']}"


def benchmark_markers(row: dict[str, str]) -> str:
    labels = [rule.label for rule in normalized_benchmarks(row["benchmarks_utilizados"])]
    return "; ".join(labels) if labels else "NR"


def count_with_studies(rows: list[dict[str, str]], field: str) -> list[list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        grouped[row[field] or "NR"].append(study_ref(row))
    total = len(rows)
    table = [["Value", "N", "%", "Studies"]]
    for value, studies in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        table.append([f"`{value}`", str(len(studies)), pct(len(studies), total), "; ".join(studies)])
    return table


def counter_table(counter: Counter[str], denominator: int) -> list[list[str]]:
    table = [["Value", "N", "%"]]
    for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        table.append([f"`{value}`", str(count), pct(count, denominator)])
    return table


def markdown_table(table: list[list[str]]) -> list[str]:
    if not table:
        return []
    widths = [max(len(row[index]) for row in table) for index in range(len(table[0]))]
    lines = []
    header = table[0]
    lines.append("| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(header)) + " |")
    lines.append("| " + " | ".join("---" for _ in header) + " |")
    for row in table[1:]:
        lines.append("| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)) + " |")
    return lines


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_controlled_table(architecture: list[dict[str, str]]) -> None:
    rows = []
    for row in architecture:
        status = row["controlled_comparison_status"]
        if status.startswith("yes_"):
            rows.append(
                {
                    "included_id": row["included_id"],
                    "id": row["id"],
                    "title": row["titulo"],
                    "controlled_comparison_status": status,
                    "benchmark_markers": benchmark_markers(row),
                    "baseline_comparado": row["baseline_comparado"],
                    "desempenho_vs_baseline": row["desempenho_vs_baseline"],
                    "resultado_negativo": row["resultado_negativo"],
                    "reporta_dados_custo": row["reporta_dados_custo"],
                    "pontuacao_qualidade": row["pontuacao_qualidade"],
                }
            )
    write_tsv(
        CONTROLLED_TSV,
        [
            "included_id",
            "id",
            "title",
            "controlled_comparison_status",
            "benchmark_markers",
            "baseline_comparado",
            "desempenho_vs_baseline",
            "resultado_negativo",
            "reporta_dados_custo",
            "pontuacao_qualidade",
        ],
        rows,
    )


def write_cost_table(architecture: list[dict[str, str]]) -> None:
    rows = []
    for row in architecture:
        if row["reporta_dados_custo"] == "nao":
            continue
        rows.append(
            {
                "included_id": row["included_id"],
                "id": row["id"],
                "title": row["titulo"],
                "reporta_dados_custo": row["reporta_dados_custo"],
                "tokens_entrada_por_tarefa": row["tokens_entrada_por_tarefa"],
                "tokens_saida_por_tarefa": row["tokens_saida_por_tarefa"],
                "custo_por_tarefa": row["custo_por_tarefa"],
                "reducao_tokens": row["reducao_tokens"],
                "custo_vs_baseline": row["custo_vs_baseline"],
                "pontuacao_qualidade": row["pontuacao_qualidade"],
            }
        )
    write_tsv(
        COST_TSV,
        [
            "included_id",
            "id",
            "title",
            "reporta_dados_custo",
            "tokens_entrada_por_tarefa",
            "tokens_saida_por_tarefa",
            "custo_por_tarefa",
            "reducao_tokens",
            "custo_vs_baseline",
            "pontuacao_qualidade",
        ],
        rows,
    )


def write_adverse_table(architecture: list[dict[str, str]]) -> None:
    rows = []
    for row in architecture:
        if row["resultado_negativo"] != "sim":
            continue
        rows.append(
            {
                "included_id": row["included_id"],
                "id": row["id"],
                "title": row["titulo"],
                "architecture_status": row["architecture_status"],
                "controlled_comparison_status": row["controlled_comparison_status"],
                "limitacoes": row["limitacoes"],
                "ameacas_validade": row["ameacas_validade"],
                "custo_vs_baseline": row["custo_vs_baseline"],
                "pontuacao_qualidade": row["pontuacao_qualidade"],
            }
        )
    write_tsv(
        ADVERSE_TSV,
        [
            "included_id",
            "id",
            "title",
            "architecture_status",
            "controlled_comparison_status",
            "limitacoes",
            "ameacas_validade",
            "custo_vs_baseline",
            "pontuacao_qualidade",
        ],
        rows,
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

    write_controlled_table(architecture)
    write_cost_table(architecture)
    write_adverse_table(architecture)
    write_benchmark_outputs(architecture)

    quality_values = sorted(float(row["pontuacao_qualidade"]) for row in architecture)
    control_counter = Counter(row["controlled_comparison_status"] for row in architecture)
    quality_counter = Counter(row["pontuacao_qualidade"] for row in architecture)
    benchmark_counter: Counter[str] = Counter()
    for row in architecture:
        markers = benchmark_markers(row)
        if markers == "NR":
            benchmark_counter["NR"] += 1
        else:
            benchmark_counter.update(markers.split("; "))
    performance_rows = load_optional_tsv(PERFORMANCE_NORMALIZED_TSV)
    performance_status_counter = Counter(row["normalization_status"] for row in performance_rows)
    performance_unit_counter = Counter(row["normalized_delta_unit"] for row in performance_rows)
    performance_numeric_count = sum(
        row["normalized_delta_value"] != "NR"
        and row["normalization_status"] != "count_only"
        and "/" not in row["normalized_delta_value"]
        for row in performance_rows
    )
    performance_section: list[str] = []
    if performance_rows:
        performance_section = [
            "### Representative Performance Normalization",
            "",
            f"- Broad controlled rows normalized: {len(performance_rows)}.",
            f"- Rows with scalar numeric representative values: {performance_numeric_count}.",
            f"- Rows without scalar numeric representative values: {len(performance_rows) - performance_numeric_count}.",
            "",
            *markdown_table(counter_table(performance_status_counter, len(performance_rows))),
            "",
            "### Representative Performance Units",
            "",
            *markdown_table(counter_table(performance_unit_counter, len(performance_rows))),
            "",
        ]

    lines: list[str] = [
        "# Search Synthesis Matrix",
        "",
        "Generated from `extraction/extracted-data.tsv` on 2026-04-29.",
        "This is a data matrix for synthesis rebuilding, not final manuscript prose.",
        "",
        "## Denominators",
        "",
        f"- Included search records: {len(rows)}.",
        f"- Architecture records: {len(architecture)}.",
        f"- Contextual/boundary records outside the architecture denominator: {len(contextual)}.",
        f"- Strict controlled-comparison records: {control_counter['yes_no_persistence_or_memory_ablation']} of {len(architecture)} ({pct(control_counter['yes_no_persistence_or_memory_ablation'], len(architecture))}).",
        f"- Broad controlled-comparison candidates including external/non-memory baselines: {control_counter['yes_no_persistence_or_memory_ablation'] + control_counter['yes_nonmemory_external_baseline']} of {len(architecture)} ({pct(control_counter['yes_no_persistence_or_memory_ablation'] + control_counter['yes_nonmemory_external_baseline'], len(architecture))}).",
        f"- Median quality score: {median(quality_values):.1f}/6.",
        "",
        "## SQ1 - Architecture Taxonomy",
        "",
        "### Architecture Family",
        "",
        *markdown_table(count_with_studies(architecture, "architecture_status")),
        "",
        "### Legacy Architecture Type",
        "",
        *markdown_table(count_with_studies(architecture, "tipo_arquitetura")),
        "",
        "### Temporal Scope",
        "",
        *markdown_table(count_with_studies(architecture, "escopo_temporal")),
        "",
        "### Representational Substrate",
        "",
        *markdown_table(count_with_studies(architecture, "substrato_representacional")),
        "",
        "### Control Policy",
        "",
        *markdown_table(count_with_studies(architecture, "politica_controle")),
        "",
        "### Retrieval Method",
        "",
        *markdown_table(count_with_studies(architecture, "metodo_recuperacao")),
        "",
        "### Memory Granularity",
        "",
        *markdown_table(count_with_studies(architecture, "granularidade_memoria")),
        "",
        "### Cross-Agent Sharing",
        "",
        *markdown_table(count_with_studies(architecture, "compartilhamento_entre_agentes")),
        "",
        "## SQ2 - Evaluation Methods And Benchmarks",
        "",
        "### Evaluation Method Category",
        "",
        *markdown_table(
            counter_table(
                Counter(evaluation_category(row["metodo_avaliacao"]) for row in architecture),
                len(architecture),
            )
        ),
        "",
        "### Normalized Benchmark Inventory",
        "",
        *markdown_table(counter_table(benchmark_counter, len(architecture))),
        "",
        f"- Row-level benchmark inventory: `{BENCHMARK_RECORDS_TSV.relative_to(ROOT)}`.",
        f"- Normalized benchmark count table: `{BENCHMARK_INVENTORY_TSV.relative_to(ROOT)}`.",
        "",
        "## SQ3 - Controlled Performance Evidence",
        "",
        *markdown_table(counter_table(control_counter, len(architecture))),
        "",
        f"- Row-level controlled-evidence table: `{CONTROLLED_TSV.relative_to(ROOT)}`.",
        f"- Candidate performance-delta table: `{PERFORMANCE_DELTA_TSV.relative_to(ROOT)}`.",
        f"- Candidate performance-delta summary: `{PERFORMANCE_DELTA_SUMMARY_MD.relative_to(ROOT)}`.",
        f"- Normalized representative performance table: `{PERFORMANCE_NORMALIZED_TSV.relative_to(ROOT)}`.",
        f"- Normalized performance summary: `{PERFORMANCE_NORMALIZED_SUMMARY_MD.relative_to(ROOT)}`.",
        "- Use strict rows for same-system no-memory/no-persistence or memory-ablation claims.",
        "- Use broad rows only when external/non-memory architecture baselines are acceptable for the claim.",
        "",
        *performance_section,
        "## SQ4 - Cost And Efficiency Evidence",
        "",
        *markdown_table(counter_table(Counter(row["reporta_dados_custo"] for row in architecture), len(architecture))),
        "",
        f"- Row-level cost evidence table: `{COST_TSV.relative_to(ROOT)}`.",
        f"- Cost evidence class table: `{COST_CLASSIFICATION_TSV.relative_to(ROOT)}`.",
        f"- Cost evidence summary: `{COST_SUMMARY_MD.relative_to(ROOT)}`.",
        "",
        "## SQ5 - Adverse Or Degradation Evidence",
        "",
        *markdown_table(counter_table(Counter(row["resultado_negativo"] for row in architecture), len(architecture))),
        "",
        f"- Row-level adverse-evidence table: `{ADVERSE_TSV.relative_to(ROOT)}`.",
        f"- Adverse-mechanism class table: `{ADVERSE_CLASSIFICATION_TSV.relative_to(ROOT)}`.",
        f"- Adverse-mechanism summary: `{ADVERSE_SUMMARY_MD.relative_to(ROOT)}`.",
        "",
        "## Quality And Sensitivity",
        "",
        *markdown_table(counter_table(quality_counter, len(architecture))),
        "",
        f"- Records below 3.0/6.0: {sum(value < 3.0 for value in quality_values)}.",
        "- The search quality sensitivity analysis will therefore not remove any architecture record under the original below-3.0 rule.",
        f"- Certainty/sensitivity record table: `{CERTAINTY_SENSITIVITY_TSV.relative_to(ROOT)}`.",
        f"- Certainty/sensitivity summary: `{CERTAINTY_SENSITIVITY_MD.relative_to(ROOT)}`.",
        "",
        "## Pending Manual Synthesis",
        "",
        "- Use normalized benchmark, performance, cost, and adverse-mechanism scaffolds to draft SQ2-SQ5 prose with denominator discipline.",
        "- Review qualitative, count-only, lower-bound, and low-confidence SQ3 rows before making manuscript-level effect claims.",
        "- Integrate the rendered search PRISMA diagram into the manuscript figure source after reading `manuscript/PLAYBOOK.md`.",
        "- Update PRISMA counts and manuscript denominators from frozen search artifacts.",
        "",
    ]

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    print(f"wrote {CONTROLLED_TSV.relative_to(ROOT)}")
    print(f"wrote {COST_TSV.relative_to(ROOT)}")
    print(f"wrote {ADVERSE_TSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
