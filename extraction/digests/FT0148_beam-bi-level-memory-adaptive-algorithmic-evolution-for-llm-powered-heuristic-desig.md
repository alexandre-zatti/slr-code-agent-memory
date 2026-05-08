# BEAM: Bi-level Memory-adaptive Algorithmic Evolution for LLM-Powered Heuristic Design

## Identifiers

- Included ID: I047
- Full-text ID: FT0148
- Extraction key: `xiang2026beam`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: Adaptive Memory stores high-performing generated function components with names/descriptions so future algorithm structures can import and recombine them; Knowledge Augmentation also uses HeuBase component repositories and KnoBase text knowledge.
- Evaluation: TSP, BPP, CAF, MIS, CVRP, BBOB, PMSP and related heuristic-design benchmarks using Optimality gap, objective value, runtime/time or token budget, average and variance of final gaps, token-consumption trajectory.
- Main result: BEAM reduces the optimality gap by 37.84% in aggregate on CVRP hybrid algorithm design and generates competitive or superior heuristics across MIS, CVRP, TSP, BBOB, and other optimization benchmarks.
- Performance versus baseline: In CVRP, BEAM with Split and local search reports gaps of 0.09%, 0.38%, and 0.86% for CVRP-100/200/500 versus EoH gaps of 0.22%, 0.57%, and 1.09%. In BBOB, BEAM average gap is 0.007 versus ReEvo 0.957, EoH 6.032, and LLaMEA-HPO 0.386.
- Cost/token reporting: `sim_parcial`; NR as monetary cost; experiments report time budgets from 18 minutes to 5 hours and token-budget experiments up to 55w tokens.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0148_TA00703_beam-bi-level-memory-adaptive-algorithmic-evolution-for-llm-powered-heuristic-de.txt`
- JSON: `extraction/json/FT0148_beam-bi-level-memory-adaptive-algorithmic-evolution-for-llm-powered-heuristic-desig.json`
