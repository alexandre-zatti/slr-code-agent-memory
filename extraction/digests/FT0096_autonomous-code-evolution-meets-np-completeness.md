# Autonomous Code Evolution Meets NP-Completeness

## Identifiers

- Included ID: I013
- Full-text ID: FT0096
- Extraction key: `yu2025satlution`
- Role: `architecture`
- Architecture status: `arch_self_evolution_archive`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_self_evolution_archive`.
- Storage: Evolved SAT solver repositories plus a rulebase of initialization rules, programming constraints, pre-evaluation checks, post-evaluation analysis, champion rules, forbidden patterns, and failure rules maintained across evolution cycles.
- Evaluation: SAT Competition 2024 and SAT Competition 2025 benchmark instances using PAR-2 score; number of solved instances; runtime/cactus plots; SAT and UNSAT category results; correctness validation outcomes.
- Main result: SATLUTION evolves repository-scale SAT solvers from SAT Competition 2024 codebases and reports lower PAR-2 scores and more solved instances than the top SAT Competition 2025 solvers, despite training feedback coming from 2024 benchmarks.
- Performance versus baseline: On the SAT Competition 2025 comparison, the top evolved solvers solve 347, 345, and 344 instances, compared with 334 and 331 instances for the gold and silver 2025 winners; figures report lowest PAR-2 scores on 2025 and 2024 benchmarks.
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0096_TA00287_autonomous-code-evolution-meets-np-completeness.txt`
- JSON: `extraction/json/FT0096_autonomous-code-evolution-meets-np-completeness.json`
