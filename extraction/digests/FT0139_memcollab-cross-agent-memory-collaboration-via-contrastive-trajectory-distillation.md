# MemCollab: Cross-Agent Memory Collaboration via Contrastive Trajectory Distillation

## Identifiers

- Included ID: I070
- Full-text ID: FT0139
- Extraction key: `chang2026memcollab`
- Role: `architecture`
- Architecture status: `arch_shared_memory`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_shared_memory`.
- Storage: shared contrast-derived memory bank of normative constraints that enforce reasoning invariants and avoid violated patterns.
- Evaluation: MATH500, GSM8K, MBPP, and HumanEval with cross-agent and cross-family comparisons.
- Main result: shared contrastive memory improves both smaller and larger models over vanilla and memory-transfer baselines.
- Performance versus baseline: Qwen2.5-7B average accuracy improves from 57.1 to 71.6; MBPP improves from 47.9 to 57.6 and HumanEval from 42.7 to 74.4.
- Cost/token reporting: `sim_parcial`; reasoning turns and GPU setup are reported, but no monetary cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0139_TA00417_memcollab-cross-agent-memory-collaboration-via-contrastive-trajectory-distillati.txt`
- JSON: `extraction/json/FT0139_memcollab-cross-agent-memory-collaboration-via-contrastive-trajectory-distillation.json`
