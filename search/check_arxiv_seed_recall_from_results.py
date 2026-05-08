#!/usr/bin/env python3
"""Check search seed recall from saved arXiv chunk results."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import check_arxiv_seed_recall as recall


def normalize_arxiv_id(value: str) -> str:
    return value.strip().rsplit("/", 1)[-1].split("v", 1)[0]


def load_results(path: Path) -> dict[str, list[dict[str, str]]]:
    by_id: dict[str, list[dict[str, str]]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            arxiv_id = normalize_arxiv_id(row["arxiv_id"])
            by_id.setdefault(arxiv_id, []).append(row)
    return by_id


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seed-set",
        default="search/seed-set.tsv",
        help="TSV seed set path",
    )
    parser.add_argument(
        "--results",
        default="search/arxiv-query-chunk-results.tsv",
        help="Saved arXiv chunk result TSV",
    )
    parser.add_argument(
        "--output",
        default="search/arxiv-seed-recall-from-results.tsv",
        help="Output TSV path",
    )
    parser.add_argument(
        "--groups",
        nargs="+",
        help="Only check seeds in these seed_group values",
    )
    parser.add_argument(
        "--seed-ids",
        nargs="+",
        help="Only check these seed_id values",
    )
    parser.add_argument(
        "--validate-required",
        action="store_true",
        help="Exit nonzero if any required database-query seed is unrecovered",
    )
    args = parser.parse_args()

    seeds = [seed for seed in recall.load_seeds(Path(args.seed_set)) if seed.get("arxiv_id")]
    seeds = recall.filter_seeds(seeds, groups=args.groups, seed_ids=args.seed_ids)
    results_by_id = load_results(Path(args.results))

    rows: list[dict[str, str]] = []
    for seed in seeds:
        arxiv_id = normalize_arxiv_id(seed["arxiv_id"])
        hits = results_by_id.get(arxiv_id, [])
        chunks = sorted({hit["query_chunk"] for hit in hits})
        logical_families = sorted({hit["logical_family"] for hit in hits})
        rows.append(
            {
                "seed_id": seed["seed_id"],
                "arxiv_id": seed["arxiv_id"],
                "seed_group": seed["seed_group"],
                "expected_status": seed["expected_status"],
                "search_recall_expectation": seed["search_recall_expectation"],
                "required_recall": "yes" if recall.is_required_recall(seed) else "no",
                "recovered": "yes" if hits else "no",
                "recovered_by": ";".join(chunks),
                "recovered_logical_families": ";".join(logical_families),
                "notes": seed["notes"],
            }
        )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "seed_id",
        "arxiv_id",
        "seed_group",
        "expected_status",
        "search_recall_expectation",
        "required_recall",
        "recovered",
        "recovered_by",
        "recovered_logical_families",
        "notes",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    failures = [
        row for row in rows if row["required_recall"] == "yes" and row["recovered"] != "yes"
    ]
    for row in rows:
        print(f'{row["seed_id"]}\t{row["recovered"]}\t{row["recovered_logical_families"]}')
    print(f"Wrote {output_path}", file=sys.stderr)

    if args.validate_required and failures:
        print("Required seed recall validation failed:", file=sys.stderr)
        for row in failures:
            print(f'- {row["seed_id"]}: recovered={row["recovered"]}', file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
