#!/usr/bin/env python3
"""Fetch PDFs/text for search full-text screening records."""

from __future__ import annotations

import argparse
import csv
import json
import os
import pathlib
import subprocess
import tempfile
import time
import urllib.parse
from datetime import datetime, timezone

try:
    import requests
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("Install requests or run with: uv run --with requests search/fetch_full_texts.py") from exc


DEFAULT_MANIFEST = pathlib.Path("search/full-text-retrieval.tsv")
DEFAULT_STATUS = pathlib.Path("search/full-text-retrieval-status.tsv")
DEFAULT_REPORT = pathlib.Path("search/full-text-retrieval-report.json")
DEFAULT_EMAIL = os.environ.get("UNPAYWALL_EMAIL", "user@uffs.edu.br")


STATUS_FIELDS = [
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
    parser.add_argument("--manifest", type=pathlib.Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--status-output", type=pathlib.Path, default=DEFAULT_STATUS)
    parser.add_argument("--report-output", type=pathlib.Path, default=DEFAULT_REPORT)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--only-arxiv", action="store_true", help="Skip DOI/Unpaywall fallback")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between network requests")
    parser.add_argument("--timeout", type=float, default=45.0)
    parser.add_argument("--unpaywall-email", default=DEFAULT_EMAIL)
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


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_pdf_response(response: requests.Response) -> bool:
    content_type = response.headers.get("content-type", "").lower()
    return (
        response.status_code == 200
        and len(response.content) > 1000
        and (response.content.startswith(b"%PDF") or "pdf" in content_type)
    )


def atomic_write_bytes(path: pathlib.Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "wb",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        tmp_path = pathlib.Path(handle.name)
        handle.write(data)
    tmp_path.replace(path)


def pdf_to_text(pdf_path: pathlib.Path, text_path: pathlib.Path) -> tuple[bool, str]:
    text_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), str(text_path)],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except FileNotFoundError:
        return False, "pdftotext_not_found"
    except subprocess.SubprocessError as exc:
        return False, f"pdftotext_error:{exc}"
    if result.returncode != 0:
        return False, (result.stderr or result.stdout or "pdftotext_failed").strip()
    if not text_path.exists() or text_path.stat().st_size < 100:
        return False, "text_output_too_small"
    return True, ""


def fetch_arxiv(row: dict[str, str], session: requests.Session, timeout: float) -> tuple[bool, str, str]:
    arxiv_id = row.get("arxiv_id", "").strip()
    if not arxiv_id:
        return False, "", "no_arxiv_id"
    url = f"https://arxiv.org/pdf/{urllib.parse.quote(arxiv_id)}"
    response = session.get(url, timeout=timeout, allow_redirects=True)
    if not is_pdf_response(response):
        return False, url, f"arxiv_http_{response.status_code}"
    atomic_write_bytes(pathlib.Path(row["pdf_path"]), response.content)
    return True, url, ""


def unpaywall_pdf_url(
    doi: str,
    session: requests.Session,
    email: str,
    timeout: float,
) -> tuple[str, str]:
    if not doi:
        return "", "no_doi"
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={urllib.parse.quote(email)}"
    response = session.get(url, timeout=timeout)
    if response.status_code != 200:
        return "", f"unpaywall_http_{response.status_code}"
    data = response.json()
    if not data.get("is_oa"):
        return "", "not_open_access"
    candidates = []
    best = data.get("best_oa_location") or {}
    if best.get("url_for_pdf"):
        candidates.append(best["url_for_pdf"])
    for location in data.get("oa_locations") or []:
        if location.get("url_for_pdf"):
            candidates.append(location["url_for_pdf"])
    for candidate in candidates:
        if candidate:
            return candidate, ""
    return "", "no_pdf_url"


def fetch_unpaywall(
    row: dict[str, str],
    session: requests.Session,
    email: str,
    timeout: float,
) -> tuple[bool, str, str]:
    pdf_url, reason = unpaywall_pdf_url(row.get("doi", "").strip(), session, email, timeout)
    if not pdf_url:
        return False, "", reason
    response = session.get(pdf_url, timeout=timeout, allow_redirects=True)
    if not is_pdf_response(response):
        return False, pdf_url, f"oa_pdf_http_{response.status_code}"
    atomic_write_bytes(pathlib.Path(row["pdf_path"]), response.content)
    return True, pdf_url, ""


def cached_status(row: dict[str, str]) -> dict[str, str] | None:
    pdf_path = pathlib.Path(row["pdf_path"])
    text_path = pathlib.Path(row["text_path"])
    if pdf_path.exists() and pdf_path.stat().st_size > 1000:
        if text_path.exists() and text_path.stat().st_size > 100:
            updated = dict(row)
            updated["retrieval_status"] = "cached"
            updated["retrieval_source"] = "local"
            updated["retrieved_at_utc"] = updated.get("retrieved_at_utc", "")
            updated["failure_reason"] = ""
            return updated
    return None


def fetch_row(
    row: dict[str, str],
    session: requests.Session,
    args: argparse.Namespace,
) -> dict[str, str]:
    cached = cached_status(row)
    if cached and not args.overwrite:
        return cached

    updated = dict(row)
    pdf_path = pathlib.Path(row["pdf_path"])
    text_path = pathlib.Path(row["text_path"])
    if args.overwrite:
        pdf_path.unlink(missing_ok=True)
        text_path.unlink(missing_ok=True)

    failures: list[str] = []
    url_used = ""
    source = ""
    ok = False

    if row.get("arxiv_id", "").strip():
        try:
            ok, url_used, reason = fetch_arxiv(row, session, args.timeout)
            if ok:
                source = "arxiv"
            else:
                failures.append(reason)
        except requests.RequestException as exc:
            failures.append(f"arxiv_error:{exc}")
        time.sleep(args.delay)

    if not ok and not args.only_arxiv and row.get("doi", "").strip():
        try:
            ok, url_used, reason = fetch_unpaywall(row, session, args.unpaywall_email, args.timeout)
            if ok:
                source = "unpaywall"
            else:
                failures.append(reason)
        except (requests.RequestException, json.JSONDecodeError) as exc:
            failures.append(f"unpaywall_error:{exc}")
        time.sleep(args.delay)

    if ok:
        text_ok, text_reason = pdf_to_text(pdf_path, text_path)
        updated["retrieval_status"] = "ok" if text_ok else "pdf_only"
        updated["retrieval_source"] = source
        updated["retrieved_at_utc"] = utc_now()
        updated["preferred_url"] = url_used or row.get("preferred_url", "")
        updated["failure_reason"] = "" if text_ok else text_reason
    else:
        updated["retrieval_status"] = "failed"
        updated["retrieval_source"] = ""
        updated["retrieved_at_utc"] = utc_now()
        updated["failure_reason"] = " | ".join(reason for reason in failures if reason) or "no_fetch_route"

    return updated


def main() -> int:
    args = parse_args()
    fields, rows = read_tsv(args.manifest)
    missing_fields = sorted(set(STATUS_FIELDS) - set(fields))
    if missing_fields:
        raise SystemExit(f"{args.manifest} is missing fields: {', '.join(missing_fields)}")

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "SearchV2FullTextRetrieval/1.0 (mailto:user@uffs.edu.br)",
        }
    )

    output_rows: list[dict[str, str]] = []
    processed = 0
    for row in rows:
        if args.limit is not None and processed >= args.limit:
            output_rows.append(dict(row))
            continue
        updated = fetch_row(row, session, args)
        output_rows.append(updated)
        processed += 1
        print(
            f"{updated['full_text_id']}\t{updated['screening_id']}\t"
            f"{updated['retrieval_status']}\t{updated['retrieval_source']}\t"
            f"{updated['failure_reason'][:120]}",
            flush=True,
        )

    write_tsv(args.status_output, STATUS_FIELDS, output_rows)

    counts: dict[str, int] = {}
    for row in output_rows:
        status = row.get("retrieval_status", "") or "not_attempted"
        counts[status] = counts.get(status, 0) + 1
    report = {
        "generated_at_utc": utc_now(),
        "manifest": str(args.manifest),
        "status_output": str(args.status_output),
        "processed": processed,
        "counts": counts,
        "only_arxiv": args.only_arxiv,
    }
    args.report_output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
