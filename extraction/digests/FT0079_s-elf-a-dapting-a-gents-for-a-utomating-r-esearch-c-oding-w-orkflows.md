# Self-Adapting Agents for Automating Research Coding Workflows

## Identifiers

- Included ID: I095
- Full-text ID: FT0079
- Extraction key: `gangireddi2026sare`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: Global Training Context with auxiliary context, reflection history, and cumulative cheatsheet for recurring strategies, common fixes, and domain-specific knowledge.
- Retrieval/control: Actor executes research-coding tasks using the adapted context; Reflector edits prompts and cheatsheet based on trajectories and benchmark feedback.
- Evaluation: SUPER, ResearchCodeBench, and ScienceAgentBench in offline and online adaptation settings, with ablations over cheatsheet, auxiliary context, reflection, and Global Training Context.
- Main result: SARE with ground truth reaches 52.8 overall on SUPER, 35.41 ResearchCodeBench accuracy, and 30.6 ScienceAgentBench success rate.
- Cost/token reporting: `sim_detalhado`; appendix reports per-task benchmark costs around $1-3.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0079_TA01595_s-elf-a-dapting-a-gents-for-a-utomating-r-esearch-c-oding-w-orkflows.txt`
- JSON: `extraction/json/FT0079_s-elf-a-dapting-a-gents-for-a-utomating-r-esearch-c-oding-w-orkflows.json`
