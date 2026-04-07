#!/usr/bin/env python3
"""Convert JSON results from Scopus, IEEE Xplore, and arXiv APIs to BibTeX.

Usage:
    python convert_to_bib.py scopus  input.json  output.bib
    python convert_to_bib.py ieee    input.json  output.bib
    python convert_to_bib.py arxiv   input.json  output.bib

No external dependencies — uses only Python stdlib.
"""

import json
import re
import sys
from pathlib import Path


def _make_citation_key(authors: str, year: str, title: str) -> str:
    """Generate citation key: [auth:lower][year][shorttitle].

    Follows the Better BibTeX convention used in the project.
    """
    # First author's last name
    if authors:
        first_author = authors.split(",")[0].split(" and ")[0].strip()
        # Take last word as surname
        surname = first_author.split()[-1] if first_author else "unknown"
    else:
        surname = "unknown"

    # First significant word of title (skip articles/prepositions)
    skip = {"a", "an", "the", "of", "for", "in", "on", "to", "and", "with", "by"}
    title_words = re.sub(r"[^a-zA-Z\s]", "", title).split()
    short_title = ""
    for w in title_words:
        if w.lower() not in skip:
            short_title = w.lower()
            break
    if not short_title and title_words:
        short_title = title_words[0].lower()

    return f"{surname.lower()}{year}{short_title}"


def _escape_bibtex(text: str) -> str:
    """Escape special BibTeX characters."""
    if not text:
        return ""
    # Protect & and %
    text = text.replace("&", r"\&")
    text = text.replace("%", r"\%")
    return text


def _format_entry(entry_type: str, key: str, fields: dict[str, str]) -> str:
    """Format a single BibTeX entry."""
    lines = [f"@{entry_type}{{{key},"]
    for field, value in fields.items():
        if value:
            lines.append(f"  {field} = {{{_escape_bibtex(value)}}},")
    lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Scopus (Elsevier Search API)
# ---------------------------------------------------------------------------

def scopus_to_bib(data: dict) -> tuple[str, int]:
    """Convert Scopus API JSON to BibTeX.

    Expects the full API response with 'search-results' key.
    Returns (bibtex_string, total_results_count).
    """
    results = data.get("search-results", data)
    total = int(results.get("opensearch:totalResults", 0))
    entries = results.get("entry", [])

    bib_entries = []
    for entry in entries:
        # Skip error entries
        if entry.get("error"):
            continue

        title = entry.get("dc:title", "")
        year = entry.get("prism:coverDate", "")[:4]
        authors = entry.get("dc:creator", "")
        journal = entry.get("prism:publicationName", "")
        volume = entry.get("prism:volume", "")
        issue = entry.get("prism:issueIdentifier", "")
        pages = entry.get("prism:pageRange", "")
        doi = entry.get("prism:doi", "")
        abstract = entry.get("dc:description", "")
        doc_type = entry.get("subtypeDescription", "article").lower()

        entry_type = "inproceedings" if "conference" in doc_type else "article"
        key = _make_citation_key(authors, year, title)

        fields = {
            "title": title,
            "author": authors,
            "year": year,
            "journal" if entry_type == "article" else "booktitle": journal,
            "volume": volume,
            "number": issue,
            "pages": pages,
            "doi": doi,
            "abstract": abstract,
        }

        bib_entries.append(_format_entry(entry_type, key, fields))

    return "\n\n".join(bib_entries), total


# ---------------------------------------------------------------------------
# IEEE Xplore API
# ---------------------------------------------------------------------------

def ieee_to_bib(data: dict) -> tuple[str, int]:
    """Convert IEEE Xplore API JSON to BibTeX.

    Expects the full API response with 'articles' key.
    Returns (bibtex_string, total_results_count).
    """
    total = data.get("total_records", 0)
    articles = data.get("articles", [])

    bib_entries = []
    for article in articles:
        title = article.get("title", "")
        year = str(article.get("publication_year", ""))
        doi = article.get("doi", "")
        abstract = article.get("abstract", "")
        volume = article.get("volume", "")
        issue = article.get("issue", "")
        start_page = article.get("start_page", "")
        end_page = article.get("end_page", "")
        pages = f"{start_page}--{end_page}" if start_page and end_page else ""
        pub_title = article.get("publication_title", "")
        content_type = article.get("content_type", "").lower()

        # Authors
        author_list = article.get("authors", {}).get("authors", [])
        authors = " and ".join(a.get("full_name", "") for a in author_list)

        entry_type = "inproceedings" if "conference" in content_type else "article"
        key = _make_citation_key(authors, year, title)

        fields = {
            "title": title,
            "author": authors,
            "year": year,
            "journal" if entry_type == "article" else "booktitle": pub_title,
            "volume": volume,
            "number": issue,
            "pages": pages,
            "doi": doi,
            "abstract": abstract,
        }

        bib_entries.append(_format_entry(entry_type, key, fields))

    return "\n\n".join(bib_entries), total


# ---------------------------------------------------------------------------
# arXiv API (JSON from arxiv-mcp-server or converted from Atom feed)
# ---------------------------------------------------------------------------

def arxiv_to_bib(data: dict | list) -> tuple[str, int]:
    """Convert arXiv results to BibTeX.

    Accepts either:
    - A list of paper dicts (from arxiv-mcp-server)
    - A dict with 'entries'/'results' key containing a list

    Returns (bibtex_string, total_results_count).
    """
    if isinstance(data, list):
        entries = data
        total = len(entries)
    else:
        entries = data.get("entries", data.get("results", data.get("papers", [])))
        total = data.get("total_results", data.get("totalResults", len(entries)))

    bib_entries = []
    for entry in entries:
        title = entry.get("title", "").replace("\n", " ").strip()
        abstract = entry.get("summary", entry.get("abstract", "")).replace("\n", " ").strip()

        # Published date
        published = entry.get("published", entry.get("date", ""))
        year = published[:4] if published else ""

        # Authors — may be list of strings or list of dicts
        raw_authors = entry.get("authors", [])
        if raw_authors and isinstance(raw_authors[0], dict):
            authors = " and ".join(a.get("name", "") for a in raw_authors)
        else:
            authors = " and ".join(str(a) for a in raw_authors)

        # arXiv ID
        arxiv_id = entry.get("id", entry.get("arxiv_id", ""))
        if arxiv_id.startswith("http"):
            arxiv_id = arxiv_id.rstrip("/").split("/")[-1]

        categories = entry.get("categories", entry.get("primary_category", ""))
        if isinstance(categories, list):
            categories = ", ".join(categories)

        key = _make_citation_key(authors, year, title)

        fields = {
            "title": title,
            "author": authors,
            "year": year,
            "eprint": arxiv_id,
            "archiveprefix": "arXiv",
            "primaryclass": categories,
            "abstract": abstract,
        }

        bib_entries.append(_format_entry("article", key, fields))

    return "\n\n".join(bib_entries), total


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

CONVERTERS = {
    "scopus": scopus_to_bib,
    "ieee": ieee_to_bib,
    "arxiv": arxiv_to_bib,
}


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <scopus|ieee|arxiv> <input.json> <output.bib>")
        sys.exit(1)

    source = sys.argv[1].lower()
    input_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    if source not in CONVERTERS:
        print(f"Error: unknown source '{source}'. Use: {', '.join(CONVERTERS)}")
        sys.exit(1)

    with open(input_path) as f:
        data = json.load(f)

    bib_text, total = CONVERTERS[source](data)

    with open(output_path, "w") as f:
        f.write(bib_text)
        if bib_text:
            f.write("\n")

    exported = bib_text.count("@")
    print(f"Source: {source}")
    print(f"Total results reported by API: {total}")
    print(f"Entries exported to BibTeX: {exported}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
