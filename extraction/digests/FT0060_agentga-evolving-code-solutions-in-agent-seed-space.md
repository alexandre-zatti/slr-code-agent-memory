# AgentGA: Evolving Code Solutions in Agent-Seed Space

## Identifiers

- Included ID: I045
- Full-text ID: FT0060
- Extraction key: `tan2026agentga`
- Role: `architecture`
- Architecture status: `arch_self_evolution_archive`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_self_evolution_archive`.
- Storage: Population-level archive of autonomous run artifacts, parent solutions, experiments, agent chains, and code artifacts; selected parent archives are copied into a Previous Experiments directory for child runs while each child starts from a fresh workspace.
- Evaluation: 10 of 16 Weco-Kaggle Lite tabular AutoML competitions, Kaggle private leaderboard submissions, 1,135 parent-child tournaments using Exceeds percent of human competitors, Kaggle rank, parent-child tournament win/loss share, median relative gain, prompt/completion/cached token trace for example run.
- Main result: Across 10 completed Weco-Kaggle Lite benchmark runs, AGENT GA averages 74.52% Exceeds % of Human versus 54.15% for AIDE, a +20.36 point mean improvement. All 10 completed runs beat the AIDE private-leaderboard reference.
- Performance versus baseline: Parent-conditioned operators win 48.7% of parent-child tournaments overall, while Initial proposals win only 12.2%. Continue wins 148/286 tournaments, Merge 68/104, EDA 267/593, Ablation 34/78, and Initial 9/74.
- Cost/token reporting: `sim_parcial`; No monetary cost reported; example invocation took 56 steps, 15 min 10 s, 1.87M prompt tokens, and 34,252 completion tokens.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0060_TA00917_agentga-evolving-code-solutions-in-agent-seed-space.txt`
- JSON: `extraction/json/FT0060_agentga-evolving-code-solutions-in-agent-seed-space.json`
