# MEMCoder: Multi-dimensional Evolving Memory for Private-Library-Oriented Code Generation

## Identifiers

- Included ID: I069
- Full-text ID: FT0056
- Extraction key: `li2026memcoder`
- Role: `architecture`
- Architecture status: `arch_repository_memory`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_repository_memory`.
- Storage: task-level and API-level evolving memory with generated code, execution feedback, usage guidelines, code snippets, and dynamic guideline weights.
- Evaluation: NdonnxEval and NumbaEval, RAG baselines, continual-learning baselines, ablations, and token-cost analysis.
- Main result: average absolute Pass@1 gain of 16.31% when added to static RAG baselines.
- Performance versus baseline: Qwen2.5-Coder Naive RAG plus MEMCoder reaches 52.54 Pass@1 on NdonnxEval and 33.74 on NumbaEval, versus 27.22 and 23.16 for Naive RAG.
- Cost/token reporting: `sim_detalhado`; 17,111 additional total tokens per task on NumbaEval and about USD 0.46 extra for the 187-task benchmark.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0056_TA00486_memcoder-multi-dimensional-evolving-memory-for-private-library-oriented-code-gen.txt`
- JSON: `extraction/json/FT0056_memcoder-multi-dimensional-evolving-memory-for-private-library-oriented-code-genera.json`
