# Synthesis Matrix

Thematic organization of findings per secondary research question.
Data compiled from the 28 included studies (extraction in
`extraction/data.tsv`).

**Note:** 4 studies do not propose primary persistence architectures:
Du (2026) is a survey, Deshpande (2025) and Joshi (2025) propose
benchmarks, and Srivastava (2025) is a security study. These are
analyzed separately where relevant.

---

## SQ1 — Architecture Taxonomy

### 1.1 Distribution by Architecture Type

24 primary studies propose or implement persistence architectures.

| Architecture Type | N | Studies |
|-------------------|---|---------|
| `experience_bank` | 11 | Chen (SWE-Exp), Deng (MemCoder), Guo (EET), Joshi (SWE-Bench-CL)¹, Lindenbauer (CTIM-Rover), Qian (IER), Shen (TALM), Shen (Structurally), Su (Learn-by-Interact), Tablan (Spark), Zhang (AccelOpt) |
| `hybrid` | 5 | Hosain (Xolver), Nadafian (KAPSO), Vasilopoulos (Codified), Wong (Confucius/CCA), Zhou (ToM-SWE) |
| `git_metaphor` | 2 | Wang (Repository Memory), Wu (GCC) |
| `text_notes` | 1 | Bui (OpenDev) |
| `ast_guided` | 1 | Wang (CodeMEM) |
| `knowledge_graph` | 1 | Dong (KernelBlaster) |
| `os_paging` | 0 | — |
| `other` | 3 | Li (Traversal-as-Policy/GBT), Xia (Live-SWE-Agent), Zhang (Darwin-Gödel) |

¹ SWE-Bench-CL proposes a benchmark but includes a baseline memory
implementation (FAISS vector store).

**Finding SQ1-A:** Experience banks dominate (46% of primary studies),
reflecting the prevalence of approaches that distill resolution
trajectories into reusable entries. Hybrid architectures (21%)
typically combine episodic with semantic memory.

### 1.2 Three-Dimensional Classification (Du 2026 Taxonomy)

| Study | Temporal Scope | Substrate | Policy |
|-------|---------------|-----------|--------|
| Bui (OpenDev) | hybrid | text_context | llm_self_control |
| Chen (SWE-Exp) | hybrid | structured | llm_self_control |
| Deng (MemCoder) | hybrid | structured | llm_self_control |
| Dong (KernelBlaster) | hybrid | structured | learned |
| Guo (EET) | episodic | structured | llm_self_control |
| Hosain (Xolver) | hybrid | text_context | llm_self_control |
| Li (GBT) | procedural | executable | heuristic |
| Lindenbauer (CTIM-Rover) | episodic | text_context | heuristic |
| Nadafian (KAPSO) | hybrid | hybrid | llm_self_control |
| Qian (IER) | procedural | text_context | heuristic |
| Shen (TALM) | hybrid | hybrid | heuristic |
| Shen (Structurally) | procedural | structured | heuristic |
| Su (Learn-by-Interact) | episodic | text_context | heuristic |
| Tablan (Spark) | hybrid | hybrid | llm_self_control |
| Vasilopoulos (Codified) | hybrid | text_context | heuristic |
| Wang (Repository Memory) | hybrid | hybrid | heuristic |
| Wang (CodeMEM) | hybrid | hybrid | llm_self_control |
| Wang (MemGovern) | semantic | structured | llm_self_control |
| Wong (CCA) | hybrid | text_context | llm_self_control |
| Wu (GCC) | hybrid | text_context | llm_self_control |
| Xia (Live-SWE-Agent) | procedural | executable | llm_self_control |
| Zhang (AccelOpt) | episodic | text_context | heuristic |
| Zhang (Darwin-Gödel) | procedural | executable | learned |
| Zhou (ToM-SWE) | hybrid | structured | llm_self_control |

#### Distribution by dimension

| Temporal Scope | N | % |
|----------------|---|---|
| hybrid | 14 | 58% |
| episodic | 4 | 17% |
| procedural | 5 | 21% |
| semantic | 1 | 4% |

| Representational Substrate | N | % |
|----------------------------|---|---|
| text_context | 9 | 38% |
| structured | 6 | 25% |
| hybrid | 5 | 21% |
| executable | 3 | 12% |
| vector | 1 | 4% |

| Control Policy | N | % |
|----------------|---|---|
| llm_self_control | 13 | 54% |
| heuristic | 9 | 38% |
| learned | 2 | 8% |

**Finding SQ1-B:** Hybrid temporal scope (episodic + semantic)
predominates (58%), indicating that systems need both short-term
memory (recent experiences) and long-term memory (consolidated
knowledge). Only Wang (MemGovern) uses purely semantic scope.

**Finding SQ1-C:** The LLM as memory controller (llm_self_control,
54%) surpassed fixed heuristics (38%). Learned policies via
optimization are rare (8%), limited to KernelBlaster and Darwin-Gödel.

**Finding SQ1-D:** Plain text in context (38%) and structured
substrates (25%) dominate. Executable substrates (12%) — GBT,
Live-SWE-Agent, Darwin-Gödel — represent an emerging trend where
memory is directly executable (behavior trees, scripts, entire
agents).

### 1.3 Retrieval Method

| Method | N | Studies |
|--------|---|---------|
| `hybrid` | 11 | Chen, Deng, Hosain, Nadafian, Shen (TALM), Shen (Structurally), Su, Tablan, Wang (Repository Memory), Wang (CodeMEM), Wu |
| `embeddings` | 3 | Joshi, Lindenbauer, Qian |
| `bm25` | 3 | Guo, Wang (Repository Memory)¹, Zhou |
| `full_load` | 2 | Xia, Zhang (AccelOpt) |
| `ast_intersection` | 1 | Wang (CodeMEM)¹ |
| `other` | 3 | Dong (KB lookup), Li (tree traversal), Zhang (Darwin-Gödel, evolutionary selection) |

¹ Some studies appear in multiple categories because they use
different methods for distinct memory components.

**Finding SQ1-E:** Hybrid retrieval (combining BM25, embeddings,
and/or heuristics) is the dominant pattern (46%). Full memory load
into context is used only when memory is compact (AccelOpt: ~50KB;
Live-SWE-Agent: ~3 tools per task).

### 1.4 Granularity and Sharing

| Granularity | N |
|-------------|---|
| task | 16 |
| subtask | 4 |
| repository | 2 |
| commit | 1 |
| function | 1 |
| other | 3 |

Cross-agent sharing: only Chen (SWE-Exp) reports
`cross_agent_sharing = yes`. 21 studies report `no`, 2 report
`not_applicable`.

**Finding SQ1-F:** The dominant granularity is task (67%), aligned
with the structure of benchmarks (SWE-bench = 1 issue = 1 task).
Memory shared across agents is virtually unexplored.

---

## SQ2 — Evaluation Methods and Benchmarks

### 2.1 Evaluation Methods

| Method | N | Studies |
|--------|---|---------|
| benchmark | 21 | Chen, Deng, Deshpande, Dong, Guo, Hosain, Joshi, Li, Lindenbauer, Nadafian, Qian, Shen (TALM), Shen (Structurally), Su, Tablan, Wang (RepoMem), Wang (CodeMEM), Wang (MemGovern), Wong, Wu, Xia, Zhang (AccelOpt), Zhang (DGM) |
| case_study | 3 | Bui, Srivastava, Vasilopoulos |
| mixed | 1 | Zhou |
| NA (survey) | 1 | Du |

### 2.2 Benchmarks Used

| Benchmark | N | Studies |
|-----------|---|---------|
| SWE-bench Verified | 14 | Chen, Deng, Li, Lindenbauer, Shen (Structurally), Wang (RepoMem), Wang (MemGovern), Wong, Wu, Xia, Zhang (DGM), Zhou, Guo, Hosain¹ |
| SWE-Bench-CL | 1 | Joshi |
| SWE-Bench Pro | 2 | Wong, Xia |
| SWE-bench Lite | 2 | Guo, Wu |
| HumanEval | 1 | Shen (TALM) |
| BigCodeBench | 1 | Shen (TALM) |
| ClassEval | 1 | Shen (TALM) |
| CodeIF-Bench / CoderEval | 1 | Wang (CodeMEM) |
| KernelBench (L1-L3) | 1 | Dong |
| NKIBench | 1 | Zhang (AccelOpt) |
| DS-1000 | 1 | Tablan |
| MLE-Bench / ALE-Bench | 1 | Nadafian |
| WebArena | 2 | Li, Su |
| OSWorld | 1 | Su |
| MemTrack | 1 | Deshpande |
| BrowseComp-Plus | 1 | Wu |
| SRDD | 1 | Qian |
| GSM8K / AIME / Math-500 / LiveCodeBench | 1 | Hosain |

¹ Hosain (Xolver) focuses on math/code competition, not SE directly.

**Finding SQ2-A:** SWE-bench Verified is the dominant benchmark
(14/21 studies with benchmark, 67%), creating a natural point of
comparability. However, subsets vary (500 vs. 300 instances), and
experimental conditions differ (models, temperature, number of
attempts).

**Finding SQ2-B:** 7 studies use unique benchmarks not shared by any
other study (MemTrack, SRDD, NKIBench, DS-1000, KernelBench,
CodeIF-Bench, MLE/ALE-Bench), limiting direct comparability.

### 2.3 Performance Metrics

| Metric | N (approx.) |
|--------|-------------|
| Pass@1 / Resolve Rate | 18 |
| Accuracy@k (k>1) | 2 |
| Speedup (geomean) | 2 |
| Code Quality Score (LLM judge) | 1 |
| Correctness (LLM judge) | 1 |
| CL metrics (ACC, F, FT, BWT) | 1 |

**Finding SQ2-C:** Pass@1 / Resolve Rate is the universal metric for
SE (18/21 studies with benchmark). Continual learning metrics
(forgetting, backward/forward transfer) are proposed by Joshi
(SWE-Bench-CL) but have not yet been adopted by other studies.

### 2.4 Comparability

Despite convergence on SWE-bench Verified, direct comparability is
limited by:

1. **Different models** — the 14 studies use at least 8 distinct LLMs
   as backbone (GPT-4o, GPT-5.2, Claude 3.5/4/4.5 Sonnet, DeepSeek-V3,
   Gemini 2.5/3 Pro, Qwen3)
2. **Different frameworks** — SWE-Agent, OpenHands, custom
3. **Execution conditions** — temperature, number of attempts,
   timeout, and maximum cost vary or are not reported
4. **Subsets** — some use 500 instances, others smaller subsets

**Finding SQ2-D:** No study compares ≥3 persistence architectures on
the same benchmark with the same model, confirming Gap 1 (zero
head-to-head comparisons). Comparability depends entirely on results
reported in different papers, with heterogeneous experimental
conditions.

---

## SQ3 — Performance Results

### 3.1 Gains vs. Baseline without Persistence

Only studies with an explicit comparison against a memory-less
baseline are included. Ordered by absolute gain on the main benchmark.

| Study | Benchmark | Baseline (no mem.) | With memory | Gain |
|-------|-----------|-------------------|-------------|------|
| Li (GBT) | SWE-bench V. | 34.6% | 73.6% | +39.0pp |
| Zhang (DGM) | SWE-bench V. | 20.0% | 50.0% | +30.0pp |
| Wang (CodeMEM) | CodeIF-Bench (IA) | ~73% | 85.2% | +12.2pp |
| Su (Learn-by-Interact) | OSWorld | 12.4% | 22.5% | +10.1pp |
| Deng (MemCoder) | SWE-bench V. | 68.4% | 77.8% | +9.4pp |
| Wang (MemGovern) | SWE-bench V. (GPT-4o) | 23.2% | 32.6% | +9.4pp |
| Su (Learn-by-Interact) | SWE-bench V. | 51.2% | 60.0% | +8.8pp |
| Guo (EET) | SWE-bench V. | ~32% | ~35% | +2.7pp avg |
| Shen (Structurally) | SWE-bench V. | 53.5% | 60.3% | +6.8pp¹ |
| Dong (KernelBlaster) | KernelBench | 1.0× | 1.67× | +67% speedup |
| Shen (TALM) | BigCodeBench | 50.1% | 53.3% | +3.2pp |
| Wang (RepoMem) | SWE-bench V. | 37.0% | 40.4% | +3.4pp |
| Chen (SWE-Exp) | SWE-bench V. | 70.8% | 73.0% | +2.2pp |
| Wong (CCA) | SWE-Bench-Pro | ~56.0% | 59.0% | +3.0pp |
| Zhou (ToM-SWE) | Ambig. SWE-bench | 51.9% | 63.4% | +11.5pp |
| Tablan (Spark) | DS-1000 | 4.23/5 | 4.89/5 | +0.66 pts |
| Wu (GCC) | SWE-bench V. | 74.0%² | 80.2% | +6.2pp |
| Xia (Live-SWE) | SWE-bench V. | 74.2% | 77.4% | +3.2pp |
| Nadafian (KAPSO) | MLE-Bench | 35.1% | 50.7% | +15.6pp |

¹ Best result (Gemini 2.5 Pro); varies by LLM (+2.3pp to +6.8pp).
² Baseline is Folding Agent (best control with partial memory).

**Finding SQ3-A:** All 19 studies with a controlled comparison report
positive gains from memory persistence. Magnitude varies from +2.2pp
(SWE-Exp) to +39.0pp (GBT), with a median of +6.8pp on SWE-bench
Verified (recomputed over the 11 SWE-bench V. entries in the
performance table).

**Finding SQ3-B:** The largest gains (>+10pp) occur in systems that
start from weaker baselines (Li: 34.6%, Zhang DGM: 20.0%, Su: 12.4%).
Where baselines are already strong (>65%), marginal gains are smaller
(+2–9pp), suggesting diminishing returns.

**Finding SQ3-C:** Gains are consistent across LLMs — Shen
(Structurally) demonstrates +4.7pp average across 4 different LLMs,
and Wang (MemGovern) reports +4.65pp average across 7 LLMs.
Persistence improves performance regardless of the backbone model.

### 3.2 Studies without Controlled Comparison

| Study | Reason |
|-------|--------|
| Bui (OpenDev) | Technical report without empirical evaluation |
| Vasilopoulos (Codified) | Observational case study, no control |
| Qian (IER) | Baseline is ChatDev (another system), not memory ablation |
| Hosain (Xolver) | Baseline is LongCoT, not memory ablation |
| Zhang (AccelOpt) | Comparison against beam search, not pure ablation |

---

## SQ4 — Cost and Efficiency

### 4.1 Cost Data Reporting Level

| Level | N | Studies |
|-------|---|---------|
| `yes_detailed` | 6 | Chen, Guo, Wang (MemGovern), Wu, Xia, Zhang (AccelOpt), Zhou |
| `yes_partial` | 8 | Dong, Hosain, Li, Shen (TALM), Su, Wang (RepoMem), Wang (CodeMEM), Wong |
| `no` | 12 | Bui, Deng, Deshpande, Du, Joshi, Lindenbauer, Nadafian¹, Qian, Shen (Structurally), Srivastava, Tablan, Vasilopoulos, Zhang (DGM) |

¹ Nadafian reports total cost ($914.8) but does not break it down by
component.

**Finding SQ4-A:** 57% of studies (16/28) do not report detailed cost
data, confirming Gap 2. Only 6 studies provide a complete breakdown
(tokens + monetary cost + comparison against baseline).

### 4.2 Monetary Cost per Task

| Study | Cost/task | LLM | Benchmark |
|-------|-----------|-----|-----------|
| Guo (EET) | $0.012 | GPT-5-mini | SWE-bench V. |
| Zhou (ToM-SWE) | $0.02 overhead | GPT-5-nano | Stateful SWE |
| Wang (MemGovern) | $0.07 | Qwen3-Coder-30B | SWE-bench V. |
| Chen (SWE-Exp) | $0.13 | DeepSeek-V3 | SWE-bench V. |
| Xia (Live-SWE) | $0.05–$0.73 | GPT-5-Mini–Claude 4.5 S | SWE-bench V./Pro |
| Wang (RepoMem) | $0.58–$0.89 | — | SWE-bench V. |
| Wu (GCC) | $0.57–$1.21 | GPT-3.5–Claude 3.5 S | SWE-bench Lite |
| Wang (MemGovern) | $7.27 | Claude 4 Sonnet | SWE-bench V. |
| Zhang (AccelOpt) | $6.87–$15.95/config | open-source models | NKIBench |
| Nadafian (KAPSO) | ~$83/competition | Gemini | ALE-Bench |

### 4.3 Impact of Memory on Cost

| Study | Cost variation with memory | Direction |
|-------|---------------------------|-----------|
| Guo (EET) | -31.8% average total cost | ↓ reduces |
| Li (GBT) | -39% tokens (208k→126k) | ↓ reduces |
| Shen (TALM) | ~50% fewer tokens than MapCoder | ↓ reduces |
| Dong (KernelBlaster) | 2.4× fewer tokens than without KB | ↓ reduces |
| Wang (CodeMEM) | ~30k fewer tokens/round | ↓ reduces |
| Wong (CCA) | -11k tokens/task (104k→93k) | ↓ reduces |
| Bui (OpenDev) | ~88% reduction via prompt caching | ↓ reduces |
| Zhang (AccelOpt) | 26× cheaper than Claude Sonnet 4 | ↓ reduces |
| Chen (SWE-Exp) | +7.5% tokens, +8.3% cost | ↑ increases |
| Wang (MemGovern) | +4.8% cost (Claude 4 Sonnet) | ↑ increases |
| Xia (Live-SWE) | comparable online cost (+4–21%) | ↑ slight |
| Wang (RepoMem) | higher cost on harder problems | ↑ increases |

**Finding SQ4-B:** The cost-memory relationship is bimodal. Systems
that use memory to *replace* context (EET, GBT, TALM, CodeMEM) reduce
costs. Systems that *add* context via retrieval (SWE-Exp, MemGovern,
RepoMem) increase costs marginally (+5–20%), but with proportional
performance gains.

**Finding SQ4-C:** EET (Guo 2026) demonstrates the best trade-off:
-31.8% cost with negligible performance loss (-0.2pp maximum), by
identifying early termination opportunities in 11.3% of issues.

**Finding SQ4-D:** No study constructs an explicit Pareto frontier
between accuracy and cost. The available data suggest that the
frontier is not convex — some systems (EET, GBT) dominate on both
dimensions, while others (MemGovern with Claude 4) offer high
performance at elevated cost.

---

## SQ5 — Complexity vs. Effectiveness

### 5.1 Studies with Negative Results (Memory-Induced Degradation)

9 studies report `negative_result = yes`:

| Study | Degradation scenario |
|-------|---------------------|
| Deshpande (MemTrack) | Mem0 and Zep do not improve and increase tool-call redundancy (~21%); Gemini+Mem0 degrades -18% vs. no memory |
| Joshi (SWE-Bench-CL) | Enabling memory does not help; garbage-in garbage-out due to incompatible harness |
| Lindenbauer (CTIM-Rover) | CTIM-Rover 40% vs. AutoCodeRover 42% (-2pp); CTIM-only degrades to 31% (-11pp); noisy items divert exploration |
| Chen (SWE-Exp) | k>1 experiences degrades (42.0%→39.0% with k=4); over-dependence on experiences |
| Shen (TALM) | Memory degrades on simple tasks where retrieval overhead is not amortized |
| Vasilopoulos (Codified) | Knowledge-to-code ratio of 24% requires continuous maintenance (~1–2h/week) |
| Xia (Live-SWE) | Weak LLMs (GPT-5-Nano) degrade -68.2% with tool creation |
| Srivastava (MemoryGraft) | 9.1% poisoned experiences compromise 47.9% of retrievals |
| Zhou (ToM-SWE) | User simulator may introduce biases (over-compliance) |

**Finding SQ5-A:** 9/28 studies (32%) report scenarios where memory
degrades performance. The degradation mechanisms are:

1. **Retrieval noise** (Lindenbauer, Chen, Deshpande) — irrelevant
   or excessive experiences divert the agent
2. **Unnecessary overhead** (Shen TALM, Xia) — retrieval cost is not
   amortized on simple tasks or with weak models
3. **Poisoning** (Srivastava) — security vulnerability in open
   memory stores
4. **Infrastructure incompatibility** (Joshi) — evaluation harness
   incompatible with the memory mechanism

### 5.2 Architectural Complexity vs. Outcome

| Complexity | Studies | Typical outcome |
|------------|---------|-----------------|
| **Low** (full load, simple heuristic) | AccelOpt, Su, Zhang (DGM) | Effective when memory is compact; DGM +30pp with simple evolutionary selection |
| **Medium** (bank + retrieval) | Chen, Deng, Guo, Shen (Struct.), Wang (MemGovern) | Consistent gains +2–9pp; predictable trade-off |
| **High** (multiple tiers, graphs, AST) | Wang (CodeMEM), Nadafian (KAPSO), Wong (CCA), Wu (GCC) | Superior gains on harder benchmarks; higher implementation cost |

**Finding SQ5-B:** There is no evidence that higher architectural
complexity produces systematically larger gains. AccelOpt (simple
experience queue) and EET (heuristic early termination) achieve
results comparable to multi-tier systems (KAPSO, GCC) in their
respective domains, with much lower implementation and maintenance
cost.

**Finding SQ5-C:** The most determining factor of gain is not memory
complexity but the gap between the baseline and the benchmark's
potential. Simple memory on a weak baseline (DGM: +30pp) outperforms
sophisticated memory on a strong baseline (SWE-Exp: +2.2pp).

**Finding SQ5-D:** Retrieval calibration (how many items to retrieve)
is critical. Chen (SWE-Exp) demonstrates degradation with k>1
experiences, and Shen (Structurally) demonstrates that category
isolation outperforms global retrieval by +2.3pp. More memory ≠
better result.

---

## Cross-cutting Findings

### Methodological Maturity

| Indicator | Value |
|-----------|-------|
| Venue type: preprint | 24/28 (86%) |
| Venue type: conference | 2/28 (7%) |
| Venue type: workshop | 2/28 (7%) |
| Median quality | 5.0/6 |
| Quality ≥4/6 | 24/28 (86%) |
| Quality <3/6 | 2/28 (7%): OpenDev (2.0), Du survey (2.5) |

**Finding T-A:** The field is dominated by preprints (86%),
indicating early maturity. Only 2 studies were published at a
conference (Wang RepoMem, Zhang DGM) and 2 at a workshop (Deshpande
MemTrack, Shen TALM).

### Open Source

| Open source | N |
|-------------|---|
| yes | 17 |
| no | 4 |
| partial | 3 |
| NA | 4 |

**Finding T-B:** 71% of primary studies make the source code
available (yes or partial), favoring reproducibility.

### Relevance to Identified Gaps

| Gap | N | Studies |
|-----|---|---------|
| gap1_comparison | 12 | Deng, Deshpande, Hosain, Joshi, Nadafian, Shen (Struct.), Su, Tablan, Wang (CodeMEM), Wang (MemGovern), Wong, Wu, Zhou |
| gap2_cost | 6 | Chen, Dong, Guo, Li, Wang (RepoMem), Xia, Zhang (AccelOpt) |
| gap3_complexity | 6 | Bui, Lindenbauer, Qian, Shen (TALM), Srivastava, Vasilopoulos, Zhang (DGM) |
| multiple | 1 | Du |

**Finding T-C:** Gap 1 (absence of head-to-head comparisons) remains
confirmed — none of the 28 studies compares ≥3 persistence
architectures on the same benchmark with the same model.

---

## Sensitivity Analyses

### S1 — Excluding Preprints

24/28 studies are preprints. Retaining only the 4 peer-reviewed
studies (Deshpande/workshop, Shen TALM/workshop, Wang
RepoMem/conference, Zhang DGM/conference):

- **SQ1:** Only 3 architectures represented (experience_bank ×2,
  git_metaphor ×1, benchmark ×1). The three-dimensional taxonomy
  does not change.
- **SQ2:** SWE-bench Verified retained (Wang, Zhang). Comparability
  unchanged — the same heterogeneity issues persist.
- **SQ3:** Retained gains: Wang RepoMem +3.4pp, Zhang DGM +30.0pp.
  CTIM-Rover (Lindenbauer) removed — CTIM-specific degradation
  evidence is lost, but Deshpande (workshop) still provides
  degradation evidence from off-the-shelf memory components.
- **SQ4:** Detailed cost reduced to Wang RepoMem ($0.58–$0.89/example).
  EET, MemGovern, and GCC are lost — findings SQ4-B and SQ4-C would
  lose support.
- **SQ5:** Negative results retained: Deshpande (Mem0/Zep do not
  improve), Shen TALM (simple-task degradation). Finding SQ5-A
  partially sustained.

**Conclusion S1:** Excluding preprints would eliminate 86% of the
corpus. The main findings (positive gains, diminishing returns on
strong baselines, noise-induced degradation) are sustained
qualitatively by the 4 remaining studies, but with very limited
evidence. Cost findings (SQ4) and the detailed taxonomy (SQ1) would
be substantially weakened. **No main conclusion inverts**, but
confidence would be drastically reduced.

### S2 — Excluding Studies with Quality <3/6

2 studies excluded: Bui/OpenDev (2.0) and Du survey (2.5).

- **SQ1:** OpenDev (`text_notes`) removed — the category becomes
  empty, but the global taxonomy does not change. Du (survey) was
  already excluded from the primary architecture analysis.
- **SQ2–SQ4:** No impact — neither contributes quantitative data.
- **SQ5:** No impact — OpenDev does not report negative results with
  empirical data.

**Conclusion S2:** Excluding the 2 low-quality studies (<3/6)
**does not alter any finding**. Both contribute only qualitative
descriptions, and their removal does not affect the quantitative
syntheses.

---

## Per-Finding Certainty Assessment

Scale: **High** (≥3 studies of quality ≥4/6 converge), **Moderate**
(2 studies or variable quality), **Low** (single study or conflicting
evidence).

| Finding | Certainty | Rationale |
|---------|-----------|-----------|
| SQ1-A: Experience banks dominate (46%) | High | 11 independent studies, direct count |
| SQ1-B: Hybrid temporal scope predominates (58%) | High | 14 studies, direct classification |
| SQ1-C: LLM as controller predominates (54%) | High | 13 studies, direct classification |
| SQ1-D: Emerging executable substrates | Low | Only 3 studies (GBT, Live-SWE, DGM) |
| SQ1-E: Dominant hybrid retrieval | High | 11 studies |
| SQ1-F: Cross-agent sharing unexplored | High | 23/24 studies report `no` |
| SQ2-A: Dominant SWE-bench Verified | High | 14/21 studies with benchmark |
| SQ2-D: Gap 1 confirmed (zero head-to-head comparisons) | High | Exhaustive verification of 28 studies |
| SQ3-A: Universally positive gains | High | 19 controlled comparisons, zero inversions |
| SQ3-B: Diminishing returns on strong baselines | Moderate | Pattern observed but not formally tested; correlation, not causation |
| SQ3-C: Consistent gains across LLMs | Moderate | 2 studies with multi-LLM evaluation (Shen Struct. 4 LLMs, MemGovern 7 LLMs) |
| SQ4-A: 57% do not report detailed cost | High | Direct count |
| SQ4-B: Bimodal cost-memory relationship | Moderate | 12 studies with cost data, clear pattern but not all report both metrics |
| SQ4-D: Absence of explicit Pareto frontier | High | Exhaustive verification |
| SQ5-A: 32% report degradation | High | 9 studies with direct evidence |
| SQ5-B: Complexity ≠ larger gain | Moderate | Cross-study inference; benchmarks and models differ |
| SQ5-D: Retrieval calibration is critical | Moderate | 2 studies with direct evidence (Chen k>1, Shen category isolation) |
| T-A: Field dominated by preprints (86%) | High | Direct count |
| T-C: Gap 1 persists | High | Exhaustive verification |
