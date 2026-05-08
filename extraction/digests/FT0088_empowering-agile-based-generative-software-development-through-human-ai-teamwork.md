# Empowering Agile-Based Generative Software Development through Human-AI Teamwork

## Identifiers

- Included ID: I003
- Full-text ID: FT0088
- Extraction key: `zhang2024agilegen`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Memory pool of prior user decision-making scenarios and requirements/scenario entries, populated after user scenario decisions and reused as human experiential knowledge for similar new requirements.
- Evaluation: 50projects50days; SRDD; 30 website-application cases; 10 real user-created projects; 20 sampled SRDD projects using CodeBLEU, Pass@1, execution time, Pro_Code, cost, Code Executability, User Experience Questionnaire.
- Main result: AgileGen uses Gherkin-centered agile generation plus a memory pool of user decision scenarios. On 50projects50days, AgileGen GPT3.5 reports CodeBLEU 0.339 and Pass@1 62.5%; AgileGen GPT4 reports CodeBLEU 0.362 and Pass@1 71.5%.
- Performance versus baseline: AgileGen GPT3.5 outperforms ChatDev_24 GPT3.5 by +0.089 CodeBLEU and +16.4pp Pass@1; AgileGen GPT4 outperforms GPT4o+CoT by +0.105 CodeBLEU and +24.7pp Pass@1.
- Cost/token reporting: `sim_detalhado`; AgileGen GPT3.5 reports $0.0110 average cost, lower than AutoGPT GPT3.5 ($0.0442), ChatDev_23 ($0.0259), and ChatDev_24 ($0.0192), but higher than GPT3.5+CoT ($0.0028).

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0088_TA01157_empowering-agile-based-generative-software-development-through-human-ai-teamwork.txt`
- JSON: `extraction/json/FT0088_empowering-agile-based-generative-software-development-through-human-ai-teamwork.json`
