#!/usr/bin/env python3
"""Create search full-text screening and retrieval ledgers."""

from __future__ import annotations

import argparse
import csv
import pathlib
import re
import tempfile
from collections import Counter


DEFAULT_TITLE_ABSTRACT = pathlib.Path("screening/title-abstract-screening.tsv")
DEFAULT_FULL_TEXT = pathlib.Path("screening/full-text-screening.tsv")
DEFAULT_RETRIEVAL = pathlib.Path("search/full-text-retrieval.tsv")
PDF_ROOT = pathlib.Path("search/full-texts")


FULL_TEXT_FIELDS = [
    "full_text_id",
    "screening_id",
    "dedup_group",
    "title",
    "year",
    "authors",
    "venue",
    "doi",
    "arxiv_id",
    "sources",
    "source_files",
    "provenance",
    "duplicate_row_count",
    "title_abstract_decision",
    "title_abstract_rationale",
    "has_abstract",
    "needs_metadata_lookup",
    "retrieval_priority",
    "retrieval_status",
    "pdf_path",
    "text_path",
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


RETRIEVAL_FIELDS = [
    "full_text_id",
    "screening_id",
    "title",
    "year",
    "title_abstract_decision",
    "retrieval_priority",
    "needs_metadata_lookup",
    "doi",
    "arxiv_id",
    "sources",
    "preferred_url",
    "pdf_path",
    "text_path",
    "retrieval_status",
    "retrieval_source",
    "retrieved_at_utc",
    "failure_reason",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title-abstract", type=pathlib.Path, default=DEFAULT_TITLE_ABSTRACT)
    parser.add_argument("--full-text-output", type=pathlib.Path, default=DEFAULT_FULL_TEXT)
    parser.add_argument("--retrieval-output", type=pathlib.Path, default=DEFAULT_RETRIEVAL)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def read_tsv(path: pathlib.Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise SystemExit(f"{path} has no header")
        return reader.fieldnames, list(reader)


def write_tsv(path: pathlib.Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
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


def slugify(value: str, fallback: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value.lower()).strip("-")
    value = re.sub(r"-{2,}", "-", value)
    if not value:
        return fallback.lower()
    return value[:80].strip("-") or fallback.lower()


def normalize_arxiv_id(value: str) -> str:
    value = (value or "").strip()
    if value.lower().startswith("arxiv:"):
        value = value.split(":", 1)[1]
    return re.sub(r"v\d+$", "", value)


def priority_for(row: dict[str, str]) -> str:
    decision = row["title_abstract_decision"]
    has_abstract = bool(row.get("abstract", "").strip())
    if decision == "include":
        return "1_include"
    if not has_abstract:
        return "2_missing_abstract_maybe"
    return "3_maybe"


def preferred_url(row: dict[str, str]) -> str:
    arxiv_id = normalize_arxiv_id(row.get("arxiv_id", ""))
    if arxiv_id:
        return f"https://arxiv.org/pdf/{arxiv_id}"
    doi = (row.get("doi") or "").strip()
    if doi:
        return f"https://doi.org/{doi}"
    return ""


def make_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    selected = [
        row
        for row in rows
        if row.get("title_abstract_decision", "").strip() in {"include", "maybe"}
    ]
    selected.sort(
        key=lambda row: (
            priority_for(row),
            row.get("year", "") or "9999",
            row.get("screening_id", ""),
        )
    )

    full_text_rows: list[dict[str, str]] = []
    retrieval_rows: list[dict[str, str]] = []
    for idx, row in enumerate(selected, 1):
        full_text_id = f"FT{idx:04d}"
        screening_id = row["screening_id"]
        slug = slugify(row.get("title", ""), screening_id)
        pdf_path = PDF_ROOT / "pdf" / f"{full_text_id}_{screening_id}_{slug}.pdf"
        text_path = PDF_ROOT / "text" / f"{full_text_id}_{screening_id}_{slug}.txt"
        has_abstract = "yes" if row.get("abstract", "").strip() else "no"
        needs_metadata_lookup = "yes" if has_abstract == "no" else "no"
        retrieval_priority = priority_for(row)
        base_notes = row.get("notes", "").strip()
        if needs_metadata_lookup == "yes":
            base_notes = (
                f"{base_notes} | missing abstract; verify metadata/full text"
                if base_notes
                else "missing abstract; verify metadata/full text"
            )

        full_text_rows.append(
            {
                "full_text_id": full_text_id,
                "screening_id": screening_id,
                "dedup_group": row.get("dedup_group", ""),
                "title": row.get("title", ""),
                "year": row.get("year", ""),
                "authors": row.get("authors", ""),
                "venue": row.get("venue", ""),
                "doi": row.get("doi", ""),
                "arxiv_id": normalize_arxiv_id(row.get("arxiv_id", "")),
                "sources": row.get("sources", ""),
                "source_files": row.get("source_files", ""),
                "provenance": row.get("provenance", ""),
                "duplicate_row_count": row.get("duplicate_row_count", ""),
                "title_abstract_decision": row.get("title_abstract_decision", ""),
                "title_abstract_rationale": row.get("criterion_rationale", ""),
                "has_abstract": has_abstract,
                "needs_metadata_lookup": needs_metadata_lookup,
                "retrieval_priority": retrieval_priority,
                "retrieval_status": "",
                "pdf_path": str(pdf_path),
                "text_path": str(text_path),
                "full_text_decision": "",
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
                "full_text_rationale": "",
                "reviewer": "",
                "reviewed_at_utc": "",
                "notes": base_notes,
            }
        )
        retrieval_rows.append(
            {
                "full_text_id": full_text_id,
                "screening_id": screening_id,
                "title": row.get("title", ""),
                "year": row.get("year", ""),
                "title_abstract_decision": row.get("title_abstract_decision", ""),
                "retrieval_priority": retrieval_priority,
                "needs_metadata_lookup": needs_metadata_lookup,
                "doi": row.get("doi", ""),
                "arxiv_id": normalize_arxiv_id(row.get("arxiv_id", "")),
                "sources": row.get("sources", ""),
                "preferred_url": preferred_url(row),
                "pdf_path": str(pdf_path),
                "text_path": str(text_path),
                "retrieval_status": "",
                "retrieval_source": "",
                "retrieved_at_utc": "",
                "failure_reason": "",
                "notes": base_notes,
            }
        )
    return full_text_rows, retrieval_rows


def main() -> int:
    args = parse_args()
    for path in [args.full_text_output, args.retrieval_output]:
        if path.exists() and not args.overwrite:
            raise SystemExit(f"{path} exists; use --overwrite if intended")

    _, rows = read_tsv(args.title_abstract)
    full_text_rows, retrieval_rows = make_rows(rows)
    if len(full_text_rows) != 165:
        raise SystemExit(f"expected 165 include/maybe rows, found {len(full_text_rows)}")

    write_tsv(args.full_text_output, FULL_TEXT_FIELDS, full_text_rows)
    write_tsv(args.retrieval_output, RETRIEVAL_FIELDS, retrieval_rows)
    for subdir in ["pdf", "text"]:
        (PDF_ROOT / subdir).mkdir(parents=True, exist_ok=True)

    decisions = Counter(row["title_abstract_decision"] for row in full_text_rows)
    priorities = Counter(row["retrieval_priority"] for row in full_text_rows)
    print(f"full_text_output\t{args.full_text_output}")
    print(f"retrieval_output\t{args.retrieval_output}")
    print(f"rows\t{len(full_text_rows)}")
    print(f"include\t{decisions['include']}")
    print(f"maybe\t{decisions['maybe']}")
    for key in sorted(priorities):
        print(f"{key}\t{priorities[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
