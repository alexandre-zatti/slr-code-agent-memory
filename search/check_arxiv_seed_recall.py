#!/usr/bin/env python3
"""Check search arXiv seed recall with rate limiting.

This script is intentionally conservative after ad hoc probing hit HTTP 429
rate limits. It checks each seed by querying:

    id:<arxiv_id> AND <query-family>

for each draft search arXiv query family.
It does not freeze the final search search. It only reports whether the
draft strings recover known seeds.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path


OPENSEARCH = "{http://a9.com/-/spec/opensearch/1.1/}"
API_URL = "https://export.arxiv.org/api/query"
DEFAULT_RATE_LIMIT_SECONDS = 5.0
REQUEST_LINE_WARNING_CHARS = 4000
DEFAULT_MAX_URL_CHARS = 3200
DEFAULT_SORT_BY = "submittedDate"
DEFAULT_SORT_ORDER = "ascending"


def quoted_or(field: str, terms: list[str]) -> str:
    return "(" + " OR ".join(f'{field}:"{term}"' for term in terms) + ")"


def fielded_or(fields: list[str], terms: list[str]) -> str:
    return "(" + " OR ".join(quoted_or(field, terms) for field in fields) + ")"


def and_query(parts: list[str], date_clause: str | None = None) -> str:
    query_parts = [part for part in parts if part]
    if date_clause:
        query_parts.append(date_clause)
    return " AND ".join(query_parts)


CATEGORIES = "(cat:cs.SE OR cat:cs.AI OR cat:cs.CL OR cat:cs.LG)"

C1_GENERIC_ABS = [
    "LLM agent",
    "LLM agents",
    "LLM-based agent",
    "LLM-based agents",
    "large language model agent",
    "large language model agents",
    "language model agent",
    "language model agents",
    "language agent",
    "language agents",
]

C1_SEED_GAP_ABS = [
    "LLM agentic system",
    "LLM agentic systems",
    "multi-agent reasoning",
    "multi-agent reasoning framework",
]

C1_CODING_ABS = [
    "AI coding agent",
    "AI coding agents",
    "software engineering agent",
    "software engineering agents",
    "SWE agent",
    "SWE agents",
    "coding agent",
    "coding agents",
    "code agent",
    "code agents",
    "programming agent",
    "programming agents",
    "autonomous coding",
    "agentic coding",
    "coding assistant",
    "code assistant",
    "software-developing agent",
    "software developing agent",
]

C1_GENERIC_TITLE = [
    "LLM-based agent",
    "LLM-based agents",
    "large language model agent",
    "large language model agents",
    "LLM agent",
    "LLM agents",
    "language model agent",
    "language model agents",
    "language agent",
    "language agents",
]

C1_SEED_GAP_TITLE = [
    "LLM agentic system",
    "LLM agentic systems",
    "multi-agent reasoning",
    "multi-agent reasoning framework",
]

C1_CODING_TITLE = [
    "AI coding agent",
    "AI coding agents",
    "coding agent",
    "coding agents",
    "code agent",
    "code agents",
    "software engineering agent",
    "software engineering agents",
    "SWE agent",
    "SWE agents",
    "programming agent",
    "programming agents",
    "autonomous coding",
    "agentic coding",
    "coding assistant",
    "code assistant",
    "software-developing agent",
    "software developing agent",
]

C2_BROAD_ABS = [
    "memory",
    "experience",
    "knowledge persistence",
    "context management",
    "long-term memory",
    "long term memory",
    "episodic memory",
    "semantic memory",
    "procedural memory",
    "knowledge reuse",
    "experience reuse",
    "continual learning",
    "experience replay",
    "memory-augmented",
    "persistent memory",
    "persistent context",
    "cross-task",
    "cross task",
    "reasoning memory",
    "experience memory",
    "experience learning",
    "evolving memory",
    "optimization memory",
    "experience bank",
    "memory bank",
    "failure memory",
    "trajectory memory",
    "skill memory",
    "case base",
    "case-based",
    "experience sharing",
    "context reuse",
    "self-evolving",
    "self evolving",
    "context learning",
    "context engineering",
    "state tracking",
    "memory management",
    "dynamic memory management",
    "adaptive memory",
    "context memory",
    "session memory",
    "repository context",
    "forgetting",
    "cross-session",
    "cross session",
    "history-aware",
    "history aware",
    "experience-driven",
    "experience driven",
    "learning from experience",
    "cross-domain experience",
    "self-evolve",
    "self-evolves",
    "self-evolution",
    "self-improving",
    "self-improvement",
    "continuously evolve",
    "open-ended evolution",
]

C2_STRONG_ABS = [
    "episodic memory",
    "semantic memory",
    "procedural memory",
    "long-term memory",
    "long term memory",
    "persistent memory",
    "reasoning memory",
    "experience memory",
    "experience learning",
    "evolving memory",
    "optimization memory",
    "memory bank",
    "failure memory",
    "experience bank",
    "case base",
    "case-based",
    "experience sharing",
    "context reuse",
    "experience reuse",
    "knowledge reuse",
    "cross-task",
    "cross task",
    "continual learning",
    "self-evolving",
    "self evolving",
    "structured memory",
    "trajectory memory",
    "knowledge accumulation",
    "context learning",
    "context engineering",
    "state tracking",
    "memory management",
    "dynamic memory management",
    "adaptive memory",
    "context memory",
    "session memory",
    "repository context",
    "forgetting",
    "cross-session",
    "cross session",
    "history-aware",
    "history aware",
    "experience-driven",
    "experience driven",
    "learning from experience",
    "cross-domain experience",
    "self-evolve",
    "self-evolves",
    "self-evolution",
    "self-improving",
    "self-improvement",
    "continuously evolve",
    "open-ended evolution",
]

C3_ABS = [
    "SWE-bench",
    "HumanEval",
    "MBPP",
    "CodeContests",
    "Defects4J",
    "software engineering",
    "software development",
    "repository-level",
    "program repair",
    "code repair",
    "software repair",
    "automated program repair",
    "repository-level program repair",
    "issue resolution",
    "code generation",
    "program synthesis",
    "test generation",
    "software testing",
    "code optimization",
    "coding benchmark",
    "programming benchmark",
    "software engineering benchmark",
    "bug fix",
    "bug fixing",
    "CodeIF-Bench",
    "CoderEval",
    "SWE-Bench Pro",
    "SWE-Bench Verified",
    "code localization",
    "patch generation",
    "automated debugging",
]

C3_SEED_GAP_ABS = [
    "LiveCodeBench",
    "LiveCodeBench-V5",
    "kernel optimization",
    "accelerator kernel",
    "accelerator kernels",
    "AI accelerator",
    "AI accelerators",
    "NKIBench",
    "MetaGPT",
    "DataInterpreter",
]


def build_query_families(date_clause: str | None = None) -> dict[str, str]:
    c1_coding = "(" + " OR ".join([quoted_or("abs", C1_CODING_ABS), quoted_or("ti", C1_CODING_TITLE)]) + ")"
    c1_generic = "(" + " OR ".join(
        [
            quoted_or("abs", [*C1_GENERIC_ABS, *C1_SEED_GAP_ABS]),
            quoted_or("ti", [*C1_GENERIC_TITLE, *C1_SEED_GAP_TITLE]),
        ]
    ) + ")"
    c2_broad = fielded_or(["abs", "ti"], C2_BROAD_ABS)
    c2_strong = fielded_or(["abs", "ti"], C2_STRONG_ABS)
    c3 = fielded_or(["abs", "ti"], [*C3_ABS, *C3_SEED_GAP_ABS])

    families = {
        "family_a_coding_agent_memory": and_query([CATEGORIES, c1_coding, c2_broad], date_clause),
        "family_b_generic_agent_memory_se": and_query(
            [CATEGORIES, c1_generic, c2_broad, c3], date_clause
        ),
        "family_c_strong_memory_se": and_query([CATEGORIES, c2_strong, c3], date_clause),
    }
    return families


def c1_coding_expr() -> str:
    return "(" + " OR ".join(
        [quoted_or("abs", C1_CODING_ABS), quoted_or("ti", C1_CODING_TITLE)]
    ) + ")"


def c1_generic_expr() -> str:
    return "(" + " OR ".join(
        [quoted_or("abs", C1_GENERIC_ABS), quoted_or("ti", C1_GENERIC_TITLE)]
    ) + ")"


def c1_generic_seed_gap_expr() -> str:
    return "(" + " OR ".join(
        [
            quoted_or("abs", [*C1_GENERIC_ABS, *C1_SEED_GAP_ABS]),
            quoted_or("ti", [*C1_GENERIC_TITLE, *C1_SEED_GAP_TITLE]),
        ]
    ) + ")"


def chunked_term_queries(
    logical_family: str,
    fixed_parts: list[str],
    variable_terms: list[str],
    variable_fields: list[str],
    date_clause: str | None,
    max_url_chars: int,
    start_index: int = 1,
) -> dict[str, str]:
    chunks: list[list[str]] = []
    current: list[str] = []

    for term in variable_terms:
        candidate = [*current, term]
        candidate_query = and_query(
            [*fixed_parts, fielded_or(variable_fields, candidate)],
            date_clause,
        )
        if current and request_url_length(candidate_query) > max_url_chars:
            chunks.append(current)
            current = [term]
            current_query = and_query(
                [*fixed_parts, fielded_or(variable_fields, current)],
                date_clause,
            )
            if request_url_length(current_query) > max_url_chars:
                raise ValueError(
                    f"single term {term!r} exceeds max URL length for {logical_family}"
                )
        else:
            current = candidate

    if current:
        chunks.append(current)

    return {
        f"{logical_family}__chunk{index:02d}": and_query(
            [*fixed_parts, fielded_or(variable_fields, terms)],
            date_clause,
        )
        for index, terms in enumerate(chunks, start=start_index)
    }


def logical_family_for_chunk(chunk_name: str) -> str:
    return chunk_name.split("__chunk", 1)[0]


def build_query_chunks(
    date_clause: str | None = None,
    max_url_chars: int = DEFAULT_MAX_URL_CHARS,
) -> dict[str, str]:
    c1_coding = c1_coding_expr()
    c1_generic = c1_generic_expr()
    c1_generic_seed_gap = c1_generic_seed_gap_expr()
    c3 = fielded_or(["abs", "ti"], C3_ABS)
    c3_seed_gap = fielded_or(["abs", "ti"], C3_SEED_GAP_ABS)

    chunks: dict[str, str] = {}
    family_a_chunks = chunked_term_queries(
        logical_family="family_a_coding_agent_memory",
        fixed_parts=[CATEGORIES, c1_coding],
        variable_terms=C2_BROAD_ABS,
        variable_fields=["abs", "ti"],
        date_clause=date_clause,
        max_url_chars=max_url_chars,
    )
    chunks.update(family_a_chunks)
    family_b_chunks = chunked_term_queries(
        logical_family="family_b_generic_agent_memory_se",
        fixed_parts=[CATEGORIES, c1_generic, c3],
        variable_terms=C2_BROAD_ABS,
        variable_fields=["abs", "ti"],
        date_clause=date_clause,
        max_url_chars=max_url_chars,
    )
    chunks.update(family_b_chunks)
    family_b_seed_gap_chunks = chunked_term_queries(
        logical_family="family_b_generic_agent_memory_se",
        fixed_parts=[CATEGORIES, c1_generic_seed_gap, c3_seed_gap],
        variable_terms=C2_BROAD_ABS,
        variable_fields=["abs", "ti"],
        date_clause=date_clause,
        max_url_chars=max_url_chars,
        start_index=len(family_b_chunks) + 1,
    )
    chunks.update(family_b_seed_gap_chunks)
    family_c_chunks = chunked_term_queries(
        logical_family="family_c_strong_memory_se",
        fixed_parts=[CATEGORIES, c3],
        variable_terms=C2_STRONG_ABS,
        variable_fields=["abs", "ti"],
        date_clause=date_clause,
        max_url_chars=max_url_chars,
    )
    chunks.update(family_c_chunks)
    family_c_seed_gap_chunks = chunked_term_queries(
        logical_family="family_c_strong_memory_se",
        fixed_parts=[CATEGORIES, c3_seed_gap],
        variable_terms=C2_STRONG_ABS,
        variable_fields=["abs", "ti"],
        date_clause=date_clause,
        max_url_chars=max_url_chars,
        start_index=len(family_c_chunks) + 1,
    )
    chunks.update(family_c_seed_gap_chunks)
    return chunks


def date_bound(value: str, *, end_of_day: bool) -> str:
    digits = "".join(char for char in value if char.isdigit())
    if len(digits) == 8:
        return f"{digits}{'2359' if end_of_day else '0000'}"
    if len(digits) == 12:
        return digits
    raise ValueError(
        f"invalid arXiv date bound {value!r}; use YYYY-MM-DD, YYYYMMDD, or YYYYMMDDHHMM"
    )


def build_date_clause(submitted_from: str | None, submitted_to: str | None) -> str | None:
    if not submitted_from and not submitted_to:
        return None

    start = date_bound(submitted_from or "1991-01-01", end_of_day=False)
    end = date_bound(submitted_to or "2999-12-31", end_of_day=True)
    return f"submittedDate:[{start} TO {end}]"


def arxiv_total(query: str, retries: int, rate_limit_seconds: float) -> int:
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": 1,
            "sortBy": DEFAULT_SORT_BY,
            "sortOrder": DEFAULT_SORT_ORDER,
        }
    )
    url = f"{API_URL}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "SLR-SearchV2/0.1"})

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=40) as response:
                root = ET.fromstring(response.read())
                return int(root.findtext(f"{OPENSEARCH}totalResults", "0"))
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < retries - 1:
                sleep_for = rate_limit_seconds * (attempt + 2)
                print(f"429 from arXiv; sleeping {sleep_for:.1f}s", file=sys.stderr)
                time.sleep(sleep_for)
                continue
            raise
        except (TimeoutError, urllib.error.URLError) as exc:
            if attempt < retries - 1:
                sleep_for = rate_limit_seconds * (attempt + 2)
                print(
                    f"{type(exc).__name__} from arXiv; sleeping {sleep_for:.1f}s",
                    file=sys.stderr,
                )
                time.sleep(sleep_for)
                continue
            raise

    raise RuntimeError("unreachable")


def format_exception(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        return f"ERROR:HTTPError:{exc.code}"
    return f"ERROR:{type(exc).__name__}"


def request_url_length(query: str) -> int:
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": 1,
            "sortBy": DEFAULT_SORT_BY,
            "sortOrder": DEFAULT_SORT_ORDER,
        }
    )
    return len(f"{API_URL}?{params}")


def git_value(args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:  # noqa: BLE001 - metadata best effort
        return "unavailable"


def load_seeds(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def filter_seeds(
    seeds: list[dict[str, str]],
    groups: list[str] | None,
    seed_ids: list[str] | None,
) -> list[dict[str, str]]:
    group_filter = set(groups or [])
    seed_id_filter = set(seed_ids or [])
    selected = []
    for seed in seeds:
        if group_filter and seed["seed_group"] not in group_filter:
            continue
        if seed_id_filter and seed["seed_id"] not in seed_id_filter:
            continue
        selected.append(seed)
    return selected


def is_required_recall(seed: dict[str, str]) -> bool:
    if seed["search_recall_expectation"] != "database_query":
        return False
    return seed["expected_status"] not in {"probably_exclude", "exclude_withdrawn"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seed-set",
        default="search/seed-set.tsv",
        help="TSV seed set path",
    )
    parser.add_argument(
        "--output",
        default="search/arxiv-seed-recall.tsv",
        help="Output TSV path",
    )
    parser.add_argument(
        "--query-counts",
        action="store_true",
        help="Also fetch total result count for each query family",
    )
    parser.add_argument(
        "--groups",
        nargs="+",
        help="Only check seeds in these seed_group values",
    )
    parser.add_argument(
        "--seed-ids",
        nargs="+",
        help="Only check these seed_id values",
    )
    parser.add_argument(
        "--submitted-from",
        help="Optional arXiv submittedDate lower bound, e.g. 2023-01-01",
    )
    parser.add_argument(
        "--submitted-to",
        help="Optional arXiv submittedDate upper bound, e.g. 2026-04-27",
    )
    parser.add_argument(
        "--query-output",
        help="Optional TSV path that records the exact executable query chunks used",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build filters and write query output without calling arXiv",
    )
    parser.add_argument(
        "--metadata-output",
        help="Optional TSV path that records run metadata",
    )
    parser.add_argument(
        "--validate-required",
        action="store_true",
        help="Exit nonzero if any required database-query seed misses or errors",
    )
    parser.add_argument(
        "--max-url-chars",
        type=int,
        default=DEFAULT_MAX_URL_CHARS,
        help="Maximum generated URL length for executable query chunks",
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=DEFAULT_RATE_LIMIT_SECONDS,
        help="Seconds to sleep between arXiv requests",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=6,
        help="Retries per arXiv request before recording an error",
    )
    args = parser.parse_args()

    seed_path = Path(args.seed_set)
    output_path = Path(args.output)
    date_clause = build_date_clause(args.submitted_from, args.submitted_to)
    seeds = [seed for seed in load_seeds(seed_path) if seed.get("arxiv_id")]
    seeds = filter_seeds(seeds, groups=args.groups, seed_ids=args.seed_ids)
    families = build_query_chunks(date_clause=date_clause, max_url_chars=args.max_url_chars)

    if args.query_output:
        query_output = Path(args.query_output)
        query_output.parent.mkdir(parents=True, exist_ok=True)
        with query_output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                delimiter="\t",
                fieldnames=[
                    "query_chunk",
                    "logical_family",
                    "url_chars",
                    "url_length_warning",
                    "search_query",
                ],
            )
            writer.writeheader()
            for name, query in families.items():
                url_chars = request_url_length(query)
                writer.writerow(
                    {
                        "query_chunk": name,
                        "logical_family": logical_family_for_chunk(name),
                        "url_chars": url_chars,
                        "url_length_warning": "yes"
                        if url_chars >= REQUEST_LINE_WARNING_CHARS
                        else "no",
                        "search_query": query,
                    }
                )

    if args.metadata_output:
        metadata_output = Path(args.metadata_output)
        metadata_output.parent.mkdir(parents=True, exist_ok=True)
        with metadata_output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["key", "value"])
            writer.writeheader()
            writer.writerow({"key": "run_started_utc", "value": datetime.now(UTC).isoformat()})
            writer.writerow({"key": "script", "value": __file__})
            writer.writerow({"key": "git_head", "value": git_value(["rev-parse", "HEAD"])})
            git_status = git_value(["status", "--short"])
            writer.writerow({"key": "git_dirty", "value": "yes" if git_status else "no"})
            writer.writerow(
                {
                    "key": "git_status_entries",
                    "value": str(len(git_status.splitlines())) if git_status else "0",
                }
            )
            writer.writerow({"key": "seed_set", "value": str(seed_path)})
            writer.writerow({"key": "output", "value": str(output_path)})
            writer.writerow({"key": "query_output", "value": args.query_output or ""})
            writer.writerow({"key": "submitted_from", "value": args.submitted_from or ""})
            writer.writerow({"key": "submitted_to", "value": args.submitted_to or ""})
            writer.writerow({"key": "arxiv_categories", "value": CATEGORIES})
            writer.writerow({"key": "groups", "value": ";".join(args.groups or [])})
            writer.writerow({"key": "seed_ids", "value": ";".join(args.seed_ids or [])})
            writer.writerow({"key": "rate_limit_seconds", "value": str(args.rate_limit)})
            writer.writerow({"key": "retries", "value": str(args.retries)})
            writer.writerow({"key": "max_url_chars", "value": str(args.max_url_chars)})
            writer.writerow({"key": "query_chunks", "value": ";".join(families.keys())})
            writer.writerow(
                {
                    "key": "logical_families",
                    "value": ";".join(dict.fromkeys(logical_family_for_chunk(name) for name in families)),
                }
            )

    if args.dry_run:
        for name, query in families.items():
            print(f"{name}\t{query}")
        return 0

    rows: list[dict[str, str]] = []

    if args.query_counts:
        for name, query in families.items():
            try:
                total = arxiv_total(query, retries=args.retries, rate_limit_seconds=args.rate_limit)
            except Exception as exc:  # noqa: BLE001 - fail-soft audit script
                total = format_exception(exc)
            print(f"{name}\t{total}", flush=True)
            time.sleep(args.rate_limit)

    for seed in seeds:
        recovered_by: list[str] = []
        recovered_logical_families: list[str] = []
        counts: dict[str, str] = {}
        errors = 0
        for name, query in families.items():
            try:
                count = arxiv_total(
                    f'id:{seed["arxiv_id"]} AND {query}',
                    retries=args.retries,
                    rate_limit_seconds=args.rate_limit,
                )
                counts[name] = str(count)
                if count > 0:
                    recovered_by.append(name)
                    logical_family = logical_family_for_chunk(name)
                    if logical_family not in recovered_logical_families:
                        recovered_logical_families.append(logical_family)
            except Exception as exc:  # noqa: BLE001 - preserve partial recall table
                counts[name] = format_exception(exc)
                errors += 1
            time.sleep(args.rate_limit)

        if errors == 0:
            request_status = "ok"
        elif errors == len(families):
            request_status = "all_error"
        else:
            request_status = "partial_error"
        row = {
            "seed_id": seed["seed_id"],
            "arxiv_id": seed["arxiv_id"],
            "seed_group": seed["seed_group"],
            "expected_status": seed["expected_status"],
            "search_recall_expectation": seed["search_recall_expectation"],
            "required_recall": "yes" if is_required_recall(seed) else "no",
            "recovered": "yes" if recovered_by else "no",
            "recovered_by": ";".join(recovered_by),
            "recovered_logical_families": ";".join(recovered_logical_families),
            "request_status": request_status,
            "notes": seed["notes"],
        }
        row.update(counts)
        rows.append(row)
        print(f'{row["seed_id"]}\t{row["recovered"]}\t{row["recovered_by"]}', flush=True)

    fieldnames = [
        "seed_id",
        "arxiv_id",
        "seed_group",
        "expected_status",
        "search_recall_expectation",
        "required_recall",
        "recovered",
        "recovered_by",
        "recovered_logical_families",
        "request_status",
        "notes",
        *families.keys(),
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {output_path}", file=sys.stderr)

    if args.validate_required:
        failures = [
            row
            for row in rows
            if row["required_recall"] == "yes"
            and (row["request_status"] != "ok" or row["recovered"] != "yes")
        ]
        if failures:
            print("Required seed recall validation failed:", file=sys.stderr)
            for row in failures:
                print(
                    f'- {row["seed_id"]}: recovered={row["recovered"]}, '
                    f'request_status={row["request_status"]}',
                    file=sys.stderr,
                )
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
