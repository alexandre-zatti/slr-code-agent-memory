# SWE-Exp: Experience-Driven Software Issue Resolution

## Identifiers

- Included ID: I037
- Full-text ID: FT0009
- Extraction key: `chen2025sweexp`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `banco_experiencia`.
- Storage format: Multi-facet Experience Bank em vector database (embeddings Multilingual-E5-Large): cada experiência é dicionário com issue_type (label descritivo, e.g. VariableReferenceError), description (condições e cenários), e perspective ou modification (insights abstratos). Comprehension experiences guiam diagnóstico (perspectiva do problema); modification experiences guiam edição segura de código (estratégias de reparo). Extração offline via Experiencer agent de trajetórias successful e failed.
- Retrieval method: `hibrido`.
- Evaluation method: `benchmark`.
- Benchmarks: SWE-Bench Verified (500)
- Main result: SWE-Exp atinge 73.0% Pass@1 com Claude 4 Sonnet e 42.0% com DeepSeek-V3-0324 no SWE-bench Verified, superando todos baselines. Comprehension e modification experiences contribuem independentemente (+3.2% e +2.6%); extração de experiências é o componente mais crítico (-6.0% sem ela).
- Performance versus baseline: +2.2pp vs SWE-Search com Claude 4 Sonnet (73.0% vs 70.8%); +6.6pp vs SWE-Search com DeepSeek (42.0% vs 35.4%); +3.2pp vs SWE-Agent com DeepSeek (42.0% vs 38.8%); +4.2pp vs EvoCoder com DeepSeek (42.0% vs 38.0%)
- Cost reporting: `sim_detalhado`; $0.13 vs $0.12 per issue com DeepSeek (+8.3%); wall time 15min49s vs 12min37s (+25%); retrieval+rerank overhead 37.5s avg

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0009_TA00096_swe-exp-experience-driven-software-issue-resolution.txt`
- JSON: `extraction/json/FT0009_swe-exp-experience-driven-software-issue-resolution.json`
