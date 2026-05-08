# Multi-Agent Code-Orchestrated Generation for Reliable Infrastructure-as-Code

## Identifiers

- Included ID: I030
- Full-text ID: FT0092
- Extraction key: `khan2025macog`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: Memory Curator stores verified Infrastructure-as-Code tuples (P,T,Pi) with metadata, indexes typed motifs in a symbolic catalog and dense store, and returns typed motifs rather than raw code text for later planning and compilation.
- Evaluation: IaC-Eval using IaC-Eval score, BLEU, CodeBERTScore, LLM-judge score, ablation scores.
- Main result: MACOG improves IaC-Eval over prompt-only and RAG baselines. GPT-5 improves from 54.90 with RAG to 74.02 with MACOG, and Gemini-2.5 Pro improves from 43.56 with RAG to 60.13 with MACOG.
- Performance versus baseline: GPT-5 MACOG reaches 74.02 IaC-Eval, BLEU 11.86, CodeBERTScore 80.54, and LLM-judge 94.10. Ablations reduce IaC-Eval, including -Engineer at 64.89, -Security Prover at 61.45, -DevOps at 56.93, and -Memory Curator at 72.17.
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0092_TA00119_multi-agent-code-orchestrated-generation-for-reliable-infrastructure-as-code.txt`
- JSON: `extraction/json/FT0092_multi-agent-code-orchestrated-generation-for-reliable-infrastructure-as-code.json`
