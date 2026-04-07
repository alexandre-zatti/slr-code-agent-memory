# Systematic Literature Review Protocol

## 1. Administrative Information

- **Title:** Knowledge Persistence Architectures for AI-Based Coding Agents:
  A Systematic Literature Review
- **Authors:** Alexandre Zatti, Samuel Feitosa
- **Affiliation:** Programa de Pós-Graduação em Computação Aplicada (PPGPCA),
  Universidade Federal da Fronteira Sul (UFFS)
- **Protocol date:** March 2026
- **Version:** 1.0
- **Methodological framework:** Kitchenham and Charters (2007), with updates
  from Kitchenham and Brereton (2013)
- **Reporting guideline:** SEGRESS (Kitchenham, Madeyski, and Budgen, 2023)
  — adaptation of PRISMA 2020 for secondary studies in software engineering
- **Reporting checklist:** PRISMA 2020 (Page et al., 2021) — 27 items

## 2. Research Questions

PICo framework:
- **P**opulation: AI-based coding agents with mechanisms for knowledge
  persistence across sessions
- **I**nterest: Persistence architectures, their effectiveness and
  cost-efficiency
- **Co**ntext: Empirical evaluations, benchmarks, and tool/framework
  proposals

### Main Research Question (RQ)
> How does the existing literature address knowledge persistence in
> AI-based coding agents, and what empirical evidence exists regarding the
> effectiveness and cost-efficiency of different persistence architectures?

### Secondary Research Questions
- **SQ1 (Taxonomy):** Which knowledge persistence architectures have been
  proposed for coding agents, and how are they classified with respect to
  temporal scope, representational substrate, and control policy?
- **SQ2 (Evaluation):** Which evaluation methods and benchmarks are used to
  assess persistence mechanisms, and how comparable are the reported
  results?
- **SQ3 (Performance):** Which performance results are reported, and what
  is the magnitude of gains relative to baselines without persistence?
- **SQ4 (Cost):** Which cost and efficiency metrics are reported, and what
  is the relationship between computational cost and effectiveness?
- **SQ5 (Complexity-Effectiveness):** What evidence exists regarding the
  relationship between architectural complexity and effectiveness,
  including memory-induced degradation cases?

## 3. Eligibility Criteria

### Inclusion Criteria
- **IC1:** Proposes or evaluates a mechanism to persist knowledge or
  experience across sessions in AI-based coding agents
- **IC2:** Reports empirical results (experiment, benchmark, case study)
  OR proposes a tool/framework with systematic evaluation
- **IC3:** Published between 2023 and 2026
- **IC4:** Written in English or Portuguese
- **IC5:** Peer-reviewed publication (conference, journal) OR preprint
  with identifiable authors/institutions

### Exclusion Criteria
- **EC1:** Addresses only RAG or generic context retrieval without
  cross-session persistence
- **EC2:** Addresses only natural language tasks, not software development
- **EC3:** No evaluation beyond anecdotal examples
- **EC4:** Tutorial, editorial, or position paper without technical
  contribution
- **EC5:** Duplicate version or superseded by a later version from the
  same authors

### Application Guide
- IC1 requires an explicit component for storing and reusing knowledge
  across sessions or sequential tasks. Systems that only retrieve context
  within a single session (generic RAG) do not qualify.
- IC3 reflects the field's emergence in 2025, with a safety margin back to
  2023 to capture precursors (e.g., MemGPT).
- EC1 is the main precision filter: it separates cross-session persistence
  (in scope) from intra-session retrieval (out of scope).

The complete operationalization of these criteria, including decision
flowchart, borderline cases, and detailed guide for IC1, is available in
`screening/criteria.md`.

## 4. Information Sources

Searches are performed in academic databases that support reproducible
Boolean search with exact counts, ensuring PRISMA 2020 compliance.

### Databases (Boolean search via API)

| # | Database | Access | Coverage |
|---|----------|--------|----------|
| 1 | **Scopus** | Elsevier API | Largest CS coverage; indexes journals broadly |
| 2 | **arXiv** | arXiv public API with pagination | Recent preprints in cs.SE, cs.AI, cs.CL |

### Rationale for a Two-Database Search Strategy

The two-database strategy (Scopus + arXiv) complemented by citation
chasing is empirically validated by Mourão et al. (2020), who demonstrated
that Scopus combined with snowballing achieves recall comparable to
searches across four or more databases for software engineering systematic
reviews. Additionally, Stradowski and Madeyski (2023) — co-author of
SEGRESS — published a PRISMA 2020 review in *Information and Software
Technology* using only Scopus as a database.

### IEEE Xplore — Rationale for Non-Inclusion

Scopus fully indexes IEEE proceedings and journals (ICSE, ASE, SANER,
MSR, TSE, etc.). A separate search in IEEE Xplore would result
predominantly in duplicates.

### Other Methods (PRISMA Item 7)

| # | Method | Tool | Description |
|---|--------|------|-------------|
| 3 | **Citation chasing** | Semantic Scholar API | Forward + backward citations from seed papers |

### Seed Papers for Citation Chasing

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

## 5. Search Strategy

### Phase 0: String Definition and Validation (before any search)
Search strings are formalized first and guide all searches across all
databases. Validation is performed by checking whether seed papers appear
in the results.

### Concepts and Terms

| Concept | Terms (OR) |
|---------|-----------|
| **AI agents for code** | "LLM agent" OR "AI coding agent" OR "software engineering agent" OR "autonomous coding" OR "code agent" OR "LLM-based software" OR "AI-assisted software" OR "coding assistant" OR "language agent" OR "code assistant" OR "agentic coding" OR "SWE agent" |
| **Memory/Persistence** | "memory" OR "knowledge persistence" OR "experience" OR "context management" OR "long-term memory" OR "episodic memory" OR "knowledge reuse" OR "continual learning" OR "experience replay" OR "memory-augmented" OR "persistent memory" OR "persistent context" OR "cross-task" |
| **Software engineering** | "software engineering" OR "software development" OR "code generation" OR "bug fix" OR "code repair" OR "repository" OR "software maintenance" OR "issue resolution" |

### Combined String
```
(Concept1) AND (Concept2) AND (Concept3)
```

### Execution per Database
1. **Scopus:** string adapted to TITLE-ABS-KEY syntax + PUBYEAR > 2022 filter
2. **arXiv:** string adapted to arXiv syntax with cs.SE/cs.AI/cs.CL category
   filter
3. Database-specific adaptations documented in `search/search-strategy.md`

### Period
2023–2026

## 6. Study Selection Process

All records identified in the searches are exported as BibTeX and
consolidated into a single dataset for centralized screening.

### Deduplication
- Records from all sources are deduplicated before screening
- Duplicate counts recorded per source

### Phase 1: Title and Abstract Screening
- The researcher applies the IC/EC criteria to each record
- Decision: include, exclude, or maybe
- Records classified as "maybe" advance to full-text screening
- Exclusion reason recorded by criterion
- Logged in `screening/title-abstract.tsv`

### Phase 2: Full-Text Screening
- Full texts accessed via DOI and institutional access
- Criteria reapplied with complete information
- Logged in `screening/full-text.tsv`

### Resolution of Borderline Cases
- Discussion with advisor for ambiguous cases
- Justification recorded

### Screening Reliability
- **Primary reviewer:** the student (all records)
- **Limitation:** single primary reviewer, mitigated by systematic
  calibration of criteria against five comparable published reviews and
  by pilot-tested decision flowchart, reported in the methods section of
  the manuscript

## 7. Data Extraction

Fields extracted from each included paper (complete template in
`extraction/extraction-form.md`):

### Metadata
- ID, authors, year, venue, publication type

### Persistence Architecture
- Architecture type (text notes, experience bank, AST-guided, knowledge
  graph, OS-paging, git-metaphor, hybrid)
- Temporal scope, representational substrate, control policy (Du 2026
  taxonomy)
- Storage format, retrieval method, granularity, cross-agent sharing

### Agent and Model
- Agent framework, LLM used, autonomy level, open-source status

### Evaluation
- Evaluation method, benchmarks, performance metrics, continual learning
  metrics, compared baseline

### Cost and Efficiency
- Input/output tokens per task, memory size over time, cost per task,
  token reduction, cost data reporting level

### Results
- Main result, performance vs. baseline, cost vs. baseline, negative
  result

### Quality and Limitations
- Quality score (0–6), limitations, validity threats, addressed gaps

### Extraction Procedure
1. Researcher reads the full PDF and populates each field in the
   structured form
2. Programmatic validation of enum-typed fields
3. Cross-field consistency checks (cost reporting, NA conventions,
   continual-learning metrics)
4. Compilation of per-paper JSON files into `extraction/data.tsv`

## 8. Quality Assessment / Risk of Bias

Checklist adapted from Kitchenham (2007) guidelines for software
engineering systematic reviews:

1. Are the research objectives clearly defined?
2. Is the evaluation method adequate to the objectives?
3. Are threats to validity discussed?
4. Are the results based on empirical data (not just examples)?
5. Is the study context sufficiently described for replication?
6. Are the evaluation metrics clearly defined?

Scale: 0 (does not meet), 0.5 (partially), 1 (meets). Maximum score: 6.

## 9. Synthesis Methods

### Narrative/Thematic Synthesis
Given the expected heterogeneity of the studies (different architectures,
benchmarks, models, metrics), the synthesis is narrative and thematically
organized:

1. **By persistence architecture (SQ1)** — taxonomy of proposed
   approaches, classified according to temporal scope, substrate, and
   control policy
2. **By evaluation method and benchmark (SQ2)** — how comparable results
   are across studies
3. **By performance results (SQ3)** — reported gains vs. baselines
   without persistence
4. **By cost and efficiency (SQ4)** — Pareto frontier between accuracy
   and cost
5. **Complexity-effectiveness relationship (SQ5)** — evidence of
   "simple beats complex" and memory-induced degradation cases

### Meta-analysis
Likely infeasible due to heterogeneity. If sufficiently homogeneous
studies are found, meta-analysis for specific subgroups may be
considered.

### Sensitivity Analyses and Bias (PRISMA Items 13d–13f)

**Sensitivity analysis (Item 13d):**
The synthesis is re-executed excluding: (a) preprints not yet
peer-reviewed, (b) studies with quality score below 3/6. Report whether
main conclusions change in each scenario.

**Publication bias (Item 13e):**
Formal publication bias assessment (e.g., funnel plot) is not applicable
— the synthesis is narrative, not meta-analytic. The predominance of
preprints in the corpus is acknowledged as a potential source of bias
and discussed in the limitations section of the manuscript.

**Certainty of evidence (Item 13f):**
GRADE assessment is not applicable for narrative synthesis. A qualitative
per-finding confidence assessment is used: high (multiple studies of
quality ≥4/6 converge), moderate (few studies or variable quality), low
(finding based on a single study or low-quality studies). Classification
reported in the results section of the manuscript.

## 10. Timeline

| Period | Phase |
|--------|-------|
| Mar–Apr 2026 | Protocol + search string validation |
| May 2026 | Execution of searches in all databases + citation chasing |
| May–Jun 2026 | Screening (title/abstract + full text) |
| Jul–Aug 2026 | Data extraction + synthesis |
| Sep 2026 | Manuscript writing |
