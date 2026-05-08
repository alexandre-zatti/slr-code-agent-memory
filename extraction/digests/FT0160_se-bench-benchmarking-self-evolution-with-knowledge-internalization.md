# SE-Bench: Benchmarking Self-Evolution with Knowledge Internalization

## Identifiers

- Included ID: I084
- Full-text ID: FT0160
- Extraction key: `yuan2026sebench`
- Role: `contextual_benchmark`
- Architecture status: `contextual_not_applicable`
- Architecture denominator decision: `exclude_contextual`

## Evidence Role

Contextual benchmark.
Benchmark evidence for self-evolution through knowledge internalization on coding tasks.

## Key Extracted Facts

- SE-Bench evaluates whether agents internalize an obfuscated NumPy/ZWC API and solve coding tasks without documentation.
- Closed-SFT-RL reaches 54.4% Single and 17.9% Multiple accuracy for Qwen3-8B; Open/Closed RL and Absolute-Zero report 0.0%.
- Memory-based methods are non-trivial but imperfect; treat as benchmark evidence for knowledge internalization.

## Denominator Notes

- Controlled-comparison status: `not_applicable_contextual`.
- Extraction verification status: `verified_from_full_text`.
- Notes: Contextual benchmark; evaluates internalization and memory/self-evolution baselines rather than proposing one deployed persistence architecture.

## Source Files

- PDF text: `search/full-texts/text/FT0160_TA01615_se-bench-benchmarking-self-evolution-with-knowledge-internalization.txt`
- JSON: `extraction/json/FT0160_se-bench-benchmarking-self-evolution-with-knowledge-internalization.json`
