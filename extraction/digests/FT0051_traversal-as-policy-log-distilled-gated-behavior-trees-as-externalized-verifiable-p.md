# Traversal-as-Policy: Log-Distilled Gated Behavior Trees as Externalized, Verifiable Policies for Safe, Robust, and Efficient Agents

## Identifiers

- Included ID: I092
- Full-text ID: FT0051
- Extraction key: `li2026traversalaspolicy`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `outro`.
- Storage format: Gated Behavior Tree (GBT): árvore executável single-rooted com 21 task-family roots. Cada nó macro = (description NL, coarse tags, risk_level, behavior_signature σ = (σ_disc, σ_cont), env_context pointer). Gates determinísticos: RuleGates (code predicates sobre ctx estruturado) + ContentGates (frozen Llama-Guard-3-8B classifier, temp=0). Spine memory = sequência compacta de macros visitados como estado de longo prazo. Self-evolution (GBT-SE): repair local via analogical successes com regression testing preservando safety invariants.
- Retrieval method: `outro`.
- Evaluation method: `benchmark`.
- Benchmarks: SWE-bench Verified (500), WebArena (812), GPQA (448), AgentSafetyBench, AgentHarm (public), Agent Security Bench (ASB)
- Main result: GBT-SE eleva success rate de 34.6% para 73.6% no SWE-bench Verified e de 19.7% para 66.9% no WebArena, enquanto reduz violations para 0.2% e unsafe success para 0.0%. Tokens reduzidos ~40%. Com 8B executors (Qwen3-VL-8B), GBT mais que triplica success no SWE-bench (14.0%→58.8%), demonstrando decoupling entre reasoning capacity offline e execução online.
- Performance versus baseline: +39.0pp SWE-bench (73.6% vs 34.6%); +47.2pp WebArena (66.9% vs 19.7%); +28.5pp GPQA (87.3% vs 58.7%); violations 2.8%→0.2% SWE-bench; unsafe success 1.2%→0.0%
- Cost reporting: `sim_parcial`; Tok/Chars 208k/820k→126k/490k SWE-bench (-39%/-40%); 94k/360k→52k/205k WebArena (-45%/-43%); 8B executors viáveis com same GBT artifact

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0051_TA00405_traversal-as-policy-log-distilled-gated-behavior-trees-as-externalized-verifiabl.txt`
- JSON: `extraction/json/FT0051_traversal-as-policy-log-distilled-gated-behavior-trees-as-externalized-verifiable-p.json`
