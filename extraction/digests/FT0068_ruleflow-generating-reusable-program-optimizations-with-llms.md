# RuleFlow: Generating Reusable Program Optimizations with LLMs

## Identifiers

- Included ID: I082
- Full-text ID: FT0068
- Extraction key: `singh2026ruleflow`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: reusable Pandas rewrite rules in a DSL with LHS pattern, RHS optimized code, and runtime preconditions.
- Lifecycle: offline LLM discovery accepts 157 optimization pairs, RuleGen converts 120 pairs into rules, and final evaluation uses 88 manually validated rules.
- Evaluation: PandasBench, DIAS, MODIN, DASK, KOALAS, rule speedups, hit rates, yield analysis, invalid-rule analysis, and multi-agent versus single-agent RuleGen comparison.
- Main result: RuleFlow executes 101 of 102 notebooks and achieves mean speedups of 1.54x over DIAS, 112.79x over MODIN, 12.32x over DASK, and 140.15x over KOALAS.
- Cost/token reporting: `sim_parcial`; deployment uses no LLM calls, but discovery monetary/token cost is not reported.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0068_TA01594_ruleflow-generating-reusable-program-optimizations-with-llms.txt`
- JSON: `extraction/json/FT0068_ruleflow-generating-reusable-program-optimizations-with-llms.json`
