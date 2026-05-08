# Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine

## Identifiers

- Included ID: I024
- Full-text ID: FT0098
- Extraction key: `wang2025huxleygodel`
- Role: `architecture`
- Architecture status: `arch_self_evolution_archive`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_self_evolution_archive`.
- Storage: Tree/archive of self-modified coding agents with clade-level metaproductivity estimates; descendant performance aggregates guide which agents to expand or evaluate.
- Evaluation: SWE-bench Verified-60, SWE-bench Lite, Polyglot using Accuracy; allocated CPU-hours for 800 evaluations; Pearson correlation of CMP estimates; leaderboard/transfer accuracy.
- Main result: HGM outperforms prior self-improving coding-agent development methods while using fewer allocated CPU-hours. Table 2 reports HGM 56.7% on SWE-Verified-60 and 30.5% on Polyglot, compared with DGM 53.3% and 27.1%.
- Performance versus baseline: HGM requires 517 CPU-hours versus DGM 1231 on SWE-Verified-60, and 347 versus DGM 2385 on Polyglot; on SWE-Lite standard, the HGM best-belief agent reaches 49.0% with GPT-5-mini and 57.0% with GPT-5 transfer.
- Cost/token reporting: `sim`; NR as monetary cost; reports allocated CPU-hours: HGM 517 hours on SWE-Verified-60 and 347 hours on Polyglot for 800 evaluations.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0098_TA00292_huxley-g-del-machine-human-level-coding-agent-development-by-an-approximation-of.txt`
- JSON: `extraction/json/FT0098_huxley-gödel-machine-human-level-coding-agent-development-by-an-approximation-of-th.json`
