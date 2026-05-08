# TOM-SWE: User Mental Modeling For Software Engineering Agents

## Identifiers

- Included ID: I040
- Full-text ID: FT0010
- Extraction key: `zhou2025tomswe`
- Role: `architecture`
- Architecture status: `arch_user_model_memory`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `hibrido`.
- Storage format: Three-tier hierarchical memory como database externo: (1) Raw session storage — históricos completos de sessões anteriores como texto, (2) Session-based user models — JSON estruturado com user_intent, user_profile, message_preferences (inferred constraints, preferred_approach) extraídos via LLM analyze_session, (3) Overall user model — JSON agregado com profile_description, interaction_style (verbosity, question_timing), coding_preferences list, session_summaries. BM25 search across all tiers.
- Retrieval method: `bm25`.
- Evaluation method: `misto`.
- Benchmarks: Ambiguous SWE-bench (500 instâncias), Stateful SWE benchmark (500 instâncias, custom com 15 perfis de desenvolvedor), In-the-wild human study (209 sessões, 174 sugestões ToM, 17 desenvolvedores profissionais, 3 semanas)
- Main result: ToM-SWE com Claude Sonnet 4 atinge 63.4% no Ambiguous SWE-bench (+11.5pp vs CodeAct) e 59.7% no Stateful SWE (+41.6pp vs CodeAct 18.1%). User satisfaction 3.62 vs 2.57 (+41%). Estudo in-the-wild com 17 devs profissionais: 86.2% aceitação de sugestões ToM (74.1% accept + 12.1% partial).
- Performance versus baseline: +11.5pp Ambiguous SWE-bench (63.4% vs 51.9%) com Claude Sonnet 4; +41.6pp Stateful SWE (59.7% vs 18.1%); satisfaction 3.62 vs 2.57 (+41%); RAGCodeAct inferior ao ToMCodeAct em todos modelos
- Cost reporting: `sim_detalhado`; $0.17 overhead ToM por sessão (~16% do custo total); GPT-5-nano ToM ($0.02) atinge 38.0% resolve rate no Stateful SWE; custo marginal para ganhos substanciais

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0010_TA00127_tom-swe-user-mental-modeling-for-software-engineering-agents.txt`
- JSON: `extraction/json/FT0010_tom-swe-user-mental-modeling-for-software-engineering-agents.json`
