# Search Final arXiv Execution Log

Date: 2026-04-28

Status: final arXiv export completed from saved API results.

## Query Scope

- Cutoff: `submittedDate:[202301010000 TO 202604272359]`.
- Categories: `cs.SE OR cs.AI OR cs.CL OR cs.LG`.
- Final chunk file: `search/arxiv-query-chunks.tsv`.
- Chunk count: 24.
- Page size: `--max-results 100`.

## Execution

First attempt:

- Command family: arXiv chunk export helper.
- Output target: `search/arxiv-query-chunk-results.tsv`.
- Rate limit: 300 seconds.
- Retry policy: `--retries 2 --stop-on-429`.
- Completed all `family_a` and `family_b` chunks.
- Outcome: stopped on HTTP 429 before `family_c_strong_memory_se__chunk01`.
- Quarantined partial files:
  `search/partial-runs/2026-04-28-arxiv-final-300s-429/`.

Continuation:

- Output target:
  `search/arxiv-query-chunk-results-continuation-600.tsv`.
- Rate limit: 600 seconds.
- Remaining chunks:
  `family_c_strong_memory_se__chunk01` through
  `family_c_strong_memory_se__chunk06`.
- Outcome: completed without additional HTTP 429.

Merged canonical artifacts:

- `search/arxiv-query-chunk-results.tsv`.
- `search/arxiv-query-chunk-results-pages.tsv`.
- `search/arxiv-query-chunk-results-metadata.tsv`.
- `search/arxiv-query-chunk-results-coverage.tsv`.

## Validation

- Coverage validation: all 24 chunks complete.
- Page metadata rows: 30.
- Raw result rows: 1,118.
- Unique arXiv IDs before cross-source deduplication: 763.
- Family raw rows:
  - `family_a_coding_agent_memory`: 349.
  - `family_b_generic_agent_memory_se`: 251.
  - `family_c_strong_memory_se`: 518.
- Fetched entries sum: 1,118.
- Total-result sum by chunk: 1,118.
- Final saved-result seed recall:
  `search/arxiv-seed-recall.tsv`.
- Required seed rows: 35.
- Required seed-recall failures: 0.

## Notes

- The final live fetch returned 1,118 raw rows, while the earlier count-only
  final dry run summed to 1,109.
  The saved final export, not the earlier count-only probe, is the auditable
  arXiv database-search record.
- The 300-second lower-start policy reduced initial delay and correctly
  stopped on HTTP 429.
  The 600-second continuation completed the remaining `family_c` chunks.
