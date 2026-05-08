# Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents

## Identifiers

- Included ID: I017
- Full-text ID: FT0089
- Extraction key: `zhang2025darwingodel`
- Role: `architecture`
- Architecture status: `arch_self_evolution_archive`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_self_evolution_archive`.
- Storage: Growing archive/tree of generated coding-agent codebases, benchmark evaluations, and auditable lineages; archived agents can be selected as parents for self-modification.
- Evaluation: SWE-bench Verified, Polyglot using Solved-task percentage / pass@1; best-agent score over iterations; cost estimate; baseline comparison curves.
- Main result: After 80 iterations, DGM improves coding-agent performance from 20.0% to 50.0% on SWE-bench and from 14.0% to 38.0% on the Polyglot subset; full Polyglot improves from 14.2% to 30.7%.
- Performance versus baseline: DGM outperforms variants without self-improvement and without open-ended exploration; best discovered SWE-bench agent is comparable to checked open-source human-designed SoTA, while Polyglot improves 14.2% to 30.7% on the full benchmark.
- Cost/token reporting: `sim`; Estimated cost for one SWE-bench DGM run is about $22,000; each baseline SWE-bench run is about $10,000; one 60-task SWE-bench evaluation costs about $350 and one 60-task Polyglot evaluation about $5.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0089_TA00075_darwin-godel-machine-open-ended-evolution-of-self-improving-agents.txt`
- JSON: `extraction/json/FT0089_darwin-godel-machine-open-ended-evolution-of-self-improving-agents.json`
