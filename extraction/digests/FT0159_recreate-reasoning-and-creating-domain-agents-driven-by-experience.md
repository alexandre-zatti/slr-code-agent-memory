# ReCreate: Reasoning and Creating Domain Agents Driven by Experience

## Identifiers

- Included ID: I080
- Full-text ID: FT0159
- Extraction key: `hao2026recreate`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: ReCreate-Environment stores scaffold, trajectories, execution and evaluation results, artifacts, context, evidence indexes, scaffold diffs, tools, and static memory entries.
- Retrieval/control: a ReCreate-Agent inspects stored experience on demand, routes scaffold/tool/memory edits, and synthesizes instance updates into domain-level scaffold updates.
- Evaluation: SWE-Bench Verified, DA-Code, DS-1000, MATH, AppWorld, human-designed scaffolds, self-evolving baselines, agent-generation baselines, ablations, and cost comparison.
- Main result: ReCreate averages 66.15 across 13 benchmark subsets, exceeding ExpeL at 60.62 and LIVE at 60.57.
- Cost/token reporting: `sim_parcial`; ReCreate is reported to reduce scaffold-optimization cost relative to ADAS by about 36% to 82%.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0159_TA01555_recreate-reasoning-and-creating-domain-agents-driven-by-experience.txt`
- JSON: `extraction/json/FT0159_recreate-reasoning-and-creating-domain-agents-driven-by-experience.json`
