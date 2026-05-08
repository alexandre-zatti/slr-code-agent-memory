# Search Post-Extraction Recomputed Counts

Date: 2026-04-29

## Scope

This report recomputes deterministic counts from `extraction/extracted-data.tsv`.
It does not infer final controlled-comparison or quality labels where the extraction
TSV still marks those fields as pending or `NR`.

## Denominators

- Included search records with extraction rows: 95.
- Architecture denominator: 85.
- Contextual/boundary records outside the architecture denominator: 10.

## Architecture Taxonomy

### Architecture Status

| Value | N | % |
| --- | ---: | ---: |
| `arch_experience_bank` | 34 | 40.0% |
| `arch_skill_rule_library` | 15 | 17.6% |
| `arch_self_evolution_archive` | 12 | 14.1% |
| `arch_repository_memory` | 6 | 7.1% |
| `arch_persistent_workspace_state` | 5 | 5.9% |
| `arch_knowledge_graph_case_base` | 4 | 4.7% |
| `arch_shared_memory` | 4 | 4.7% |
| `arch_security_memory` | 3 | 3.5% |
| `arch_structured_knowledge_base` | 1 | 1.2% |
| `arch_user_model_memory` | 1 | 1.2% |

### Legacy Architecture Type

| Value | N | % |
| --- | ---: | ---: |
| `banco_experiencia` | 40 | 47.1% |
| `outro` | 29 | 34.1% |
| `hibrido` | 8 | 9.4% |
| `grafo_conhecimento` | 5 | 5.9% |
| `git_metafora` | 3 | 3.5% |

### Temporal Scope

| Value | N | % |
| --- | ---: | ---: |
| `hibrida` | 44 | 51.8% |
| `procedural` | 22 | 25.9% |
| `semantica` | 14 | 16.5% |
| `episodica` | 5 | 5.9% |

### Representational Substrate

| Value | N | % |
| --- | ---: | ---: |
| `estruturado` | 36 | 42.4% |
| `hibrido` | 23 | 27.1% |
| `executavel` | 13 | 15.3% |
| `texto_contexto` | 9 | 10.6% |
| `grafo` | 2 | 2.4% |
| `latente` | 1 | 1.2% |
| `texto` | 1 | 1.2% |

### Control Policy

| Value | N | % |
| --- | ---: | ---: |
| `self_control_llm` | 40 | 47.1% |
| `heuristica` | 30 | 35.3% |
| `aprendida` | 15 | 17.6% |

### Retrieval Method

| Value | N | % |
| --- | ---: | ---: |
| `hibrido` | 37 | 43.5% |
| `embeddings` | 16 | 18.8% |
| `outro` | 14 | 16.5% |
| `carga_total` | 10 | 11.8% |
| `consulta_estruturada` | 4 | 4.7% |
| `bm25` | 2 | 2.4% |
| `grafo` | 1 | 1.2% |
| `tf_idf` | 1 | 1.2% |

### Memory Granularity

| Value | N | % |
| --- | ---: | ---: |
| `tarefa` | 50 | 58.8% |
| `repositorio` | 19 | 22.4% |
| `subtarefa` | 5 | 5.9% |
| `funcao` | 4 | 4.7% |
| `outro` | 3 | 3.5% |
| `agente` | 2 | 2.4% |
| `api` | 1 | 1.2% |
| `commit` | 1 | 1.2% |

### Cross-Agent Sharing

| Value | N | % |
| --- | ---: | ---: |
| `nao` | 50 | 58.8% |
| `sim` | 33 | 38.8% |
| `nao_aplicavel` | 2 | 2.4% |

## Evaluation And Benchmarks

### Evaluation Method Category

| Value | N | % |
| --- | ---: | ---: |
| `benchmark` | 82 | 96.5% |
| `mixed` | 2 | 2.4% |
| `case_study` | 1 | 1.2% |

### Benchmark Markers

| Value | N | % |
| --- | ---: | ---: |
| `SWE-bench Verified` | 22 | 25.9% |
| `SWE-bench Lite` | 8 | 9.4% |
| `HumanEval` | 7 | 8.2% |
| `KernelBench` | 4 | 4.7% |
| `LiveCodeBench` | 4 | 4.7% |
| `MBPP` | 4 | 4.7% |
| `BigCodeBench` | 3 | 3.5% |
| `DS-1000` | 3 | 3.5% |
| `MATH` | 3 | 3.5% |
| `Terminal-Bench` | 3 | 3.5% |
| `WebArena` | 3 | 3.5% |
| `CyberGym` | 2 | 2.4% |
| `LoCoMo` | 2 | 2.4% |
| `MLE-Bench` | 2 | 2.4% |
| `ResearchCodeBench` | 2 | 2.4% |
| `SUPER` | 2 | 2.4% |
| `SWE-Bench Pro` | 2 | 2.4% |
| `ScienceAgentBench` | 2 | 2.4% |
| `ALE-Bench` | 1 | 1.2% |
| `AppWorld` | 1 | 1.2% |
| `DafnyBench` | 1 | 1.2% |
| `DevOps-Gym` | 1 | 1.2% |
| `HumanEvalDafny` | 1 | 1.2% |
| `NKIBench` | 1 | 1.2% |
| `PaperBench` | 1 | 1.2% |
| `tau2-bench` | 1 | 1.2% |

## Controlled-Comparison Recode Status

| Value | N | % |
| --- | ---: | ---: |
| `yes_no_persistence_or_memory_ablation` | 56 | 65.9% |
| `yes_nonmemory_external_baseline` | 20 | 23.5% |
| `no_no_persistence_or_nonmemory_baseline` | 9 | 10.6% |

- Strict no-persistence or memory-ablation comparators: 56 of 85 (65.9%).
- External/non-memory architecture comparators: 20 of 85 (23.5%).
- Broad controlled-comparison candidates: 76 of 85 (89.4%).
- Boundary records needing PDF review before final denominator use: 0.
- Architecture records still marked `pending_extraction` for controlled-comparison status: 0.

Use the strict denominator when the claim requires a same-system
no-memory/no-persistence or memory-ablation comparator. Use the broad
candidate denominator only if external non-memory architecture baselines
are accepted in the target synthesis. Boundary records are excluded until
PDF review resolves them.

## Cost And Efficiency

| Value | N | % |
| --- | ---: | ---: |
| `sim_parcial` | 32 | 37.6% |
| `nao` | 26 | 30.6% |
| `sim_detalhado` | 19 | 22.4% |
| `sim` | 8 | 9.4% |

## Negative Or Adverse Results

| Value | N | % |
| --- | ---: | ---: |
| `sim` | 59 | 69.4% |
| `nao` | 26 | 30.6% |

## Quality Score Distribution

- Architecture records with numeric quality scores: 85.
- Architecture records needing manual quality scoring: 0.
- Median quality score: 5.0 of 6.0.
- Records below 3.0/6.0 for sensitivity exclusion: 0.

| Value | N | % |
| --- | ---: | ---: |
| `5.0` | 31 | 36.5% |
| `5.5` | 24 | 28.2% |
| `4.5` | 22 | 25.9% |
| `4.0` | 5 | 5.9% |
| `3.5` | 2 | 2.4% |
| `6.0` | 1 | 1.2% |

Quality scores are final only when `analysis/quality-assessment.tsv`
contains Q1-Q6 values and `final_score` for every architecture record.

## Record-Level Flag File

- `analysis/post-extraction-recompute-records.tsv` records per-study
  flags for controlled-comparison status, baseline text, quality-score status,
  cost reporting, adverse-result reporting, and benchmark markers.

## Next Manual Pass

1. Rebuild benchmark, cost, adverse-result, and performance-delta synthesis tables.
2. Create the search synthesis matrix from the finalized extraction TSV.
3. Update PRISMA and manuscript claims only from saved search artifacts.
