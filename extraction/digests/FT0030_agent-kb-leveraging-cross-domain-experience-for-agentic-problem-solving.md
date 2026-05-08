# Agent KB: Leveraging Cross-Domain Experience for Agentic Problem Solving

## Identifiers

- Included ID: I010
- Full-text ID: FT0030
- Extraction key: `tang2025agentkb`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Framework-agnostic structured experience units E=<task embedding, structured goal constraints, action-reasoning pairs, metadata> stored behind REST APIs, with addition, deduplication, conflict resolution, and adaptive utility-based eviction.
- Evaluation: SWE-bench Lite, GAIA, Humanity's Last Exam Bio/Chem, GPQA using Pass@1/pass@2/pass@3 accuracy; success rate; retrieval latency; memory footprint; token and monetary cost budgets; ablation accuracy.
- Main result: AGENT KB enables cross-framework experience sharing and improves multiple agent/model combinations. On SWE-bench Lite, GPT-4.1 with SWE-Agent improves from 24.3% to 38.0% at max-iteration 50 and 42.3% at max-iteration 100 by pass@3; OpenHands with Claude-3.7 improves from 30.0% to 51.0% at max-iteration 50.
- Performance versus baseline: SWE-Agent GPT-4.1 improves 24.3% to 38.0% at 50 iterations (+13.7pp) and 27.0% to 42.3% at 100 iterations (+15.3pp). OpenHands Claude-3.7 improves 30.0% to 51.0% at 50 iterations (+21.0pp) and 41.3% to 53.3% at 100 iterations (+12.0pp).
- Cost/token reporting: `sim`; GAIA evaluation averages $0.52 per task, with retrieval loop adding about $0.27 over the full validation run; SWE-bench hinting averages $0.0037 per issue.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0030_TA00588_agent-kb-leveraging-cross-domain-experience-for-agentic-problem-solving.txt`
- JSON: `extraction/json/FT0030_agent-kb-leveraging-cross-domain-experience-for-agentic-problem-solving.json`
