# EET: Experience-Driven Early Termination for Cost-Efficient Software Engineering Agents

## Identifiers

- Included ID: I059
- Full-text ID: FT0035
- Extraction key: `guo2026eet`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `banco_experiencia`.
- Storage format: Experience objects estruturados (JSON: issue_id, task_description, execution_summary, evaluation_result, confidence, confidence_reason); abstrações de trajetórias de resolução bem-sucedidas armazenadas em experience base
- Retrieval method: `tf_idf`.
- Evaluation method: `benchmark`.
- Benchmarks: SWE-bench Verified (500 tarefas; 207 de SWE-bench Lite para geração de experiência)
- Main result: EET reduz custo total em 19.3-55.1% (média 31.8%) em 3 agentes × 2 LLMs, com perda negligível de resolve rate (máximo 0.2%). Early termination identifica oportunidades em 11.3% dos issues em média.
- Performance versus baseline: +2.7% resolve rate médio vs agentes sem EET; Agentless beneficia mais (+7.5% abs com GPT-5-mini)
- Cost reporting: `sim_detalhado`; -31.8% custo total médio vs sem EET; vs Turn-control: -31.8% vs -41.4% (Turn-control reduz mais custo mas degrada resolve rate em -10.7%)

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0035_TA00171_eet-experience-driven-early-termination-for-cost-efficient-software-engineering.txt`
- JSON: `extraction/json/FT0035_eet-experience-driven-early-termination-for-cost-efficient-software-engineering-age.json`
