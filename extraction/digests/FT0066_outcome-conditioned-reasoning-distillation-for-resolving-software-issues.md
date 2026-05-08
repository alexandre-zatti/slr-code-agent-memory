# Outcome-Conditioned Reasoning Distillation for Resolving Software Issues

## Identifiers

- Included ID: I078
- Full-text ID: FT0066
- Extraction key: `li2026ocrd`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: repository-specific historical bug exemplars with resolved issues, verified patches, code context, timestamps, and outcome-conditioned stage-wise repair reasoning plans.
- Retrieval/control: All-MiniLM textual filtering retrieves top-five same-repository candidates, an LLM Exemplar Guardian filters compatibility, and BRD distills guidance injected into Agentless repair stages.
- Evaluation: SWE-Bench Lite, three LLM backbones, leaderboard baselines, Exemplar Guardian ablation, MCTS-style reasoning-plan ablation, and token/call overhead analysis.
- Main result: O-CRD reaches 37.7% Pass@1 with GPT-4o, 40.0% with GPT-5, and 35.6% with DeepSeek-V3.
- Cost/token reporting: `sim_detalhado`; BRD averages 24.7 calls and 14.3k total tokens per issue versus 240 calls and 35.4k tokens for the MCTS-style baseline.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0066_TA01485_outcome-conditioned-reasoning-distillation-for-resolving-software-issues.txt`
- JSON: `extraction/json/FT0066_outcome-conditioned-reasoning-distillation-for-resolving-software-issues.json`
