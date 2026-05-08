#!/usr/bin/env python3
"""Build search certainty and sensitivity scaffolds.

This is a record-level sensitivity artifact for manuscript rebuilding. It does
not assign final certainty to narrative findings; that remains a synthesis
writing task. The script records the main sensitivity cuts that can change
denominators: publication status, quality thresholds, and strict versus broad
controlled-comparison evidence.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from recompute_counts import pct


ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "extraction" / "extracted-data.tsv"
OUT_TSV = ROOT / "analysis" / "certainty-sensitivity-records.tsv"
OUT_MD = ROOT / "analysis" / "certainty-sensitivity-summary.md"


PEER_REVIEWED_TYPES = {"conferencia", "conference", "periodico", "workshop"}


def load_rows() -> list[dict[str, str]]:
    with IN_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def numeric_quality(row: dict[str, str]) -> float | None:
    try:
        return float(row["pontuacao_qualidade"])
    except ValueError:
        return None


def publication_group(row: dict[str, str]) -> str:
    tipo = row["tipo_venue"].strip().lower()
    if tipo == "preprint":
        return "preprint"
    if tipo in PEER_REVIEWED_TYPES:
        return "peer_reviewed"
    return "unknown"


def quality_band(score: float | None) -> str:
    if score is None:
        return "missing"
    if score < 3.0:
        return "below_protocol_threshold"
    if score < 4.0:
        return "low_retained"
    if score < 4.5:
        return "moderate_low"
    if score < 5.0:
        return "moderate"
    if score < 5.5:
        return "high"
    return "very_high"


def controlled_group(row: dict[str, str]) -> str:
    status = row["controlled_comparison_status"]
    if status == "yes_no_persistence_or_memory_ablation":
        return "strict_no_persistence_or_memory_ablation"
    if status == "yes_nonmemory_external_baseline":
        return "broad_external_nonmemory_baseline"
    return "no_suitable_controlled_comparison"


def write_records(rows: list[dict[str, str]]) -> None:
    fields = [
        "included_id",
        "id",
        "title",
        "architecture_denominator_decision",
        "study_role",
        "publication_group",
        "tipo_venue",
        "venue",
        "quality_score",
        "quality_band",
        "retained_quality_ge_3_0",
        "retained_quality_ge_4_0",
        "retained_quality_ge_4_5",
        "retained_quality_ge_5_0",
        "controlled_group",
        "strict_controlled",
        "broad_controlled",
        "peer_reviewed_only_retained",
        "cost_reporting",
        "adverse_evidence",
    ]
    with OUT_TSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for row in rows:
            score = numeric_quality(row)
            pub_group = publication_group(row)
            control = controlled_group(row)
            broad = control in {
                "strict_no_persistence_or_memory_ablation",
                "broad_external_nonmemory_baseline",
            }
            writer.writerow(
                {
                    "included_id": row["included_id"],
                    "id": row["id"],
                    "title": row["titulo"],
                    "architecture_denominator_decision": row[
                        "architecture_denominator_decision"
                    ],
                    "study_role": row["study_role"],
                    "publication_group": pub_group,
                    "tipo_venue": row["tipo_venue"],
                    "venue": row["venue"],
                    "quality_score": f"{score:.1f}" if score is not None else "NR",
                    "quality_band": quality_band(score),
                    "retained_quality_ge_3_0": "yes" if score is not None and score >= 3.0 else "no",
                    "retained_quality_ge_4_0": "yes" if score is not None and score >= 4.0 else "no",
                    "retained_quality_ge_4_5": "yes" if score is not None and score >= 4.5 else "no",
                    "retained_quality_ge_5_0": "yes" if score is not None and score >= 5.0 else "no",
                    "controlled_group": control,
                    "strict_controlled": "yes"
                    if control == "strict_no_persistence_or_memory_ablation"
                    else "no",
                    "broad_controlled": "yes" if broad else "no",
                    "peer_reviewed_only_retained": "yes" if pub_group == "peer_reviewed" else "no",
                    "cost_reporting": row["reporta_dados_custo"],
                    "adverse_evidence": row["resultado_negativo"],
                }
            )


def markdown_counter_table(counter: Counter[str], denominator: int) -> list[str]:
    lines = ["| Value | N | % |", "| --- | ---: | ---: |"]
    for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{value}` | {count} | {pct(count, denominator)} |")
    return lines


def threshold_table(rows: list[dict[str, str]]) -> list[str]:
    thresholds = [3.0, 4.0, 4.5, 5.0]
    lines = ["| Quality cut | Retained | Removed | Retained % |", "| --- | ---: | ---: | ---: |"]
    scored = [row for row in rows if numeric_quality(row) is not None]
    for threshold in thresholds:
        retained = sum(numeric_quality(row) >= threshold for row in scored)
        removed = len(rows) - retained
        lines.append(
            f"| `>= {threshold:.1f}/6` | {retained} | {removed} | {pct(retained, len(rows))} |"
        )
    return lines


def write_summary(rows: list[dict[str, str]]) -> None:
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
    all_publication = Counter(publication_group(row) for row in rows)
    arch_publication = Counter(publication_group(row) for row in architecture)
    arch_controlled = Counter(controlled_group(row) for row in architecture)
    arch_quality = Counter(quality_band(numeric_quality(row)) for row in architecture)
    peer_reviewed_arch = arch_publication["peer_reviewed"]
    strict = arch_controlled["strict_no_persistence_or_memory_ablation"]
    broad = strict + arch_controlled["broad_external_nonmemory_baseline"]

    lines = [
        "# Search Certainty And Sensitivity Scaffold",
        "",
        "Generated from `extraction/extracted-data.tsv` on 2026-04-29.",
        "This scaffold records sensitivity cuts for later synthesis. It does not assign final certainty to manuscript findings.",
        "",
        "## Denominators",
        "",
        f"- Included search records: {len(rows)}.",
        f"- Architecture records: {len(architecture)}.",
        f"- Contextual/boundary records: {len(contextual)}.",
        "",
        "## Publication-Status Sensitivity",
        "",
        "### Included Records",
        "",
        *markdown_counter_table(all_publication, len(rows)),
        "",
        "### Architecture Records",
        "",
        *markdown_counter_table(arch_publication, len(architecture)),
        "",
        f"- Peer-reviewed-only architecture sensitivity retains {peer_reviewed_arch} of {len(architecture)} records ({pct(peer_reviewed_arch, len(architecture))}).",
        f"- Preprint-heavy evidence base: {arch_publication['preprint']} of {len(architecture)} architecture records are preprints ({pct(arch_publication['preprint'], len(architecture))}).",
        "",
        "## Quality Sensitivity",
        "",
        *markdown_counter_table(arch_quality, len(architecture)),
        "",
        "### Threshold Cuts",
        "",
        *threshold_table(architecture),
        "",
        "- Protocol sensitivity threshold `< 3.0/6` removes zero architecture records.",
        "- Raising the cut to `>= 5.0/6` would retain only the highest-scored 56 architecture records and should be treated as an exploratory robustness check, not the protocol rule.",
        "",
        "## Controlled-Comparison Sensitivity",
        "",
        *markdown_counter_table(arch_controlled, len(architecture)),
        "",
        f"- Strict no-persistence or memory-ablation claims should use {strict} of {len(architecture)} architecture records ({pct(strict, len(architecture))}).",
        f"- Broad controlled-comparison claims, including external/non-memory baselines, can use {broad} of {len(architecture)} architecture records ({pct(broad, len(architecture))}).",
        "",
        "## Use Notes",
        "",
        "- Architecture taxonomy claims use the full 85-record architecture denominator unless explicitly framed as sensitivity analysis.",
        "- Peer-reviewed-only sensitivity is informative but too restrictive for the main emerging-field synthesis.",
        "- Quality-threshold sensitivity does not alter the corpus under the protocol `< 3.0/6` rule.",
        "- Strict controlled claims and broad comparative claims must keep separate denominators.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = load_rows()
    write_records(rows)
    write_summary(rows)
    print(f"wrote {OUT_TSV.relative_to(ROOT)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
