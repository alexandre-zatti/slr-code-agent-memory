#!/usr/bin/env python3
"""Finalize search controlled-comparison recoding.

Statuses use a conservative denominator rule:

- yes_no_persistence_or_memory_ablation: explicit no-memory/no-persistence or
  memory-component removal comparator.
- yes_nonmemory_external_baseline: comparator is an external or generic system
  that does not implement the reviewed persistence architecture.
- no_no_persistence_or_nonmemory_baseline: no documented comparator suitable
  for the controlled-comparison denominator.
- boundary_needs_pdf_review: extracted fields suggest a possible comparator, but
  the record should not enter final controlled-comparison counts until the PDF
  is checked.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECODE_PATH = ROOT / "analysis" / "controlled-comparison-recode.tsv"
QUEUE_PATH = ROOT / "extraction" / "extraction-queue.tsv"

YES_STRICT = "yes_no_persistence_or_memory_ablation"
YES_EXTERNAL = "yes_nonmemory_external_baseline"
NO = "no_no_persistence_or_nonmemory_baseline"
BOUNDARY = "boundary_needs_pdf_review"

DECISIONS = {
    "I001": YES_STRICT,
    "I002": YES_STRICT,
    "I003": YES_EXTERNAL,
    "I004": YES_STRICT,
    "I005": NO,
    "I006": YES_STRICT,
    "I007": YES_EXTERNAL,
    "I008": YES_STRICT,
    "I009": YES_STRICT,
    "I010": YES_STRICT,
    "I012": YES_STRICT,
    "I013": NO,
    "I015": YES_EXTERNAL,
    "I016": YES_EXTERNAL,
    "I017": YES_STRICT,
    "I018": NO,
    "I019": YES_EXTERNAL,
    "I020": YES_STRICT,
    "I021": YES_STRICT,
    "I022": YES_STRICT,
    "I023": YES_EXTERNAL,
    "I024": YES_STRICT,
    "I025": YES_STRICT,
    "I026": NO,
    "I027": YES_STRICT,
    "I030": YES_STRICT,
    "I031": YES_STRICT,
    "I032": NO,
    "I033": YES_STRICT,
    "I035": YES_STRICT,
    "I037": YES_EXTERNAL,
    "I038": YES_EXTERNAL,
    "I039": YES_EXTERNAL,
    "I040": YES_STRICT,
    "I041": YES_STRICT,
    "I042": YES_EXTERNAL,
    "I043": YES_STRICT,
    "I044": YES_STRICT,
    "I045": YES_STRICT,
    "I046": YES_STRICT,
    "I047": YES_STRICT,
    "I048": YES_STRICT,
    "I049": YES_STRICT,
    "I050": YES_EXTERNAL,
    "I051": YES_STRICT,
    "I052": YES_STRICT,
    "I053": YES_STRICT,
    "I054": YES_STRICT,
    "I055": YES_STRICT,
    "I056": YES_STRICT,
    "I057": NO,
    "I058": YES_STRICT,
    "I059": YES_STRICT,
    "I060": YES_STRICT,
    "I061": YES_STRICT,
    "I062": NO,
    "I063": YES_EXTERNAL,
    "I064": YES_STRICT,
    "I065": YES_EXTERNAL,
    "I066": NO,
    "I067": YES_STRICT,
    "I068": YES_STRICT,
    "I069": YES_STRICT,
    "I070": YES_STRICT,
    "I071": YES_STRICT,
    "I073": YES_STRICT,
    "I074": YES_STRICT,
    "I076": YES_EXTERNAL,
    "I077": YES_STRICT,
    "I078": YES_EXTERNAL,
    "I079": YES_STRICT,
    "I080": YES_EXTERNAL,
    "I081": YES_STRICT,
    "I082": YES_EXTERNAL,
    "I083": YES_STRICT,
    "I085": YES_EXTERNAL,
    "I086": YES_EXTERNAL,
    "I087": YES_STRICT,
    "I088": NO,
    "I090": YES_STRICT,
    "I091": YES_STRICT,
    "I092": YES_EXTERNAL,
    "I093": YES_STRICT,
    "I094": YES_STRICT,
    "I095": YES_STRICT,
}

RATIONALE_BY_STATUS = {
    YES_STRICT: (
        "Extracted evidence names a no-memory/no-persistence comparator or a "
        "memory-component ablation."
    ),
    YES_EXTERNAL: (
        "Extracted evidence reports quantitative comparison against external "
        "or generic systems without the reviewed persistence architecture; "
        "count separately from strict ablations if needed."
    ),
    NO: (
        "Extracted evidence does not document a no-persistence or non-memory "
        "baseline suitable for the controlled-comparison denominator."
    ),
    BOUNDARY: (
        "Potential comparator is visible in extracted evidence, but the "
        "no-persistence interpretation needs PDF review before counting."
    ),
}

RATIONALE_OVERRIDES = {
    "I018": (
        "PDF/text review found ECO comparisons against human edits, retrieval "
        "methods, unoptimized programs, and production before/after measures, "
        "but no clean no-persistence or non-memory coding-agent comparator."
    ),
    "I045": (
        "PDF/text review found a direct initial/de novo proposal comparator "
        "against parent-conditioned operators using inherited archives."
    ),
    "I057": (
        "PDF/text review found model, training, acceptance-shaping, and "
        "curriculum comparisons, but no clean no-memory or no-success-memory "
        "ablation for DockSmith's persistence mechanism."
    ),
    "I061": (
        "PDF/text review found explicit memory-free/no-historical-memory "
        "FailureMem comparators and component ablations."
    ),
    "I066": (
        "PDF/text review found baseline implementation and evolutionary-search "
        "comparisons, but no clean no-persistence or no-trajectory-memory "
        "comparator for PhyloEvolve."
    ),
}


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def update_recode_tsv() -> None:
    fieldnames, rows = load_tsv(RECODE_PATH)
    seen = {row["included_id"] for row in rows}
    missing = sorted(set(DECISIONS) - seen)
    extra = sorted(seen - set(DECISIONS))
    if missing or extra:
        raise SystemExit(f"decision coverage mismatch: missing={missing}, extra={extra}")

    for row in rows:
        status = DECISIONS[row["included_id"]]
        row["final_status"] = status
        row["manual_rationale"] = RATIONALE_OVERRIDES.get(
            row["included_id"], RATIONALE_BY_STATUS[status]
        )
    write_tsv(RECODE_PATH, fieldnames, rows)


def update_json_files() -> int:
    _, queue_rows = load_tsv(QUEUE_PATH)
    path_by_included = {
        row["included_id"]: ROOT / row["json_path"]
        for row in queue_rows
        if row["included_id"] in DECISIONS
    }
    missing = sorted(set(DECISIONS) - set(path_by_included))
    if missing:
        raise SystemExit(f"missing JSON paths for included IDs: {missing}")

    updated = 0
    for included_id, status in DECISIONS.items():
        path = path_by_included[included_id]
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        data["controlled_comparison_status"] = status
        with path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        updated += 1
    return updated


def main() -> None:
    update_recode_tsv()
    updated = update_json_files()
    print(f"updated {RECODE_PATH.relative_to(ROOT)}")
    print(f"updated {updated} JSON extraction files")


if __name__ == "__main__":
    main()
