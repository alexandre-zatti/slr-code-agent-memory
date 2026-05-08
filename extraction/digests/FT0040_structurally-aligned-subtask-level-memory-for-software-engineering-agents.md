# Structurally Aligned Subtask-Level Memory for Software Engineering Agents

## Identifiers

- Included ID: I087
- Full-text ID: FT0040
- Extraction key: `shen2026structurally`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `banco_experiencia`.
- Storage format: Memory state S_sub como repositório de subtask entries estruturadas: cada entry m = (z, d, e) onde z = categoria funcional (ANALYZE, REPRODUCE, EDIT, VERIFY), d = descrição estruturada (objective + mechanism keywords), e = experiência abstrata transferível extraída pelo LLM Extractor. Indexado por embeddings; atualizado online após cada subtask completion.
- Retrieval method: `hibrido`.
- Evaluation method: `benchmark`.
- Benchmarks: SWE-bench Verified (500)
- Main result: Subtask-level memory melhora Pass@1 em +4.7pp em média sobre vanilla agents em 4 LLMs no SWE-bench Verified. Ganhos são maiores em tarefas Hard (+8.7pp, >28 steps) e crescem com experiências acumuladas. Category isolation é crítica: global retrieval perde +2.3pp.
- Performance versus baseline: +6.8pp Gemini 2.5 Pro (60.3% vs 53.5%); +5.6pp Gemini 2.5 Flash (41.9% vs 36.3%); +3.9pp Claude 3.7 Sonnet (56.1% vs 52.2%); +2.3pp Claude 4.0 Sonnet (65.8% vs 63.5%); média +4.7pp
- Cost reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0040_TA00207_structurally-aligned-subtask-level-memory-for-software-engineering-agents.txt`
- JSON: `extraction/json/FT0040_structurally-aligned-subtask-level-memory-for-software-engineering-agents.json`
