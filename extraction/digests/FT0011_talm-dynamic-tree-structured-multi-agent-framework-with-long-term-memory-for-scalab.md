# TALM: Dynamic Tree-Structured Multi-Agent Framework with Long-Term Memory for Scalable Code Generation

## Identifiers

- Included ID: I039
- Full-text ID: FT0011
- Extraction key: `shen2025talm`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `banco_experiencia`.
- Storage format: Vector database com entries contendo: task description, reasoning process, generated code, e tree depth metadata. Consolidação automática: entries com similaridade > 0.95 são merged pelo LLM em entry representativa unificada (shared problem descriptions + solution patterns + code); originais removidas para evitar crescimento descontrolado. Retrieval: top-3 ANN search filtrado por tree depth.
- Retrieval method: `embeddings`.
- Evaluation method: `benchmark`.
- Benchmarks: HumanEval (164), BigCodeBench (1140), ClassEval (100)
- Main result: TALM com memória atinge 92.55% HumanEval, 53.27% BigCodeBench e 38.00% ClassEval (class level) com GPT-4o, superando todos baselines. Memória contribui mais em tarefas complexas (BigCodeBench +2.14pp, ClassEval class +2.00pp). Decomposição estruturada em árvore com re-reasoning localizado complementa acumulação de experiência.
- Performance versus baseline: +3.17pp BigCodeBench vs Direct (53.27% vs 50.10% GPT-4o); +5.00pp ClassEval class vs Direct (38.00% vs 33.00%); +2.00pp ClassEval class vs MapCoder (38.00% vs 36.00%); ~50% menos tokens que MapCoder
- Cost reporting: `sim_parcial`; ~50% menos tokens totais que MapCoder em ClassEval; overhead marginal de memória vs TALM sem memória

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0011_TA00129_talm-dynamic-tree-structured-multi-agent-framework-with-long-term-memory-for-sca.txt`
- JSON: `extraction/json/FT0011_talm-dynamic-tree-structured-multi-agent-framework-with-long-term-memory-for-scalab.json`
