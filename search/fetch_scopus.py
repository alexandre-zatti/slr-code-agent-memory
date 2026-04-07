#!/usr/bin/env python3
"""Fetch all Scopus results for the SLR query via the Elsevier Search API.

Paginates through the full result set and outputs JSON compatible with
convert_to_bib.py's scopus converter.

Requires a Scopus API key from Elsevier Developer Portal
(https://dev.elsevier.com/). Institutional access via CAPES or a
subscribed organization is typically required for full abstract content.

Usage:
    SCOPUS_API_KEY=xxx python fetch_scopus.py                  # uses default query
    SCOPUS_API_KEY=xxx python fetch_scopus.py --output out.json
    python fetch_scopus.py --api-key xxx --count-only          # just print total count

No external dependencies — uses only Python stdlib.
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from pathlib import Path

# Default query from search-strategy.md (Search 1)
DEFAULT_QUERY = (
    'TITLE-ABS-KEY('
    '("LLM agent" OR "AI coding agent" OR "software engineering agent" '
    'OR "autonomous coding" OR "code agent" OR "LLM-based software" '
    'OR "AI-assisted software" OR "coding assistant" OR "language agent" '
    'OR "code assistant" OR "agentic coding" OR "SWE agent") '
    'AND '
    '("memory" OR "knowledge persistence" OR "experience" '
    'OR "context management" OR "long-term memory" OR "episodic memory" '
    'OR "knowledge reuse" OR "continual learning" OR "experience replay" '
    'OR "memory-augmented" OR "persistent memory" OR "persistent context" '
    'OR "cross-task") '
    'AND '
    '("software engineering" OR "software development" OR "code generation" '
    'OR "bug fix" OR "code repair" OR "repository" '
    'OR "software maintenance" OR "issue resolution")'
    ') AND PUBYEAR > 2022'
)

BASE_URL = "https://api.elsevier.com/content/search/scopus"
PAGE_SIZE = 25  # Standard API key cap; institutional keys may allow up to 200
RATE_LIMIT_SECONDS = 1  # Elsevier weekly quota allows ~20k req/week; stay polite


def fetch_page(query: str, api_key: str, start: int, count: int) -> dict:
    """Fetch one page of results from the Scopus Search API."""
    params = urllib.parse.urlencode({
        "query": query,
        "start": start,
        "count": count,
    })
    url = f"{BASE_URL}?{params}"

    req = urllib.request.Request(
        url,
        headers={
            "X-ELS-APIKey": api_key,
            "Accept": "application/json",
            "User-Agent": "SLR-fetch/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        print(f"HTTP {e.code} from Scopus API: {body[:500]}", file=sys.stderr)
        raise


def get_total_results(response: dict) -> int:
    """Extract opensearch:totalResults from a Scopus API response."""
    return int(response.get("search-results", {}).get("opensearch:totalResults", 0))


def get_entries(response: dict) -> list[dict]:
    """Extract the entry list from a Scopus API response."""
    entries = response.get("search-results", {}).get("entry", [])
    # Filter out error entries (Scopus returns an error entry when count=0)
    return [e for e in entries if not e.get("error")]


def fetch_all(query: str, api_key: str, count_only: bool = False) -> tuple[list[dict], int]:
    """Fetch all results with pagination.

    Returns (entries_list, total_reported_by_api).
    """
    print("Fetching first page to get total count...", file=sys.stderr)
    response = fetch_page(query, api_key, start=0, count=1 if count_only else PAGE_SIZE)
    total = get_total_results(response)
    print(f"Scopus reports {total} total results", file=sys.stderr)

    if count_only:
        return [], total

    # Parse first page
    all_entries = get_entries(response)
    print(
        f"Page 1: {len(all_entries)} entries (total so far: {len(all_entries)})",
        file=sys.stderr,
    )

    # Paginate through remaining results
    fetched = len(all_entries)
    while fetched < total:
        time.sleep(RATE_LIMIT_SECONDS)
        response = fetch_page(query, api_key, start=fetched, count=PAGE_SIZE)
        entries = get_entries(response)

        if not entries:
            print(f"No more entries returned at start={fetched}", file=sys.stderr)
            break

        all_entries.extend(entries)
        fetched = len(all_entries)
        page_num = (fetched // PAGE_SIZE) + 1
        print(
            f"Page {page_num}: {len(entries)} entries (total so far: {fetched})",
            file=sys.stderr,
        )

    return all_entries, total


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Scopus results for SLR with pagination"
    )
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Scopus search query")
    parser.add_argument("--output", "-o", default=None, help="Output JSON file path")
    parser.add_argument(
        "--count-only",
        action="store_true",
        help="Only print total count, don't fetch all",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Scopus API key (or set SCOPUS_API_KEY env var)",
    )
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("SCOPUS_API_KEY")
    if not api_key:
        print(
            "Error: Scopus API key required. Pass --api-key or set SCOPUS_API_KEY.",
            file=sys.stderr,
        )
        sys.exit(1)

    entries, total = fetch_all(args.query, api_key, count_only=args.count_only)

    if args.count_only:
        print(f"Total results: {total}")
        return

    # Build output structure compatible with convert_to_bib.py
    output = {
        "total_results": total,
        "query": args.query,
        "fetch_date": datetime.now().isoformat(),
        "entries": entries,
    }

    if args.output:
        out_path = Path(args.output)
        with open(out_path, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {out_path}", file=sys.stderr)
    else:
        json.dump(output, sys.stdout, indent=2, ensure_ascii=False)

    print("\nSummary:", file=sys.stderr)
    print(f"  Total reported by API: {total}", file=sys.stderr)
    print(f"  Entries fetched: {len(entries)}", file=sys.stderr)
    print(f"  Fetch date: {output['fetch_date']}", file=sys.stderr)


if __name__ == "__main__":
    main()
