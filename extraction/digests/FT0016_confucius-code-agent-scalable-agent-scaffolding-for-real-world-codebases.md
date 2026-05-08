# Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases

## Identifiers

- Included ID: I016
- Full-text ID: FT0016
- Extraction key: `wong2025confucius`
- Role: `architecture`
- Architecture status: `arch_persistent_workspace_state`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `hibrido`.
- Storage format: Hierarchical working memory (árvore de arquivos Markdown com tags de metadados e escopos de visibilidade: session, entry, runnable) + notas persistentes cross-session (Markdown em diretório por sessão, e.g. research/findings.md, solutions/bug_fix.md, incluindo hindsight notes para falhas) + context compression summaries (plano estruturado com goals, decisions, TODOs, gerado pelo Architect Agent)
- Retrieval method: `hibrido`.
- Evaluation method: `benchmark`.
- Benchmarks: SWE-Bench-Pro (731 tasks), SWE-Bench-Verified (500 tasks), PyTorch-Bench (custom)
- Main result: CCA atinge 59.0% Resolve@1 no SWE-Bench-Pro com GPT-5.2, superando OpenAI (56.0%); com Claude 4.5 Sonnet atinge 52.7% vs Live-SWE-Agent 45.8%. Notas persistentes reduzem turnos de 64 para 61 e tokens de 104k para 93k, com ganho de +1.4pp em Resolve Rate.
- Performance versus baseline: +3.0pp vs OpenAI (59.0% vs 56.0%) com GPT-5.2; +6.9pp vs Live-SWE-Agent (52.7% vs 45.8%) com Claude 4.5 Sonnet; +1.8pp vs OpenHands (74.6% vs 72.8%) no SWE-Bench-Verified
- Cost reporting: `sim_parcial`; NR

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0016_TA00156_confucius-code-agent-scalable-agent-scaffolding-for-real-world-codebases.txt`
- JSON: `extraction/json/FT0016_confucius-code-agent-scalable-agent-scaffolding-for-real-world-codebases.json`
