# Smarter Together: Creating Agentic Communities of Practice through Shared Experiential Learning

## Identifiers

- Included ID: I035
- Full-text ID: FT0012
- Extraction key: `tablan2025smarter`
- Role: `architecture`
- Architecture status: `arch_shared_memory`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `banco_experiencia`.
- Storage format: Knowledge base: ~34000 documentation blobs de bibliotecas data science (NumPy, Pandas, Matplotlib, SciPy, scikit-learn, PyTorch, TensorFlow) indexados como embeddings + texto. Experiential memory: traces estruturados de interações agente-usuário (contexto do problema, recomendação, feedback), clusterizados por similaridade semântica e curados em padrões generalizáveis. Aprendizado contínuo via epochs de curação.
- Retrieval method: `hibrido`.
- Evaluation method: `benchmark`.
- Benchmarks: DS-1000 (1000 problemas de data science de StackOverflow: NumPy, Pandas, Matplotlib, SciPy, scikit-learn, PyTorch, TensorFlow)
- Main result: Spark melhora qualidade de código em todos os modelos: Qwen3-Coder +0.66 (4.23→4.89), Haiku 4.5 +0.41 (4.50→4.91), GPT-5-Codex +0.05 (4.78→4.83). Modelo open-weights 30B com Spark iguala GPT-5-Codex sem Spark. 98.2% das recomendações classificadas como pelo menos GOOD.
- Performance versus baseline: +0.66 code quality Qwen3-Coder (4.23→4.89); +0.41 Haiku 4.5 (4.50→4.91); +0.05 GPT-5-Codex (4.78→4.83); todos WITH-SPARK excedem qualidade humana (4.28)
- Cost reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0012_TA00142_smarter-together-creating-agentic-communities-of-practice-through-shared-experie.txt`
- JSON: `extraction/json/FT0012_smarter-together-creating-agentic-communities-of-practice-through-shared-experienti.json`
