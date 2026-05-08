#!/usr/bin/env python3
"""Apply reviewed full-text decisions to the search screening ledger."""

from __future__ import annotations

import argparse
import csv
import pathlib
import tempfile
from collections import Counter
from datetime import datetime, timezone


DEFAULT_SCREENING = pathlib.Path("screening/full-text-screening.tsv")

SCREENING_COLUMNS = [
    "full_text_decision",
    "ci1_persistence",
    "ci2_evaluation",
    "ci3_year",
    "ci4_language",
    "ci5_publication_type",
    "ce1_no_cross_session_persistence",
    "ce2_not_software_dev",
    "ce3_no_evaluation",
    "ce4_tutorial_editorial_or_descriptive_survey",
    "ce5_duplicate_or_superseded",
    "exclusion_code",
    "full_text_rationale",
    "reviewer",
    "reviewed_at_utc",
    "notes",
]

VALID_DECISIONS = {"include", "exclude", "not_retrieved"}
CRITERION_COLUMNS = [
    "ci1_persistence",
    "ci2_evaluation",
    "ci3_year",
    "ci4_language",
    "ci5_publication_type",
    "ce1_no_cross_session_persistence",
    "ce2_not_software_dev",
    "ce3_no_evaluation",
    "ce4_tutorial_editorial_or_descriptive_survey",
    "ce5_duplicate_or_superseded",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply search full-text decisions.")
    parser.add_argument("decisions_file", type=pathlib.Path)
    parser.add_argument("--screening-file", type=pathlib.Path, default=DEFAULT_SCREENING)
    parser.add_argument("--reviewer", default="codex_full_text_001")
    parser.add_argument("--overwrite-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def read_tsv(path: pathlib.Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise SystemExit(f"{path} has no header")
        return reader.fieldnames, list(reader)


def write_tsv(path: pathlib.Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
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


def append_note(existing: str, addition: str) -> str:
    existing = (existing or "").strip()
    addition = (addition or "").strip()
    if not addition:
        return existing
    if not existing:
        return addition
    if addition in existing:
        return existing
    return f"{existing} | {addition}"


def validate_decision(row: dict[str, str]) -> None:
    full_text_id = row.get("full_text_id", "").strip()
    decision = row.get("full_text_decision", "").strip()
    if not full_text_id:
        raise SystemExit("decision row missing full_text_id")
    if decision not in VALID_DECISIONS:
        raise SystemExit(f"{full_text_id}: invalid full_text_decision {decision!r}")
    rationale = row.get("full_text_rationale", "").strip()
    if not rationale:
        raise SystemExit(f"{full_text_id}: missing full_text_rationale")
    exclusion_code = row.get("exclusion_code", "").strip()
    if decision == "exclude" and not exclusion_code:
        raise SystemExit(f"{full_text_id}: exclude decision missing exclusion_code")
    if decision != "exclude" and exclusion_code:
        raise SystemExit(f"{full_text_id}: non-exclude decision has exclusion_code {exclusion_code!r}")


def derived_values(row: dict[str, str]) -> dict[str, str]:
    decision = row.get("full_text_decision", "").strip()
    exclusion_code = row.get("exclusion_code", "").strip()
    values = {column: "" for column in SCREENING_COLUMNS}
    values["full_text_decision"] = decision
    values["exclusion_code"] = exclusion_code
    values["full_text_rationale"] = row.get("full_text_rationale", "").strip()

    if decision == "include":
        values.update(
            {
                "ci1_persistence": "yes",
                "ci2_evaluation": "yes",
                "ci3_year": "yes",
                "ci4_language": "yes",
                "ci5_publication_type": "yes",
                "ce1_no_cross_session_persistence": "no",
                "ce2_not_software_dev": "no",
                "ce3_no_evaluation": "no",
                "ce4_tutorial_editorial_or_descriptive_survey": "no",
                "ce5_duplicate_or_superseded": "no",
            }
        )
    elif decision == "exclude":
        values.update(
            {
                "ci1_persistence": "yes",
                "ci2_evaluation": "yes",
                "ci3_year": "yes",
                "ci4_language": "yes",
                "ci5_publication_type": "yes",
                "ce1_no_cross_session_persistence": "no",
                "ce2_not_software_dev": "no",
                "ce3_no_evaluation": "no",
                "ce4_tutorial_editorial_or_descriptive_survey": "no",
                "ce5_duplicate_or_superseded": "no",
            }
        )
        if exclusion_code == "CE1":
            values["ci1_persistence"] = "no"
            values["ce1_no_cross_session_persistence"] = "yes"
        elif exclusion_code == "CE2":
            values["ci1_persistence"] = "uncertain"
            values["ce2_not_software_dev"] = "yes"
        elif exclusion_code == "CE3":
            values["ci2_evaluation"] = "no"
            values["ce3_no_evaluation"] = "yes"
        elif exclusion_code == "CE4":
            values["ce4_tutorial_editorial_or_descriptive_survey"] = "yes"
        elif exclusion_code == "CE5":
            values["ce5_duplicate_or_superseded"] = "yes"
        elif exclusion_code == "CI3":
            values["ci3_year"] = "no"
        elif exclusion_code == "CI4":
            values["ci4_language"] = "no"
        elif exclusion_code == "CI5":
            values["ci5_publication_type"] = "no"
        else:
            raise SystemExit(f"{row.get('full_text_id', '')}: unsupported exclusion_code {exclusion_code!r}")

    for column in CRITERION_COLUMNS:
        if column in row and row[column].strip():
            values[column] = row[column].strip()
    return values


def main() -> int:
    args = parse_args()
    screening_fields, screening_rows = read_tsv(args.screening_file)
    decision_fields, decision_rows = read_tsv(args.decisions_file)

    missing_screening_columns = sorted(set(SCREENING_COLUMNS + ["full_text_id"]) - set(screening_fields))
    if missing_screening_columns:
        raise SystemExit(
            f"{args.screening_file} is missing columns: {', '.join(missing_screening_columns)}"
        )
    if "full_text_id" not in decision_fields or "full_text_decision" not in decision_fields:
        raise SystemExit(f"{args.decisions_file} must include full_text_id and full_text_decision")

    screening_by_id = {row["full_text_id"]: row for row in screening_rows}
    if len(screening_by_id) != len(screening_rows):
        raise SystemExit("screening file has duplicate full_text_id values")

    seen: set[str] = set()
    reviewed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    counter: Counter[str] = Counter()
    for decision_row in decision_rows:
        validate_decision(decision_row)
        full_text_id = decision_row["full_text_id"].strip()
        if full_text_id in seen:
            raise SystemExit(f"duplicate decision for {full_text_id}")
        seen.add(full_text_id)
        if full_text_id not in screening_by_id:
            raise SystemExit(f"{full_text_id}: not found in screening file")

        target = screening_by_id[full_text_id]
        existing_decision = target.get("full_text_decision", "").strip()
        if existing_decision and not args.overwrite_existing:
            raise SystemExit(
                f"{full_text_id}: existing decision {existing_decision!r}; use --overwrite-existing if intended"
            )

        values = derived_values(decision_row)
        for column in SCREENING_COLUMNS:
            if column == "reviewed_at_utc":
                target[column] = reviewed_at
            elif column == "reviewer":
                target[column] = decision_row.get(column, "").strip() or args.reviewer
            elif column == "notes":
                target[column] = append_note(
                    target.get("notes", ""),
                    decision_row.get(column, "").strip(),
                )
            elif column in decision_fields:
                target[column] = decision_row.get(column, "").strip()
            else:
                target[column] = values.get(column, "")
        counter[target["full_text_decision"]] += 1

    print(f"screening_file\t{args.screening_file}")
    print(f"decisions_file\t{args.decisions_file}")
    print(f"decisions_read\t{len(decision_rows)}")
    print(f"reviewed_at_utc\t{reviewed_at}")
    for decision, count in sorted(counter.items()):
        print(f"applied_{decision}\t{count}")
    if args.dry_run:
        print("dry_run\ttrue")
        return 0
    write_tsv(args.screening_file, screening_fields, screening_rows)
    print("dry_run\tfalse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
