# RedCodeAgent: Automatic Red-teaming Agent against Diverse Code Agents

## Identifiers

- Included ID: I032
- Full-text ID: FT0091
- Extraction key: `guo2025redcodeagent`
- Role: `architecture`
- Architecture status: `arch_security_memory`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_security_memory`.
- Storage: Adaptive memory entries for successful attacks store risk scenario, risk description, attack trajectory, final evaluation result, and final self-reflection; memory starts empty and successful attacks are logged for later tasks.
- Evaluation: RedCode-Exec, RedCode-Gen, RMCbench; 27 risk scenarios and 810 test cases across code agents and languages using Attack Success Rate (ASR), Refusal Rate (RR), language/task/agent-specific ASR and RR.
- Main result: RedCodeAgent achieves the highest ASR and lowest RR across reported benchmark/code-agent combinations. For example, on OCI RedCode-Exec it reports 72.47% ASR and 7.53% RR, and on RA RedCode-Gen it reports 81.52% ASR and 2.50% RR.
- Performance versus baseline: Compared with no-jailbreak and jailbreak baselines, RedCodeAgent reports higher ASR across RedCode-Exec, RedCode-Gen, and RMCbench. In selected subtasks it reaches 70.00% ASR/20.00% RR for deleting sensitive files and 93.33% ASR/6.67% RR for adding risky aliases.
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0091_TA00117_redcodeagent-automatic-red-teaming-agent-against-diverse-code-agents.txt`
- JSON: `extraction/json/FT0091_redcodeagent-automatic-red-teaming-agent-against-diverse-code-agents.json`
