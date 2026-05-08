# CodeDistiller: Automatically Generating Code Libraries for Scientific Coding Agents

## Identifiers

- Included ID: I015
- Full-text ID: FT0013
- Extraction key: `jansen2025codedistiller`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: Vetted library of executable, debugged scientific code examples distilled from GitHub repositories, including example code, requirements, suitability descriptions, and evidence of successful execution.
- Evaluation: 250 materials-science GitHub repositories; 50-repository domain-expert validation subset; 60 downstream materials-science tasks from 12 repositories using Automatic successful completion; manual code-execution success; manual repository-functionality and correct-functionality judgments; runtime; debug iterations; API cost; A/B preference proportions for accuracy, completeness, and scientific soundness.
- Main result: CodeDistiller converts scientific GitHub repositories into reusable code examples. Domain-expert validation reports correct functionality for 25.9% with GPT-OSS-120B, 60.5% with GPT-5, and 74.1% with Claude 4.5; downstream A/B tests prefer CodeDistiller-augmented outputs in nearly half of cases across accuracy, completeness, and soundness.
- Performance versus baseline: Downstream A/B preference proportions favor CodeDistiller over the generic-example baseline for accuracy (0.50 vs 0.26), completeness (0.46 vs 0.16), and soundness (0.50 vs 0.30), with ties making up the remainder.
- Cost/token reporting: `sim`; Successful-case average cost: GPT-OSS-120B $0.09, GPT-5 $0.70, Claude 4.5 $1.71; downstream runs allow up to $5 of LLM-associated costs per run.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0013_TA00148_codedistiller-automatically-generating-code-libraries-for-scientific-coding-agen.txt`
- JSON: `extraction/json/FT0013_codedistiller-automatically-generating-code-libraries-for-scientific-coding-agents.json`
