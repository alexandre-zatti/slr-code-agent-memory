# Search Strategy

Status: canonical search documentation for the current corpus.

## Scope

- Sources: Scopus, arXiv, Semantic Scholar citation chasing, and documented
  manual full-text retrieval.
- Search date: 2026-04-28.
- arXiv cutoff: `submittedDate:[202301010000 TO 202604272359]`.
- arXiv categories: `cs.SE OR cs.AI OR cs.CL OR cs.LG`.
- Scopus year clause: `PUBYEAR > 2022`.
- Language eligibility: English at screening.

## Concept Blocks

The final strategy used three logical families.

### Family A - Explicit Coding-Agent Memory

Purpose: recover records that explicitly use coding-agent, code-agent,
programming-agent, software-engineering-agent, SWE-agent, or coding-assistant
wording plus memory, experience, context, or self-evolution wording.

Logical shape:

```text
(C1 explicit coding-agent terms)
AND (C2 broad memory/persistence terms)
AND date/category limits
```

### Family B - Generic LLM-Agent Memory With SE Evidence

Purpose: recover records using generic LLM-agent, language-model-agent, or
language-agent wording, but only when title or abstract also contains
software-engineering or coding evidence.

Logical shape:

```text
(C1 generic LLM/language-agent terms)
AND (C2 broad memory/persistence terms)
AND (C3 software-engineering/coding evidence terms)
AND date/category limits
```

### Family C - Strong Memory With SE Evidence

Purpose: recover records that do not use explicit agent wording but do use
strong memory, experience-reuse, context-reuse, case-base, self-evolution, or
memory-management terminology plus explicit software-engineering or coding
evidence.

Logical shape:

```text
(C2 strong memory/persistence terms)
AND (C3 software-engineering/coding evidence terms)
AND date/category limits
```

## arXiv Execution

Canonical files:

| Artifact | Path |
| --- | --- |
| Query chunks | `search/arxiv-query-chunks.tsv` |
| Chunk metadata | `search/arxiv-query-chunks-metadata.tsv` |
| Chunk counts | `search/arxiv-query-chunk-counts.tsv` |
| Saved result rows | `search/arxiv-query-chunk-results.tsv` |
| Continuation rows | `search/arxiv-query-chunk-results-continuation-600.tsv` |
| Page metadata | `search/arxiv-query-chunk-results-pages.tsv` |
| Coverage report | `search/arxiv-query-chunk-results-coverage.tsv` |
| Seed recall | `search/arxiv-seed-recall.tsv` |
| Execution log | `search/final-arxiv-execution-log.md` |

Final arXiv execution produced 1,118 raw rows across 24 chunks.
Coverage validation recorded all chunks as complete and required seed recall
failures as zero.

## Scopus Execution

Scopus used branch-split execution because the combined query returned HTTP
413 during API validation.
The branch strings are archived in `search/scopus-query-branches.tsv`.

| Branch | Raw rows | TSV | Raw JSON |
| --- | ---: | --- | --- |
| `family_a_coding_agent_memory` | 53 | `search/scopus-results-family-a-coding-agent-memory.tsv` | `search/scopus-results-family-a-coding-agent-memory.json` |
| `family_b_generic_agent_memory_se` | 32 | `search/scopus-results-family-b-generic-agent-memory-se.tsv` | `search/scopus-results-family-b-generic-agent-memory-se.json` |
| `family_c_strong_memory_se` | 45 | `search/scopus-results-family-c-strong-memory-se.tsv` | `search/scopus-results-family-c-strong-memory-se.json` |

Family C uses a Scopus-specific narrowed translation to avoid excessive
false-positive burden while preserving the strong-memory plus
software-engineering evidence intent.
The final Scopus execution log is `search/final-scopus-execution-log.md`.

## Citation Chasing

Citation chasing uses Semantic Scholar routes recorded in:

- `search/citation-chasing-seeds.tsv`
- `search/results-citations.json`
- `search/results-citations-metadata.tsv`
- `search/results-citations-requests.tsv`

Citation records were deduplicated with database results before screening.

## Deduplication And Screening Inputs

Canonical deduplication outputs:

- `search/dedup.tsv`
- `search/dedup-database.tsv`

Canonical screening ledgers:

- `screening/title-abstract-screening.tsv`
- `screening/full-text-screening.tsv`
- `screening/included-studies.tsv`

## Full Text Retrieval

Canonical full-text retrieval artifacts:

- `search/full-text-manual-urls.tsv`
- `search/full-text-retrieval.tsv`
- `search/full-text-retrieval-status.tsv`
- `search/full-text-retrieval-report.md`
- `search/full-text-retrieval-report.json`
- `search/full-texts/text/`

PDFs are not redistributed in the repository.
PDF-derived text is retained for private verification and replication-package
preparation.

## Final Counts

The current corpus contains:

- 95 included studies.
- 85 architecture studies.
- 10 contextual/boundary studies.
- 56 strict controlled-comparison studies.
- 76 broad controlled-comparison studies.

Counts are verified from `extraction/extracted-data.tsv` by:

```bash
python analysis/recompute_counts.py
```
