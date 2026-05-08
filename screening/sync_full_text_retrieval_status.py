#!/usr/bin/env python3
"""Sync search retrieval status into the full-text screening ledger."""

from __future__ import annotations

import argparse
import csv
import pathlib
import tempfile


DEFAULT_SCREENING = pathlib.Path("screening/full-text-screening.tsv")
DEFAULT_STATUS = pathlib.Path("search/full-text-retrieval-status.tsv")

SYNC_FIELDS = [
    "retrieval_status",
    "pdf_path",
    "text_path",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screening-file", type=pathlib.Path, default=DEFAULT_SCREENING)
    parser.add_argument("--status-file", type=pathlib.Path, default=DEFAULT_STATUS)
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


def main() -> int:
    args = parse_args()
    screening_fields, screening_rows = read_tsv(args.screening_file)
    _, status_rows = read_tsv(args.status_file)
    by_id = {row["full_text_id"]: row for row in status_rows}
    if len(by_id) != len(status_rows):
        raise SystemExit("status file contains duplicate full_text_id values")

    synced = 0
    missing = []
    for row in screening_rows:
        full_text_id = row["full_text_id"]
        status = by_id.get(full_text_id)
        if not status:
            missing.append(full_text_id)
            continue
        for field in SYNC_FIELDS:
            row[field] = status.get(field, "")
        retrieval_note = ""
        if status.get("retrieval_status") == "failed":
            retrieval_note = f"retrieval failed: {status.get('failure_reason', '')}".strip()
        elif status.get("retrieval_status"):
            retrieval_note = f"retrieval {status.get('retrieval_status')} via {status.get('retrieval_source', '')}".strip()
        if retrieval_note and retrieval_note not in row.get("notes", ""):
            row["notes"] = f"{row.get('notes', '').strip()} | {retrieval_note}".strip(" |")
        synced += 1

    if missing:
        raise SystemExit(f"missing retrieval statuses for: {', '.join(missing[:10])}")
    write_tsv(args.screening_file, screening_fields, screening_rows)
    print(f"screening_file\t{args.screening_file}")
    print(f"status_file\t{args.status_file}")
    print(f"synced\t{synced}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
