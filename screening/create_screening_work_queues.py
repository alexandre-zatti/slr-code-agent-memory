#!/usr/bin/env python3
"""Create search title/abstract screening work queues.

The queues are derived from the canonical screening ledger and do not make
substantive eligibility decisions.  They identify records that need metadata
lookup and reconcile seed papers against the screening pool.
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone


DEFAULT_SCREENING = pathlib.Path("screening/title-abstract-screening.tsv")
DEFAULT_SEEDS = pathlib.Path("search/seed-set.tsv")
DEFAULT_MISSING_ABSTRACTS = pathlib.Path(
    "screening/title-abstract-screening-missing-abstracts.tsv"
)
DEFAULT_SEED_RECONCILIATION = pathlib.Path(
    "screening/title-abstract-screening-seed-reconciliation.tsv"
)
DEFAULT_METADATA = pathlib.Path("screening/title-abstract-screening-work-queues-metadata.tsv")
DEFAULT_PRIORITY_QUEUE = pathlib.Path("screening/title-abstract-screening-priority-queue.tsv")

MISSING_ABSTRACT_COLUMNS = [
    "screening_id",
    "dedup_group",
    "title",
    "year",
    "authors",
    "venue",
    "doi",
    "arxiv_id",
    "sources",
    "source_record_ids",
    "source_files",
    "logical_families",
    "provenance",
    "title_abstract_decision",
    "exclusion_code",
    "notes",
]

SEED_RECONCILIATION_COLUMNS = [
    "seed_id",
    "title",
    "year",
    "arxiv_id",
    "doi",
    "seed_group",
    "expected_status",
    "search_recall_expectation",
    "match_status",
    "match_method",
    "screening_id",
    "dedup_group",
    "matched_title",
    "matched_year",
    "matched_sources",
    "matched_source_record_ids",
    "matched_decision",
    "matched_exclusion_code",
    "notes",
]

PRIORITY_QUEUE_COLUMNS = [
    "screening_id",
    "priority_bucket",
    "priority_reason",
    "has_abstract",
    "sources",
    "year",
    "title",
    "authors",
    "venue",
    "doi",
    "arxiv_id",
    "abstract",
    "logical_families",
    "query_chunks",
    "provenance",
    "duplicate_row_count",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create search screening work queues.")
    parser.add_argument("--screening-file", type=pathlib.Path, default=DEFAULT_SCREENING)
    parser.add_argument("--seed-file", type=pathlib.Path, default=DEFAULT_SEEDS)
    parser.add_argument("--missing-abstracts-output", type=pathlib.Path, default=DEFAULT_MISSING_ABSTRACTS)
    parser.add_argument("--seed-reconciliation-output", type=pathlib.Path, default=DEFAULT_SEED_RECONCILIATION)
    parser.add_argument("--priority-output", type=pathlib.Path, default=DEFAULT_PRIORITY_QUEUE)
    parser.add_argument("--metadata-output", type=pathlib.Path, default=DEFAULT_METADATA)
    parser.add_argument(
        "--include-decided-missing-abstracts",
        action="store_true",
        help="Include already decided records in the missing-abstract queue.",
    )
    return parser.parse_args()


def read_tsv(path: pathlib.Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise SystemExit(f"{path} has no header")
        return reader.fieldnames, list(reader)


def write_tsv(path: pathlib.Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def split_values(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in re.split(r"[;|]", value) if part.strip()]


def normalize_doi(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    value = re.sub(r"^doi:\s*", "", value)
    return value.strip().rstrip(".")


def normalize_title(value: str) -> str:
    value = (value or "").lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def normalize_arxiv_id(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    value = re.sub(r"^https?://arxiv\.org/(abs|pdf)/", "", value, flags=re.I)
    value = re.sub(r"\.pdf$", "", value, flags=re.I)
    value = re.sub(r"^arxiv:", "", value, flags=re.I)
    value = re.sub(r"^10\.48550/arxiv\.", "", value, flags=re.I)
    match = re.search(r"(\d{4}\.\d{4,5})(?:v\d+)?", value, flags=re.I)
    if match:
        return match.group(1)
    value = re.sub(r"v\d+$", "", value, flags=re.I)
    return value.lower()


def build_maps(rows: list[dict[str, str]]) -> dict[str, dict[str, list[dict[str, str]]]]:
    maps: dict[str, dict[str, list[dict[str, str]]]] = {
        "arxiv_id": defaultdict(list),
        "doi": defaultdict(list),
        "title": defaultdict(list),
    }

    def add_unique(kind: str, key: str, row: dict[str, str]) -> None:
        bucket = maps[kind][key]
        row_id = row.get("screening_id", "")
        if any(existing.get("screening_id", "") == row_id for existing in bucket):
            return
        bucket.append(row)

    for row in rows:
        arxiv_values = split_values(row.get("arxiv_id", ""))
        doi_values = split_values(row.get("doi", ""))
        for doi in doi_values:
            normalized = normalize_doi(doi)
            if normalized:
                add_unique("doi", normalized, row)
            arxiv_from_doi = normalize_arxiv_id(normalized)
            if arxiv_from_doi:
                add_unique("arxiv_id", arxiv_from_doi, row)
        for arxiv_id in arxiv_values:
            normalized = normalize_arxiv_id(arxiv_id)
            if normalized:
                add_unique("arxiv_id", normalized, row)
        title = normalize_title(row.get("title", ""))
        if title:
            add_unique("title", title, row)
    return maps


def source_set(row: dict[str, str]) -> set[str]:
    return {part.strip() for part in row.get("sources", "").split(";") if part.strip()}


def priority_for_row(row: dict[str, str]) -> tuple[int, str]:
    sources = source_set(row)
    has_abstract = bool(row.get("abstract", "").strip())
    has_arxiv = "arxiv_chunk" in sources
    has_scopus = "scopus" in sources
    has_citation = "citations" in sources
    has_database = has_arxiv or has_scopus

    if not has_abstract:
        return 5, "missing abstract; resolve through title-only triage or metadata/PDF lookup"
    if has_database and has_citation:
        return 1, "database and citation-chasing overlap"
    if has_arxiv and has_scopus:
        return 2, "arXiv and Scopus overlap"
    if has_database:
        return 3, "database-search record"
    if has_citation:
        return 4, "citation-chasing-only record with abstract"
    return 6, "unclassified source route"


def sort_year_key(row: dict[str, str]) -> int:
    year = (row.get("year") or "").strip()
    if len(year) == 4 and year.isdigit():
        return int(year)
    return 0


def match_seed(
    seed: dict[str, str],
    maps: dict[str, dict[str, list[dict[str, str]]]],
) -> tuple[str, str, dict[str, str] | None]:
    arxiv_candidates: list[str] = []
    for value in split_values(seed.get("arxiv_id", "")):
        normalized = normalize_arxiv_id(value)
        if normalized:
            arxiv_candidates.append(normalized)
    doi = normalize_doi(seed.get("doi", ""))
    arxiv_from_doi = normalize_arxiv_id(doi)
    if arxiv_from_doi:
        arxiv_candidates.append(arxiv_from_doi)

    for arxiv_id in arxiv_candidates:
        rows = maps["arxiv_id"].get(arxiv_id, [])
        if rows:
            return ("matched_unique" if len(rows) == 1 else "matched_multiple", "arxiv_id", rows[0])

    if doi:
        rows = maps["doi"].get(doi, [])
        if rows:
            return ("matched_unique" if len(rows) == 1 else "matched_multiple", "doi", rows[0])

    title = normalize_title(seed.get("title", ""))
    if title:
        rows = maps["title"].get(title, [])
        if rows:
            return ("matched_unique" if len(rows) == 1 else "matched_multiple", "title", rows[0])

    return "not_matched", "", None


def main() -> int:
    args = parse_args()
    _, screening_rows = read_tsv(args.screening_file)
    _, seed_rows = read_tsv(args.seed_file)

    missing_rows = []
    for row in screening_rows:
        if row.get("abstract", "").strip():
            continue
        if not args.include_decided_missing_abstracts and row.get("title_abstract_decision", "").strip():
            continue
        missing_rows.append({column: row.get(column, "") for column in MISSING_ABSTRACT_COLUMNS})

    maps = build_maps(screening_rows)
    priority_rows = []
    priority_counter: Counter[str] = Counter()
    for row in screening_rows:
        if row.get("title_abstract_decision", "").strip():
            continue
        bucket, reason = priority_for_row(row)
        priority_counter[str(bucket)] += 1
        priority_rows.append(
            {
                "screening_id": row.get("screening_id", ""),
                "priority_bucket": str(bucket),
                "priority_reason": reason,
                "has_abstract": str(bool(row.get("abstract", "").strip())).lower(),
                "sources": row.get("sources", ""),
                "year": row.get("year", ""),
                "title": row.get("title", ""),
                "authors": row.get("authors", ""),
                "venue": row.get("venue", ""),
                "doi": row.get("doi", ""),
                "arxiv_id": row.get("arxiv_id", ""),
                "abstract": row.get("abstract", ""),
                "logical_families": row.get("logical_families", ""),
                "query_chunks": row.get("query_chunks", ""),
                "provenance": row.get("provenance", ""),
                "duplicate_row_count": row.get("duplicate_row_count", ""),
                "notes": row.get("notes", ""),
            }
        )
    priority_rows.sort(
        key=lambda row: (
            int(row["priority_bucket"]),
            -sort_year_key(row),
            row.get("screening_id", ""),
        )
    )

    reconciliation_rows = []
    match_counter: Counter[str] = Counter()
    method_counter: Counter[str] = Counter()
    for seed in seed_rows:
        match_status, match_method, matched = match_seed(seed, maps)
        match_counter[match_status] += 1
        if match_method:
            method_counter[match_method] += 1
        reconciliation_rows.append(
            {
                "seed_id": seed.get("seed_id", ""),
                "title": seed.get("title", ""),
                "year": seed.get("year", ""),
                "arxiv_id": seed.get("arxiv_id", ""),
                "doi": seed.get("doi", ""),
                "seed_group": seed.get("seed_group", ""),
                "expected_status": seed.get("expected_status", ""),
                "search_recall_expectation": seed.get("search_recall_expectation", ""),
                "match_status": match_status,
                "match_method": match_method,
                "screening_id": matched.get("screening_id", "") if matched else "",
                "dedup_group": matched.get("dedup_group", "") if matched else "",
                "matched_title": matched.get("title", "") if matched else "",
                "matched_year": matched.get("year", "") if matched else "",
                "matched_sources": matched.get("sources", "") if matched else "",
                "matched_source_record_ids": matched.get("source_record_ids", "") if matched else "",
                "matched_decision": matched.get("title_abstract_decision", "") if matched else "",
                "matched_exclusion_code": matched.get("exclusion_code", "") if matched else "",
                "notes": seed.get("notes", ""),
            }
        )

    metadata_rows = [
        {"metric": "generated_at_utc", "value": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")},
        {"metric": "screening_rows", "value": str(len(screening_rows))},
        {"metric": "missing_abstract_rows_queued", "value": str(len(missing_rows))},
        {"metric": "missing_abstract_queue_includes_decided", "value": str(args.include_decided_missing_abstracts).lower()},
        {"metric": "priority_queue_rows", "value": str(len(priority_rows))},
        {"metric": "seed_rows", "value": str(len(seed_rows))},
        {"metric": "seed_matched_unique", "value": str(match_counter["matched_unique"])},
        {"metric": "seed_matched_multiple", "value": str(match_counter["matched_multiple"])},
        {"metric": "seed_not_matched", "value": str(match_counter["not_matched"])},
        {"metric": "seed_match_by_arxiv_id", "value": str(method_counter["arxiv_id"])},
        {"metric": "seed_match_by_doi", "value": str(method_counter["doi"])},
        {"metric": "seed_match_by_title", "value": str(method_counter["title"])},
    ]
    for bucket in sorted(priority_counter, key=int):
        metadata_rows.append(
            {"metric": f"priority_bucket_{bucket}_rows", "value": str(priority_counter[bucket])}
        )

    write_tsv(args.missing_abstracts_output, MISSING_ABSTRACT_COLUMNS, missing_rows)
    write_tsv(args.seed_reconciliation_output, SEED_RECONCILIATION_COLUMNS, reconciliation_rows)
    write_tsv(args.priority_output, PRIORITY_QUEUE_COLUMNS, priority_rows)
    write_tsv(args.metadata_output, ["metric", "value"], metadata_rows)

    print(f"screening_rows\t{len(screening_rows)}")
    print(f"missing_abstract_rows_queued\t{len(missing_rows)}")
    print(f"priority_queue_rows\t{len(priority_rows)}")
    print(f"seed_rows\t{len(seed_rows)}")
    print(f"seed_matched_unique\t{match_counter['matched_unique']}")
    print(f"seed_matched_multiple\t{match_counter['matched_multiple']}")
    print(f"seed_not_matched\t{match_counter['not_matched']}")
    print(f"missing_abstracts_output\t{args.missing_abstracts_output}")
    print(f"seed_reconciliation_output\t{args.seed_reconciliation_output}")
    print(f"priority_output\t{args.priority_output}")
    print(f"metadata_output\t{args.metadata_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
