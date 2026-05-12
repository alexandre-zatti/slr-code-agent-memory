#!/usr/bin/env python3
"""Check manuscript BibTeX coverage for search included-study keys."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTRACTION = ROOT / "extraction" / "extracted-data.tsv"
BIB_DIR = ROOT / "manuscript" / "references"
if not BIB_DIR.exists():
    BIB_DIR = ROOT / "references"
OUT_TSV = ROOT / "analysis" / "bibliography-coverage.tsv"
OUT_MD = ROOT / "analysis" / "bibliography-coverage.md"


def bib_keys_by_file() -> dict[str, set[str]]:
    keys: dict[str, set[str]] = defaultdict(set)
    pattern = re.compile(r"^@\w+\s*\{\s*([^,\s]+)", re.MULTILINE)
    for path in sorted(BIB_DIR.glob("*.bib")):
        text = path.read_text(encoding="utf-8")
        keys[path.relative_to(ROOT).as_posix()].update(pattern.findall(text))
    return dict(keys)


def read_extraction() -> list[dict[str, str]]:
    with EXTRACTION.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    rows = read_extraction()
    keys_by_file = bib_keys_by_file()
    all_keys = {key for keys in keys_by_file.values() for key in keys}

    output_rows: list[dict[str, str]] = []
    for row in rows:
        key = row["id"]
        files = [path for path, keys in keys_by_file.items() if key in keys]
        status = "present" if files else "missing"
        output_rows.append(
            {
                "included_id": row["included_id"],
                "bibtex_key": key,
                "coverage_status": status,
                "bib_files": ";".join(files) if files else "NR",
                "study_role": row["study_role"],
                "architecture_denominator_decision": row["architecture_denominator_decision"],
                "year": row["ano"],
                "title": row["titulo"],
                "venue": row["venue"],
                "source_routes": row["source_routes"],
                "source_files": row["source_files"],
            }
        )

    with OUT_TSV.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = list(output_rows[0])
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    status_counts = Counter(row["coverage_status"] for row in output_rows)
    missing_rows = [row for row in output_rows if row["coverage_status"] == "missing"]
    missing_by_role = Counter(row["architecture_denominator_decision"] for row in missing_rows)
    present_rows = [row for row in output_rows if row["coverage_status"] == "present"]
    bib_scope = f"`{BIB_DIR.relative_to(ROOT).as_posix()}/*.bib`."

    lines = [
        "# Search Bibliography Coverage",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "Scope: exact-key coverage for search included-study IDs against",
        bib_scope,
        "",
        "This check does not validate bibliographic metadata quality; it only",
        "identifies which search included-study keys already exist locally.",
        "",
        "## Summary",
        "",
        f"- Included search rows checked: {len(output_rows)}",
        f"- Present exact keys: {status_counts['present']}",
        f"- Missing exact keys: {status_counts['missing']}",
        f"- Coverage TSV: `{OUT_TSV.relative_to(ROOT)}`",
        "",
        "## Missing By Denominator Role",
        "",
        "| Denominator decision | Missing keys |",
        "| --- | ---: |",
    ]
    for label, count in sorted(missing_by_role.items()):
        lines.append(f"| `{label}` | {count} |")

    lines.extend(
        [
            "",
            "## Present Keys",
            "",
            "| Included ID | Key | File | Title |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in present_rows:
        title = row["title"].replace("|", "\\|")
        lines.append(
            f"| {row['included_id']} | `{row['bibtex_key']}` | "
            f"`{row['bib_files']}` | {title} |"
        )

    lines.extend(
        [
            "",
            "## Missing Keys",
            "",
            "| Included ID | Key | Year | Denominator | Title |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    for row in missing_rows:
        title = row["title"].replace("|", "\\|")
        lines.append(
            f"| {row['included_id']} | `{row['bibtex_key']}` | {row['year']} | "
            f"`{row['architecture_denominator_decision']}` | {title} |"
        )

    lines.extend(
        [
            "",
            "## Use Constraint",
            "",
            "Do not add manuscript `\\citep{}` or `\\citet{}` calls for missing",
            "keys until BibTeX entries are added from verified metadata.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_TSV.relative_to(ROOT)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    print(
        f"summary: present={status_counts['present']} "
        f"missing={status_counts['missing']}"
    )
    return 1 if status_counts["missing"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
