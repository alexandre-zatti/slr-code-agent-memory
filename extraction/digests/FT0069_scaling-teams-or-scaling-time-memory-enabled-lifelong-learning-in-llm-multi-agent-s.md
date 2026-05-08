# Scaling Teams or Scaling Time? Memory Enabled Lifelong Learning in LLM Multi-Agent Systems

## Identifiers

- Included ID: I083
- Full-text ID: FT0069
- Extraction key: `wu2026llmamem`
- Role: `architecture`
- Architecture status: `arch_shared_memory`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_shared_memory`.
- Storage: episodic task trajectories, procedural strategies with success/failure counts, and transactive memory for agent profiles and team patterns under local, shared, and hybrid topologies.
- Retrieval/control: relevance-importance retrieval, top-3 memory items, JSON persistence across tasks, and periodic episodic-to-procedural consolidation.
- Evaluation: MultiAgentBench collaborative coding, research, and database environments; no-memory, MARBLE, A-Mem, topology ablation, consolidation-interval ablation, team-size scaling, and token-usage analysis.
- Main result: LLMA-Mem improves AAS in most model-environment settings, including +5.92 for DeepSeek-V3.2 on research and +3.19 for Qwen3-32B-Instruct on database.
- Cost/token reporting: `sim_detalhado`; LLMA-Mem reports average-token reductions from 9.4% to 71.7% relative to memory baselines.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0069_TA01607_scaling-teams-or-scaling-time-memory-enabled-lifelong-learning-in-llm-multi-agen.txt`
- JSON: `extraction/json/FT0069_scaling-teams-or-scaling-time-memory-enabled-lifelong-learning-in-llm-multi-agent-s.json`
