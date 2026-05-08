# SEVerA: Verified Self-Evolving Agents

## Identifiers

- Included ID: I085
- Full-text ID: FT0133
- Extraction key: `banerjee2026severa`
- Role: `architecture`
- Architecture status: `arch_self_evolution_archive`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_self_evolution_archive`.
- Storage: SEVerA preserves verified candidate agent programs, formal output contracts, learned parameters, execution traces, verifier feedback, and error diagnostics across synthesis iterations.
- Retrieval/control: a planner synthesizes new candidate agent programs using task specifications and feedback from the current best candidate; verifier and learning stages filter and improve candidates while preserving hard constraints.
- Evaluation: HumanEvalDafny, DafnyBench, GSM-Symbolic, and tau2-bench airline/retail.
- Main result: zero constraint violations are reported; SEVerA reaches 97.0% verification plus NoDiff on HumanEvalDafny, 89.1% on DafnyBench, and 66.0% on GSM-Symbolic.
- Cost/token reporting: `sim_parcial`; the paper reports wall-clock overhead but not monetary/token cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0133_TA00303_severa-verified-synthesis-of-self-evolving-agents.txt`
- JSON: `extraction/json/FT0133_severa-verified-synthesis-of-self-evolving-agents.json`
