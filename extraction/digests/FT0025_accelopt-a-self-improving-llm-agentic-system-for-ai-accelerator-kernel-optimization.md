# AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization

## Identifiers

- Included ID: I009
- Full-text ID: FT0025
- Extraction key: `zhang2025accelopt`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `banco_experiencia`.
- Storage format: Fila de experience items com capacidade fixa (ExpN): cada item contém par slow-fast kernel (pseudocódigo dos segmentos otimizados) + estratégia de otimização generalizada em NL gerada pelo summarizer. Itens positivos (speedup > t_pos) e negativos (slowdown > 1/t_neg) curados separadamente.
- Retrieval method: `carga_total`.
- Evaluation method: `benchmark`.
- Benchmarks: NKIBench (14 kernels de workloads LLM reais em AWS Trainium 1 e 2)
- Main result: AccelOpt melhora throughput médio de 49% para 61% do pico no Trainium 1 e de 45% para 59% no Trainium 2, igualando Claude Sonnet 4 com custo 26x menor usando modelos open-source.
- Performance versus baseline: +12pp throughput médio no Trainium 1 (49%→61%); +14pp no Trainium 2 (45%→59%) vs kernels iniciais; equivalente a Claude Sonnet 4
- Cost reporting: `sim_detalhado`; 26x mais barato que Claude Sonnet 4 com desempenho equivalente ($139 AccelOpt vs ~$1733 Claude Sonnet 4); memória economiza 16-17% do custo vs beam search puro

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0025_TA00450_accelopt-a-self-improving-llm-agentic-system-for-ai-accelerator-kernel-optimizat.txt`
- JSON: `extraction/json/FT0025_accelopt-a-self-improving-llm-agentic-system-for-ai-accelerator-kernel-optimization.json`
