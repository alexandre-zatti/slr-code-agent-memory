# CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery

## Identifiers

- Included ID: I054
- Full-text ID: FT0063
- Extraction key: `qu2026coral`
- Role: `architecture`
- Architecture status: `arch_shared_memory`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_shared_memory`.
- Storage: shared persistent filesystem under `.coral/public` with `attempts/`, `notes/`, `skills/`, heartbeat configuration, session state, and private evaluator state symlinked into isolated worktrees.
- Evaluation: mathematical optimization, systems optimization, Anthropic kernel engineering, and Polyominoes packing benchmarks using final score, improvement rate, evaluation count, trajectory statistics, and ablations.
- Main result: single-agent CORAL achieves the best final score on all 11 mathematical and systems tasks and establishes new SOTA on eight tasks; four-agent co-evolution further improves stress-test results, including Kernel Engineering from 1350 cycles to 1103 cycles.
- Performance versus baseline: CORAL improvement rates are reported as 3-10 times higher than fixed evolutionary-search baselines; removing knowledge worsens Kernel Engineering from 1350 to 1601 cycles.
- Cost/token reporting: `sim_detalhado`; a typical 3-hour Claude Opus 4.6 single-agent run costs about USD 30-60, and four-agent runs cost about 3-4 times more.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0063_TA01090_coral-towards-autonomous-multi-agent-evolution-for-open-ended-discovery.txt`
- JSON: `extraction/json/FT0063_coral-towards-autonomous-multi-agent-evolution-for-open-ended-discovery.json`
