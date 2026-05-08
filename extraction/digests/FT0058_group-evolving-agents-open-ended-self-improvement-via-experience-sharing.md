# Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing

## Identifiers

- Included ID: I062
- Full-text ID: FT0058
- Extraction key: `weng2026groupevolving`
- Role: `architecture`
- Architecture status: `arch_self_evolution_archive`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_self_evolution_archive`.
- Storage: archive of evolving agent groups and shared group-level experience, including framework patches, task patches, tool-use logs, workflows, outcomes, and learned artifacts.
- Evaluation: SWE-bench Verified and Polyglot, compared with DGM-style self-evolution and human-designed framework baselines.
- Main result: GEA reaches 71.0% on SWE-bench Verified and 88.3% on Polyglot.
- Performance versus baseline: DGM-style baseline reaches 56.7% and 68.3%; GEA fixes framework-level bugs in 1.4 iterations on average versus 5.0.
- Cost/token reporting: `sim_detalhado`; full-run estimates are about USD 13,000 per method on SWE-bench and USD 1,500 on Polyglot.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0058_TA00632_group-evolving-agents-open-ended-self-improvement-via-experience-sharing.txt`
- JSON: `extraction/json/FT0058_group-evolving-agents-open-ended-self-improvement-via-experience-sharing.json`
