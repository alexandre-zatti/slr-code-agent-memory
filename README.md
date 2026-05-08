# Knowledge Persistence Architectures for AI-Based Coding Agents

Replication package for a systematic literature review following PRISMA 2020 on knowledge persistence architectures for AI-based coding agents.
The package contains the protocol, search strategy, saved database exports, citation-chasing records, deduplication ledger, screening decisions, structured extraction data, synthesis tables, and PRISMA flow source.

**Author:** Alexandre Zatti  
**Affiliation:** Programa de Pos-Graduacao em Computacao Aplicada (PPGPCA), Universidade Federal da Fronteira Sul (UFFS)  
**License:** [CC-BY-4.0](LICENSE)  
**Version:** 1.0.0  
**Zenodo:** DOI pending.

## Summary

The review used Scopus, arXiv, and Semantic Scholar citation chasing.
The final arXiv cutoff was `submittedDate:[202301010000 TO 202604272359]`, and final Scopus branches used `PUBYEAR > 2022`.
The Scopus method is branch-split because the combined query returned HTTP 413 during validation.

| Quantity | Count |
| --- | ---: |
| arXiv raw rows | 1,118 |
| Scopus raw rows | 130 |
| Database raw rows | 1,248 |
| Citation-chasing unique records | 1,071 |
| Rows read by final deduplication | 2,319 |
| Duplicate rows removed or marked | 484 |
| Title/abstract screening records | 1,835 |
| Reports sought for retrieval | 165 |
| Retrieved full texts | 163 |
| Publisher-abstract-resolved records | 1 |
| Reports not retrieved and not assessed | 1 |
| Reports assessed for eligibility | 164 |
| Full-text included records | 95 |
| Full-text excluded records | 69 |

Synthesis denominators:

| Denominator | N | Use |
| --- | ---: | --- |
| Included studies | 95 | All full-text included records. |
| Architecture studies | 85 | Architecture taxonomy, mechanisms, quality, cost, adverse evidence, and synthesis. |
| Contextual/boundary studies | 10 | Contextual, benchmark, security, or boundary records reported separately. |
| Strict controlled-comparison studies | 56 | Same-system no-persistence or memory-ablation claims. |
| Broad controlled-comparison studies | 76 | Strict comparisons plus external or non-memory architecture baselines. |

## Repository Contents

```text
protocol/       Protocol, PRISMA checklist, and amendments
search/         Search strategy, execution logs, scripts, and saved exports
screening/      Criteria plus title/abstract and full-text decisions
extraction/     Extraction schema, compiled TSV, per-record JSON, and digests
analysis/       Validation scripts and generated synthesis tables
synthesis/      Synthesis matrix and PRISMA flow summary
references/     BibTeX entries for all 95 included records
```

Full-text PDFs are not redistributed in this package.
The package stores retrieval metadata, screening decisions, extraction data, factual digests, and citations instead.

## Key Files

- Search strategy: [`search/search-strategy.md`](search/search-strategy.md)
- arXiv rows: [`search/arxiv-query-chunk-results.tsv`](search/arxiv-query-chunk-results.tsv)
- Scopus branch strings: [`search/scopus-query-branches.tsv`](search/scopus-query-branches.tsv)
- Citation chasing records: [`search/results-citations.json`](search/results-citations.json)
- Deduplication ledger: [`search/dedup.tsv`](search/dedup.tsv)
- Title/abstract screening: [`screening/title-abstract-screening.tsv`](screening/title-abstract-screening.tsv)
- Full-text screening: [`screening/full-text-screening.tsv`](screening/full-text-screening.tsv)
- Included studies ledger: [`screening/included-studies.tsv`](screening/included-studies.tsv)
- Extraction TSV: [`extraction/extracted-data.tsv`](extraction/extracted-data.tsv)
- Extraction JSON files: [`extraction/json/`](extraction/json/)
- Factual digests: [`extraction/digests/`](extraction/digests/)
- Synthesis matrix: [`synthesis/synthesis-matrix.md`](synthesis/synthesis-matrix.md)
- PRISMA flow summary: [`synthesis/prisma-flow.md`](synthesis/prisma-flow.md)

## Reproducing Counts

The final PRISMA and synthesis counts should be reproduced from saved artifacts, not from live database calls.
Live arXiv, Scopus, or Semantic Scholar queries may return different counts after the execution date.

Recommended checks:

```bash
python analysis/recompute_counts.py
python analysis/audit_row_level_synthesis.py
python analysis/check_bibliography_coverage.py
```

Expected results:

- `recompute_counts.py`: 95 included, 85 architecture, 10 contextual/boundary.
- `audit_row_level_synthesis.py`: 35 checks, 0 warnings, 0 failures.
- `check_bibliography_coverage.py`: 95 present, 0 missing.

## Citation

The Zenodo DOI is pending.
After the archive is minted, cite the version-specific Zenodo DOI.
Until then, cite this repository snapshot as:

```bibtex
@misc{zatti2026slrreplication,
  author    = {Zatti, Alexandre},
  title     = {{Knowledge Persistence Architectures for AI-Based Coding Agents: Replication Package}},
  year      = {2026},
  version   = {1.0.0},
  publisher = {Zenodo},
  note      = {DOI pending}
}
```

## License

This work is licensed under [Creative Commons Attribution 4.0 International (CC-BY-4.0)](LICENSE).
Original publications referenced in `references/included-studies.bib` remain under their respective authors' copyrights and are not redistributed here.
