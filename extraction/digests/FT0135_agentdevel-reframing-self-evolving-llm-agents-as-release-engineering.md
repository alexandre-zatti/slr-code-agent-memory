# AgentDevel: Reframing Self-Evolving LLM Agents as Release Engineering

## Identifiers

- Included ID: I044
- Full-text ID: FT0135
- Extraction key: `zhang2026agentdevel`
- Role: `architecture`
- Architecture status: `arch_self_evolution_archive`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_self_evolution_archive`.
- Storage: Versioned release-engineering artifacts for agents: execution traces, rubric/programmatic scores, symptom labels, diagnostic scripts, release candidates, promoted blueprint versions, flip lists, and regression-gate decisions.
- Evaluation: SWE-bench Lite, SWE-bench Verified, WebArena, StableToolBench using Resolved rate, success rate, SoWR, fail-to-pass flips, pass-to-fail regressions, regression rate, hit rate, bad release count.
- Main result: AgentDevel doubles SWE-bench Lite resolved rate from 11.0% to 22.0% and SWE-bench Verified from 15.0% to 30.0%. It also improves WebArena from 17.0% to 35.5% and StableToolBench SoWR from 54.0% to 73.5%.
- Performance versus baseline: On SWE-bench Lite, AgentDevel reaches 22.0% versus base 11.0% and reported SWE-agent 18.0%. On WebArena ablation, the full pipeline keeps P2F regression rate at 3.1% with zero bad releases; removing the flip gate raises P2F to 14.8% and creates four bad releases.
- Cost/token reporting: `sim_parcial`; NR; paper reports non-trivial compute and wall-clock overhead but no per-task monetary/token cost in extracted evidence.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0135_TA00395_agentdevel-reframing-self-evolving-llm-agents-as-release-engineering.txt`
- JSON: `extraction/json/FT0135_agentdevel-reframing-self-evolving-llm-agents-as-release-engineering.json`
