# Screening Criteria

---

## Inclusion Criteria

All criteria must be met.

| ID | Criterion | Application Guide |
|----|-----------|-------------------|
| IC1 | Proposes or evaluates a mechanism to persist knowledge or experience across sessions in AI-based coding agents | See **Detailed IC1 Guide** below. |
| IC2 | Reports empirical results (experiment, benchmark, case study) OR proposes a tool/framework with systematic evaluation | **Minimum floor:** quantitative evaluation on ≥2 tasks/examples with reported metrics. An N=1 case study with quantitative metrics across multiple sessions is acceptable. A demo without metrics or a single anecdotal example does not qualify. |
| IC3 | Published between 2023 and 2026 | Publication or arXiv submission date. The window reflects the field's emergence in 2025, with a margin for precursors (MemGPT, 2023). Pre-2023 papers from citation chasing are excluded by this criterion — this is by design, not a failure. |
| IC4 | Written in English or Portuguese | — |
| IC5 | Peer-reviewed publication (conference, journal) OR preprint with identifiable authors/institutions | Conference, journal, or arXiv with clear affiliation. Papers with <7 pages (excluding references) are classified as "maybe" and contribution is verified in the full text. |

## Exclusion Criteria

Any single criterion excludes the paper.

| ID | Criterion | Application Guide |
|----|-----------|-------------------|
| EC1 | Addresses only RAG, context retrieval, or intra-session context management without cross-session persistence | Includes: code retrieval, context window compression/pruning, prompt stuffing, file selection. All are intra-session unless there is an explicit write/accumulation component across sessions. See signals list in **Detailed IC1 Guide**. |
| EC2 | Main contribution is not software development | **Conditional rule:** a generic agent paper (unspecified domain) is excluded UNLESS the evaluation explicitly includes SE benchmarks (SWE-bench, HumanEval, MBPP, CodeContests, repository tasks). If the abstract does not mention SE but the paper is generic, classify as "maybe" and check benchmarks in the full text. Examples of exclusion: dialogue agents, chatbots, finance, healthcare, games, robotics. |
| EC3 | No evaluation beyond anecdotal examples | There must be quantitative or systematic qualitative evaluation with metrics. Tool demo without metrics = exclude. |
| EC4 | Tutorial, editorial, position paper, or descriptive survey without original technical contribution | Surveys with original taxonomy and quantitative/comparative analysis are **included** (see borderline case). Surveys that only list works without analysis are excluded. |
| EC5 | Duplicate version or superseded by a later version from the same authors | **Operationalization:** same first author + title similarity >80% = verify. arXiv preprint + version published at a conference = keep the conference version. Multiple arXiv versions (v1, v2) = keep the most recent. |

---

## Detailed IC1 Guide — Knowledge Persistence

IC1 is the most demanding criterion of the screening. This guide details
how to apply it.

### What IC1 requires

The paper must propose or evaluate a mechanism that:
1. **Stores** knowledge/experience explicitly (retrievable artifact:
   file, bank, graph, structured memory)
2. **Persists** this knowledge **across sessions or independent tasks**
   (not only within a single interaction)
3. **Reuses** the knowledge in future sessions/tasks
4. **Applies to** coding agents or software engineering tasks

### What IC1 does NOT include

| System type | Why it does not meet IC1 |
|-------------|--------------------------|
| Fine-tuning / continual learning of weights | **Parametric** persistence (in the model's weights), not **explicit** (retrievable artifact). The agent does not consult a memory — the weights change. Exclude. |
| Model editing / knowledge editing | Same — modifies internal representations of the model. |
| Offline training with historical data | Persistence at **training time**, not at **interactive use time**. Experiential Co-Learning (Qian 2024) trains with experiences but does not persist at runtime. Exclude. |
| Manually curated rules by humans | Cursor rules, .clinerules, project-level instruction files — the **human** persists knowledge, not the **agent**. Exclude, unless the paper studies the impact of such rules on agent performance (in which case, include as evidence for SQ3/SQ5). |
| Context window compression/pruning | Intra-session optimization. SWE-Pruner, context truncation — exclude (EC1). |
| RAG for repository (without write-back) | Retrieval without accumulation. The agent does not **write** to memory. Exclude (EC1). |
| Infrastructure/protocol (MCP, tool frameworks) | Enables but does not implement persistence. Exclude. |

### Positive signals (suggest IC1 is met)

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

| # | Case | Decision | Rationale |
|---|------|----------|-----------|
| 1 | Survey with original taxonomy and analysis (e.g., Du 2026) | **Include** | EC4 excludes only descriptive surveys; analytical surveys contribute to SQ1 |
| 2 | Benchmark for continual learning (e.g., SWE-Bench-CL) | **Include** | Proposes metrics for persistence → IC2 is met, contributes to SQ2 |
| 3 | Intra-session context management (paging, compression) | **Exclude** (EC1) | Does not persist across sessions — optimizes context window |
| 4 | Cross-task accumulated experience system (e.g., ExpeRepair) | **Include** | Accumulates knowledge across tasks = explicit persistence |
| 5 | Fine-tuning models with commit data | **Exclude** | Parametric persistence, not explicit. Focus is on the model, not on the agent's memory |
| 6 | RAG for repository without a session component | **Exclude** (EC1) | Retrieval without cross-session accumulation |
| 7 | MemGPT/generic paging without SE application | **Exclude** (EC2) | Outside the software development scope |
| 8 | Negative result showing that memory degrades performance | **Include** | Negative results are valuable for SQ5 (complexity-effectiveness) |
| 9 | Experience sharing across distinct agents | **Include** | Persistence + sharing = contributes to SQ1 |
| 10 | Generic agent memory paper with SWE-bench evaluation | **Include** | EC2 does not apply when evaluation includes SE benchmarks |
| 11 | Generic agent memory paper without SE evaluation | **Exclude** (EC2) | Main contribution is not SE; no evidence of SE applicability |
| 12 | Human-curated rules (cursor rules, .clinerules) | **Exclude** | Persistence by the human, not by the agent. Exception: if the paper studies the impact on agent performance → "maybe" |
| 13 | Continual learning / incremental fine-tuning for code | **Exclude** | Parametric persistence (weights), not explicit (artifact). See IC1 guide |
| 14 | System that transfers context across sessions (GCC, CMV) | **Include** | Explicit cross-session transfer = persistence, even if the mechanism is framed as context management |
| 15 | Offline training with accumulated experiences | **Exclude** | Training-time persistence, not interactive agent use. Experiential Co-Learning (Qian 2024) |
| 16 | Infrastructure/protocol that enables persistence (MCP) | **Exclude** | Enables but does not implement knowledge persistence |
| 17 | Multi-agent with shared memory within a single execution | **Exclude** (EC1) | Sharing within a single execution, not across sessions. ChatDev (2307.07924) |

---

## Decision Flowchart

Apply in the indicated order. Each question has three possible outcomes:
**INCLUDE**, **EXCLUDE (code)**, or **MAYBE (reason)**.

```
START: Read title + abstract
│
├─ Q1. Written in English or Portuguese?
│  NO  → EXCLUDE (IC4)
│  YES → continue
│
├─ Q2. Published in 2023 or later?
│  NO  → EXCLUDE (IC3)
│  YES → continue
│
├─ Q3. Peer-reviewed publication or preprint with identifiable authors?
│  NO  → EXCLUDE (IC5)
│  YES → continue
│
├─ Q4. Is it a tutorial, editorial, position paper, or descriptive survey?
│  YES, without original analysis → EXCLUDE (EC4)
│  YES, but with original taxonomy/analysis → continue (borderline case #1)
│  NO  → continue
│
├─ Q5. Duplicate or superseded version?
│     (same first author + title similarity >80%, or preprint + venue)
│  YES → EXCLUDE (EC5), keep the most recent/complete version
│  NO  → continue
│
├─ Q6. Does the paper address software development / code tasks?
│  │  Positive signals: code, software, programming, repository, bug,
│  │  SWE-bench, HumanEval, MBPP, code generation, code repair, IDE,
│  │  pull request, commit, refactor, debug, test generation
│  │
│  CLEARLY YES → continue
│  CLEARLY NO (dialogue, finance, healthcare, games, robotics)
│    → EXCLUDE (EC2)
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
│  │    - Only RAG/retrieval without write-back → EXCLUDE (EC1)
│  │    - Intra-session context compression/pruning → EXCLUDE (EC1)
│  │    - Fine-tuning/continual learning of weights → EXCLUDE (EC1)
│  │    - Offline training with experiences → EXCLUDE (EC1)
│  │    - Human-curated rules (not by the agent) → EXCLUDE (EC1)
│  │    - Infrastructure/protocol without implementation → EXCLUDE (EC1)
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
│    → EXCLUDE (EC3)
│  UNCERTAIN → MAYBE
│
└─ DECISION: **INCLUDE**
   (all ICs met, no EC triggered)
```

---

## Screening Procedure

### Phase 1: Title and Abstract
- Apply the flowchart above to each paper
- Researcher applies the criteria and records the decision
- Decision: **include**, **exclude**, or **maybe**
- "Maybe" papers advance to Phase 2 (full text)
- Exclusion reason recorded by code (IC/EC)
- Logged in `title-abstract.tsv`

### Phase 2: Full Text
- Reapplication of the criteria with complete information
- Special attention to:
  - **IC1:** verify that there is actual cross-session persistence
  - **EC2 "maybe":** verify whether the evaluation includes SE benchmarks
  - **IC2:** verify whether the evaluation meets the minimum floor
- Logged in `full-text.tsv`

### Resolution of Borderline Cases
- Discussion with advisor
- Justification recorded
