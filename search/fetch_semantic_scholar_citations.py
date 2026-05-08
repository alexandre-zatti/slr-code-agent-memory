#!/usr/bin/env python3
"""Run search forward/backward citation chasing through Semantic Scholar."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path


API_BASE = "https://api.semanticscholar.org/graph/prior"
USER_AGENT = "SLR-SearchV2/0.1"
PAPER_FIELDS = (
    "paperId,title,year,authors,externalIds,venue,publicationVenue,abstract,"
    "publicationDate,referenceCount,citationCount"
)
INCLUDE_SEED_GROUPS = {
    "known_included_seed",
    "v1_included_contextual",
    "delta_high_confidence",
    "delta_boundary",
    "post_search_candidate",
}


def git_value(args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:  # noqa: BLE001 - metadata best effort
        return "unavailable"


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def normalize_doi(value: object) -> str:
    value = clean(value).lower()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    return value.rstrip(".")


def normalize_arxiv_id(value: object) -> str:
    value = clean(value)
    value = value.rsplit("/", 1)[-1]
    value = re.sub(r"^arxiv:", "", value, flags=re.IGNORECASE)
    value = re.sub(r"v\d+$", "", value)
    return value


def seed_api_id(row: dict[str, str]) -> str:
    if row.get("arxiv_id"):
        return f"ARXIV:{normalize_arxiv_id(row['arxiv_id'])}"
    if row.get("doi"):
        return f"DOI:{normalize_doi(row['doi'])}"
    return ""


def read_seed_rows(path: Path, seed_ids: set[str] | None) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    selected = [
        row
        for row in rows
        if row.get("seed_group") in INCLUDE_SEED_GROUPS
        and row.get("expected_status") != "exclude_withdrawn"
        and seed_api_id(row)
        and (seed_ids is None or row.get("seed_id") in seed_ids)
    ]
    if not selected:
        raise SystemExit("no citation-chasing seeds selected")
    return selected


def write_seed_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "seed_id",
        "title",
        "year",
        "arxiv_id",
        "doi",
        "seed_group",
        "expected_status",
        "search_recall_expectation",
        "semantic_scholar_api_id",
        "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            output = {field: row.get(field, "") for field in fieldnames}
            output["semantic_scholar_api_id"] = seed_api_id(row)
            writer.writerow(output)


def request_json(url: str, retries: int, backoff: float) -> dict:
    for attempt in range(retries):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code in {429, 500, 502, 503, 504} and attempt < retries - 1:
                sleep_for = backoff * (2**attempt)
                print(
                    f"HTTP {exc.code} from Semantic Scholar; sleeping {sleep_for:.1f}s",
                    file=sys.stderr,
                    flush=True,
                )
                time.sleep(sleep_for)
                continue
            raise
        except (TimeoutError, urllib.error.URLError) as exc:
            if attempt < retries - 1:
                sleep_for = backoff * (2**attempt)
                print(
                    f"{type(exc).__name__} from Semantic Scholar; sleeping {sleep_for:.1f}s",
                    file=sys.stderr,
                    flush=True,
                )
                time.sleep(sleep_for)
                continue
            raise
    raise RuntimeError("unreachable")


def relation_url(api_id: str, relation: str, offset: int, limit: int) -> str:
    target = "citedPaper" if relation == "backward" else "citingPaper"
    params = urllib.parse.urlencode(
        {
            "fields": f"{target}.{PAPER_FIELDS}",
            "offset": offset,
            "limit": limit,
        }
    )
    quoted = urllib.parse.quote(api_id, safe="")
    endpoint = "references" if relation == "backward" else "citations"
    return f"{API_BASE}/paper/{quoted}/{endpoint}?{params}"


def paper_from_relation(item: dict, relation: str) -> dict | None:
    key = "citedPaper" if relation == "backward" else "citingPaper"
    paper = item.get(key)
    if not paper or paper.get("paperId") is None:
        return None
    return paper


def paper_identity(paper: dict) -> str:
    external = paper.get("externalIds") or {}
    doi = normalize_doi(external.get("DOI", ""))
    arxiv_id = normalize_arxiv_id(external.get("ArXiv", ""))
    title = clean(paper.get("title", "")).lower()
    if paper.get("paperId"):
        return f"s2:{paper['paperId']}"
    if doi:
        return f"doi:{doi}"
    if arxiv_id:
        return f"arxiv:{arxiv_id}"
    return f"title:{title}"


def merge_paper(
    papers: dict[str, dict],
    paper: dict,
    seed_id: str,
    relation: str,
) -> None:
    identity = paper_identity(paper)
    external = paper.get("externalIds") or {}
    record = papers.setdefault(
        identity,
        {
            "paperId": paper.get("paperId"),
            "title": clean(paper.get("title", "")),
            "year": paper.get("year"),
            "authors": [clean(author.get("name", "")) for author in paper.get("authors", [])],
            "doi": normalize_doi(external.get("DOI", "")),
            "arxivId": normalize_arxiv_id(external.get("ArXiv", "")),
            "externalIds": external,
            "venue": clean(paper.get("venue", "")),
            "publicationVenue": paper.get("publicationVenue"),
            "publicationDate": clean(paper.get("publicationDate", "")),
            "abstract": clean(paper.get("abstract", "")),
            "referenceCount": paper.get("referenceCount"),
            "citationCount": paper.get("citationCount"),
            "source": relation,
            "forward_from": [],
            "backward_from": [],
        },
    )
    route_key = "backward_from" if relation == "backward" else "forward_from"
    if seed_id not in record[route_key]:
        record[route_key].append(seed_id)
    sources = set(str(record.get("source", "")).split("+"))
    sources.add(relation)
    record["source"] = "+".join(sorted(source for source in sources if source))


def fetch_relation(
    seed: dict[str, str],
    relation: str,
    args: argparse.Namespace,
    papers: dict[str, dict],
    request_rows: list[dict[str, str]],
) -> int:
    api_id = seed_api_id(seed)
    offset = 0
    raw_count = 0
    while True:
        url = relation_url(api_id, relation, offset, args.page_size)
        timestamp = datetime.now(UTC).isoformat()
        try:
            data = request_json(url, retries=args.retries, backoff=args.backoff)
            status = "ok"
            error = ""
        except urllib.error.HTTPError as exc:
            status = f"http_{exc.code}"
            error = clean(exc.read().decode("utf-8", "ignore"))
            data = {"data": [], "next": None}
        request_rows.append(
            {
                "timestamp_utc": timestamp,
                "seed_id": seed["seed_id"],
                "semantic_scholar_api_id": api_id,
                "relation": relation,
                "offset": str(offset),
                "limit": str(args.page_size),
                "status": status,
                "returned_rows": str(len(data.get("data", []) or [])),
                "next": "" if data.get("next") is None else str(data.get("next")),
                "error": error,
                "request_url": url,
            }
        )
        if status != "ok":
            return raw_count

        for item in data.get("data", []) or []:
            paper = paper_from_relation(item, relation)
            if paper:
                raw_count += 1
                merge_paper(papers, paper, seed["seed_id"], relation)

        next_offset = data.get("next")
        if next_offset is None:
            return raw_count
        offset = int(next_offset)
        time.sleep(args.rate_limit)


def write_requests(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "timestamp_utc",
        "seed_id",
        "semantic_scholar_api_id",
        "relation",
        "offset",
        "limit",
        "status",
        "returned_rows",
        "next",
        "error",
        "request_url",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(
    path: Path,
    args: argparse.Namespace,
    seeds: list[dict[str, str]],
    total_forward: int,
    total_backward: int,
    papers: dict[str, dict],
) -> None:
    git_status = git_value(["status", "--short"])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["key", "value"])
        writer.writerow(["timestamp_utc", datetime.now(UTC).isoformat()])
        writer.writerow(["script", __file__])
        writer.writerow(["git_head", git_value(["rev-parse", "HEAD"])])
        writer.writerow(["git_dirty", "yes" if git_status else "no"])
        writer.writerow(
            ["git_status_entries", str(len(git_status.splitlines())) if git_status else "0"]
        )
        writer.writerow(["seed_set", args.seed_set])
        writer.writerow(["seed_count", str(len(seeds))])
        writer.writerow(["seed_output", args.seed_output])
        writer.writerow(["page_size", str(args.page_size)])
        writer.writerow(["rate_limit_seconds", str(args.rate_limit)])
        writer.writerow(["retries", str(args.retries)])
        writer.writerow(["backoff_seconds", str(args.backoff)])
        writer.writerow(["total_forward_raw", str(total_forward)])
        writer.writerow(["total_backward_raw", str(total_backward)])
        writer.writerow(["unique_papers", str(len(papers))])
        writer.writerow(["output", args.output])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-set", default="search/seed-set.tsv")
    parser.add_argument("--seed-output", default="search/citation-chasing-seeds.tsv")
    parser.add_argument("--output", default="search/results-citations.json")
    parser.add_argument("--metadata-output", default="search/results-citations-metadata.tsv")
    parser.add_argument("--request-log", default="search/results-citations-requests.tsv")
    parser.add_argument("--seed-ids", nargs="+")
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--rate-limit", type=float, default=2.0)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--backoff", type=float, default=60.0)
    args = parser.parse_args()

    seed_ids = set(args.seed_ids) if args.seed_ids else None
    seeds = read_seed_rows(Path(args.seed_set), seed_ids=seed_ids)
    write_seed_tsv(Path(args.seed_output), seeds)

    papers: dict[str, dict] = {}
    request_rows: list[dict[str, str]] = []
    total_forward = 0
    total_backward = 0
    for index, seed in enumerate(seeds, start=1):
        print(f"{index}/{len(seeds)}\t{seed['seed_id']}", flush=True)
        total_backward += fetch_relation(seed, "backward", args, papers, request_rows)
        time.sleep(args.rate_limit)
        total_forward += fetch_relation(seed, "forward", args, papers, request_rows)
        if index < len(seeds):
            time.sleep(args.rate_limit)

    output = {
        "seed_papers": [seed["seed_id"] for seed in seeds],
        "seed_file": args.seed_output,
        "fetch_date": datetime.now(UTC).isoformat(),
        "total_forward_raw": total_forward,
        "total_backward_raw": total_backward,
        "unique_papers": len(papers),
        "papers": sorted(papers.values(), key=lambda paper: clean(paper.get("title", "")).lower()),
    }
    Path(args.output).write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_requests(Path(args.request_log), request_rows)
    write_metadata(Path(args.metadata_output), args, seeds, total_forward, total_backward, papers)
    print(
        f"seeds={len(seeds)} forward={total_forward} backward={total_backward} "
        f"unique={len(papers)}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
