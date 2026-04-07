# Search Strategy

## Phase 0: Formal Strings

The search strings below are formalized before any search is executed and
guide all databases. They are the primary reproducibility artifact for the
search phase.

## Search Period
- **Temporal coverage:** 2023–2026
- **Execution date:** 2026-03-25

## Concepts and Terms

| Concept | Terms (OR) |
|---------|-----------|
| **AI agents for code** | "LLM agent" OR "AI coding agent" OR "software engineering agent" OR "autonomous coding" OR "code agent" OR "LLM-based software" OR "AI-assisted software" OR "coding assistant" OR "language agent" OR "code assistant" OR "agentic coding" OR "SWE agent" |
| **Memory/Persistence** | "memory" OR "knowledge persistence" OR "experience" OR "context management" OR "long-term memory" OR "episodic memory" OR "knowledge reuse" OR "continual learning" OR "experience replay" OR "memory-augmented" OR "persistent memory" OR "persistent context" OR "cross-task" |
| **Software engineering** | "software engineering" OR "software development" OR "code generation" OR "bug fix" OR "code repair" OR "repository" OR "software maintenance" OR "issue resolution" |

### Refinement Notes

The string set was refined through two iterations against a list of 19
known relevant systems and benchmarking against eight comparable
published reviews.

**First iteration:**
- Concept 1: replaced "AI developer" with "language agent" — "AI
  developer" brought noise from studies on developer productivity;
  "language agent" captures papers such as Repository Memory (Wang et
  al., 2025) that use this exact term.
- Concept 2: replaced "session" with "memory-augmented" — "session" is
  too generic; "memory-augmented" captures papers describing agents
  augmented with memory.
- Concept 2: removed stand-alone "knowledge base" — generated excessive
  noise in Scopus from articles on generic knowledge bases.

**Second iteration (systematic audit against eight comparable reviews,
16 known systems, and 10 alternative term formulations):**

- Concept 1: added "code assistant" — variant without "-ing" used by
  several recent systems
- Concept 1: added "agentic coding" — emerging term, published at
  TOSEM (2025), surveys and multiple 2025–2026 papers. +19 unique
  papers in arXiv
- Concept 1: added "SWE agent" — has become a category name
  (not only a specific tool). +12 unique papers in arXiv
- Concept 2: added "persistent memory" — more frequent than
  "knowledge persistence" in the literature
- Concept 2: added "persistent context" — exact phrase used by several
  recent systems
- Concept 2: added "cross-task" — directly signals cross-session
  knowledge transfer (central scope of the review)
- arXiv: corrected asymmetry with Scopus — 4 Concept-1 terms and 2
  Concept-2 terms were absent from the arXiv string without
  documented justification. Alignment recovered +53 papers
- arXiv: added title-field search (`ti:`) for key Concept-1 terms —
  papers such as SWE-Bench-CL and CTIM-Rover place agent terms only in
  the title, not in the abstract. Recovered +13 papers and 2
  additional seed papers

Terms evaluated and **not** added (with justification):
- "knowledge graph" (C2) — tested: +31 papers but precision ~7–13%
  (most about KGs in non-SE domains). Relevant papers with KG
  (Prometheus, RANGER) were already captured by "memory"
- "working memory" (C2) — zero delta in arXiv; subsumed by bare "memory"
- "self-evolving" (C2) — conceptual mismatch with C2 (persistence/memory)
- "developer agent" / "programming agent" (C1) — rarely used as
  primary terms in recent literature

### Generic Combined String
```
("LLM agent" OR "AI coding agent" OR "software engineering agent"
 OR "autonomous coding" OR "code agent" OR "LLM-based software"
 OR "AI-assisted software" OR "coding assistant" OR "language agent"
 OR "code assistant" OR "agentic coding" OR "SWE agent")
AND
("memory" OR "knowledge persistence" OR "experience"
 OR "context management" OR "long-term memory" OR "episodic memory"
 OR "knowledge reuse" OR "continual learning" OR "experience replay"
 OR "memory-augmented" OR "persistent memory" OR "persistent context"
 OR "cross-task")
AND
("software engineering" OR "software development" OR "code generation"
 OR "bug fix" OR "code repair" OR "repository"
 OR "software maintenance" OR "issue resolution")
```

---

## Rationale for a Two-Database Search Strategy

The two-database strategy (Scopus + arXiv) complemented by citation
chasing is empirically validated by Mourão et al. (2020, IST, 142
citations), who demonstrated that Scopus combined with snowballing
achieves recall comparable to searches across four or more databases.
Stradowski and Madeyski (2023, IST) — co-author of SEGRESS — published
a PRISMA 2020 review using Scopus as the only database.

---

## Search 1: Scopus

Primary source. Largest coverage of computer science venues.

```
TITLE-ABS-KEY(
  ("LLM agent" OR "AI coding agent" OR "software engineering agent"
   OR "autonomous coding" OR "code agent" OR "LLM-based software"
   OR "AI-assisted software" OR "coding assistant" OR "language agent"
   OR "code assistant" OR "agentic coding" OR "SWE agent")
  AND
  ("memory" OR "knowledge persistence" OR "experience"
   OR "context management" OR "long-term memory" OR "episodic memory"
   OR "knowledge reuse" OR "continual learning" OR "experience replay"
   OR "memory-augmented" OR "persistent memory" OR "persistent context"
   OR "cross-task")
  AND
  ("software engineering" OR "software development" OR "code generation"
   OR "bug fix" OR "code repair" OR "repository"
   OR "software maintenance" OR "issue resolution")
)
AND PUBYEAR > 2022
```

Raw API response: `raw/results-scopus.json`. BibTeX export:
`exports/scopus.bib`.

---

## IEEE Xplore — Rationale for Non-Inclusion

IEEE Xplore was not searched separately because Scopus fully indexes
IEEE proceedings and journals (ICSE, ASE, SANER, MSR, TSE, etc.). A
separate IEEE Xplore search would result predominantly in duplicates.
This decision is consistent with CS systematic review practice that
uses Scopus as the comprehensive database (Scopus covers >27,000
journals and conferences, including the full IEEE catalog).

---

## Search 2: arXiv

Recent preprints not yet indexed in Scopus. Executed via the arXiv REST
API with full pagination (`fetch_arxiv.py` in this directory).

```
(cat:cs.SE OR cat:cs.AI OR cat:cs.CL) AND
(abs:"LLM agent" OR abs:"AI coding agent"
 OR abs:"software engineering agent" OR abs:"autonomous coding"
 OR abs:"code agent" OR abs:"LLM-based software"
 OR abs:"AI-assisted software" OR abs:"coding assistant"
 OR abs:"language agent" OR abs:"code assistant"
 OR abs:"agentic coding" OR abs:"SWE agent"
 OR ti:"coding agent" OR ti:"code agent"
 OR ti:"software engineering agent" OR ti:"SWE agent") AND
(abs:"memory" OR abs:"knowledge persistence" OR abs:"experience"
 OR abs:"context management" OR abs:"long-term memory"
 OR abs:"episodic memory" OR abs:"knowledge reuse"
 OR abs:"continual learning" OR abs:"experience replay"
 OR abs:"memory-augmented" OR abs:"persistent memory"
 OR abs:"persistent context" OR abs:"cross-task")
```

Filtered to 2023–2026 via `fetch_arxiv.py --year-from 2023` and
converted to BibTeX via `convert_to_bib.py arxiv`.

**Notes on the arXiv string:**
- Concept 3 (Software Engineering) is covered by the category filter
  `cs.SE`, making duplicated terms in the `abs:` field unnecessary.
  Papers in `cs.AI` and `cs.CL` are filtered only by C1 AND C2 (without
  explicit SE filter), which increases recall but reduces precision to
  ~40–50%. Noise is handled at the screening stage.
- Four C1 terms include title-field search (`ti:`) in addition to
  abstract (`abs:`) to capture papers that use agent terms only in the
  title (e.g., SWE-Bench-CL, CTIM-Rover). The remaining C1 terms
  search only the abstract.
- Only exact phrases (quoted) to reduce noise.
- The arXiv API handles plurals automatically ("coding agent" =
  "coding agents") and hyphens as spaces ("LLM-agent" = "LLM agent").
- The arXiv API does not support a native year filter; filtering is
  done post-fetch via `fetch_arxiv.py --year-from 2023`.

Raw API response: `raw/results-arxiv.json`. BibTeX export:
`exports/arxiv.bib`.

---

## Search 3: Citation Chasing (PRISMA other method)

A separate method in the PRISMA diagram (not a database search).

### Seed Papers
1. Du (2026) — Survey of memory in AI agents (arXiv:2603.07670)
2. Joshi et al. (2025) — SWE-Bench-CL, continual learning benchmark
   (arXiv:2507.00014)
3. Wang et al. (2026) — CodeMEM, AST-guided memory (arXiv:2601.02868)
4. Deng et al. (2026) — MemCoder, commit-based memory (arXiv:2603.13258)
5. Wu et al. (2025) — GCC, git-inspired context (arXiv:2508.00031)
6. Wang et al. (2025) — Repository Memory, commit corpus + BM25
   (arXiv:2510.01003)
7. Lindenbauer et al. (2025) — CTIM-Rover, negative result with episodic
   memory (arXiv:2505.23422)

### Process
1. Insert the seven seed papers into the citation graph tool (Semantic
   Scholar API)
2. Collect forward citations (papers that cited the seed) and backward
   citations (references of the seed)
3. Export as BibTeX: `exports/citations.bib`

Raw API response: `raw/results-citations.json`.

---

## String Validation

Before executing the complete searches, each string was validated
against three criteria: (1) do the seed papers appear in the results;
(2) is the precision of a first-page sample reasonable; (3) is the
total volume manageable.

### Validation Results

**Scopus:**
- None of the seven seed papers appear — all are recent arXiv preprints
  not yet indexed in Scopus. Expected for an emerging field (2025–2026).
- Sample of first 25 results: low precision (~10–15% relevant). Most
  are articles about AI coding assistants in general, not knowledge
  persistence.
- Relevant papers captured: L2MAC (ICLR 2024 — memory for code
  generation), Experiential Co-Learning (ACL 2024 — experiential
  learning across agents)
- Conclusion: Scopus will yield low but complete coverage (for PRISMA
  completeness). The field is almost entirely composed of arXiv
  preprints from 2025–2026.

**arXiv (pre-refinement, via 50-result sample):**
- 4/7 seed papers found: CTIM-Rover, MemCoder, SWE-Bench-CL, GCC
- 3 seed papers not found: Du (2026 — generic AI survey, no "coding
  agent" term), CodeMEM (uses "system" without "agent"), Repository
  Memory (uses "language agents" — corrected by adding "language
  agent" to Concept 1)
- Additional known systems found: Subtask Memory, ToM-SWE, MemGovern,
  Prometheus, CMV, Spark — total of 10/19 known systems in just 48 results
- Estimated precision: ~40–50% (much higher than Scopus)

**Semantic Scholar (seed paper verification):**
- 6/7 seed papers confirmed with Semantic Scholar IDs; citation chasing
  is feasible for all seed papers

### Diagnosis: Why Does Scopus Return Few Relevant Results?

Three diagnostic searches were performed:

1. **Search by system names:** `TITLE("CodeMEM" OR "MemCoder" OR
   "SWE-Bench-CL" OR "CTIM-Rover" OR "MemGovern" OR "Repository Memory")`
   → zero results. None of the 19 known systems are indexed in Scopus.
2. **Broad search:** `TITLE-ABS-KEY("memory" AND "LLM" AND "software
   engineering") AND PUBYEAR > 2023` → ~22 results, mostly irrelevant.
   Two relevant findings not captured by the main query:
   - "Enhancing Contextual Memory in LLMs for SE via Ontology-based
     Inference" (Araya, CEUR 2025)
   - "Agents in SE: survey, landscape, and vision" (Wang, ASE journal,
     2025)
3. **Title search with agent + memory + code:** `TITLE("memory" AND
   "agent" AND ("code" OR "software")) AND PUBYEAR > 2023` → zero
   relevant results.

**Conclusion: coverage problem, not string problem.** The field of
knowledge persistence for coding agents is composed almost entirely of
arXiv preprints from 2025–2026. These papers have not yet completed the
conference publication pipeline (submission → review → acceptance →
Scopus indexing), which typically takes 6–12 months. This is normal for
rapidly evolving ML/SE subfields — the same pattern occurred with RAG,
SWE-bench, and coding agents in general.

**Implications for the search strategy:**
- The strings are adequate — low Scopus yield reflects the field's
  publication maturity, not a string flaw
- Scopus is executed for PRISMA completeness, even though expected
  yield is low (<10 directly relevant articles)
- arXiv is the primary source for this field (~40–50% precision)
- Citation chasing (Search 3) is the most important method for
  completeness, capturing papers that do not use agent terms in the
  abstract (CodeMEM, Du survey) or that use variant terminology
- This field characteristic is documented as a limitation in the
  manuscript and reinforces the research narrative: the field is so new
  and fragmented that no systematic comparison exists yet

### Post-Refinement Validation Results

**arXiv (full pagination via `fetch_arxiv.py`):**
- 6/7 seed papers found: MemCoder, GCC, Repository Memory, Du survey,
  SWE-Bench-CL, CTIM-Rover (improvement from 4/7 to 6/7 after refinement)
- 1 seed paper not found: CodeMEM — abstract does not contain any C1
  agent/system term. Captured via citation chasing (Search 3)
- 14/22 known systems found (improvement from 12/22 before refinement)
- Total count: 973 results (960 raw, 955 after year filter ≥2023)
- Increase from 876 → 973 (+11.1%) relative to the previous string
- Estimated precision remained at ~40–50%

**arXiv API behavior (verified 2026-03-25):**
- Plurals handled automatically: "coding agent" = "coding agents"
- Hyphens treated as spaces: "LLM-agent" = "LLM agent"
- Terms subsumed in arXiv (zero delta): "persistent memory",
  "persistent context", "cross-task", "working memory" — all subsumed
  by bare "memory". Retained for Scopus coverage and defensibility

**Scopus (hardened string):**
- ≥25 results (mostly noise, consistent with the diagnosis above)
- String executed without syntax errors

---

## Result Log

### Databases (PRISMA: "Records identified from databases")

| Source | Date | Results | BibTeX export |
|--------|------|---------|---------------|
| Scopus | 2026-03-25 | 39 | `exports/scopus.bib` |
| arXiv | 2026-03-25 | 968 (973 raw, 5 before 2023) | `exports/arxiv.bib` |
| **Database subtotal** | — | **1,007** | — |

### Other Methods (PRISMA: "Records identified from other methods")

| Source | Date | Results | BibTeX export |
|--------|------|---------|---------------|
| Citation chasing (forward) | 2026-03-25 | 10 (8 unique) | `exports/citations.bib` |
| Citation chasing (backward) | 2026-03-25 | 202 (178 unique) | (combined above) |
| **Other-methods subtotal** | — | **186 unique** | — |

### Consolidation

| Stage | Count |
|-------|-------|
| Raw total (databases + other methods) | 1,193 (1,007 databases + 186 citations) |
| Manual addition (seed not captured by strings) | +1 (CodeMEM) |
| **Raw identified** | **1,194** |
| Duplicates removed | 83 |
| **Total after deduplication** | **1,111** |

---

## PRISMA 2020 Mapping — Flow Diagram Numbers

Reference: Page et al. (2021), Figure 1.

### Identification

| PRISMA box | Count | Notes |
|------------|-------|-------|
| Records identified from databases (Scopus) | 39 | TITLE-ABS-KEY, PUBYEAR > 2022 |
| Records identified from databases (arXiv) | 968 | cs.SE/AI/CL, ≥2023 |
| **Database subtotal** | **1,007** | |
| Records identified from other methods (forward citations) | 10 | 7 seed papers, Semantic Scholar |
| Records identified from other methods (backward citations) | 202 | 7 seed papers, Semantic Scholar |
| **Other-methods subtotal** | **186** (unique) | 26 duplicates between forward/backward and between seeds |
| Manual addition | 1 | CodeMEM |

### Pre-screening

| PRISMA box | Count |
|------------|-------|
| Records removed before screening: duplicates | 83 |
| Records removed before screening: other reasons | 0 |
| **Records screened** | **1,111** |

### Screening

| PRISMA box | Count |
|------------|-------|
| Records excluded (title/abstract) | 1,060 |
| Reports sought for retrieval | 51 |
| Reports not retrieved | 0 |
| Reports assessed for eligibility | 51 |
| Reports excluded (full text), with reasons | 23 (EC2: 12, IC1/EC1: 11) |
| **Studies included in review** | **28** |

---

## PRISMA-S Compliance (Rethlefsen et al., 2021)

16-item checklist for reporting the search strategy.

| # | Item | Description |
|---|------|-------------|
| 1 | Database names | Scopus, arXiv |
| 2 | Platform/interface | Scopus via Elsevier API; arXiv via REST API (`fetch_arxiv.py`) |
| 3 | Study registers | No study registers (e.g., PROSPERO) consulted |
| 4 | Online resources | No organizational websites consulted separately |
| 5 | Citation chasing | Forward + backward via Semantic Scholar API from seven seed papers |
| 6 | Contact with authors | No authors contacted |
| 7 | Other methods | None beyond those described |
| 8 | Full strategies | Exact strings per database documented above (Scopus §Search 1, arXiv §Search 2) |
| 9 | Limits and restrictions | Scopus: `PUBYEAR > 2022`; arXiv: categories `cs.SE`, `cs.AI`, `cs.CL` + post-fetch filter `--year-from 2023`; languages: English and Portuguese |
| 10 | Strategy development | Concept mapping (3 blocks) → string construction with OR/AND terms → validation against 7 seed papers → iterative refinement (two iterations: first for term substitution; second for systematic audit against 8 comparable reviews and 16 known systems, adding emerging terms, correcting arXiv/Scopus asymmetry, and adding title-field search) |
| 11 | Peer review | Search strategy reviewed by the advisor |
| 12 | Record management | BibTeX files versioned in git (`exports/*.bib`) |
| 13 | Total records | 1,194 raw; 1,111 after deduplication |
| 14 | Deduplication | Automated matching by DOI/title + manual verification; duplicates recorded per source |
| 15 | Automation tools | Scopus via API; arXiv via Python script (`fetch_arxiv.py`); citation chasing via Semantic Scholar API |
| 16 | Updates | Search to be re-executed before manuscript submission if more than 3 months have elapsed since the initial execution |
