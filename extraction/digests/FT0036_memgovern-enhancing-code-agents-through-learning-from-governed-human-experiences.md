# MemGovern: Enhancing Code Agents through Learning from Governed Human Experiences

## Identifiers

- Included ID: I071
- Full-text ID: FT0036
- Extraction key: `wang2026memgovern`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `banco_experiencia`.
- Storage format: 135K experience cards em vector database. Cada card: Index Layer (Problem Summary normalizado + Diagnostic Signals generalizáveis como exception types, error signatures, component tags) + Resolution Layer (Root Cause, Fix Strategy abstrata, Patch Digest semântico, Verification steps). Pipeline de governança: Experience Selection (repo scoring) → Standardization (content purification + unified repair experience protocol) → Quality Control (LLM checklist scoring com refine loop).
- Retrieval method: `hibrido`.
- Evaluation method: `benchmark`.
- Benchmarks: SWE-bench Verified (500)
- Main result: MemGovern melhora SWE-Agent em média +4.65pp em resolve rate no SWE-bench Verified, consistente em 7 LLMs. Maiores ganhos em modelos fracos (+9.4pp GPT-4o, +8.2pp Qwen3-235B). Agentic Search (search-then-browse) supera RAG estático e Agentic RAG em todos os modelos testados.
- Performance versus baseline: +3.2pp com Claude 4 Sonnet (69.8% vs 66.6%); +8.2pp com Qwen3-235B (55.4% vs 47.2%); +9.4pp com GPT-4o (32.6% vs 23.2%); média +4.65pp em 7 LLMs
- Cost reporting: `sim_detalhado`; Overhead moderado: $6.94→$7.27 com Claude 4 Sonnet (+4.8%); $0.14→$0.20 com GPT-4o-Mini (+43%); proporcional ao uso de Searching/Browsing tools

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0036_TA00173_memgovern-enhancing-code-agents-through-learning-from-governed-human-experiences.txt`
- JSON: `extraction/json/FT0036_memgovern-enhancing-code-agents-through-learning-from-governed-human-experiences.json`
