# TAI3: Testing Agent Integrity in Interpreting User Intent

## Identifiers

- Included ID: I038
- Full-text ID: FT0020
- Extraction key: `feng2025tai3`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: Datatype-aware strategy memory stores successful mutation strategies indexed by parameter datatype and integrity category; novel strategies are added after an LLM duplicate check and top strategies are adapted for later seed tasks.
- Evaluation: 80 toolkit APIs, 233 parameters, five domains: Finance, Healthcare, Smart Home, Logistics, and Office using Error-Exposing Success Rate (EESR), Average Queries to First Failure (AQFF), per-domain/category/model deltas.
- Main result: TAI3 consistently outperforms the SelfRef baseline in EESR across domains and input categories. In the VALID category it improves EESR by up to 15.5 points in Finance for Llama-3.1-8B and by 10.0 points in Office for GPT-4o-mini.
- Performance versus baseline: Table 1 reports broad EESR gains over SelfRef, including Finance GPT-4o-mini VALID 41.5 to 61.0 (+19.5), Healthcare GPT-4o-mini INVALID 44.7 to 57.4 (+12.7), and Office Llama-3.1-8B UNDERSPEC 65.7 to 82.0 (+16.3).
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0020_TA00355_tai3-testing-agent-integrity-in-interpreting-user-intent.txt`
- JSON: `extraction/json/FT0020_tai3-testing-agent-integrity-in-interpreting-user-intent.json`
