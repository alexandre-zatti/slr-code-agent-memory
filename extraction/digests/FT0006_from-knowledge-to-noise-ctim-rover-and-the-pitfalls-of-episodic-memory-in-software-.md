# From Knowledge to Noise: CTIM-Rover and the Pitfalls of Episodic Memory in Software Engineering Agents

## Identifiers

- Included ID: I022
- Full-text ID: FT0006
- Extraction key: `lindenbauer2025ctimrover`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `banco_experiencia`.
- Storage format: CTIM items (regras textuais destiladas de trajetórias bem-sucedidas via Knowledge Distillation com o1; general + repository-level) + trajetórias exemplares (full trajectory text) armazenadas em índice Milvus (Code-T5 embeddings)
- Retrieval method: `embeddings`.
- Evaluation method: `benchmark`.
- Benchmarks: SWE-bench Verified (subconjunto: 401 treino, 45 teste)
- Main result: AutoCodeRover 42% vs CTIM-Rover 40% (melhor config); CTIM only degrada para 31%. Memória episódica introduz ruído que degrada performance; itens CTIM ruidosos desviam o agente de explorações produtivas.
- Performance versus baseline: -2pp vs baseline (40% vs 42%); CTIM only -11pp (31% vs 42%)
- Cost reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0006_TA00077_from-knowledge-to-noise-ctim-rover-and-the-pitfalls-of-episodic-memory-in-softwa.txt`
- JSON: `extraction/json/FT0006_from-knowledge-to-noise-ctim-rover-and-the-pitfalls-of-episodic-memory-in-software-.json`
