#!/usr/bin/env python3
"""Create the search title/abstract screening pool from a dedup ledger."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def join_unique(rows: list[dict[str, str]], field: str) -> str:
    values = []
    seen = set()
    for row in rows:
        value = clean(row.get(field, ""))
        if value and value not in seen:
            values.append(value)
            seen.add(value)
    return "; ".join(values)


def first_nonempty(rows: list[dict[str, str]], field: str, preferred: dict[str, str]) -> str:
    preferred_value = clean(preferred.get(field, ""))
    if preferred_value:
        return preferred_value
    for row in rows:
        value = clean(row.get(field, ""))
        if value:
            return value
    return ""


def longest_value(rows: list[dict[str, str]], field: str) -> str:
    return max((clean(row.get(field, "")) for row in rows), key=len, default="")


def choose_keeper(rows: list[dict[str, str]]) -> dict[str, str]:
    for row in rows:
        if row.get("keep_record") == "yes":
            return row
    return rows[0]


def read_groups(path: Path) -> list[tuple[str, list[dict[str, str]]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            groups[row["dedup_group"]].append(row)
    return sorted(groups.items(), key=lambda item: item[0])


def write_pool(input_path: Path, output_path: Path, metadata_path: Path) -> None:
    groups = read_groups(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "screening_id",
        "dedup_group",
        "title",
        "year",
        "authors",
        "venue",
        "doi",
        "arxiv_id",
        "abstract",
        "sources",
        "source_record_ids",
        "source_files",
        "query_chunks",
        "logical_families",
        "provenance",
        "duplicate_row_count",
        "duplicate_record_ids",
        "title_abstract_decision",
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
        "criterion_rationale",
        "reviewer",
        "reviewed_at_utc",
        "notes",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for index, (dedup_group, rows) in enumerate(groups, start=1):
            keeper = choose_keeper(rows)
            duplicate_ids = [
                row["record_id"]
                for row in rows
                if row["record_id"] != keeper.get("record_id", "")
            ]
            writer.writerow(
                {
                    "screening_id": f"TA{index:05d}",
                    "dedup_group": dedup_group,
                    "title": keeper.get("title", ""),
                    "year": first_nonempty(rows, "year", keeper),
                    "authors": first_nonempty(rows, "authors", keeper),
                    "venue": first_nonempty(rows, "venue", keeper),
                    "doi": first_nonempty(rows, "doi", keeper),
                    "arxiv_id": first_nonempty(rows, "arxiv_id", keeper),
                    "abstract": longest_value(rows, "abstract"),
                    "sources": join_unique(rows, "source"),
                    "source_record_ids": join_unique(rows, "source_record_id"),
                    "source_files": join_unique(rows, "source_file"),
                    "query_chunks": join_unique(rows, "query_chunk"),
                    "logical_families": join_unique(rows, "logical_family"),
                    "provenance": join_unique(rows, "provenance"),
                    "duplicate_row_count": str(len(rows) - 1),
                    "duplicate_record_ids": "; ".join(duplicate_ids),
                    "title_abstract_decision": "",
                    "ci1_persistence": "",
                    "ci2_evaluation": "",
                    "ci3_year": "",
                    "ci4_language": "",
                    "ci5_publication_type": "",
                    "ce1_no_cross_session_persistence": "",
                    "ce2_not_software_dev": "",
                    "ce3_no_evaluation": "",
                    "ce4_tutorial_editorial_or_descriptive_survey": "",
                    "ce5_duplicate_or_superseded": "",
                    "exclusion_code": "",
                    "criterion_rationale": "",
                    "reviewer": "",
                    "reviewed_at_utc": "",
                    "notes": "",
                }
            )

    source_counts: dict[str, int] = defaultdict(int)
    missing_abstract = 0
    for _dedup_group, rows in groups:
        if not longest_value(rows, "abstract"):
            missing_abstract += 1
        for source in {row.get("source", "") for row in rows if row.get("source")}:
            source_counts[source] += 1

    with metadata_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["key", "value"])
        writer.writerow(["timestamp_utc", datetime.now(UTC).isoformat()])
        writer.writerow(["input", str(input_path)])
        writer.writerow(["output", str(output_path)])
        writer.writerow(["deduplicated_groups", str(len(groups))])
        writer.writerow(["missing_screening_abstracts", str(missing_abstract)])
        for source, count in sorted(source_counts.items()):
            writer.writerow([f"groups_with_source_{source}", str(count)])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dedup", default="search/dedup.tsv")
    parser.add_argument(
        "--output",
        default="screening/title-abstract-screening.tsv",
    )
    parser.add_argument(
        "--metadata-output",
        default="screening/title-abstract-screening-metadata.tsv",
    )
    args = parser.parse_args()

    write_pool(Path(args.dedup), Path(args.output), Path(args.metadata_output))
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
