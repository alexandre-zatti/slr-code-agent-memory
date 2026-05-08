# When the Specification Emerges: Benchmarking Faithfulness Loss in Long-Horizon Coding Agents

## Identifiers

- Included ID: I093
- Full-text ID: FT0165
- Extraction key: `yan2026slump`
- Role: `architecture`
- Architecture status: `arch_persistent_workspace_state`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_persistent_workspace_state`.
- Storage: ProjectGuard stores semantic project commitments and structural codebase state across long-horizon coding turns.
- Retrieval/control: compatibility-aware forecasting and proactive restarts use the external project state to mitigate faithfulness loss under emergent specification.
- Evaluation: SLUMP benchmark with 20 ML papers, 371 components, Claude Code and Codex conditions, emergent versus single-shot controls, and ProjectGuard mitigation.
- Main result: ProjectGuard raises Claude Code MCF from 2.718 to 3.000, recovers 90% of the single-shot gap, increases fully faithful components from 118 to 181, and reduces severe failures from 72 to 49.
- Cost/token reporting: `sim_parcial`; external state size and compaction/restart behavior are reported, but monetary/token cost is not.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0165_TA01818_when-the-specification-emerges-benchmarking-faithfulness-loss-in-long-horizon-co.txt`
- JSON: `extraction/json/FT0165_when-the-specification-emerges-benchmarking-faithfulness-loss-in-long-horizon-codin.json`
