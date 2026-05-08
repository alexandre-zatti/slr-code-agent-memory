# Lingxi: Repository-Level Issue Resolution Framework Enhanced by Procedural Knowledge Guided Scaling

## Identifiers

- Included ID: I027
- Full-text ID: FT0034
- Extraction key: `yang2025lingxi`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: Transferable procedural knowledge extracted from historical issue-fixing data; target issue summaries are embedded, similar historical issues are retrieved and reranked, and procedural knowledge guides analysis scaling and patch generation.
- Evaluation: SWE-bench Verified using Pass@1 resolve rate; ablation pass rate; model/backbone comparison.
- Main result: Lingxi reaches 74.60% Pass@1 on SWE-bench Verified with Claude 4 Sonnet and 70.33% with Kimi-K2. Ablations show the full method at 74.80%, while replacing transferable procedural knowledge with raw issue-patch pairs drops to 68.30% and removing knowledge drops to 67.74%.
- Performance versus baseline: With Claude 4 Sonnet, Lingxi reports 74.60% versus OpenHands and Augment Agent prior at 70.40%, SWE-search at 70.08%, SWE-agent at 66.60%, and mini-SWE-agent at 64.93%. With Kimi-K2, Lingxi reports 70.33% versus OpenHands 65.40% and mini-SWE-agent 43.80%.
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0034_TA01346_lingxi-repository-level-issue-resolution-framework-enhanced-by-procedural-knowle.txt`
- JSON: `extraction/json/FT0034_lingxi-repository-level-issue-resolution-framework-enhanced-by-procedural-knowledge.json`
