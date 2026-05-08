# Software Self-Extension with SelfEvolve: an Agentic Architecture for Runtime Code Generation

## Identifiers

- Included ID: I086
- Full-text ID: FT0132
- Extraction key: `fahim2026selfevolve`
- Role: `architecture`
- Architecture status: `arch_skill_rule_library`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_skill_rule_library`.
- Storage: persistent knowledge base with Prompts, Functions, and Tool Descriptors repositories; accepted generated functions and descriptors become reusable runtime capabilities.
- Retrieval/control: dispatcher first checks available tools, then generates requirements, tests, code, feedback, and accepted function registrations when a requested capability is missing.
- Evaluation: 11 manually designed self-extension tasks, five runs per task, compared against AgentCoder, AutoGen, MetaGPT, and a no-TDD ablation.
- Main result: SelfEvolve succeeds on 51 of 55 runs, or 92.7% Pass@1, versus 30.9% for AutoGen, 27.3% for MetaGPT, and 0.0% for AgentCoder.
- Cost/token reporting: `nao`; functional performance and iteration counts are reported, but monetary/token cost is not.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0132_TA00297_software-self-extension-with-selfevolve-an-agentic-architecture-for-runtime-code.txt`
- JSON: `extraction/json/FT0132_software-self-extension-with-selfevolve-an-agentic-architecture-for-runtime-code-ge.json`
