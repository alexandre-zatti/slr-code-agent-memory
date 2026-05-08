# REVERE: Reflective Evolving Research Engineer for Scientific Workflows

## Identifiers

- Included ID: I081
- Full-text ID: FT0067
- Extraction key: `gangireddi2026revere`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: Global Training Context with auxiliary context, reflection history, and cumulative cheatsheet; Reflector edits system prompt, task prompt, and cheatsheet fields.
- Evaluation: SUPER Expert, ResearchCodeBench, ScienceAgentBench, offline/online adaptation, GEPA and ACE comparisons, component ablations, and efficiency analysis.
- Main result: with ground-truth hints, REVERE reaches SUPER Overall 29.8, ResearchCodeBench Accuracy 33.2, and ScienceAgentBench SuccessRate 28.39.
- Performance versus baseline: improves SUPER Overall by +4.50 over Static SOTA, RCB Accuracy by +1.3, and ScienceAgentBench SuccessRate by +4.89.
- Cost/token reporting: `sim_detalhado`; per-task benchmark costs and adaptation-cost comparisons are reported, with adaptation overhead nearly 10x lower than ACE and GEPA on SUPER.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0067_TA01586_revere-reflective-evolving-research-engineer-for-scientific-workflows.txt`
- JSON: `extraction/json/FT0067_revere-reflective-evolving-research-engineer-for-scientific-workflows.json`
