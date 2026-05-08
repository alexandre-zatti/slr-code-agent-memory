# AlphaOPT: Formulating Optimization Programs with Self-Improving LLM Experience Library

## Identifiers

- Included ID: I012
- Full-text ID: FT0114
- Extraction key: `kong2025alphaopt`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Self-improving experience library of solver-verified modeling and code-implementation insights represented as taxonomy, condition, explanation, and example tuples, organized in a dynamic hierarchical taxonomy.
- Evaluation: NLP4LP, NL4OPT, IndustryOR, MAMO/ComplexLP, LogiOR, OptiBench using Accuracy/success rate; micro-averaged accuracy; macro-averaged accuracy; ablation accuracy; training-size growth curve.
- Main result: AlphaOPT outperforms prompt-based, fine-tuning, and experience-learning baselines across optimization-program formulation benchmarks. Table 1 reports AlphaOPT micro/macro averages of 80.1/76.4 on test splits and 86.5/74.8 on out-of-distribution datasets.
- Performance versus baseline: AlphaOPT exceeds ExpeL on test micro/macro averages (80.1/76.4 vs 69.9/66.3) and out-of-distribution micro/macro averages (86.5/74.8 vs 74.3/64.1). Removing refinement reduces out-of-distribution macro from 74.8 to 70.5.
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0114_TA00960_alphaopt-formulating-optimization-programs-with-self-improving-llm-experience-li.txt`
- JSON: `extraction/json/FT0114_alphaopt-formulating-optimization-programs-with-self-improving-llm-experience-libra.json`
