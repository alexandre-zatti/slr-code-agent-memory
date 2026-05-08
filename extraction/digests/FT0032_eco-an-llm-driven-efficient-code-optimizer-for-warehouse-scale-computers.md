# ECO: An LLM-Driven Efficient Code Optimizer for Warehouse Scale Computers

## Identifiers

- Included ID: I018
- Full-text ID: FT0032
- Extraction key: `lin2025eco`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Database/dictionary of performance anti-patterns and corresponding optimizations mined from historical performance-improving commits, code review comments, issue tracker entries, and before/after source snapshots; the performance-specific fine-tuning dataset contains about 55k commits.
- Evaluation: Google production code-review/deployment pipeline, microbenchmark edits, retrieval-model evaluation, human/automated code review, fleet-wide production profiler using Submitted commits; changed lines of code; production success rate; normalized-core savings; MAP@K retrieval metrics; CodeBLEU and human quality scores; code-review outcomes.
- Main result: ECO mines reusable optimization patterns from historical commits and applies them through an LLM-driven optimizer at warehouse scale. The system has landed over 6.4k production commits and over 25k changed lines with >99.5% production success rate.
- Performance versus baseline: Production deployment reports over 2M normalized cores saved, more than 500k normalized cores saved per quarter, and successful edits across multiple anti-pattern categories; ECO scales human optimization effort beyond manual search.
- Cost/token reporting: `sim`; NR as monetary LLM cost; deployment reports over 2M normalized cores saved, over 500k normalized cores per quarter, and fleet-wide resource savings from 6.4k landed commits.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0032_TA01147_eco-an-llm-driven-efficient-code-optimizer-for-warehouse-scale-computers.txt`
- JSON: `extraction/json/FT0032_eco-an-llm-driven-efficient-code-optimizer-for-warehouse-scale-computers.json`
