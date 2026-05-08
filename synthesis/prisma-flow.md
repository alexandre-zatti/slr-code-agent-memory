# PRISMA Flow Draft - Current Search

Date: 2026-04-29

Status: draft intake counts after final database exports, citation chasing,
deduplication, deterministic CI3 exclusions, title/abstract calibration, and
full-text screening batches 001-020, updated with the post-extraction
architecture/contextual denominator split.
Title/abstract screening, false-negative audit, and full-text screening for
retrieved, metadata-resolved, or publisher-abstract-resolved records are
complete; one closed record is finalized as not retrieved.
Standalone rendered artifacts are now available at
`analysis/prisma-flow-diagram.tex`,
`analysis/prisma-flow-diagram.pdf`, and
`analysis/prisma-flow-diagram.png`.

## Identification

Records identified from database searches:

- arXiv: 1,118 raw rows.
- Scopus: 130 raw rows.
- Database subtotal: 1,248 raw rows.

Records identified from other methods:

- Semantic Scholar citation chasing: 1,071 unique records before cross-source
  deduplication.
- Citation-chasing raw links before within-route merging: 466 forward and
  1,003 backward.

Total records read by final deduplication:

- 2,319 rows.

## Deduplication

- Duplicate rows removed or marked: 484.
- Deduplicated records for title/abstract screening: 1,835.

## Source Routes After Deduplication

Deduplicated groups with each source route:

- arXiv: 763.
- Scopus: 126.
- Citation chasing: 1,064.

Common exclusive/combined routes in the title/abstract screening pool:

- Citation-only: 979.
- arXiv-only: 651.
- Scopus-only: 92.
- arXiv + citation: 79.
- arXiv + Scopus: 28.
- arXiv + Scopus + citation: 5.
- Scopus + citation: 1.

## Screening

- Title/abstract screening records: 1,835.
- Title/abstract included: 70.
- Title/abstract maybe: 95.
- Title/abstract excluded: 1,670.
  This includes 142 deterministic CI3 exclusions and 1,528 substantive
  calibration-batch exclusions.
- Title/abstract records still awaiting screening: 0.
- Records moving to full-text retrieval/screening: 165.
- Full texts sought: 165.
- Full texts retrieved: 163.
- Full texts not retrieved: 2.
- Full texts not retrieved but resolved from publisher abstract: 1.
- Reports not retrieved and not assessed for eligibility: 1.
- Full-text included: 95.
- Full-text excluded: 69.
- Full-text records still awaiting decision: 0.

## Included Corpus After Extraction

- search included records with extraction rows: 95.
- Architecture records for synthesis denominator: 85.
- Contextual/boundary records outside the architecture denominator: 10.
- Strict controlled-comparison architecture records: 56.
- Broad controlled-comparison candidates including external/non-memory
  baselines: 76.
- Architecture records with numeric protocol Q1-Q6 quality scores: 85.
- Architecture records below the 3.0/6 quality sensitivity threshold: 0.

## Notes

- These are internal search counts and supersede earlier March/April draft
  corpus counts for the rebuild workflow.
- Citation-chasing records remain separated from database-search records in
  source-route columns for PRISMA accounting.
- `screening/title-abstract-screening.tsv` is the canonical screening
  ledger for the next phase.
- The deterministic CI3 batch does not decide substantive persistence,
  software-engineering, evaluation, language, or publication-type criteria.
