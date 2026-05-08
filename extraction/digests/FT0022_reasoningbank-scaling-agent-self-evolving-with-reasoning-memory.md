# ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory

## Identifiers

- Included ID: I031
- Full-text ID: FT0022
- Extraction key: `ouyang2025reasoningbank`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Reasoning memory items distilled from self-judged successful and failed trajectories, with structured fields such as title, description, and when-to-apply guidance; new experiences are consolidated back into the repository.
- Evaluation: WebArena, Mind2Web, SWE-bench Verified using Resolve rate, average interaction steps, benchmark success metrics, ablation scores.
- Main result: ReasoningBank improves across web and software-engineering benchmarks. On SWE-bench Verified, Gemini-2.5-flash improves from 34.2% No Memory to 38.8%, and Gemini-2.5-pro improves from 54.0% to 57.4%, with fewer average interaction steps.
- Performance versus baseline: On SWE-bench Verified, Gemini-2.5-flash ReasoningBank reports 38.8% resolve versus 34.2% No Memory and 35.4% Synapse; Gemini-2.5-pro reports 57.4% versus 54.0% No Memory and 53.4% Synapse. Failure-trajectory ablations report larger gains than success-only memory variants.
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0022_TA00370_reasoningbank-scaling-agent-self-evolving-with-reasoning-memory.txt`
- JSON: `extraction/json/FT0022_reasoningbank-scaling-agent-self-evolving-with-reasoning-memory.json`
