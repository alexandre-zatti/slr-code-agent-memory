#!/usr/bin/env python3
"""Fetch all arXiv results for the SLR query with full pagination.

The arxiv-mcp-server caps at 50 results. This script hits the arXiv API
directly, paginates through all results, and outputs JSON compatible with
convert_to_bib.py's arxiv converter.

Usage:
    python fetch_arxiv.py                          # uses default query
    python fetch_arxiv.py --output results.json    # custom output path
    python fetch_arxiv.py --count-only             # just print total count

No external dependencies — uses only Python stdlib.
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# arXiv API namespace
ATOM = "{http://www.w3.org/2005/Atom}"
OPENSEARCH = "{http://a9.com/-/spec/opensearch/1.1/}"
ARXIV = "{http://arxiv.org/schemas/atom}"

# Default query from estrategia-busca.md (Busca 2)
DEFAULT_QUERY = (
    '(cat:cs.SE OR cat:cs.AI OR cat:cs.CL) AND '
    '(abs:"LLM agent" OR abs:"AI coding agent" '
    'OR abs:"software engineering agent" OR abs:"autonomous coding" '
    'OR abs:"code agent" OR abs:"LLM-based software" '
    'OR abs:"AI-assisted software" OR abs:"coding assistant" '
    'OR abs:"language agent" OR abs:"code assistant" '
    'OR abs:"agentic coding" OR abs:"SWE agent" '
    'OR ti:"coding agent" OR ti:"code agent" '
    'OR ti:"software engineering agent" OR ti:"SWE agent") AND '
    '(abs:"memory" OR abs:"knowledge persistence" OR abs:"experience" '
    'OR abs:"context management" OR abs:"long-term memory" '
    'OR abs:"episodic memory" OR abs:"knowledge reuse" '
    'OR abs:"continual learning" OR abs:"experience replay" '
    'OR abs:"memory-augmented" OR abs:"persistent memory" '
    'OR abs:"persistent context" OR abs:"cross-task")'
)

PAGE_SIZE = 100  # arXiv recommends max 100 per request
RATE_LIMIT_SECONDS = 3  # arXiv asks for 3s between requests


def fetch_page(query: str, start: int, max_results: int) -> ET.Element:
    """Fetch one page of results from the arXiv API."""
    params = urllib.parse.urlencode({
        "search_query": query,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    url = f"https://export.arxiv.org/api/query?{params}"

    req = urllib.request.Request(url, headers={"User-Agent": "SLR-fetch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return ET.fromstring(resp.read())


def parse_entry(entry: ET.Element) -> dict:
    """Parse a single Atom entry into a paper dict."""
    # arXiv ID from the <id> URL
    raw_id = entry.findtext(f"{ATOM}id", "")
    arxiv_id = raw_id.rstrip("/").split("/")[-1]

    # Authors
    authors = []
    for author in entry.findall(f"{ATOM}author"):
        name = author.findtext(f"{ATOM}name", "")
        if name:
            authors.append({"name": name})

    # Categories
    categories = []
    for cat in entry.findall(f"{ATOM}category"):
        term = cat.get("term", "")
        if term:
            categories.append(term)

    # Published date
    published = entry.findtext(f"{ATOM}published", "")

    # Links
    pdf_url = ""
    for link in entry.findall(f"{ATOM}link"):
        if link.get("title") == "pdf":
            pdf_url = link.get("href", "")

    return {
        "id": arxiv_id,
        "title": (entry.findtext(f"{ATOM}title", "") or "").replace("\n", " ").strip(),
        "authors": authors,
        "abstract": (entry.findtext(f"{ATOM}summary", "") or "").replace("\n", " ").strip(),
        "published": published,
        "categories": categories,
        "url": pdf_url or raw_id,
    }


def get_total_results(root: ET.Element) -> int:
    """Extract opensearch:totalResults from the feed."""
    val = root.findtext(f"{OPENSEARCH}totalResults", "0")
    return int(val)


def fetch_all(query: str, year_from: int = 2023, count_only: bool = False) -> tuple[list[dict], int]:
    """Fetch all results with pagination and optional year filter.

    Returns (papers_list, total_reported_by_api).
    """
    print(f"Fetching first page to get total count...", file=sys.stderr)
    root = fetch_page(query, start=0, max_results=1 if count_only else PAGE_SIZE)
    total = get_total_results(root)
    print(f"arXiv reports {total} total results", file=sys.stderr)

    if count_only:
        return [], total

    # Parse first page
    all_papers = []
    entries = root.findall(f"{ATOM}entry")
    for entry in entries:
        paper = parse_entry(entry)
        all_papers.append(paper)

    fetched = len(entries)
    print(f"Page 1: {fetched} entries (total so far: {len(all_papers)})", file=sys.stderr)

    # Paginate through remaining results
    while fetched < total:
        time.sleep(RATE_LIMIT_SECONDS)
        root = fetch_page(query, start=fetched, max_results=PAGE_SIZE)
        entries = root.findall(f"{ATOM}entry")

        if not entries:
            print(f"No more entries returned at start={fetched}", file=sys.stderr)
            break

        for entry in entries:
            paper = parse_entry(entry)
            all_papers.append(paper)

        fetched += len(entries)
        page_num = (fetched // PAGE_SIZE) + 1
        print(f"Page {page_num}: {len(entries)} entries (total so far: {len(all_papers)})", file=sys.stderr)

    # Filter by year if needed
    if year_from:
        before = len(all_papers)
        all_papers = [
            p for p in all_papers
            if p.get("published", "")[:4] >= str(year_from)
        ]
        filtered = before - len(all_papers)
        if filtered:
            print(f"Year filter (>= {year_from}): removed {filtered}, kept {len(all_papers)}", file=sys.stderr)

    return all_papers, total


def main():
    parser = argparse.ArgumentParser(description="Fetch arXiv results for SLR with pagination")
    parser.add_argument("--query", default=DEFAULT_QUERY, help="arXiv search query")
    parser.add_argument("--output", "-o", default=None, help="Output JSON file path")
    parser.add_argument("--count-only", action="store_true", help="Only print total count, don't fetch all")
    parser.add_argument("--year-from", type=int, default=2023, help="Filter papers from this year (default: 2023)")
    args = parser.parse_args()

    papers, total = fetch_all(args.query, year_from=args.year_from, count_only=args.count_only)

    if args.count_only:
        print(f"Total results: {total}")
        return

    # Build output structure compatible with convert_to_bib.py
    output = {
        "total_results": total,
        "query": args.query,
        "fetch_date": datetime.now().isoformat(),
        "year_filter": f">= {args.year_from}" if args.year_from else "none",
        "papers_after_filter": len(papers),
        "papers": papers,
    }

    if args.output:
        out_path = Path(args.output)
        with open(out_path, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {out_path}", file=sys.stderr)
    else:
        json.dump(output, sys.stdout, indent=2, ensure_ascii=False)

    print(f"\nSummary:", file=sys.stderr)
    print(f"  Total reported by API: {total}", file=sys.stderr)
    print(f"  Papers after year filter: {len(papers)}", file=sys.stderr)
    print(f"  Fetch date: {output['fetch_date']}", file=sys.stderr)


if __name__ == "__main__":
    main()
