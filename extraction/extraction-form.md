# Data Extraction Form

Template for extracting structured data from each included paper.

## Fields

### Metadata
| Field | Description |
|-------|-------------|
| `id` | Unique identifier (BibTeX citation key) |
| `authors` | Author list |
| `year` | Publication year |
| `title` | Full title |
| `venue` | Conference or journal |
| `venue_type` | conference \| journal \| preprint \| workshop |

### Persistence Architecture
| Field | Allowed values |
|-------|----------------|
| `architecture_type` | text_notes \| experience_bank \| ast_guided \| knowledge_graph \| os_paging \| git_metaphor \| hybrid \| other |
| `temporal_scope` | episodic \| semantic \| procedural \| hybrid — taxonomy adapted from Du (2026) |
| `representational_substrate` | text_context \| vector \| structured \| executable \| hybrid — taxonomy adapted from Du (2026) |
| `control_policy` | heuristic \| llm_self_control \| learned — taxonomy adapted from Du (2026) |
| `storage_format` | free text — concrete format (markdown, JSON, vector DB, graph, AST k-v, etc.) |
| `retrieval_method` | bm25 \| embeddings \| ast_intersection \| full_load \| graph_traversal \| hybrid \| other |
| `memory_granularity` | task \| subtask \| commit \| function \| file \| repository \| other |
| `cross_agent_sharing` | yes \| no \| not_applicable — is memory shareable across distinct agents? |

### Agent and Model
| Field | Allowed values |
|-------|----------------|
| `agent_framework` | openhands \| swe_agent \| custom \| other — free text if other |
| `llm_used` | free text — LLM model(s) used as backbone for the agent |
| `autonomy_level` | autonomous \| interactive \| semi_autonomous |
| `open_source` | yes \| no \| partial — availability of the source code |

### Evaluation
| Field | Allowed values |
|-------|----------------|
| `evaluation_method` | benchmark \| case_study \| user_study \| mixed |
| `benchmarks_used` | free text — list of benchmarks (SWE-bench Verified, SWE-Bench-CL, HumanEval, etc.) |
| `performance_metrics` | free text — list of metrics (Pass@1, Acc@5, Resolve@1, etc.) |
| `continual_learning_metrics` | free text — continual learning metrics when applicable (ACC, F, FT, BWT, CL-F1, TUE) |
| `baseline_compared` | free text — compared baseline(s) |

### Cost and Efficiency
| Field | Allowed values |
|-------|----------------|
| `input_tokens_per_task` | numeric or free text — average input tokens per task |
| `output_tokens_per_task` | numeric or free text — average output tokens per task |
| `memory_size_over_time` | free text — memory growth (bounded, unbounded, compacted) |
| `cost_per_task` | free text — monetary cost per task when reported |
| `token_reduction` | free text — token reduction percentage when reported |
| `reports_cost_data` | yes_detailed \| yes_partial \| no — level of detail in cost data |

### Results
| Field | Allowed values |
|-------|----------------|
| `main_result` | free text — main result |
| `performance_vs_baseline` | free text — percentage gain/loss vs. baseline without persistence |
| `cost_vs_baseline` | free text — cost difference vs. baseline when reported |
| `negative_result` | yes \| no — did memory degrade performance in any scenario? |

### Quality and Limitations
| Field | Allowed values |
|-------|----------------|
| `quality_score` | 0–6 (per protocol §8 checklist) |
| `limitations` | free text — limitations reported by the authors |
| `validity_threats` | free text — reported validity threats |
| `gap_relevance` | gap1_comparison \| gap2_cost \| gap3_complexity \| multiple — which gap this paper addresses |

## Convention for Missing Data

- **`NR`** (Not Reported): the paper does not mention this datum
- **`NA`** (Not Applicable): the field does not apply to this system
- Concrete value when available

This convention applies especially to the Cost and Efficiency fields,
which are frequently not reported.

## Note on `validity_threats`

If the paper does not have a formal "threats to validity" section, infer
from the reported limitations and from the typical threats: single
model, single benchmark, absence of production testing, sample size.

## TSV Format

Header of `data.tsv`:
```
id	authors	year	title	venue	venue_type	architecture_type	temporal_scope	representational_substrate	control_policy	storage_format	retrieval_method	memory_granularity	cross_agent_sharing	agent_framework	llm_used	autonomy_level	open_source	evaluation_method	benchmarks_used	performance_metrics	continual_learning_metrics	baseline_compared	input_tokens_per_task	output_tokens_per_task	memory_size_over_time	cost_per_task	token_reduction	reports_cost_data	main_result	performance_vs_baseline	cost_vs_baseline	negative_result	quality_score	limitations	validity_threats	gap_relevance
```

## Extraction Procedure

1. Researcher reads each PDF and populates a per-paper JSON file in
   `extraction/per-paper/{key}.json` with the 37 fields
2. Programmatic validation of enum-typed fields
3. Cross-field consistency checks (cost reporting, NA conventions,
   continual-learning metrics)
4. Per-paper JSON files compiled into `extraction/data.tsv`
