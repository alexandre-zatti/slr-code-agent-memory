# Data Extraction Form

This form defines the canonical extraction schema for the current corpus.
All JSON values are strings.
Use `NR` when the paper does not report a datum and `NA` when the field does
not apply.
Do not invent cost, token, benchmark, source-code, or quality data.

## Corpus And Provenance Fields

| Field | Description |
| --- | --- |
| `included_id` | Included-study identifier, e.g. `I001`. |
| `full_text_id` | Full-text screening identifier, e.g. `FT0001`. |
| `screening_id` | Title/abstract screening identifier. |
| `dedup_group` | Deduplication group. |
| `study_role` | `architecture`, `contextual_survey`, `contextual_benchmark`, `contextual_assessment`, `contextual_security`, `contextual_human_artifact`, or `boundary_case_study`. |
| `architecture_status` | Architecture-family/status label from `classification-decisions.tsv`. |
| `controlled_comparison_status` | Comparator status after extraction and recoding. |
| `classification_status` | Classification provenance, e.g. `classified_from_full_text_rationale` or `classified_from_prior_prefill_recheck_required`. |
| `architecture_denominator_decision` | `include_architecture`, `exclude_contextual`, `boundary_pending`, or `exclude_after_extraction`. |
| `contextual_role` | Contextual contribution when not an architecture; otherwise `NA`. |
| `full_text_rationale` | Full-text screening rationale used for inclusion. |
| `source_routes` | Databases or routes that retrieved the record. |
| `source_files` | Saved raw files that contain the record. |
| `route_provenance` | Route-level provenance such as arXiv categories, Scopus family, or citation route. |
| `extraction_verification_status` | `verified_from_full_text`, `verified_prior_extraction`, `pending_recheck`, or `needs_pdf_check`. |
| `extractor_notes` | Short notes about boundary decisions, missing data, or fields needing later verification. |

## Extraction Fields

```text
id
autores
ano
titulo
venue
tipo_venue
tipo_arquitetura
escopo_temporal
substrato_representacional
politica_controle
formato_armazenamento
metodo_recuperacao
granularidade_memoria
compartilhamento_entre_agentes
framework_agente
llm_utilizado
nivel_autonomia
codigo_aberto
metodo_avaliacao
benchmarks_utilizados
metricas_desempenho
metricas_cl
baseline_comparado
tokens_entrada_por_tarefa
tokens_saida_por_tarefa
tamanho_memoria_ao_longo_tempo
custo_por_tarefa
reducao_tokens
reporta_dados_custo
resultado_principal
desempenho_vs_baseline
custo_vs_baseline
resultado_negativo
pontuacao_qualidade
limitacoes
ameacas_validade
relevancia_gaps
```

## TSV Header

`extracted-data.tsv` must use this exact header:

```text
included_id	full_text_id	screening_id	dedup_group	study_role	architecture_status	controlled_comparison_status	classification_status	architecture_denominator_decision	contextual_role	full_text_rationale	source_routes	source_files	route_provenance	extraction_verification_status	extractor_notes	id	autores	ano	titulo	venue	tipo_venue	tipo_arquitetura	escopo_temporal	substrato_representacional	politica_controle	formato_armazenamento	metodo_recuperacao	granularidade_memoria	compartilhamento_entre_agentes	framework_agente	llm_utilizado	nivel_autonomia	codigo_aberto	metodo_avaliacao	benchmarks_utilizados	metricas_desempenho	metricas_cl	baseline_comparado	tokens_entrada_por_tarefa	tokens_saida_por_tarefa	tamanho_memoria_ao_longo_tempo	custo_por_tarefa	reducao_tokens	reporta_dados_custo	resultado_principal	desempenho_vs_baseline	custo_vs_baseline	resultado_negativo	pontuacao_qualidade	limitacoes	ameacas_validade	relevancia_gaps
```

## Extraction Order

1. Extract contextual and boundary records first to lock the architecture
   denominator.
2. Verify any prefilled extraction against the current full text before marking
   it `verified_prior_extraction`.
3. Extract architecture candidates from full text into `extraction/json/*.json`.
4. Compile `extraction/json/*.json` into `extraction/extracted-data.tsv`:

```bash
python extraction/compile_extracted_data.py
```

5. Update `extraction/digests/INDEX.md` after digest changes.
