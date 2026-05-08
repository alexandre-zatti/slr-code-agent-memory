# ODEL: An Experience-Augmented Self-Evolving Framework for Efficient Python-to-C++ Code Translation

## Identifiers

- Included ID: I074
- Full-text ID: FT0077
- Extraction key: `feng2026odel`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: structured corrective experience records generated after verification failures and reused across later Python-to-C++ translation phases.
- Evaluation: HumanEval-X with Pass@1, Pass@10, multi-phase performance, experience-source ablation, and Deepseek-Coder transfer.
- Main result: ODEL External Experience improves Pass@1 from 71.82% to 81.10% and Pass@10 from 74.30% to 89.02%.
- Performance versus baseline: ODEL External Experience exceeds UniTrans at 72.16% Pass@1 and 76.64% Pass@10; external experience exceeds internal experience by 6.35 Pass@1 points.
- Cost/token reporting: `sim_parcial`; parameter-free and selective external-model use are discussed, but no numeric token or monetary cost is reported.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0077_TA00824_odel-an-experience-augmented-self-evolving-framework-for-efficient-python-to-c-c.txt`
- JSON: `extraction/json/FT0077_odel-an-experience-augmented-self-evolving-framework-for-efficient-python-to-c-code.json`
