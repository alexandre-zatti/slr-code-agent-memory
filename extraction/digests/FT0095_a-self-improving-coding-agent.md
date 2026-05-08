# A Self-Improving Coding Agent

## Identifiers

- Included ID: I008
- Full-text ID: FT0095
- Extraction key: `robeyns2025sica`
- Role: `architecture`
- Architecture status: `arch_self_evolution_archive`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_self_evolution_archive`.
- Storage: Archive of previous self-modified coding-agent implementations, benchmark results, average cost/time/token metrics, and archive-analysis traces; the best archived agent is selected as the next meta-agent for self-modification.
- Evaluation: SWE-Bench Verified subset, LiveCodeBench, synthetic file-editing benchmark, synthetic symbol-location benchmark using Benchmark accuracy; average per-problem cost; average per-problem time; average total tokens; cached-token percentage; utility combining score, cost, and time.
- Main result: SICA self-edits its own agent code and improves on coding benchmarks. Table 1 reports SWE-Bench Verified accuracy increasing from 0.17 at iteration 0 to a peak of 0.53 at iteration 14, with LiveCodeBench improving from 0.65 to 0.71 by iteration 15.
- Performance versus baseline: SWE-Bench Verified improves from 17% to 53% at the best reported iteration (+36pp). File editing improves from 0.82 to 0.96 at peak, symbol location from 0.35 to 0.43 at peak, and LiveCodeBench from 0.65 to 0.71 by iteration 15.
- Cost/token reporting: `sim`; Average per-problem cost ranges from $1.58 to $2.70 across iterations; the 15-iteration API run cost approximately $7,000.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0095_TA00284_a-self-improving-coding-agent.txt`
- JSON: `extraction/json/FT0095_a-self-improving-coding-agent.json`
