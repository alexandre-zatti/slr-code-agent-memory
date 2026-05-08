# Improving Code Localization with Repository Memory

## Identifiers

- Included ID: I025
- Full-text ID: FT0023
- Extraction key: `wang2025repositorymemory`
- Role: `architecture`
- Architecture status: `arch_repository_memory`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `git_metafora`.
- Storage format: Corpus de commits recentes (episódica: mensagens + patches + issues linkadas, buscável via BM25 com tokenizer LLM) + sumários de funcionalidade de arquivos ativos (semântica: texto NL gerado por LLM para top-200 arquivos mais editados)
- Retrieval method: `bm25`.
- Evaluation method: `benchmark`.
- Benchmarks: SWE-bench-verified (500 exemplos, 12 repositórios), SWE-bench-live (130 exemplos, 62 repositórios)
- Main result: Acc@5 76.5% no SWE-bench-verified (+4.9% vs LocAgent); memória episódica e semântica contribuem de forma complementar; agente muda comportamento de exploração bruta para investigação guiada por hipóteses
- Performance versus baseline: +4.9% Acc@5 absoluto vs LocAgent em SWE-bench-verified; +3.1% em SWE-bench-live; resolve rate +3.4% em end-to-end (40.4% vs 37.0%)
- Cost reporting: `sim_parcial`; Custo maior em problemas difíceis ($0.54→$0.89 quando LocAgent falha); alta variância por exemplo; memória é investimento estratégico em problemas difíceis

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0023_TA00371_improving-code-localization-with-repository-memory.txt`
- JSON: `extraction/json/FT0023_improving-code-localization-with-repository-memory.json`
