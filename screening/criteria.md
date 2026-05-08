# Screening Criteria

Version 2.0 — updated after the criteria stress test (2026-03-26).
Changes recorded in `protocol/amendments.md`.

---

## Inclusion Criteria

All criteria must be met.

| ID | Criterion | Application Guide |
|----|-----------|-------------------|
| CI1 | Proposes or evaluates a mechanism to persist knowledge or experience across sessions in AI-based coding agents | See the **Detailed CI1 Guide** below. |
| CI2 | Reports empirical results (experiment, benchmark, case study) OR proposes a tool/framework with systematic evaluation | **Minimum floor:** quantitative evaluation on ≥2 tasks/examples with reported metrics. An N=1 case study with quantitative metrics across multiple sessions is acceptable. A demo without metrics or a single anecdotal example does not qualify. |
| CI3 | Published between 2023 and 2026 | Publication date or arXiv submission date. The window reflects the field's emergence in 2025, with a margin for precursors (MemGPT, 2023). Pre-2023 papers from citation chasing are excluded by this criterion — not a failure, by design. |
| CI4 | Written in English or Portuguese | — |
| CI5 | Peer-reviewed publication (conference, journal) OR preprint with identifiable authors/institutions | Conference, journal, or arXiv with clear affiliation. Papers with <7 pages (excluding references) are classified as "maybe" and the contribution is verified in the full text. |

## Exclusion Criteria

Any single criterion excludes the paper.

| ID | Criterion | Application Guide |
|----|-----------|-------------------|
| CE1 | Addresses only RAG, context retrieval, or intra-session context management without cross-session persistence | Includes: code retrieval, context window compression/pruning, prompt stuffing, file selection. All are intra-session unless there is an explicit cross-session write/accumulation component. See signals list in the **Detailed CI1 Guide**. |
| CE2 | Main contribution is not software development | **Conditional rule:** a generic agent paper (unspecified domain) is excluded UNLESS the evaluation explicitly includes SE benchmarks (SWE-bench, HumanEval, MBPP, CodeContests, repository tasks). If the abstract does not mention SE but the paper is generic, classify as "maybe" and verify benchmarks in the full text. Examples of exclusion: dialogue agents, chatbots, finance, healthcare, games, robotics. |
| CE3 | No evaluation beyond anecdotal examples | There must be quantitative or systematic qualitative evaluation with metrics. Tool demo without metrics = exclude. |
| CE4 | Tutorial, editorial, position paper, or descriptive survey without original technical contribution | Surveys with an original taxonomy and quantitative/comparative analysis are **included** (see borderline case). Surveys that only list works without analysis are excluded. |
| CE5 | Duplicate version or superseded by a later version from the same authors | **Operationalization:** same first author + title similarity >80% = verify. arXiv preprint + version published at a conference = keep the conference version. Multiple arXiv versions = keep the most recent. |

---

## Detailed CI1 Guide — Knowledge Persistence

CI1 is the most demanding criterion of the screening. This guide details
how to apply it.

### What CI1 requires

The paper must propose or evaluate a mechanism that:
1. **Stores** knowledge/experience explicitly (retrievable artifact:
   file, bank, graph, structured memory)
2. **Persists** this knowledge **across sessions or independent tasks**
   (not only within a single interaction)
3. **Reuses** the knowledge in future sessions/tasks
4. **Applies to** coding agents or software engineering tasks

### What CI1 does NOT include

| System type | Why it does not meet CI1 |
|-------------|--------------------------|
| Fine-tuning / continual learning of weights | **Parametric** persistence (in the model's weights), not **explicit** (retrievable artifact). The agent does not consult a memory — the weights change. Exclude. |
| Model editing / knowledge editing | Same — modifies internal representations of the model. |
| Offline training with historical data | Persistence at **training time**, not at **interactive use time**. Experiential Co-Learning (Qian 2024) trains with experiences but does not persist at runtime. Exclude. |
| Manually curated rules by humans | Editor rules, project instruction files, or local style guides — the **human** persists knowledge, not the **agent**. Exclude, unless the paper studies the impact of such rules on agent performance (in which case include as evidence for SQ3/SQ5). |
| Context window compression/pruning | Intra-session optimization. SWE-Pruner, context truncation — exclude (CE1). |
| RAG for repository (without write-back) | Retrieval without accumulation. The agent does not **write** to memory. Exclude (CE1). |
| Infrastructure/protocol (MCP, tool frameworks) | Enables but does not implement persistence. Exclude. |

### Positive signals (suggest CI1 is met)

- "cross-session", "between sessions", "across sessions", "across tasks"
- "accumulated experience/knowledge", "episodic memory" + write/update
- "persistent memory/context" + storage mechanism
- "long-term memory" + write operations + reuse
- "memory bank/store" + growth over time

### Ambiguous signals (classify as "maybe")

- "long-term memory" or "experience" without specifying cross-session
- "memory-augmented" without persistence detail
- "continual learning" without specifying whether parametric or explicit
- "context management" that mentions transfer across sessions

### Negative signals (suggest exclude)

- "context window", "context length", "token limit", "compression"
- "retrieval-augmented" without mention of write-back or accumulation
- "fine-tuning", "training", "model weights", "RLHF"
- "prompt engineering", "prompt optimization"

---

## Borderline Cases

| # | Case | Decision | Rationale | Source |
|---|------|----------|-----------|--------|
| 1 | Survey with original taxonomy and analysis (e.g., Du 2026) | **Include** | CE4 excludes only descriptive surveys; analytical surveys contribute to SQ1 | Pilot |
| 2 | Benchmark for continual learning (e.g., SWE-Bench-CL) | **Include** | Proposes metrics for persistence → CI2 is met, contributes to SQ2 | Pilot |
| 3 | Intra-session context management (paging, compression) | **Exclude** (CE1) | Does not persist across sessions — optimizes context window | Pilot |
| 4 | Cross-task accumulated-experience system (e.g., ExpeRepair) | **Include** | Accumulates knowledge across tasks = explicit persistence | Pilot |
| 5 | Fine-tuning models with commit data | **Exclude** | Parametric persistence, not explicit. Focuses on the model, not on the agent's memory | Pilot |
| 6 | RAG for repository without a session component | **Exclude** (CE1) | Retrieval without cross-session accumulation | Pilot |
| 7 | MemGPT/generic paging without SE application | **Exclude** (CE2) | Outside the software development scope | Pilot |
| 8 | Negative result showing that memory degrades performance | **Include** | Negative results are valuable for SQ5 (complexity-effectiveness) | Pilot |
| 9 | Experience sharing across distinct agents | **Include** | Persistence + sharing = contributes to SQ1 | Pilot |
| 10 | Generic agent memory paper with SWE-bench evaluation | **Include** | CE2 does not apply when evaluation includes SE benchmarks | Stress test — Liu IC2 |
| 11 | Generic agent memory paper without SE evaluation | **Exclude** (CE2) | Main contribution is not SE; no evidence of applicability | Stress test — A-MEM, MemSkill |
| 12 | Human-curated rules (cursor rules, .clinerules) | **Exclude** | Persistence by the human, not by the agent. Exception: if the paper studies impact on agent performance → "maybe" | Stress test — Cursor Rules (2512.18925) |
| 13 | Continual learning / incremental fine-tuning for code | **Exclude** | Parametric persistence (weights), not explicit (artifact). See CI1 guide | Stress test |
| 14 | System that transfers context across sessions (GCC, CMV) | **Include** | Explicit cross-session transfer = persistence, even if the mechanism is framed as context management | Stress test — GCC (2508.00031) |
| 15 | Offline training with accumulated experiences | **Exclude** | Training-time persistence, not interactive agent use. Experiential Co-Learning (Qian 2024) | Stress test |
| 16 | Infrastructure/protocol that enables persistence (MCP) | **Exclude** | Enables but does not implement knowledge persistence | Stress test |
| 17 | Multi-agent with shared memory within a single execution | **Exclude** (CE1) | Sharing within a single execution, not across sessions. ChatDev (2307.07924) | Stress test |

---

## Decision Flowchart

Apply in the indicated order. Each question has three possible outcomes:
**INCLUDE**, **EXCLUDE (code)**, or **MAYBE (reason)**.

```
START: Read title + abstract
│
├─ Q1. Written in English or Portuguese?
│  NO  → EXCLUDE (CI4)
│  YES → continue
│
├─ Q2. Published in 2023 or later?
│  NO  → EXCLUDE (CI3)
│  YES → continue
│
├─ Q3. Peer-reviewed publication or preprint with identifiable authors?
│  NO  → EXCLUDE (CI5)
│  YES → continue
│
├─ Q4. Is it a tutorial, editorial, position paper, or descriptive survey?
│  YES, without original analysis → EXCLUDE (CE4)
│  YES, but with original taxonomy/analysis → continue (borderline case #1)
│  NO  → continue
│
├─ Q5. Duplicate or superseded version?
│     (same first author + title similarity >80%, or preprint + venue)
│  YES → EXCLUDE (CE5), keep the most recent/complete version
│  NO  → continue
│
├─ Q6. Does the paper address software development / code tasks?
│  │  Positive signals: code, software, programming, repository, bug,
│  │  SWE-bench, HumanEval, MBPP, code generation, code repair, IDE,
│  │  pull request, commit, refactor, debug, test generation
│  │
│  CLEARLY YES → continue
│  CLEARLY NO (dialogue, finance, healthcare, games, robotics)
│    → EXCLUDE (CE2)
│  UNCERTAIN (generic agent, unspecified domain):
│    Does the abstract mention SE benchmarks in the evaluation?
│      YES → continue
│      NO / IMPOSSIBLE TO DETERMINE → MAYBE (check benchmarks
│        in the full text)
│
├─ Q7. Does the paper propose/evaluate knowledge persistence ACROSS
│      sessions or independent tasks?
│  │
│  │  EXPLICIT PERSISTENCE (retrievable artifact that grows/updates):
│  │    "cross-session", "between sessions", "across tasks",
│  │    "accumulated experience", "memory bank" + write/update,
│  │    "episodic memory" + cross-task storage
│  │  → CLEARLY YES → continue
│  │
│  │  NOT PERSISTENCE (exclude):
│  │    - Only RAG/retrieval without write-back → EXCLUDE (CE1)
│  │    - Intra-session context compression/pruning → EXCLUDE (CE1)
│  │    - Fine-tuning/continual learning of weights → EXCLUDE (CE1)
│  │    - Offline training with experiences → EXCLUDE (CE1)
│  │    - Human-curated rules (not by the agent) → EXCLUDE (CE1)
│  │    - Infrastructure/protocol without implementation → EXCLUDE (CE1)
│  │
│  │  AMBIGUOUS:
│  │    "long-term memory" or "experience" without specifying cross-session
│  │    "memory-augmented" without mechanism detail
│  │    "context management" with possible cross-session transfer
│  │  → MAYBE (verify in full text)
│
├─ Q8. Does the paper report empirical evaluation with metrics?
│  │  (experiment, benchmark, case study with quantitative data)
│  │  Floor: ≥2 tasks/examples with metrics, OR N=1 with multiple
│  │  sessions/metrics over time
│  │
│  YES → continue
│  NO (only conceptual proposal or demo without metrics)
│    → EXCLUDE (CE3)
│  UNCERTAIN → MAYBE
│
└─ DECISION: **INCLUDE**
   (all CIs met, no CE triggered)
```

---

## Screening Procedure

### Phase 1: Title and Abstract
- Apply the flowchart above to each paper
- Elicit Pro applies the criteria and recommends include/exclude
- The researcher validates each decision using the flowchart
- Decision: **include**, **exclude**, or **maybe**
- "Maybe" papers advance to Phase 2 (full text)
- Exclusion reason recorded by code (CI/CE)
- Logged in `title-abstract-screening.tsv`

### Phase 2: Full Text
- Reapplication of criteria with complete information
- Special attention to:
  - **CI1:** verify that there is actual cross-session persistence
  - **CE2 "maybe":** verify whether the evaluation includes SE benchmarks
  - **CI2:** verify whether the evaluation meets the minimum floor
- Logged in `full-text-screening.tsv`

### Resolution of Borderline Cases
- Discussion with the advisor
- Justification recorded

### Quality Gates (checkpoints during screening)
- **Gate 1 (after 100 papers):** check include/maybe/exclude rates.
  If inclusion rate >20% or <3%, pause and recalibrate.
- **Gate 2 (after 555 papers, 50%):** compute all metrics. If CE2
  represents >70% or <30% of exclusions, investigate.
- **Gate 3 (after 1,110 papers):** final metrics for the manuscript.

### Target Metrics

| Metric | Target | Action if out of target |
|--------|--------|-------------------------|
| Inclusion rate (title/abstract) | 3–7% | >10%: loose criteria. <2%: strict criteria |
| "Maybe" rate | ≤15% overall, ≤35% grey zone | >20%: refine ambiguous flowchart nodes |
| CE2 as % of exclusions | 30–50% | <20%: CE2 too narrow. >60%: strings too broad |
| Reversal rate (full text) | ≤20% | >30%: title/abstract screening not reliable |
| Inter-rater agreement | Cohen's κ ≥0.70 | <0.60: subjective criteria, rewrite |
