# AdaExplore: Failure-Driven Adaptation and Diversity-Preserving Search for Efficient Kernel Generation

## Identifiers

- Included ID: I043
- Full-text ID: FT0053
- Extraction key: `du2026adaexplore`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Cross-task skill memory of validity rules distilled from recurring execution failures on synthesized Triton/kernel tasks, plus local working memory from recent search-path states and a representative kernel pool as progress storage.
- Evaluation: KernelBench Level-2 and Level-3, FlashInfer-Bench, TritonBench-T transfer checks using Accuracy, speedup over PyTorch eager baseline, Fast@1.2, Fast@2, pass rates with and without skill memory, ablation speedup.
- Main result: AdaExplore reaches 100% accuracy and 3.12x speedup on KernelBench Level-2 at 100 steps, and 100% accuracy and 1.72x speedup on Level-3. At 50 steps it reaches 2.65x Level-2 speedup and 1.55x Level-3 speedup.
- Performance versus baseline: At 50 steps on Level-2, AdaExplore reaches 2.65x speedup versus IR with skill memory at 2.59x and PS with skill memory at 2.12x. Removing cross-task skill memory drops speedup from 2.65x to 2.32x and Fast@1.2 from 71% to 56%.
- Cost/token reporting: `nao`; NR; inference budgets are reported in steps rather than monetary/token cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0053_TA00430_adaexplore-failure-driven-adaptation-and-diversity-preserving-search-for-efficie.txt`
- JSON: `extraction/json/FT0053_adaexplore-failure-driven-adaptation-and-diversity-preserving-search-for-efficient-.json`
