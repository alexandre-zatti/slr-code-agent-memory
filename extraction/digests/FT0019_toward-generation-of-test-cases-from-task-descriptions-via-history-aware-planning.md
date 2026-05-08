# Toward Generation of Test Cases from Task Descriptions via History-aware Planning

## Identifiers

- Included ID: I041
- Full-text ID: FT0019
- Extraction key: `cao2025hxagent`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: HxAgent maintains short-term sequence-action memory as JSON/text state-action traces and long-term experience containing correct and incorrect action sequences selected from training for later evaluation prompts.
- Evaluation: MiniWoB++ shared tasks, 125 challenging MiniWoB++ task instances, and 350 real-world web-application task instances using Exact-Match accuracy, Prefix-Match accuracy, correct runs, ablation accuracy, prompt/output token consumption.
- Main result: HxAgent reaches 97% Exact-Match and 99% Prefix-Match on MiniWoB++, 82% Exact-Match on 125 challenging MiniWoB++ task instances, and 87% Exact-Match / 93% Prefix-Match on 350 real-world web-application task instances.
- Performance versus baseline: On challenging MiniWoB++ tasks, HxAgent averages 82% Exact-Match versus 10% for Li et al. (GPT-4o). On real-world applications it averages 87% Exact-Match versus 28% and 93% Prefix-Match versus 34%. Removing experience drops Exact-Match from 97% to 88%; removing both SAM and experience drops it to 47%.
- Cost/token reporting: `sim_parcial`; No monetary cost reported; average token consumption is 800,000 prompt tokens and 22,000 output tokens.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0019_TA00346_toward-generation-of-test-cases-from-task-descriptions-via-history-aware-plannin.txt`
- JSON: `extraction/json/FT0019_toward-generation-of-test-cases-from-task-descriptions-via-history-aware-planning.json`
