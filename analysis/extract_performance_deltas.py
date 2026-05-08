#!/usr/bin/env python3
"""Extract candidate numeric performance deltas for current search.

The output is a scaffold, not a final meta-analysis. Metrics are heterogeneous
across pass rates, speedups, costs, judge scores, and benchmark-specific
scores, so the script preserves raw text and separates candidate numeric forms.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "analysis" / "controlled-evidence-table.tsv"
OUT_TSV = ROOT / "analysis" / "performance-delta-candidates.tsv"
OUT_MD = ROOT / "analysis" / "performance-delta-summary.md"

PATTERNS = {
    "signed_percentage_points": r"[+-]\s*\d+(?:\.\d+)?\s*(?:pp|percentage points?)",
    "from_to_percent": r"(?:from|de)\s+\d+(?:\.\d+)?%?\s+(?:to|para|→)\s+\d+(?:\.\d+)?%?",
    "arrow_change": r"\d+(?:\.\d+)?\s*(?:%|/5)?\s*(?:→|->)\s*\d+(?:\.\d+)?\s*(?:%|/5)?",
    "multiplicative": r"\d+(?:\.\d+)?\s*x",
    "signed_percent": r"[+-]\s*\d+(?:\.\d+)?%",
    "relative_percent": r"\d+(?:\.\d+)?%\s+(?:fewer|less|lower|higher|reduction|increase|improvement|speedup|gain|decrease|reduces|faster)",
    "score_points": r"[+-]\s*\d+(?:\.\d+)?\s*(?:points?|pts?|score)",
    "ratio_or_count": r"\d+\s*/\s*\d+",
}

PRIORITY = [
    "signed_percentage_points",
    "from_to_percent",
    "arrow_change",
    "multiplicative",
    "signed_percent",
    "relative_percent",
    "score_points",
    "ratio_or_count",
]


def load_rows() -> list[dict[str, str]]:
    with IN_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def matches_by_type(text: str) -> dict[str, list[str]]:
    output: dict[str, list[str]] = {}
    for label, pattern in PATTERNS.items():
        matches = [match.group(0).strip() for match in re.finditer(pattern, text, re.IGNORECASE)]
        if matches:
            output[label] = sorted(set(matches), key=matches.index)
    return output


def primary_candidate(matches: dict[str, list[str]]) -> tuple[str, str]:
    for label in PRIORITY:
        values = matches.get(label)
        if values:
            return label, values[0]
    return "manual_review", "NR"


def main() -> None:
    rows = load_rows()
    output_rows = []
    status_counter: Counter[str] = Counter()
    primary_counter: Counter[str] = Counter()

    for row in rows:
        text = row["desempenho_vs_baseline"]
        matches = matches_by_type(text)
        primary_type, primary_value = primary_candidate(matches)
        status = "candidate_extracted" if primary_type != "manual_review" else "manual_review"
        status_counter[status] += 1
        primary_counter[primary_type] += 1
        output_rows.append(
            {
                "included_id": row["included_id"],
                "id": row["id"],
                "title": row["title"],
                "controlled_comparison_status": row["controlled_comparison_status"],
                "benchmark_markers": row["benchmark_markers"],
                "primary_delta_type": primary_type,
                "primary_delta_candidate": primary_value,
                "all_delta_candidates": " | ".join(
                    f"{label}: {'; '.join(values)}"
                    for label, values in matches.items()
                )
                or "NR",
                "extraction_status": status,
                "desempenho_vs_baseline": text,
            }
        )

    with OUT_TSV.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "included_id",
            "id",
            "title",
            "controlled_comparison_status",
            "benchmark_markers",
            "primary_delta_type",
            "primary_delta_candidate",
            "all_delta_candidates",
            "extraction_status",
            "desempenho_vs_baseline",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(output_rows)

    lines = [
        "# Search Performance Delta Candidate Summary",
        "",
        "Generated from `analysis/controlled-evidence-table.tsv` on 2026-04-29.",
        "This is a candidate-extraction scaffold; heterogeneous metrics still require manual normalization before manuscript claims.",
        "",
        "## Extraction Status",
        "",
        "| Status | N |",
        "| --- | ---: |",
    ]
    for value, count in sorted(status_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} |")

    lines.extend(["", "## Primary Candidate Type", "", "| Type | N |", "| --- | ---: |"])
    for value, count in sorted(primary_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} |")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_TSV.relative_to(ROOT)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
