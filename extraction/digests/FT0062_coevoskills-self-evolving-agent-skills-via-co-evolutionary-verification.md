# CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification

## Identifiers

- Included ID: I051
- Full-text ID: FT0062
- Extraction key: `zhang2026coevoskills`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: Persistent structured multi-file skill packages with SKILL.md, instructions, scripts, reusable utility functions, and verifier-derived improvement notes; skills are installed for fresh Claude Code/Codex agents and updated across evolution rounds.
- Evaluation: SkillsBench: 87 tasks across roughly 20 professional domains and 11 reported domain groups using Pass rate, delta versus no-skill/human-curated baselines, cross-model transfer pass rate, per-domain pass rate, verification-cycle counts, ablation pass rate.
- Main result: CoEvoSkills reaches 71.1% pass rate on SkillsBench with Claude Opus 4.6 + Claude Code, versus 30.6% no-skill baseline and 53.5% human-curated skills. It also reports GPT-5.2 self-evolved skills at 69.8% and broad cross-model transfer gains of about 36-44pp.
- Performance versus baseline: CoEvoSkills improves +40.5pp over no-skill and +17.6pp over human-curated skills. Skill-Creator reaches 34.1%, single-session generation 32.4%, SkillsBench self-generated 32.0%, and CoT-guided self-generation 30.7%. Removing the surrogate verifier drops pass rate from 71.1% to 41.1%; removing evolution drops to 48.6%.
- Cost/token reporting: `sim_parcial`; NR; paper states convergence within five rounds keeps evolution cost practical and reports average verification-cycle counts, but no monetary/token cost per task is extracted.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0062_TA01060_coevoskills-self-evolving-agent-skills-via-co-evolutionary-verification.txt`
- JSON: `extraction/json/FT0062_coevoskills-self-evolving-agent-skills-via-co-evolutionary-verification.json`
