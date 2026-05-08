# FALCON: Feedback-driven Adaptive Long/short-term memory reinforced Coding OptimizatioN

## Identifiers

- Included ID: I004
- Full-text ID: FT0003
- Extraction key: `li2024falcon`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Long-term memory buffer stores task descriptions, generated code/solutions, test/compiler feedback, and evaluation scores; short-term memory stores recent samples, error lines, compiler feedback, and immediate feedback for reward allocation.
- Evaluation: APPS, HumanEval, MBPP, CODAL-Bench using pass@1, pass@5, coding-preference metrics.
- Main result: FALCON combines long/short-term memory with meta-reinforcement learning for code generation. On APPS with CodeT5 770M, it reports pass@1 all 3.50 and pass@5 all 8.17, outperforming RLTF (3.27 / 7.87). On HumanEval/MBPP, it reports 82.9 and 80.7 pass@1.
- Performance versus baseline: HumanEval improves from RLTF 76.8 to 82.9 (+6.1pp); MBPP improves from RLTF 75.9 to 80.7 (+4.8pp); APPS all pass@1 improves from RLTF 3.27 to 3.50 (+0.23pp).
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0003_TA00466_falcon-feedback-driven-adaptive-long-short-term-memory-reinforced-coding-optimiz.txt`
- JSON: `extraction/json/FT0003_falcon-feedback-driven-adaptive-long-short-term-memory-reinforced-coding-optimizati.json`
