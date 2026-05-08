# DomAgent: Leveraging Knowledge Graphs and Case-Based Reasoning for Domain-Specific Code Generation

## Identifiers

- Included ID: I058
- Full-text ID: FT0128
- Extraction key: `wang2026domagent`
- Role: `architecture`
- Architecture status: `arch_knowledge_graph_case_base`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_knowledge_graph_case_base`.
- Storage: knowledge graph of packages, functions, descriptions, parameters, and relations plus a vector-database case base of executable code cases selected for package and functional-cluster coverage.
- Evaluation: DS-1000 and Truck CAN Signal code-generation tasks using pass@1 and ablations.
- Main result: DomAgent improves DS-1000 total pass@1 to 39.2% with Qwen2.5-7B and 40.5% with LLaMA3.1-8B; on Truck CAN Signal, Qwen2.5-7B DomAgent reaches 96.64% total pass@1 and DomRetriever plus GPT-4o reaches 98.04%.
- Performance versus baseline: on Truck CAN Signal, Qwen2.5-7B improves from 39.62% to 96.64% total pass@1; on DS-1000, Qwen2.5-7B improves from 29.3% to 39.2%.
- Cost/token reporting: `nao`; no monetary or token-cost data reported, though KG-guided selection reaches comparable case-base performance with 30% selected cases versus 80% random sampling.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0128_TA00230_domagent-leveraging-knowledge-graphs-and-case-based-reasoning-for-domain-specifi.txt`
- JSON: `extraction/json/FT0128_domagent-leveraging-knowledge-graphs-and-case-based-reasoning-for-domain-specific-c.json`
