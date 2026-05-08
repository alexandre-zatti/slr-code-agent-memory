#!/usr/bin/env python3
"""Finalize search protocol Q1-Q6 quality scores.

The protocol checklist uses six items scored as 0, 0.5, or 1:

- Q1: research objectives clearly defined.
- Q2: evaluation method adequate to objectives.
- Q3: threats to validity discussed.
- Q4: results based on empirical data rather than examples only.
- Q5: study context sufficiently described for replication.
- Q6: evaluation metrics clearly defined.

This script preserves already carried numeric prior scores and fills the current search
records that still had `NR` after extraction. The scored TSV is the audit trail;
the JSON extraction files keep only the final numeric `pontuacao_qualidade`.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTRACTED_PATH = ROOT / "extraction" / "extracted-data.tsv"
QUEUE_PATH = ROOT / "extraction" / "extraction-queue.tsv"
QUALITY_PATH = ROOT / "analysis" / "quality-assessment.tsv"

Q_FIELDS = [
    "q1_objectives",
    "q2_evaluation_adequacy",
    "q3_threats_discussed",
    "q4_empirical_data",
    "q5_context_replicability",
    "q6_metrics_defined",
]

PROFILE_BY_SCORE = {
    "6.0": {
        "scores": ("1", "1", "1", "1", "1", "1"),
        "rationale": (
            "Clear objectives, adequate empirical evaluation, explicit threats "
            "or limitations, reproducible context, and defined metrics."
        ),
    },
    "5.5": {
        "scores": ("1", "1", "1", "1", "0.5", "1"),
        "rationale": (
            "Strong empirical evaluation and metrics, with partial replication "
            "context because of preprint status, artifact limits, proprietary "
            "components, benchmark-specific setup, or model/provider dependence."
        ),
    },
    "5.0": {
        "scores": ("1", "1", "0.5", "1", "0.5", "1"),
        "rationale": (
            "Adequate empirical evaluation with defined metrics, but threats "
            "and/or replication context are only partially addressed."
        ),
    },
    "4.5": {
        "scores": ("1", "0.5", "1", "1", "0", "1"),
        "rationale": (
            "Empirical results and metrics are present, but evaluation adequacy "
            "is limited by narrow, internal, proxy, small, or domain-specific "
            "settings and replication context is weak."
        ),
    },
    "4.0": {
        "scores": ("1", "0.5", "0.5", "1", "0", "1"),
        "rationale": (
            "Objectives and empirical metrics are present, but evaluation "
            "adequacy, threat discussion, and replication context are limited."
        ),
    },
    "3.5": {
        "scores": ("1", "0.5", "0.5", "0.5", "0", "1"),
        "rationale": (
            "Objectives and metrics are present, but evidence is pilot-scale or "
            "proof-of-concept, with limited empirical basis and weak replication "
            "context."
        ),
    },
}

QUALITY_OVERRIDES = {
    "I001": "5.5",
    "I002": "4.5",
    "I003": "5.0",
    "I004": "5.0",
    "I006": "5.0",
    "I007": "4.5",
    "I008": "5.5",
    "I010": "5.5",
    "I012": "5.5",
    "I013": "4.0",
    "I015": "5.0",
    "I017": "5.5",
    "I018": "4.5",
    "I019": "4.5",
    "I020": "5.0",
    "I021": "5.0",
    "I024": "5.0",
    "I026": "4.5",
    "I027": "4.5",
    "I030": "4.5",
    "I031": "5.5",
    "I032": "4.5",
    "I033": "4.5",
    "I038": "4.5",
    "I041": "5.0",
    "I043": "5.5",
    "I044": "5.0",
    "I045": "4.5",
    "I046": "4.0",
    "I047": "4.5",
    "I048": "4.5",
    "I049": "4.5",
    "I050": "5.0",
    "I051": "5.0",
    "I052": "5.0",
    "I053": "5.5",
    "I054": "5.0",
    "I055": "3.5",
    "I056": "5.0",
    "I057": "5.5",
    "I058": "5.0",
    "I060": "5.0",
    "I061": "5.5",
    "I062": "4.5",
    "I065": "5.0",
    "I066": "5.0",
    "I067": "5.5",
    "I068": "3.5",
    "I069": "4.5",
    "I070": "4.5",
    "I073": "5.0",
    "I074": "5.0",
    "I076": "5.0",
    "I077": "5.0",
    "I078": "5.0",
    "I079": "5.5",
    "I080": "5.5",
    "I081": "5.0",
    "I082": "5.0",
    "I083": "5.5",
    "I085": "5.5",
    "I086": "4.0",
    "I088": "4.5",
    "I090": "5.0",
    "I091": "4.5",
    "I093": "5.0",
    "I095": "5.0",
}

RATIONALE_OVERRIDES = {
    "I013": (
        "Quality score 4.0: SATLUTION reports empirical SAT-competition "
        "metrics, but effective runs required high-level human steering, "
        "correctness failures are prominent, source availability is not "
        "reported, and replication context is weak."
    ),
    "I046": (
        "Quality score 4.0: APEX-EM reports empirical benchmark evidence, but "
        "some experiments remain in progress and key comparisons involve "
        "different backbones, leaving evaluation adequacy and replication "
        "context limited."
    ),
    "I055": (
        "Quality score 3.5: DARWIN is a proof-of-concept on a small "
        "nanoGPT/Shakespeare setup with few generations and insignificant "
        "results, so empirical strength and replication context are limited."
    ),
    "I068": (
        "Quality score 3.5: Learning to Commit is a pilot on one private "
        "repository with seven future tasks and LLM judging, so empirical "
        "breadth and replication context are limited despite defined metrics."
    ),
    "I086": (
        "Quality score 4.0: SelfEvolve is evaluated on 11 manually designed "
        "tasks with one function-calling stack and possible test-code "
        "collusion, limiting evaluation adequacy and replication context."
    ),
}


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def architecture_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if row["architecture_denominator_decision"] == "include_architecture"
    ]


def final_score(row: dict[str, str]) -> str:
    included_id = row["included_id"]
    if included_id in QUALITY_OVERRIDES:
        return QUALITY_OVERRIDES[included_id]
    current = row["pontuacao_qualidade"]
    if current not in {"", "NR", "NA"}:
        return f"{float(current):.1f}"
    raise KeyError(f"missing quality score decision for {included_id}")


def score_rationale(included_id: str, score: str) -> str:
    if included_id in RATIONALE_OVERRIDES:
        return RATIONALE_OVERRIDES[included_id]
    return f"Quality score {score}: {PROFILE_BY_SCORE[score]['rationale']}"


def update_quality_tsv(extracted_rows: list[dict[str, str]]) -> None:
    fieldnames, quality_rows = load_tsv(QUALITY_PATH)
    by_included = {row["included_id"]: row for row in extracted_rows}
    seen = {row["included_id"] for row in quality_rows}
    expected = {row["included_id"] for row in extracted_rows}
    missing = sorted(expected - seen)
    extra = sorted(seen - expected)
    if missing or extra:
        raise SystemExit(f"quality TSV coverage mismatch: missing={missing}, extra={extra}")

    for row in quality_rows:
        included_id = row["included_id"]
        score = final_score(by_included[included_id])
        profile = PROFILE_BY_SCORE[score]
        for field, value in zip(Q_FIELDS, profile["scores"], strict=True):
            row[field] = value
        row["final_score"] = score
        row["manual_rationale"] = score_rationale(included_id, score)

    write_tsv(QUALITY_PATH, fieldnames, quality_rows)


def update_json_files(score_by_included: dict[str, str]) -> int:
    _, queue_rows = load_tsv(QUEUE_PATH)
    path_by_included = {
        row["included_id"]: ROOT / row["json_path"]
        for row in queue_rows
        if row["included_id"] in score_by_included
    }
    missing = sorted(set(score_by_included) - set(path_by_included))
    if missing:
        raise SystemExit(f"missing JSON paths for included IDs: {missing}")

    updated = 0
    for included_id, score in score_by_included.items():
        path = path_by_included[included_id]
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        data["pontuacao_qualidade"] = score
        with path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        updated += 1
    return updated


def main() -> None:
    _, rows = load_tsv(EXTRACTED_PATH)
    arch_rows = architecture_rows(rows)
    score_by_included = {row["included_id"]: final_score(row) for row in arch_rows}
    update_quality_tsv(arch_rows)
    updated = update_json_files(score_by_included)
    print(f"updated {QUALITY_PATH.relative_to(ROOT)}")
    print(f"updated {updated} JSON extraction files")


if __name__ == "__main__":
    main()
