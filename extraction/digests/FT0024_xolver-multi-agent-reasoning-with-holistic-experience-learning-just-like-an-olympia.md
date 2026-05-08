# Xolver: Multi-Agent Reasoning with Holistic Experience Learning Just Like an Olympiad Team

## Identifiers

- Included ID: I042
- Full-text ID: FT0024
- Extraction key: `hosain2025xolver`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `hibrido`.
- Storage format: Dual memory: (1) Episodic memory D_E — corpus externo de problemas passados com reasoning traces e soluções (OpenMathReason para math, cp-algorithms C++ para código), recuperável via BM25 ou self-retrieval paramétrico do LLM; atualizado com cada problema resolvido (Xolver+). (2) Intermediate shared memory D_S — buffer dinâmico de tamanho fixo (|D_S|=m) contendo top-m tuplas (reasoning trace T, response R, feedback (T_S, s), agent a) ranqueadas por score s do Judge agent; evolui a cada iteração intra-problema.
- Retrieval method: `hibrido`.
- Evaluation method: `benchmark`.
- Benchmarks: GSM8K, AIME 2024 (30 problemas), AIME 2025 (30 problemas), Math-500, LiveCodeBench v5
- Main result: Xolver com o3-mini-medium atinge 97.1% GSM8K, 93.8% AIME'24, 89.4% AIME'25, 99.2% Math-500 e 87.3% LiveCodeBench, superando consistentemente todos baselines incluindo frameworks especializados. Com o3-mini-high, estabelece novos SOTA: 98.1% GSM8K, 94.4% AIME'24, 93.7% AIME'25, 99.8% Math-500, 91.6% LiveCodeBench. Memória episódica cross-problem contribui +3.5pp em média.
- Performance versus baseline: +18.6pp AIME'24 avg vs o3-mini-medium LongCoT (93.8% vs 75.8%); +13.6pp AIME'25 (89.4% vs 75.8%); +21.0pp LiveCodeBench (87.3% vs 66.3%); supera o4-mini-high em AIME'24 (93.8% vs 93.4%) e LiveCodeBench (87.3% vs 69.5%)
- Cost reporting: `sim_parcial`; ~1.5× tokens vs Search-o1; complexidade de update O(mI) vs O(n²) do CheatSheet; runtime parallelizável entre agentes

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0024_TA00449_xolver-multi-agent-reasoning-with-holistic-experience-learning-just-like-an-olym.txt`
- JSON: `extraction/json/FT0024_xolver-multi-agent-reasoning-with-holistic-experience-learning-just-like-an-olympia.json`
