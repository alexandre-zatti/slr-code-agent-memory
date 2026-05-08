# OpenSage: Self-programming Agent Generation Engine

## Identifiers

- Included ID: I077
- Full-text ID: FT0039
- Extraction key: `li2026opensage`
- Role: `architecture`
- Architecture status: `arch_knowledge_graph_case_base`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_knowledge_graph_case_base`.
- Storage: hierarchical graph memory with execution-based short-term memory, target-level long-term Neo4j memory, and a dedicated memory agent.
- Evaluation: CyberGym, Terminal-Bench 2.0, SWE-Bench Pro, DevOps-Gym, plus LOCOMO appendix evaluation.
- Main result: SageAgent via OpenSage reports 60.2% on CyberGym, 78.4 +/- 2.2 on Terminal-Bench 2.0, 59.0% on SWE-Bench Pro, and 46.8% on DevOps-Gym.
- Performance versus baseline: SWE-Bench Pro memory ablation gives OpenSage 59.0 versus Mem0g 56.4 and NoMem 56.2.
- Cost/token reporting: `sim_parcial`; Terminal-Bench cost/performance tradeoff is discussed, but no isolated memory cost is reported.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0039_TA00202_opensage-self-programming-agent-generation-engine.txt`
- JSON: `extraction/json/FT0039_opensage-self-programming-agent-generation-engine.json`
