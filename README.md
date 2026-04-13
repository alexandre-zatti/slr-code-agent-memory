# Knowledge Persistence Architectures for AI-Based Coding Agents — SLR Replication Package

[![DOI](https://zenodo.org/badge/1204331593.svg)](https://doi.org/10.5281/zenodo.19463131)

Replication package for a systematic literature review (PRISMA 2020) on
knowledge persistence architectures for AI-based coding agents. This
repository contains the protocol, search strategy, raw search results,
screening decisions, structured extraction data (37 fields × 28 included
studies), the synthesis matrix, and the PRISMA flow diagram source.

**Author:** Alexandre Zatti
**Affiliation:** Programa de Pós-Graduação em Computação Aplicada (PPGPCA),
Universidade Federal da Fronteira Sul (UFFS)
**License:** [CC-BY-4.0](LICENSE)
**Archived on Zenodo:** [10.5281/zenodo.19463131](https://doi.org/10.5281/zenodo.19463131)

---

## Abstract

**Context.** Coding agents based on Large Language Models (LLMs) suffer
from knowledge volatility across sessions: with each new task, the agent
loses the context accumulated in previous resolutions. Several
persistence architectures have been proposed to mitigate this
limitation, but the field remains fragmented, without systematic
comparison between alternatives or cross-cutting cost analysis.

**Objective.** Map the literature on knowledge persistence in AI-based
coding agents and answer five secondary questions covering taxonomy,
evaluation, performance, cost, and architectural complexity.

**Method.** Systematic review conducted according to PRISMA 2020.
Searches in Scopus and arXiv, complemented by citation chasing via
Semantic Scholar, identified 1,194 records published between 2023 and
March 2026. After duplicate removal and screening by title, abstract,
and full text, 28 studies were included for structured extraction of 37
fields.

**Results.** Experience banks account for 46% of primary studies, with
the LLM itself acting as read/write controller in 54% of cases and
hybrid temporal scope in 58%. The 19 studies with controlled comparisons
report universal gains over the memory-less baseline, with a median of
6.8 percentage points on SWE-bench Verified and a range of +2.2 to
+39.0 pp. Despite these gains, 43% of studies omit cost data, 32%
document memory-induced degradation scenarios, and none compare three
or more architectures on the same benchmark with the same model.

**Conclusion.** The absence of head-to-head comparisons and the
underreporting of cost data limit both architectural choice and
practical evaluation. These findings motivate a controlled empirical
comparative study as the next stage of this research.

**Keywords:** systematic review; coding agents; knowledge persistence;
memory for agents; cost-efficiency.

---

## Research Questions

**Main RQ:** How does the existing literature address knowledge
persistence in AI-based coding agents, and what empirical evidence
exists regarding the effectiveness and cost-efficiency of different
persistence architectures?

**Secondary questions:**

- **SQ1 (Taxonomy):** Which knowledge persistence architectures have
  been proposed, and how are they classified by temporal scope,
  representational substrate, and control policy?
- **SQ2 (Evaluation):** Which evaluation methods and benchmarks are
  used, and how comparable are the reported results?
- **SQ3 (Performance):** Which performance results are reported, and
  what is the magnitude of gains relative to baselines without
  persistence?
- **SQ4 (Cost):** Which cost and efficiency metrics are reported, and
  what is the relationship between computational cost and
  effectiveness?
- **SQ5 (Complexity-Effectiveness):** What evidence exists on the
  relationship between architectural complexity and effectiveness,
  including memory-induced degradation cases?

---

## PRISMA Flow Summary

| Stage | Count |
|-------|-------|
| Records identified (Scopus + arXiv + citations + manual) | 1,194 |
| Duplicates removed | 83 |
| Records screened (title/abstract) | 1,111 |
| Records excluded at title/abstract | 1,060 |
| Reports assessed (full text) | 51 |
| Reports excluded at full text (EC2: 12, IC1/EC1: 11) | 23 |
| **Studies included in review** | **28** |

Detailed flow diagram source: [`synthesis/prisma-flow-diagram.tex`](synthesis/prisma-flow-diagram.tex).

---

## Repository Contents

```
protocol/                 Final protocol (v1.0) + PRISMA 2020 checklist
search/                   Search strategy, scripts, raw exports
    search-strategy.md    Formal strings, PRISMA-S compliance, validation
    fetch_arxiv.py        arXiv API pagination script (stdlib only)
    fetch_scopus.py       Scopus API pagination script (stdlib only)
    convert_to_bib.py     JSON → BibTeX converter
    raw/                  Raw API responses (Scopus, arXiv, citations)
    exports/              BibTeX exports per source
screening/                Screening criteria and decisions
    criteria.md           Inclusion/exclusion criteria (v2.0)
    title-abstract.tsv    1,111 title/abstract screening decisions
    full-text.tsv         51 full-text screening decisions
extraction/               Data extraction artifacts
    extraction-form.md    37-field extraction schema
    data.tsv              Compiled extraction data (28 × 37)
    per-paper/            Per-paper JSON files (28 files)
synthesis/                Synthesis matrix and PRISMA diagram
    synthesis-matrix.md   Thematic synthesis by SQ1-SQ5
    prisma-flow-diagram.tex   Standalone TikZ source
references/               Included studies bibliography
    included-studies.bib  BibTeX of all 28 included studies
```

---

## How to Reproduce

### 1. Re-execute the arXiv search

```bash
cd search
python fetch_arxiv.py --year-from 2023 --output raw/results-arxiv.json
python convert_to_bib.py arxiv raw/results-arxiv.json exports/arxiv.bib
```

The scripts use only the Python standard library. The arXiv API is
public and rate-limited at ~1 request every 3 seconds. Expect ~1,000
records with the default query (exact count depends on the current
index).

### 2. Re-execute the Scopus search

```bash
cd search
SCOPUS_API_KEY=your_key python fetch_scopus.py --output raw/results-scopus.json
python convert_to_bib.py scopus raw/results-scopus.json exports/scopus.bib
```

Scopus requires an API key from the
[Elsevier Developer Portal](https://dev.elsevier.com/). Institutional
access (e.g., via CAPES in Brazil) is typically required for full
abstract content. The default query in `fetch_scopus.py` is the exact
string documented in
[`search/search-strategy.md`](search/search-strategy.md) under
*Search 1: Scopus*. The original raw response is in
[`search/raw/results-scopus.json`](search/raw/results-scopus.json).

### 3. Verify screening decisions

All 1,111 title/abstract decisions and 51 full-text decisions are in
[`screening/title-abstract.tsv`](screening/title-abstract.tsv) and
[`screening/full-text.tsv`](screening/full-text.tsv), with one decision
per row (include/exclude/maybe + criterion code + notes). Criteria are
defined in [`screening/criteria.md`](screening/criteria.md).

### 4. Inspect extracted data

Per-paper structured data is in
[`extraction/per-paper/`](extraction/per-paper/) (28 JSON files, one per
included study). The compiled flat dataset is
[`extraction/data.tsv`](extraction/data.tsv) (28 × 37). The schema, all
enum values, and the missing-data convention (NR/NA) are in
[`extraction/extraction-form.md`](extraction/extraction-form.md).

### 5. Build the PRISMA flow diagram

```bash
cd synthesis
pdflatex prisma-flow-diagram.tex
```

Produces a standalone PDF with the flow diagram from Page et al. (2021),
populated with the counts above.

---

## Citation

```bibtex
@misc{zatti2026slr,
  author    = {Zatti, Alexandre},
  title     = {{Knowledge Persistence Architectures for AI-Based
                Coding Agents: A Systematic Literature Review
                Replication Package}},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.19463131},
  url       = {https://doi.org/10.5281/zenodo.19463131},
}
```

The DOI above is the Zenodo *concept DOI* and always resolves to the
latest released version. To cite a specific release, use the
version-specific DOI shown on the
[Zenodo record page](https://doi.org/10.5281/zenodo.19463131)
(for example, `10.5281/zenodo.19463132` for v1.0.0).

---

## License

This work is licensed under
[Creative Commons Attribution 4.0 International (CC-BY-4.0)](LICENSE).
Original publications referenced in `references/included-studies.bib`
remain under their respective authors' copyrights and are not
redistributed here.
