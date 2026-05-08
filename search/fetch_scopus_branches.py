#!/usr/bin/env python3
"""Fetch final search Scopus branch exports with pagination."""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import time
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

import build_scopus_query


SCOPUS_API = "https://api.elsevier.com/content/search/scopus"
USER_AGENT = "SLR-Search/1.0"


BRANCH_SLUGS = {
    "family_a_coding_agent_memory": "family-a-coding-agent-memory",
    "family_b_generic_agent_memory_se": "family-b-generic-agent-memory-se",
    "family_c_strong_memory_se": "family-c-strong-memory-se",
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


def load_api_key(env_file: str | None) -> str:
    if os.environ.get("SCOPUS_API_KEY"):
        return os.environ["SCOPUS_API_KEY"]
    if env_file:
        path = Path(env_file)
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.startswith("SCOPUS_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def request_page(query: str, api_key: str, start: int, count: int) -> tuple[int, dict]:
    params = urllib.parse.urlencode({"query": query, "start": start, "count": count})
    request = urllib.request.Request(
        f"{SCOPUS_API}?{params}",
        headers={
            "X-ELS-APIKey": api_key,
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def fetch_branch(
    branch: str,
    query: str,
    api_key: str,
    page_size: int,
    rate_limit: float,
) -> tuple[int, list[dict], list[dict]]:
    entries: list[dict] = []
    pages: list[dict] = []
    total: int | None = None
    start = 0

    while total is None or start < total:
        status, data = request_page(query=query, api_key=api_key, start=start, count=page_size)
        search = data.get("search-results", {})
        total = int(search.get("opensearch:totalResults", "0"))
        page_entries = search.get("entry", []) or []
        entries.extend(page_entries)
        pages.append(
            {
                "timestamp_utc": datetime.now(UTC).isoformat(),
                "branch": branch,
                "status": status,
                "start": start,
                "count": page_size,
                "total_results": total,
                "fetched_entries": len(page_entries),
                "raw": data,
            }
        )
        start += page_size
        if start < total:
            time.sleep(rate_limit)

    if total is not None and len(entries) < total:
        raise RuntimeError(f"truncated Scopus branch {branch}: fetched {len(entries)} of {total}")
    return total or 0, entries, pages


def write_tsv(path: Path, branch: str, entries: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "branch",
        "rank",
        "scopus_id",
        "eid",
        "title",
        "year",
        "venue",
        "doi",
        "subtype",
        "abstract",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for index, entry in enumerate(entries, start=1):
            writer.writerow(
                {
                    "branch": branch,
                    "rank": index,
                    "scopus_id": clean(entry.get("dc:identifier", "")),
                    "eid": clean(entry.get("eid", "")),
                    "title": clean(entry.get("dc:title", "")),
                    "year": clean(entry.get("prism:coverDate", ""))[:4],
                    "venue": clean(entry.get("prism:publicationName", "")),
                    "doi": clean(entry.get("prism:doi", "")),
                    "subtype": clean(entry.get("subtypeDescription", "")),
                    "abstract": clean(entry.get("dc:description", "")),
                }
            )


def write_metadata(
    path: Path,
    branch: str,
    slug: str,
    query: str,
    args: argparse.Namespace,
    total: int,
    entries: list[dict],
    pages: list[dict],
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
        writer.writerow(["branch", branch])
        writer.writerow(["query", query])
        writer.writerow(["query_chars", str(len(query))])
        writer.writerow(["page_size", str(args.page_size)])
        writer.writerow(["rate_limit_seconds", str(args.rate_limit)])
        writer.writerow(["reported_total_results", str(total)])
        writer.writerow(["fetched_entries", str(len(entries))])
        writer.writerow(["page_count", str(len(pages))])
        writer.writerow(["tsv_output", str(args.output_dir / f"scopus-results-{slug}.tsv")])
        writer.writerow(["json_output", str(args.output_dir / f"scopus-results-{slug}.json")])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--branches",
        nargs="+",
        default=[
            "family_a_coding_agent_memory",
            "family_b_generic_agent_memory_se",
            "family_c_strong_memory_se",
        ],
    )
    parser.add_argument("--env-file", default="../.env")
    parser.add_argument("--output-dir", type=Path, default=Path("search"))
    parser.add_argument("--page-size", type=int, default=25)
    parser.add_argument("--rate-limit", type=float, default=2.0)
    args = parser.parse_args()

    api_key = load_api_key(args.env_file)
    if not api_key:
        raise SystemExit("SCOPUS_API_KEY not found in environment or env file")

    queries = build_scopus_query.build_branch_queries(include_year=True)
    for branch in args.branches:
        if branch not in queries:
            raise SystemExit(f"unknown branch: {branch}")
        slug = BRANCH_SLUGS.get(branch, branch.replace("_", "-"))
        query = queries[branch]
        total, entries, pages = fetch_branch(
            branch=branch,
            query=query,
            api_key=api_key,
            page_size=args.page_size,
            rate_limit=args.rate_limit,
        )
        tsv_path = args.output_dir / f"scopus-results-{slug}.tsv"
        json_path = args.output_dir / f"scopus-results-{slug}.json"
        metadata_path = args.output_dir / f"scopus-results-{slug}-metadata.tsv"
        write_tsv(tsv_path, branch, entries)
        json_path.write_text(
            json.dumps(
                {
                    "branch": branch,
                    "query": query,
                    "reported_total_results": total,
                    "fetched_entries": len(entries),
                    "pages": pages,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        write_metadata(metadata_path, branch, slug, query, args, total, entries, pages)
        print(f"{branch}\ttotal={total}\tfetched={len(entries)}\tpages={len(pages)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
