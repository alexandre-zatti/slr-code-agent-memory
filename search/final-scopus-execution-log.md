# Search Final Scopus Execution Log

Date: 2026-04-28

Status: final Scopus branch exports completed.

## Query Scope

- Final method: branch-split execution.
- Combined query status: not used for final export because API validation
  returned HTTP 413.
- Year condition: `PUBYEAR > 2022`.
- Branch strings: `search/scopus-query-branches.tsv`.

## Execution

Exporter:

```text
search/fetch_scopus_branches.py
```

Settings:

- Page size: 25 records.
- Inter-page delay: 2 seconds.
- API route: Elsevier Scopus Search API.

The earlier attempt to fetch all branch rows with `count=200` returned HTTP
400, while `count=25` succeeded.
The final exporter therefore paginated at 25 records per request.

## Branch Exports

| Branch | Reported total | Fetched | Pages | TSV | Raw JSON |
| --- | ---: | ---: | ---: | --- | --- |
| `family_a_coding_agent_memory` | 53 | 53 | 3 | `search/scopus-results-family-a-coding-agent-memory.tsv` | `search/scopus-results-family-a-coding-agent-memory.json` |
| `family_b_generic_agent_memory_se` | 32 | 32 | 2 | `search/scopus-results-family-b-generic-agent-memory-se.tsv` | `search/scopus-results-family-b-generic-agent-memory-se.json` |
| `family_c_strong_memory_se` | 45 | 45 | 2 | `search/scopus-results-family-c-strong-memory-se.tsv` | `search/scopus-results-family-c-strong-memory-se.json` |

Metadata files:

- `search/scopus-results-family-a-coding-agent-memory-metadata.tsv`.
- `search/scopus-results-family-b-generic-agent-memory-se-metadata.tsv`.
- `search/scopus-results-family-c-strong-memory-se-metadata.tsv`.

## Validation

- All branch totals equal fetched entry counts.
- Raw Scopus rows before cross-source deduplication: 130.
- Branch exports remain separate for reproducibility.
- Deduplication across Scopus branches and against arXiv is still pending.
