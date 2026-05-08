#!/usr/bin/env python3
"""Classify search cost evidence into synthesis-ready evidence classes."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "extraction" / "extracted-data.tsv"
OUT_CLASSIFICATION = ROOT / "analysis" / "cost-evidence-classification.tsv"
OUT_SUMMARY = ROOT / "analysis" / "cost-evidence-summary.md"

MISSING = {"", "NR", "NA", "nao_reportado", "not_applicable_contextual"}

CLASS_PATTERNS = {
    "monetary_cost": r"\$|usd|dollar|api cost",
    "runtime_or_latency": r"runtime|latency|wall[- ]?clock|time per|seconds|minutes|hours|tempo|iteration|steps|rounds|cycles",
    "compute_or_resource": r"gpu|cpu|core|memory efficiency|normalized[- ]?core|hardware|a100|h100|a40|a6000|trainium|cuda|resource",
    "cost_reduction_or_tradeoff": r"reduc|less|fewer|overhead|cheaper|econom|saving|saves|trade[- ]?off|frontier|higher cost|lower cost|mais barato|economiza|avoid|amortiz|practical|budget",
}
TOKEN_PATTERN = re.compile(
    r"\b(tokens?|prompt tokens?|completion tokens?|cached tokens?|token usage|"
    r"token count|token reduction|context window|context length)\b",
    re.I,
)
NEGATED_TOKEN_PATTERN = re.compile(
    r"\b(no|not|without|não)\b[^.;]{0,50}\b(token|tokens)\b",
    re.I,
)


def load_architecture_rows() -> list[dict[str, str]]:
    with IN_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return [
        row
        for row in rows
        if row["architecture_denominator_decision"] == "include_architecture"
    ]


def reported(value: str) -> bool:
    return value.strip().lower() not in MISSING


def cost_text(row: dict[str, str]) -> str:
    fields = [
        "tokens_entrada_por_tarefa",
        "tokens_saida_por_tarefa",
        "custo_por_tarefa",
        "reducao_tokens",
        "custo_vs_baseline",
        "resultado_principal",
        "desempenho_vs_baseline",
    ]
    return " ".join(row[field] for field in fields if reported(row[field]))


def token_text(row: dict[str, str]) -> str:
    fields = [
        "tokens_entrada_por_tarefa",
        "tokens_saida_por_tarefa",
        "reducao_tokens",
        "custo_por_tarefa",
        "custo_vs_baseline",
    ]
    return " ".join(row[field] for field in fields if reported(row[field]))


def has_token_evidence(row: dict[str, str]) -> bool:
    explicit_token_fields = [
        row["tokens_entrada_por_tarefa"],
        row["tokens_saida_por_tarefa"],
        row["reducao_tokens"],
    ]
    if any(reported(value) and TOKEN_PATTERN.search(value) for value in explicit_token_fields):
        return True

    text = " ".join(
        row[field]
        for field in ["custo_por_tarefa", "custo_vs_baseline"]
        if reported(row[field])
    )
    text = re.sub(r"\b(?:NR|NA)?\s*monetary/token cost\b", "", text, flags=re.I)
    return bool(TOKEN_PATTERN.search(text)) and not bool(NEGATED_TOKEN_PATTERN.search(text))


def classify(row: dict[str, str]) -> list[str]:
    if row["reporta_dados_custo"] == "nao":
        return ["no_cost_evidence"]

    text = cost_text(row).lower()
    classes = [
        label
        for label, pattern in CLASS_PATTERNS.items()
        if re.search(pattern, text)
    ]
    if has_token_evidence(row):
        classes.append("token_usage")
    return classes or ["other_cost_evidence"]


def main() -> None:
    rows = load_architecture_rows()
    output_rows = []
    class_counter: Counter[str] = Counter()
    reporting_counter: Counter[str] = Counter()
    grouped: dict[str, list[str]] = defaultdict(list)

    for row in rows:
        classes = classify(row)
        reporting_counter[row["reporta_dados_custo"]] += 1
        for label in classes:
            class_counter[label] += 1
            grouped[label].append(f"{row['included_id']} {row['id']}")
        output_rows.append(
            {
                "included_id": row["included_id"],
                "id": row["id"],
                "title": row["titulo"],
                "reporta_dados_custo": row["reporta_dados_custo"],
                "cost_evidence_classes": ";".join(classes),
                "tokens_entrada_por_tarefa": row["tokens_entrada_por_tarefa"],
                "tokens_saida_por_tarefa": row["tokens_saida_por_tarefa"],
                "custo_por_tarefa": row["custo_por_tarefa"],
                "reducao_tokens": row["reducao_tokens"],
                "custo_vs_baseline": row["custo_vs_baseline"],
            }
        )

    with OUT_CLASSIFICATION.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "included_id",
            "id",
            "title",
            "reporta_dados_custo",
            "cost_evidence_classes",
            "tokens_entrada_por_tarefa",
            "tokens_saida_por_tarefa",
            "custo_por_tarefa",
            "reducao_tokens",
            "custo_vs_baseline",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(output_rows)

    lines = [
        "# Search Cost Evidence Summary",
        "",
        "Generated from `extraction/extracted-data.tsv` on 2026-04-29.",
        "Classes are non-exclusive except `no_cost_evidence`.",
        "",
        "## Reporting Level",
        "",
        "| Value | N |",
        "| --- | ---: |",
    ]
    for value, count in sorted(reporting_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} |")

    lines.extend(["", "## Evidence Classes", "", "| Class | N | Studies |", "| --- | ---: | --- |"])
    for value, count in sorted(class_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} | {'; '.join(sorted(grouped[value]))} |")

    OUT_SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_CLASSIFICATION.relative_to(ROOT)}")
    print(f"wrote {OUT_SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
