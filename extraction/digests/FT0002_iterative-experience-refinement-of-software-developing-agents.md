# Iterative Experience Refinement of Software-Developing Agents

## Identifiers

- Included ID: I005
- Full-text ID: FT0002
- Extraction key: `qian2024iterative`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `banco_experiencia`.
- Storage format: Pool de experiências shortcut como pares chave-valor: solution-to-instruction (conhecimento do agente instructivo) e instruction-to-solution (conhecimento do agente responsivo). Shortcuts extraídos de nós não-adjacentes na cadeia de execução. Embeddings via text-embedding-ada-002 para recuperação vetorial.
- Retrieval method: `embeddings`.
- Evaluation method: `benchmark`.
- Benchmarks: SRDD dataset (1200 descrições de requisitos de software, 40 categorias, dividido em 6 batches)
- Main result: IER melhora Quality de 0.4665 (ChatDev) para 0.6372 (IER-Successive), +36.6% relativo. Padrão cumulativo oferece estabilidade maior que successive; eliminação de experiências atinge desempenho superior com apenas 11.54% do pool original.
- Performance versus baseline: +36.6% Quality vs ChatDev (0.6372 vs 0.4665); +10.3% Quality vs ECL (0.6372 vs 0.5775); +11% Executability vs ECL (0.9146 vs 0.8643)
- Cost reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0002_TA00018_iterative-experience-refinement-of-software-developing-agents.txt`
- JSON: `extraction/json/FT0002_iterative-experience-refinement-of-software-developing-agents.json`
