# Your Code Agent Can Grow Alongside You with Structured Memory

## Identifiers

- Included ID: I094
- Full-text ID: FT0041
- Extraction key: `deng2026memcoder`
- Role: `architecture`
- Architecture status: `arch_repository_memory`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `banco_experiencia`.
- Storage format: Vector database (FAISS) de memory entries estruturados como sextuplas: (commit message o, code changes c, functional keywords k, problem description p, root-cause analysis r, summarized solution s). Construídos de commits históricos via LLM polisher (Defect Management theory). Novas entradas adicionadas via self-internalization de soluções human-verified.
- Retrieval method: `hibrido`.
- Evaluation method: `benchmark`.
- Benchmarks: SWE-bench Verified (500)
- Main result: MemCoder atinge 78.8% (pass@1) e 83.8% (pass@2) com GPT-5.2 no SWE-bench Verified, comparável ao SOTA. Com DeepSeek-V3.2, alcança 77.8% vs 68.4% sem memória (+9.4pp), demonstrando que memória estruturada de commits desbloqueia modelos gerais para SE complexa.
- Performance versus baseline: +9.4pp vs sem memória com DeepSeek-V3.2 (77.8% vs 68.4%); +3.4pp vs OpenHands+GPT-5.2 (78.8% vs ~74.4%); top-6 no leaderboard SWE-bench Verified
- Cost reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0041_TA00208_your-code-agent-can-grow-alongside-you-with-structured-memory.txt`
- JSON: `extraction/json/FT0041_your-code-agent-can-grow-alongside-you-with-structured-memory.json`
