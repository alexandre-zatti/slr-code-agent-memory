# Search Performance Normalization Summary

Generated from `analysis/performance-delta-candidates.tsv` on 2026-04-29.
This artifact supports SQ3 synthesis only. It selects one representative effect per broad controlled record and preserves heterogeneous units instead of pooling effects.

## Coverage

- Broad controlled records: 76
- Records with a numeric representative value: 71
- Records without a scalar numeric representative value: 5

## Normalization Status

| Status | N |
| --- | ---: |
| `normalized_manual` | 47 |
| `normalized_candidate` | 22 |
| `insufficient_numeric_baseline` | 2 |
| `qualitative_only` | 2 |
| `count_only` | 1 |
| `low_confidence` | 1 |
| `lower_bound` | 1 |

## Direction

| Direction | N |
| --- | ---: |
| `positive` | 71 |
| `positive_lower_is_better` | 2 |
| `mixed` | 1 |
| `near_parity_with_efficiency_gain` | 1 |
| `negative` | 1 |

## Metric Family

| Metric family | N |
| --- | ---: |
| `task_success_or_accuracy` | 40 |
| `benchmark_score` | 3 |
| `efficiency_speedup` | 3 |
| `optimization_score` | 3 |
| `research_workflow_score` | 3 |
| `efficiency_or_resource_use` | 2 |
| `security_or_safety_rate` | 2 |
| `task_success_or_quality` | 2 |
| `aggregate_task_score` | 1 |
| `benchmark_faithfulness_or_guardrail` | 1 |
| `code_quality_score` | 1 |
| `coding_benchmark_score` | 1 |
| `game_generation_quality` | 1 |
| `model_training_metric` | 1 |
| `multi_agent_task_score` | 1 |
| `optimization_cost_or_objective` | 1 |
| `optimization_gap` | 1 |
| `optimization_success_rate` | 1 |
| `preference_or_judge_score` | 1 |
| `preference_or_quality_score` | 1 |
| `preference_or_win_rate` | 1 |
| `program_discovery_score` | 1 |
| `quality_efficiency_tradeoff` | 1 |
| `repair_success_count` | 1 |
| `repository_change_quality` | 1 |
| `security_or_repair_success` | 1 |

## Comparison Scope

| Comparison scope | N |
| --- | ---: |
| `external_nonmemory_baseline` | 26 |
| `memory_ablation` | 23 |
| `memory_ablation_or_no_memory_baseline` | 13 |
| `initial_agent_baseline` | 2 |
| `retrieval_ablation` | 2 |
| `case_base_ablation` | 1 |
| `experience_variant_comparison` | 1 |
| `knowledge_ablation` | 1 |
| `memory_guided_baseline` | 1 |
| `memory_or_specification_ablation` | 1 |
| `memory_topology_ablation` | 1 |
| `memory_transfer` | 1 |
| `self_improvement_baseline` | 1 |
| `self_improvement_external_baseline` | 1 |
| `self_improvement_transfer` | 1 |

## Unit

| Unit | N |
| --- | ---: |
| `percentage_points` | 38 |
| `points` | 8 |
| `score_points` | 8 |
| `qualitative` | 4 |
| `accuracy_points` | 2 |
| `pass_at_1_points` | 2 |
| `percentage_points_reported_as_percent` | 2 |
| `x_speedup` | 2 |
| `bugs_of_6` | 1 |
| `cases` | 1 |
| `cycles_reduced` | 1 |
| `pass_at_3_proportion_points` | 1 |
| `pass_score_points` | 1 |
| `percent` | 1 |
| `percent_of_baseline_quality` | 1 |
| `percent_reduction` | 1 |
| `proportion_points` | 1 |
| `relative_percent` | 1 |

## Use Notes

- Do not pool `normalized_delta_value` across rows; metric families and units are heterogeneous.
- For strict controlled rows, representative effects prefer explicit memory/no-persistence ablations when available.
- Negative and mixed evidence is retained rather than filtered out.
- `qualitative_only`, `insufficient_numeric_baseline`, `count_only`, `lower_bound`, and `low_confidence` rows require prose-level handling in SQ3.
