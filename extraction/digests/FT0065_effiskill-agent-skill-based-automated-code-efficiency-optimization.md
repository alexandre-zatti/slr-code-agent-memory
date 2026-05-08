# EffiSkill: Agent Skill Based Automated Code Efficiency Optimization

## Identifiers

- Included ID: I060
- Full-text ID: FT0065
- Extraction key: `wang2026effiskill`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: portable skill library mined from 900 Python and 900 C++ slow/fast program pairs; stores Operator Skill Cards and Meta Skill Cards for optimization mechanisms and composition guidance.
- Evaluation: EffiBench-X Python and C++ subsets using OPT@1, OPT@8, paired bootstrap tests, task win/tie/loss counts, ablations, skill-library analysis, and case study.
- Main result: EffiSkill achieves the best OPT@1 and OPT@8 across GPT-5-mini and Qwen3-Coder-30B-A3B-Instruct in Python and C++.
- Performance versus baseline: with GPT-5-mini, EffiSkill reaches Python OPT@1/OPT@8 of 26.48/37.40 and C++ 44.62/66.77; with Qwen3-Coder, it reaches Python 21.35/36.60 and C++ 34.19/56.50.
- Cost/token reporting: `sim_parcial`; fixed `k=8` candidate budget and execution-free inference are reported, but no monetary cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0065_TA01154_effiskill-agent-skill-based-automated-code-efficiency-optimization.txt`
- JSON: `extraction/json/FT0065_effiskill-agent-skill-based-automated-code-efficiency-optimization.json`
