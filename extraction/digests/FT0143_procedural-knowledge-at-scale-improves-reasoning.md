# Procedural Knowledge at Scale Improves Reasoning

## Identifiers

- Included ID: I079
- Full-text ID: FT0143
- Extraction key: `wu2026reasoningmemory`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Reasoning Memory datastore with about 32 million subquestion-subroutine procedural entries distilled from prior reasoning trajectories.
- Retrieval/control: self-verbalized in-thought queries retrieve procedural subroutines with ReasonIR; inference-time scaling samples across retrieved procedures.
- Evaluation: AIME 2024, AIME 2025, MATH500, GPQA-Diamond, LiveCodeBench V1-4, LiveCodeBench V5-6, retrieval baselines, length-scaling baseline, datastore and query ablations.
- Main result: Reasoning Memory improves over no retrieval by up to 19.2% and over the strongest compute-matched baseline by 7.9%.
- Cost/token reporting: `sim_parcial`; the paper reports inference budgets and max output length, but not monetary cost or per-task token means.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0143_TA00485_procedural-knowledge-at-scale-improves-reasoning.txt`
- JSON: `extraction/json/FT0143_procedural-knowledge-at-scale-improves-reasoning.json`
