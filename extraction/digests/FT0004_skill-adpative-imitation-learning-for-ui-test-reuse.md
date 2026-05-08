# Skill-Adpative Imitation Learning for UI Test Reuse

## Identifiers

- Included ID: I007
- Full-text ID: FT0004
- Extraction key: `wu2024sail`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: Knowledge base/archive of multi-level abstracted UI testing skills extracted from source test cases, then selectively reused for target-app test generation with context- and history-aware adaptation.
- Evaluation: 104 UI test-migration cases from 35 popular Android apps; SemFinder dataset / CraftDroid-related evaluation subjects using Success rate; Top-1 event-matching accuracy; ablation success rates.
- Main result: SAIL extracts source-test skills and reuses them for UI test migration. Table 3 reports SAIL-DeepSeek-V2 success rate 63.6%, SAIL-GPT-4o 62.9%, and SAIL-GPT-4o-mini 58.4%.
- Performance versus baseline: SAIL-DeepSeek-V2 improves over CraftDroid 25.5% to 63.6% overall (+38.1pp; reported as 149% higher SR). In non-1-to-1 mappings, SAIL-GPT-4o reaches 55.6% versus CraftDroid 14.1% (reported as 294% improvement).
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0004_TA00540_skill-adpative-imitation-learning-for-ui-test-reuse.txt`
- JSON: `extraction/json/FT0004_skill-adpative-imitation-learning-for-ui-test-reuse.json`
