# DARWIN: Dynamic Agentically Rewriting Self-Improving Network

## Identifiers

- Included ID: I055
- Full-text ID: FT0064
- Extraction key: `jiang2026darwin`
- Role: `architecture`
- Architecture status: `arch_self_evolution_archive`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_self_evolution_archive`.
- Storage: persistent JSON-based memory files recording evolutionary history, source paths, code-modification summaries, timestamps, benchmark outcomes, token counts, backend metadata, file hierarchy, and prior structure across generations.
- Evaluation: nanoGPT on a Shakespeare prose dataset using perplexity, MFU, generation time, and training-error metrics.
- Main result: after five generations, DARWIN reports best perplexity 37.70 versus baseline 38.498 and best MFU 0.392 versus baseline 0.397; the paper characterizes the overall result as not significant.
- Performance versus baseline: the paper reports a 2.07% reduction in perplexity and a 1.26% reduction in MFU; removing persistent memory produced about 3% worse performance, with caution about insignificant results.
- Cost/token reporting: `sim_parcial`; reports average generation time of 223 seconds but no monetary cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0064_TA01109_darwin-dynamic-agentically-rewriting-self-improving-network.txt`
- JSON: `extraction/json/FT0064_darwin-dynamic-agentically-rewriting-self-improving-network.json`
