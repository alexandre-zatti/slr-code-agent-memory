# EvoLattice: Persistent Internal-Population Evolution through Multi-Alternative Quality-Diversity Graph Representations for LLM-Guided Program Discovery

## Identifiers

- Included ID: I019
- Full-text ID: FT0033
- Extraction key: `yuksel2025evolattice`
- Role: `architecture`
- Architecture status: `arch_self_evolution_archive`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_self_evolution_archive`.
- Storage: Persistent directed acyclic graph where each node stores multiple alternatives; every valid path defines an executable candidate, and alternatives retain performance statistics for reuse, recombination, mutation, and pruning.
- Evaluation: NAS-Bench-Suite-Zero Medium proxy-quality benchmark; program-synthesis proxy and optimizer meta-learning tasks using Spearman rank correlation; confidence interval half-width; best-score trajectory; structural validity; stability under mutation.
- Main result: EvoLattice preserves internal diversity and outperforms fixed and LLM-guided single-path evolution baselines on NAS-Bench-Suite-Zero. Table 1 reports EvoLattice proxy Spearman rho 0.15-0.16 with CI half-width ±0.04, the highest among listed methods.
- Performance versus baseline: EvoLattice exceeds AlphaEvolve-style diff evolution (0.11 ±0.06), ShinkaEvolve-like parent sampling (0.12 ±0.05), FunSearch-style proxy generation (0.09 ±0.07), and LPZero (0.10 ±0.05).
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0033_TA01175_evolattice-persistent-internal-population-evolution-through-multi-alternative-qu.txt`
- JSON: `extraction/json/FT0033_evolattice-persistent-internal-population-evolution-through-multi-alternative-quali.json`
