# Memory Transfer Learning: How Memories are Transferred Across Domains in Coding Agents

## Identifiers

- Included ID: I073
- Full-text ID: FT0048
- Extraction key: `kim2026memorytransfer`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: unified heterogeneous-domain memory pools with Trajectory, Workflow, Summary, and Insight formats.
- Evaluation: six coding benchmarks plus self-evolving baseline comparison, negative-transfer analysis, abstraction analysis, scaling, cross-model transfer, and retrieval ablations.
- Main result: cross-domain memory improves GPT-5-mini average performance by 3.7%, with Insight memories giving the best average score.
- Performance versus baseline: GPT-5-mini average Pass@3 improves from 0.523 zero-shot to 0.560 with MTL Insight; MTL averages 0.630 versus ReasoningBank 0.601 and AgentKB 0.613 in the three-benchmark comparison.
- Cost/token reporting: `nao`; memory counts are reported, but no token or monetary cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0048_TA00266_memory-transfer-learning-how-memories-are-transferred-across-domains-in-coding-a.txt`
- JSON: `extraction/json/FT0048_memory-transfer-learning-how-memories-are-transferred-across-domains-in-coding-agen.json`
