# KAPSO: A Knowledge-grounded framework for Autonomous Program Synthesis and Optimization

## Identifiers

- Included ID: I063
- Full-text ID: FT0124
- Extraction key: `nadafian2026kapso`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `hibrido`.
- Storage format: Knowledge system: MediaWiki typed pages (Principle, Implementation, Environment, Heuristic) com Neo4j graph index + Weaviate vector index, ingerindo repos, docs, papers e web content de 2000+ fontes. Cognitive memory: episodic store em Weaviate vector DB com JSON fallback (trigger, lesson, recommended action, provenance para experiment branch). Experimentation engine: git branches isoladas com artifacts commitados.
- Retrieval method: `hibrido`.
- Evaluation method: `benchmark`.
- Benchmarks: MLE-Bench (Kaggle-style ML competitions), ALE-Bench (AtCoder heuristic contests, C++)
- Main result: MLE-Bench: 50.67% medal rate (vs 35.11% melhor open-source R&D-Agent, +15.56pp); ALE-Bench: ELO 1909.4, rank percentile 6.1% (vs ALE-Agent 1879.3, 6.8%) com custo 9% menor ($914.8 vs $1003.3).
- Performance versus baseline: +15.56pp medal rate vs R&D-Agent em MLE-Bench; +30.1 ELO vs ALE-Agent em ALE-Bench; vantagem concentrada em tarefas Hard (+17.78pp)
- Cost reporting: `sim_parcial`; ALE-Bench: $914.8 vs $1003.3 ALE-Agent (-8.8%); MLE-Bench: orçamento fixo de $200 não permite comparação direta

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0124_TA00184_kapso-a-knowledge-grounded-framework-for-autonomous-program-synthesis-and-optimi.txt`
- JSON: `extraction/json/FT0124_kapso-a-knowledge-grounded-framework-for-autonomous-program-synthesis-and-optimizat.json`
