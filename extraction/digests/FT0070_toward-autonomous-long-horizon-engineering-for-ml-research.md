# Toward Autonomous Long-Horizon Engineering for ML Research

## Identifiers

- Included ID: I091
- Full-text ID: FT0070
- Extraction key: `chen2026aiscientist`
- Role: `architecture`
- Architecture status: `arch_persistent_workspace_state`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_persistent_workspace_state`.
- Storage: permission-scoped File-as-Bus workspace with paper analyses, plans, code, logs, experiment outputs, submission artifacts, and concise summaries.
- Retrieval/control: orchestrator and specialized agents coordinate by writing and re-grounding on durable workspace artifacts instead of relying only on conversation state.
- Evaluation: PaperBench and MLE-Bench Lite, with BasicAgent, IterAgent, and no-File-as-Bus ablation comparisons.
- Main result: AiScientist improves PaperBench scores from 20.60 to 30.52 with Gemini and from 22.37 to 33.73 with GLM-5; no-File-as-Bus ablation drops MLE-Bench Lite any-medal rate by 31.82 points.
- Cost/token reporting: `sim_detalhado`; PaperBench cost/task is reported.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0070_TA01747_toward-autonomous-long-horizon-engineering-for-ml-research.txt`
- JSON: `extraction/json/FT0070_toward-autonomous-long-horizon-engineering-for-ml-research.json`
