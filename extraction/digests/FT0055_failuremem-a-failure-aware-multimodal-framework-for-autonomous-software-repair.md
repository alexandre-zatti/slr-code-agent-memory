# FailureMem: A Failure-Aware Multimodal Framework for Autonomous Software Repair

## Identifiers

- Included ID: I061
- Full-text ID: FT0055
- Extraction key: `ma2026failuremem`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: hierarchical Failure Memory Bank with contextual, cognitive, and code layers built from failed multimodal repair trajectories.
- Evaluation: SWE-bench Multimodal; benchmark comparison, component ablation, and retrieval-depth sensitivity.
- Main result: FailureMem improves resolved rate over GUIRepair; with GPT-5.1 it reaches 33.1% versus 29.4%.
- Performance versus baseline: reported resolved rates are 31.1%, 33.1%, 33.3%, 32.5%, and 33.8% across GPT-4.1, GPT-5.1, GPT-5.2, Claude 4, and Claude 4.5.
- Cost/token reporting: `sim_detalhado`; USD 0.33 per issue versus USD 0.29 for GUIRepair.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0055_TA00483_failuremem-a-failure-aware-multimodal-framework-for-autonomous-software-repair.txt`
- JSON: `extraction/json/FT0055_failuremem-a-failure-aware-multimodal-framework-for-autonomous-software-repair.json`
