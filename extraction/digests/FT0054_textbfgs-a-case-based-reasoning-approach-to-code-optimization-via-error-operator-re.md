# TextBFGS: A Case-Based Reasoning Approach to Code Optimization via Error-Operator Retrieval

## Identifiers

- Included ID: I090
- Full-text ID: FT0054
- Extraction key: `zhang2026textbfgs`
- Role: `architecture`
- Architecture status: `arch_knowledge_graph_case_base`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_knowledge_graph_case_base`.
- Storage: ChromaDB case base of historical error-to-operator correction trajectories, including pre-optimization text, error feedback, abstract operator, and post-optimization text.
- Retrieval/control: retrieves cases by error/gradient similarity and performs a one-pass update that combines error diagnosis, operator application, and code revision.
- Evaluation: HumanEval-Hard and MBPP-Hard, with in-domain and cross-domain case bases.
- Main result: HumanEval-Hard with the MBPP case base reaches 97.78 Base Pass and 93.33 Plus Pass; MBPP-Hard with the MBPP case base reaches 94.02 Base Pass and 74.36 Plus Pass.
- Cost/token reporting: `sim_detalhado`; calls and token counts per task are reported.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0054_TA00478_textbfgs-a-case-based-reasoning-approach-to-code-optimization-via-error-operator.txt`
- JSON: `extraction/json/FT0054_textbfgs-a-case-based-reasoning-approach-to-code-optimization-via-error-operator-re.json`
