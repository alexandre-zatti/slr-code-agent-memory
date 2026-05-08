# LLMs as Continuous Learners: Improving the Reproduction of Defective Code in Software Issues

## Identifiers

- Included ID: I006
- Full-text ID: FT0005
- Extraction key: `lin2024evocoder`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Hierarchical experience pool with a general/common pool and repository-specific pools. Experiences are distilled from issue-reproduction trajectories by a Reflection LLM and can be added, modified, or removed.
- Evaluation: SWE-bench Lite issue reproduction; issue-resolving evaluation with AutoCodeRover and Agentless using LLM-judged and human-judged reproduction accuracy; number of resolved issues; fix rate; error-transition analysis.
- Main result: EvoCoder improves issue-code reproduction by maintaining common and repository-specific experiences. Table 1 reports EvoCoder at 54.00% LLM-judged and 53.33% human-judged reproduction accuracy. Applying EvoCoder to debuggers increases resolved issues for AutoCodeRover from 15 to 18 and Agentless from 16 to 18.
- Performance versus baseline: Compared with CodeR, reproduction accuracy improves from 34.00% to 54.00% LLM-judged (+20.00pp) and from 33.33% to 53.33% human-judged (+20.00pp). AutoCodeRover fix rate improves from 22.06% to 26.47%; Agentless from 23.53% to 26.47%.
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0005_TA01356_llms-as-continuous-learners-improving-the-reproduction-of-defective-code-in-soft.txt`
- JSON: `extraction/json/FT0005_llms-as-continuous-learners-improving-the-reproduction-of-defective-code-in-softwar.json`
