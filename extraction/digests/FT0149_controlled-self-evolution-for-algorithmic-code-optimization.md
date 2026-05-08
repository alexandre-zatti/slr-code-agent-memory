# Controlled Self-Evolution for Algorithmic Code Optimization

## Identifiers

- Included ID: I053
- Full-text ID: FT0149
- Extraction key: `hu2026cse`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Hierarchical Evolution Memory with local intra-task memory of improvement/failure lessons and global cross-task memory of compact experience items distilled from top improving/degrading evolution steps; entries are embedded with Qwen3-8B-Embedding and retrieved by cosine similarity.
- Evaluation: EffiBench-X with 623 algorithmic problems in Python and C++ using Execution-time ratio, peak-memory ratio, memory-integral ratio versus human solutions, best-so-far MI, improvement count, iteration at best, last-10 improvement count, ablation metrics.
- Main result: CSE consistently outperforms baselines on EffiBench-X across four LLM backbones. With GPT-5, CSE averages ET 67.70%, MP 65.62%, and MI 67.47%; with Claude-4.5-Sonnet, it averages ET 73.23%, MP 70.11%, and MI 74.41%.
- Performance versus baseline: With GPT-5, CSE improves average MI to 67.47% versus Direct 59.13%, Self-Reflection 60.24%, SE-Agent 64.41%, and AlphaEvolve 63.04%. Ablation on GPT-5 shows full CSE MI 68.10% versus 63.08% without memory, 63.82% without planning, and 64.72% without evolution.
- Cost/token reporting: `nao`; NR; fixed test-time budget of 30 candidates per task and no monetary/token cost per task reported.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0149_TA00744_controlled-self-evolution-for-algorithmic-code-optimization.txt`
- JSON: `extraction/json/FT0149_controlled-self-evolution-for-algorithmic-code-optimization.json`
