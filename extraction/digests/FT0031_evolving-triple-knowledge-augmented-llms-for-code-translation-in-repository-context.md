# Evolving Triple Knowledge-Augmented LLMs for Code Translation in Repository Context

## Identifiers

- Included ID: I020
- Full-text ID: FT0031
- Extraction key: `ou2025k3trans`
- Role: `architecture`
- Architecture status: `arch_repository_memory`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_repository_memory`.
- Storage: Self-evolving triple translation knowledge base containing dependency usage examples from the repository, target-language code samples from existing projects, and successful translation function pairs from prior translation history.
- Evaluation: RustRepoTrans repository-level C-to-Rust code translation benchmark using Compilation@1, Pass@1, DSR@1, Repairable Ratio, CodeBLEU, AST Match Score.
- Main result: K3 Trans improves repository-context code translation with triple knowledge retrieval and self-debugging. With Claude-3-5-Sonnet, K3 Trans reaches 75.7% Compilation@1, 67.7% Pass@1, 82.1% DSR@1, 44.6% RR, 0.733 CodeBLEU, and 0.562 AST match.
- Performance versus baseline: For Claude-3-5-Sonnet, K3 Trans improves over prompt engineering from 57.9% to 75.7% Compilation@1 and from 49.1% to 67.7% Pass@1; the paper reports relative improvements up to 135.9% on Pass@1 and 32.8% on CodeBLEU among studied LLMs.
- Cost/token reporting: `nao`; NR; implementation limits LLM repair to one iteration for cost-effectiveness but reports no monetary cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0031_TA00677_evolving-triple-knowledge-augmented-llms-for-code-translation-in-repository-cont.txt`
- JSON: `extraction/json/FT0031_evolving-triple-knowledge-augmented-llms-for-code-translation-in-repository-context.json`
