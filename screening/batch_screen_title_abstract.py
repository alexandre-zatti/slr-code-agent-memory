#!/usr/bin/env python3
"""Apply deterministic title/abstract screening batches for current search.

This script only handles decisions that do not require substantive
interpretation of the title/abstract.  At present that is the CI3 year-window
exclusion for records with a numeric year before 2023.
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import tempfile
from datetime import datetime, timezone


DEFAULT_SCREENING = pathlib.Path("screening/title-abstract-screening.tsv")

REQUIRED_COLUMNS = {
    "screening_id",
    "year",
    "title_abstract_decision",
    "ci3_year",
    "exclusion_code",
    "criterion_rationale",
    "reviewer",
    "reviewed_at_utc",
    "notes",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply deterministic search title/abstract screening batches."
    )
    parser.add_argument(
        "--screening-file",
        type=pathlib.Path,
        default=DEFAULT_SCREENING,
        help=f"Screening TSV to update (default: {DEFAULT_SCREENING}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the batch count without writing changes.",
    )
    return parser.parse_args()


def numeric_year(value: str) -> int | None:
    value = (value or "").strip()
    if len(value) != 4 or not value.isdigit():
        return None
    return int(value)


def append_note(existing: str, addition: str) -> str:
    existing = (existing or "").strip()
    if not existing:
        return addition
    if addition in existing:
        return existing
    return f"{existing} | {addition}"


def load_rows(path: pathlib.Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise SystemExit(f"{path} has no header")
        missing = sorted(REQUIRED_COLUMNS - set(reader.fieldnames))
        if missing:
            raise SystemExit(f"{path} is missing required columns: {', '.join(missing)}")
        return reader.fieldnames, list(reader)


def write_rows(path: pathlib.Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        tmp_path = pathlib.Path(handle.name)
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    tmp_path.replace(path)


def main() -> int:
    args = parse_args()
    fieldnames, rows = load_rows(args.screening_file)
    reviewed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    changed = 0
    pre_2023_total = 0
    pre_2023_already_decided = 0
    for row in rows:
        year = numeric_year(row.get("year", ""))
        if year is None or year >= 2023:
            continue
        pre_2023_total += 1
        if row.get("title_abstract_decision", "").strip():
            pre_2023_already_decided += 1
            continue
        row["title_abstract_decision"] = "exclude"
        row["ci3_year"] = "no"
        row["exclusion_code"] = "CI3"
        row["criterion_rationale"] = "Published before 2023; outside CI3 year window."
        row["reviewer"] = "codex_deterministic_ci3"
        row["reviewed_at_utc"] = reviewed_at
        row["notes"] = append_note(
            row.get("notes", ""),
            "Deterministic CI3 batch screen (year < 2023).",
        )
        changed += 1

    print(f"screening_file\t{args.screening_file}")
    print(f"rows_read\t{len(rows)}")
    print(f"pre_2023_total\t{pre_2023_total}")
    print(f"pre_2023_already_decided\t{pre_2023_already_decided}")
    print(f"ci3_exclusions_to_write\t{changed}")
    print(f"reviewed_at_utc\t{reviewed_at}")
    if args.dry_run:
        print("dry_run\ttrue")
        return 0

    write_rows(args.screening_file, fieldnames, rows)
    print("dry_run\tfalse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
