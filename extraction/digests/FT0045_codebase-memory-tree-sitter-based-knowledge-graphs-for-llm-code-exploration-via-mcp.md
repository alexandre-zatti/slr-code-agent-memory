# Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP

## Identifiers

- Included ID: I050
- Full-text ID: FT0045
- Extraction key: `vogel2026codebasememory`
- Role: `architecture`
- Architecture status: `arch_knowledge_graph_case_base`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_knowledge_graph_case_base`.
- Storage: Persistent Tree-Sitter-based codebase knowledge graph stored in a single SQLite file, maintained incrementally through file watching/content hashes, and exposed through 14 typed MCP structural-query tools.
- Evaluation: 31 real-world repositories across 31 languages; 12 structural code-question categories; system performance benchmarks on Apple M3 Pro using Answer quality score, tool calls per question, tokens per question, query latency, indexing time, incremental re-index time.
- Main result: Codebase-Memory achieves 0.83 answer-quality score versus 0.92 for an Explorer Agent, while using about 1,000 versus 10,000 tokens per question, 2.3 versus 4.8 tool calls, and sub-millisecond query latency.
- Performance versus baseline: MCP Agent reaches 90% of Explorer quality while using 10 times fewer tokens and 2.1 times fewer tool calls; it matches or exceeds explorer behavior on graph-native hub/caller queries for 19 of 31 languages.
- Cost/token reporting: `sim_parcial`; NR monetary cost; token/tool-call reductions are reported and translate to lower latency/cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0045_TA00236_codebase-memory-tree-sitter-based-knowledge-graphs-for-llm-code-exploration-via.txt`
- JSON: `extraction/json/FT0045_codebase-memory-tree-sitter-based-knowledge-graphs-for-llm-code-exploration-via-mcp.json`
