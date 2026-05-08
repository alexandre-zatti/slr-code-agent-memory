# Reflection-Driven Control for Trustworthy Code Agents

## Identifiers

- Included ID: I033
- Full-text ID: FT0017
- Extraction key: `wang2025reflectiondriven`
- Role: `architecture`
- Architecture status: `arch_security_memory`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_security_memory`.
- Storage: Evolving reflective memory repository with dynamic memory for newly safe/unsafe cases and structured reflection records, plus static memory of secure coding standards and vulnerability knowledge; retrieved examples and guidelines are injected into later reasoning.
- Evaluation: 125 secure-code evaluation scenarios across eight classes of security-critical programming tasks using Security rate, pass rate, effective total score, secure count, unresolved count, retrieval similarity, retrieval success rate, fallback usage rate, cost and token usage.
- Main result: Reflection-Driven Control improves security and policy compliance while largely preserving functional correctness. Security rate gains include gpt-4o from 85.7 to 95.0, qwen3-coder-plus from 83.7 to 94.9, and gemini-2.5-pro from 88.0 to 97.1.
- Performance versus baseline: Base+Reflex improves security rate by +2.9 for gpt-3.5-turbo, +9.3 for gpt-4o, +11.2 for qwen3-coder-plus, and +9.1 for gemini-2.5-pro; pass rate is mostly preserved but decreases for qwen3-coder-plus (86.7 to 80.1).
- Cost/token reporting: `sim_detalhado`; Average cost per scenario $5.37e-4; average cost per successful repair $5.67e-4; total token usage 4.48e4 tokens over 125 scenarios.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0017_TA00162_reflection-driven-control-for-trustworthy-code-agents.txt`
- JSON: `extraction/json/FT0017_reflection-driven-control-for-trustworthy-code-agents.json`
