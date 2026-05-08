#!/usr/bin/env python3
"""Validate the search Scopus draft query with a count-only API request."""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

import build_scopus_query


SCOPUS_API = "https://api.elsevier.com/content/search/scopus"
USER_AGENT = "SLR-Search/1.0"


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


def request_count(query: str, api_key: str) -> tuple[int, int, str]:
    params = urllib.parse.urlencode({"query": query, "start": 0, "count": 1})
    url = f"{SCOPUS_API}?{params}"
    request = urllib.request.Request(
        url,
        headers={
            "X-ELS-APIKey": api_key,
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
    total = int(data.get("search-results", {}).get("opensearch:totalResults", "0"))
    return response.status, total, url


def write_row(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    fieldnames = [
        "timestamp_utc",
        "query_name",
        "query_file",
        "query_chars",
        "status",
        "total_results",
        "error",
        "git_head",
        "git_dirty",
        "git_status_entries",
    ]
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query-file", default="search/scopus-query-draft.txt")
    parser.add_argument(
        "--branches",
        action="store_true",
        help="Validate each generated Scopus branch separately instead of the combined query.",
    )
    parser.add_argument("--env-file", default="../.env")
    parser.add_argument(
        "--output",
        default="search/scopus-query-validation.tsv",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.branches:
        queries = build_scopus_query.build_branch_queries(include_year=True)
    else:
        queries = {"combined": Path(args.query_file).read_text(encoding="utf-8").strip()}

    if args.dry_run:
        for name, query in queries.items():
            print(f"{name}\t{len(query)}")
        return 0

    api_key = load_api_key(args.env_file)
    if not api_key:
        raise SystemExit("SCOPUS_API_KEY not found in environment or env file")

    git_status = git_value(["status", "--short"])
    exit_code = 0
    for name, query in queries.items():
        timestamp = datetime.now(UTC).isoformat()
        try:
            status, total, _url = request_count(query, api_key)
            row = {
                "timestamp_utc": timestamp,
                "query_name": name,
                "query_file": args.query_file,
                "query_chars": str(len(query)),
                "status": str(status),
                "total_results": str(total),
                "error": "",
                "git_head": git_value(["rev-parse", "HEAD"]),
                "git_dirty": "yes" if git_status else "no",
                "git_status_entries": str(len(git_status.splitlines()))
                if git_status
                else "0",
            }
            write_row(Path(args.output), row)
            print(f"{name}\tstatus={status}\ttotal_results={total}")
        except urllib.error.HTTPError as exc:
            error = f"HTTP {exc.code}: {' '.join(exc.read().decode('utf-8', 'ignore').split())}"
            row = {
                "timestamp_utc": timestamp,
                "query_name": name,
                "query_file": args.query_file,
                "query_chars": str(len(query)),
                "status": "error",
                "total_results": "",
                "error": error,
                "git_head": git_value(["rev-parse", "HEAD"]),
                "git_dirty": "yes" if git_status else "no",
                "git_status_entries": str(len(git_status.splitlines()))
                if git_status
                else "0",
            }
            write_row(Path(args.output), row)
            print(f"{name}\t{error}")
            exit_code = 2
        except urllib.error.URLError as exc:
            error = f"{type(exc).__name__}: {exc.reason}"
            row = {
                "timestamp_utc": timestamp,
                "query_name": name,
                "query_file": args.query_file,
                "query_chars": str(len(query)),
                "status": "error",
                "total_results": "",
                "error": error,
                "git_head": git_value(["rev-parse", "HEAD"]),
                "git_dirty": "yes" if git_status else "no",
                "git_status_entries": str(len(git_status.splitlines()))
                if git_status
                else "0",
            }
            write_row(Path(args.output), row)
            print(f"{name}\t{error}")
            exit_code = 2
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
