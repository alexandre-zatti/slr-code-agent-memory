# Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation

## Identifiers

- Included ID: I002
- Full-text ID: FT0082
- Extraction key: `zelikman2024stop`
- Role: `architecture`
- Architecture status: `arch_self_evolution_archive`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_self_evolution_archive`.
- Storage: Successive versions of an executable language-model scaffolding improver program; the improved improver code is retained and reused to optimize downstream code-generation tasks.
- Evaluation: Learning parity with noise; string grid distance; modular quadratic assignment; Maxcut; parity without noise; sandbox-bypass probe using Meta-utility on downstream tasks; transfer utility; unsandboxing rate.
- Main result: With GPT-4, STOP improves downstream task performance over 1-3 self-improvement rounds and transfers to new tasks. Table 1 reports improvements from seed to improved improver: string grid distance 44.3% to 56.7%, modular quadratic assignment 20.6% to 22.1%, Maxcut 58.7% to 74.2%, and parity without noise 59.3% to 81.7%.
- Performance versus baseline: Improved improvers outperform the seed improver on all transfer tasks reported in Table 1; on LPN, the paper reports consistent mean downstream performance improvement with GPT-4.
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0082_TA00712_self-taught-optimizer-stop-recursively-self-improving-code-generation.txt`
- JSON: `extraction/json/FT0082_self-taught-optimizer-stop-recursively-self-improving-code-generation.json`
