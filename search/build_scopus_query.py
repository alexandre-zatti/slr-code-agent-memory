#!/usr/bin/env python3
"""Generate the search Scopus draft query.

This script performs no network calls. It keeps the Scopus draft aligned with
the local search term constants used by the arXiv validation scripts, except
for the Scopus-specific family_c branch. That branch is intentionally narrower after
Scopus API validation showed that the fully mirrored strong-memory-plus-SE
branch retrieved a large false-positive burden.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import check_arxiv_seed_recall as arxiv_terms


SCOPUS_YEAR_CLAUSE = "PUBYEAR > 2022"

SCOPUS_FAMILY_C_REMOVED_C2 = {
    "knowledge reuse",
    "continual learning",
    "knowledge accumulation",
    "state tracking",
    "memory management",
    "dynamic memory management",
    "adaptive memory",
    "forgetting",
}

SCOPUS_FAMILY_C_C3 = [
    "SWE-bench",
    "Defects4J",
    "program repair",
    "code repair",
    "software repair",
    "automated program repair",
    "repository-level program repair",
    "issue resolution",
    "code optimization",
    "bug fix",
    "bug fixing",
    "code localization",
    "patch generation",
    "automated debugging",
    "code translation",
    "kernel optimization",
    "accelerator kernel",
    "accelerator kernels",
    "AI accelerator",
    "AI accelerators",
    "NKIBench",
]


def quote_term(term: str) -> str:
    return f'"{term.replace("\"", "\"\"")}"'


def or_terms(terms: list[str]) -> str:
    return "(" + " OR ".join(quote_term(term) for term in terms) + ")"


def and_terms(parts: list[str]) -> str:
    return "(" + " AND ".join(parts) + ")"


def title_abs_key(expression: str) -> str:
    return f"TITLE-ABS-KEY({expression})"


def with_year_clause(query: str) -> str:
    return f"({query}) AND {SCOPUS_YEAR_CLAUSE}"


def git_value(args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:  # noqa: BLE001 - metadata best effort
        return "unavailable"


def build_branch_queries(*, include_year: bool = False) -> dict[str, str]:
    c1_coding = or_terms(arxiv_terms.C1_CODING_ABS)
    c1_generic = or_terms([*arxiv_terms.C1_GENERIC_ABS, *arxiv_terms.C1_SEED_GAP_ABS])
    c2_broad = or_terms(arxiv_terms.C2_BROAD_ABS)
    scopus_family_c_c2 = or_terms(
        [term for term in arxiv_terms.C2_STRONG_ABS if term not in SCOPUS_FAMILY_C_REMOVED_C2]
    )
    scopus_family_c_c3 = or_terms(SCOPUS_FAMILY_C_C3)
    c3 = or_terms([*arxiv_terms.C3_ABS, *arxiv_terms.C3_SEED_GAP_ABS])

    branches = {
        "family_a_coding_agent_memory": title_abs_key(
            and_terms(
                [
                    c1_coding,
                    c2_broad,
                ]
            )
        ),
        "family_b_generic_agent_memory_se": title_abs_key(
            and_terms(
                [
                    c1_generic,
                    c2_broad,
                    c3,
                ]
            )
        ),
        "family_c_strong_memory_se": title_abs_key(
            and_terms(
                [
                    scopus_family_c_c2,
                    scopus_family_c_c3,
                ]
            )
        ),
    }
    if include_year:
        return {branch: with_year_clause(query) for branch, query in branches.items()}
    return branches


def build_full_query() -> str:
    branches = build_branch_queries()
    return "(" + "\nOR\n".join(branches.values()) + f")\nAND {SCOPUS_YEAR_CLAUSE}"


def write_metadata(path: Path, output_path: Path, full_query: str) -> None:
    branches = build_branch_queries()
    git_status = git_value(["status", "--short"])
    rows = [
        ("generated_utc", datetime.now(UTC).isoformat()),
        ("script", __file__),
        ("git_head", git_value(["rev-parse", "HEAD"])),
        ("git_dirty", "yes" if git_status else "no"),
        ("git_status_entries", str(len(git_status.splitlines())) if git_status else "0"),
        ("output", str(output_path)),
        ("query_chars", str(len(full_query))),
        ("branch_count", str(len(branches))),
        (
            "family_c_scopus_specific",
            "yes; removes broad Scopus-noisy C2 terms and limits C3 to repair/issue/optimization evidence",
        ),
        ("family_c_removed_c2_terms", "; ".join(sorted(SCOPUS_FAMILY_C_REMOVED_C2))),
        ("family_c_c3_terms", "; ".join(SCOPUS_FAMILY_C_C3)),
    ]
    rows.extend((f"{name}_chars", str(len(query))) for name, query in branches.items())
    rows.extend(
        (f"{name}_with_year_chars", str(len(with_year_clause(query))))
        for name, query in branches.items()
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["key", "value"])
        writer.writerows(rows)


def write_branches(path: Path, branches: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            fieldnames=[
                "branch",
                "query_chars",
                "query",
                "query_with_year_chars",
                "query_with_year",
            ],
        )
        writer.writeheader()
        for branch, query in branches.items():
            writer.writerow(
                {
                    "branch": branch,
                    "query_chars": len(query),
                    "query": query,
                    "query_with_year_chars": len(with_year_clause(query)),
                    "query_with_year": with_year_clause(query),
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="search/scopus-query-draft.txt",
        help="Path for the generated Scopus query text.",
    )
    parser.add_argument(
        "--metadata-output",
        default="search/scopus-query-draft-metadata.tsv",
        help="Path for generation metadata.",
    )
    parser.add_argument(
        "--branches-output",
        default="search/scopus-query-branches.tsv",
        help="Path for the exact branch-level Scopus query strings.",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    metadata_path = Path(args.metadata_output)
    branches_path = Path(args.branches_output)
    branches = build_branch_queries()
    full_query = build_full_query()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_query + "\n", encoding="utf-8")
    write_branches(branches_path, branches)
    write_metadata(metadata_path, output_path, full_query)

    print(f"Wrote {output_path}")
    print(f"Wrote {branches_path}")
    print(f"Wrote {metadata_path}")
    print(f"Query characters: {len(full_query)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
