#!/usr/bin/env python3
"""Create a reproducible deduplication ledger for search results.

The script is intentionally local-only: it reads exported search artifacts and
writes a TSV ledger. It does not call arXiv, Scopus, Semantic Scholar, or any
other external service.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Record:
    record_id: str
    source: str
    source_file: str
    source_record_id: str
    title: str
    year: str
    doi: str
    arxiv_id: str
    authors: str
    venue: str
    abstract: str
    provenance: str
    query_chunk: str = ""
    logical_family: str = ""

    @property
    def title_key(self) -> str:
        return normalize_title(self.title)


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, index: int) -> int:
        while self.parent[index] != index:
            self.parent[index] = self.parent[self.parent[index]]
            index = self.parent[index]
        return index

    def union(self, left: int, right: int) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


def normalize_space(value: str) -> str:
    return " ".join(str(value or "").split())


def normalize_doi(value: str) -> str:
    value = normalize_space(value).lower()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    return value.rstrip(".")


def normalize_arxiv_id(value: str) -> str:
    value = normalize_space(value)
    value = value.rsplit("/", 1)[-1]
    value = re.sub(r"^arxiv:", "", value, flags=re.IGNORECASE)
    value = re.sub(r"v\d+$", "", value)
    return value


def arxiv_id_from_doi(doi: str) -> str:
    match = re.match(r"10\.48550/arxiv\.(.+)$", doi, flags=re.IGNORECASE)
    return normalize_arxiv_id(match.group(1)) if match else ""


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKD", normalize_space(value)).encode(
        "ascii", "ignore"
    ).decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return normalize_space(value)


def authors_to_text(value) -> str:  # noqa: ANN001 - accepts API-specific shapes
    if not value:
        return ""
    if isinstance(value, str):
        return normalize_space(value)
    authors: list[str] = []
    for item in value:
        if isinstance(item, dict):
            authors.append(item.get("name", "") or item.get("full_name", ""))
        else:
            authors.append(str(item))
    return "; ".join(normalize_space(author) for author in authors if author)


def year_from_date(value: str) -> str:
    return normalize_space(value)[:4]


def load_arxiv_tsv(path: Path, source_label: str) -> list[Record]:
    records: list[Record] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for index, row in enumerate(csv.DictReader(handle, delimiter="\t"), start=1):
            arxiv_id = normalize_arxiv_id(row.get("arxiv_id", ""))
            records.append(
                Record(
                    record_id=f"{source_label}:{index}",
                    source=source_label,
                    source_file=str(path),
                    source_record_id=arxiv_id,
                    title=normalize_space(row.get("title", "")),
                    year=year_from_date(row.get("published", "")),
                    doi=f"10.48550/arXiv.{arxiv_id}" if arxiv_id else "",
                    arxiv_id=arxiv_id,
                    authors="",
                    venue="arXiv",
                    abstract=normalize_space(row.get("abstract", "")),
                    provenance=normalize_space(row.get("categories", "")),
                    query_chunk=normalize_space(row.get("query_chunk", "")),
                    logical_family=normalize_space(row.get("logical_family", "")),
                )
            )
    return records


def load_arxiv_json(path: Path, source_label: str) -> list[Record]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data if isinstance(data, list) else data.get("papers", data.get("entries", []))
    records: list[Record] = []
    for index, row in enumerate(entries, start=1):
        arxiv_id = normalize_arxiv_id(row.get("id", row.get("arxiv_id", "")))
        records.append(
            Record(
                record_id=f"{source_label}:{index}",
                source=source_label,
                source_file=str(path),
                source_record_id=arxiv_id,
                title=normalize_space(row.get("title", "")),
                year=year_from_date(row.get("published", row.get("date", ""))),
                doi=f"10.48550/arXiv.{arxiv_id}" if arxiv_id else "",
                arxiv_id=arxiv_id,
                authors=authors_to_text(row.get("authors", [])),
                venue="arXiv",
                abstract=normalize_space(row.get("abstract", row.get("summary", ""))),
                provenance=";".join(row.get("categories", []))
                if isinstance(row.get("categories", []), list)
                else normalize_space(row.get("categories", "")),
            )
        )
    return records


def load_scopus_json(path: Path, source_label: str) -> list[Record]:
    data = json.loads(path.read_text(encoding="utf-8"))
    branch = normalize_space(data.get("branch", ""))
    if "pages" in data:
        entries = []
        for page in data.get("pages", []):
            search = page.get("raw", {}).get("search-results", {})
            entries.extend(search.get("entry", []) or [])
    elif "entries" in data:
        entries = data["entries"]
    else:
        entries = data.get("search-results", data).get("entry", [])
    records: list[Record] = []
    for index, row in enumerate(entries, start=1):
        doi = normalize_doi(row.get("prism:doi", ""))
        arxiv_id = arxiv_id_from_doi(doi)
        records.append(
            Record(
                record_id=f"{source_label}:{index}",
                source=source_label,
                source_file=str(path),
                source_record_id=normalize_space(
                    row.get("dc:identifier", row.get("eid", f"row-{index}"))
                ),
                title=normalize_space(row.get("dc:title", "")),
                year=year_from_date(row.get("prism:coverDate", "")),
                doi=doi,
                arxiv_id=arxiv_id,
                authors=authors_to_text(row.get("dc:creator", "")),
                venue=normalize_space(row.get("prism:publicationName", "")),
                abstract=normalize_space(row.get("dc:description", "")),
                provenance="; ".join(
                    part
                    for part in [
                        branch,
                        normalize_space(row.get("subtypeDescription", "")),
                    ]
                    if part
                ),
                query_chunk=branch,
                logical_family=branch,
            )
        )
    return records


def load_citations_json(path: Path, source_label: str) -> list[Record]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data if isinstance(data, list) else data.get("papers", data.get("results", []))
    records: list[Record] = []
    for index, row in enumerate(entries, start=1):
        doi = normalize_doi(row.get("doi", ""))
        arxiv_id = normalize_arxiv_id(row.get("arxivId", "")) or arxiv_id_from_doi(doi)
        provenance_parts = [normalize_space(row.get("source", ""))]
        for key in ["forward_from", "backward_from"]:
            values = row.get(key, [])
            if values:
                provenance_parts.append(f"{key}={';'.join(str(value) for value in values)}")
        records.append(
            Record(
                record_id=f"{source_label}:{index}",
                source=source_label,
                source_file=str(path),
                source_record_id=normalize_space(row.get("paperId", f"row-{index}")),
                title=normalize_space(row.get("title", "")),
                year=str(row.get("year", "") or ""),
                doi=doi,
                arxiv_id=arxiv_id,
                authors=authors_to_text(row.get("authors", [])),
                venue="",
                abstract=normalize_space(row.get("abstract", "")),
                provenance=" | ".join(part for part in provenance_parts if part),
            )
        )
    return records


def add_records(
    records: list[Record],
    paths: list[str] | None,
    loader,
    source_label: str,
) -> None:
    for path_str in paths or []:
        records.extend(loader(Path(path_str), source_label))


def group_records(records: list[Record]) -> dict[int, list[int]]:
    union = UnionFind(len(records))
    indexes_by_key: dict[tuple[str, str], list[int]] = {}

    for index, record in enumerate(records):
        keys: list[tuple[str, str]] = []
        if record.arxiv_id:
            keys.append(("arxiv_id", record.arxiv_id))
        if record.doi:
            keys.append(("doi", record.doi))
        if record.title_key:
            keys.append(("title", record.title_key))
        for key in keys:
            indexes_by_key.setdefault(key, []).append(index)

    for indexes in indexes_by_key.values():
        first = indexes[0]
        for other in indexes[1:]:
            union.union(first, other)

    groups: dict[int, list[int]] = {}
    for index in range(len(records)):
        groups.setdefault(union.find(index), []).append(index)
    return groups


def source_priority(source: str) -> int:
    return {
        "scopus": 40,
        "arxiv": 30,
        "arxiv_chunk": 30,
        "citations": 20,
    }.get(source, 10)


def record_score(record: Record) -> tuple[int, int, int, str]:
    doi_score = 20 if record.doi and not record.doi.startswith("10.48550/arxiv.") else 5
    abstract_score = min(len(record.abstract), 2000)
    return (
        source_priority(record.source) + doi_score,
        abstract_score,
        len(record.title),
        record.record_id,
    )


def group_keys(group: list[Record]) -> str:
    keys: list[str] = []
    for attr in ["arxiv_id", "doi", "title_key"]:
        values = sorted({getattr(record, attr) for record in group if getattr(record, attr)})
        if values:
            keys.append(f"{attr}={';'.join(values)}")
    return " | ".join(keys)


def write_ledger(records: list[Record], output_path: Path) -> None:
    groups = group_records(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "dedup_group",
        "keep_record",
        "duplicate_of",
        "duplicate_reason",
        "record_id",
        "source",
        "source_file",
        "source_record_id",
        "title",
        "year",
        "doi",
        "arxiv_id",
        "title_key",
        "authors",
        "venue",
        "query_chunk",
        "logical_family",
        "provenance",
        "abstract",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for group_number, indexes in enumerate(
            sorted(groups.values(), key=lambda values: min(values)),
            start=1,
        ):
            group = [records[index] for index in indexes]
            keeper = max(group, key=record_score)
            keys = group_keys(group)
            for record in sorted(group, key=lambda item: item.record_id):
                writer.writerow(
                    {
                        "dedup_group": f"D{group_number:05d}",
                        "keep_record": "yes" if record is keeper else "no",
                        "duplicate_of": "" if record is keeper else keeper.record_id,
                        "duplicate_reason": "keep" if record is keeper else keys,
                        "record_id": record.record_id,
                        "source": record.source,
                        "source_file": record.source_file,
                        "source_record_id": record.source_record_id,
                        "title": record.title,
                        "year": record.year,
                        "doi": record.doi,
                        "arxiv_id": record.arxiv_id,
                        "title_key": record.title_key,
                        "authors": record.authors,
                        "venue": record.venue,
                        "query_chunk": record.query_chunk,
                        "logical_family": record.logical_family,
                        "provenance": record.provenance,
                        "abstract": record.abstract,
                    }
                )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arxiv-tsv", nargs="+", help="Saved arXiv chunk TSV files.")
    parser.add_argument("--arxiv-json", nargs="+", help="arXiv JSON export files.")
    parser.add_argument("--scopus-json", nargs="+", help="Scopus JSON export files.")
    parser.add_argument("--citations-json", nargs="+", help="Citation-chasing JSON files.")
    parser.add_argument(
        "--output",
        default="search/dedup.tsv",
        help="Output TSV ledger path.",
    )
    args = parser.parse_args()

    records: list[Record] = []
    add_records(records, args.arxiv_tsv, load_arxiv_tsv, "arxiv_chunk")
    add_records(records, args.arxiv_json, load_arxiv_json, "arxiv")
    add_records(records, args.scopus_json, load_scopus_json, "scopus")
    add_records(records, args.citations_json, load_citations_json, "citations")

    if not records:
        parser.error("no input records supplied")

    output_path = Path(args.output)
    write_ledger(records, output_path)

    groups = group_records(records)
    duplicate_rows = sum(len(indexes) - 1 for indexes in groups.values())
    print(f"Records read: {len(records)}")
    print(f"Deduplicated groups: {len(groups)}")
    print(f"Duplicate rows: {duplicate_rows}")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
