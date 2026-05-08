# Decocted Experience Improves Test-Time Inference in LLM Agents

## Identifiers

- Included ID: I056
- Full-text ID: FT0140
- Extraction key: `shen2026decocted`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: raw memory stores problem statements, trajectories, and feedback; distilled lesson memory stores reusable lessons; consolidated memory keeps k-means representatives; hierarchical concept trees organize memories into concept groups for retrieval.
- Evaluation: math reasoning, WebShop, and SWE-bench/SWE-agent settings using average accuracy, average input tokens, output tokens, interaction steps, retrieval relevance, and SWE-bench resolved status.
- Main result: raw and distilled experience outperform vanilla agents; distilled lessons outperform raw experience on agentic WebShop and SWE tasks; moderate memory consolidation and concept-tree retrieval improve scalability.
- Performance versus baseline: concept-tree retrieval improves over top-k lesson retrieval on WebShop and shows noticeable improvement on SWE; excessive K/raw context can degrade performance.
- Cost/token reporting: `sim_parcial`; reports input-token, output-token, and interaction-step efficiency curves but no monetary cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0140_TA00422_decocted-experience-improves-test-time-inference-in-llm-agents.txt`
- JSON: `extraction/json/FT0140_decocted-experience-improves-test-time-inference-in-llm-agents.json`
