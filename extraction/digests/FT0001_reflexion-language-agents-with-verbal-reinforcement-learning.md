# Reflexion: Language Agents with Verbal Reinforcement Learning

## Identifiers

- Included ID: I001
- Full-text ID: FT0001
- Extraction key: `shinn2023reflexion`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Reflective natural-language experience summaries stored in a long-term episodic memory buffer and injected into later trials; trajectory history acts as short-term memory.
- Evaluation: AlfWorld, HotPotQA, HumanEval, MBPP, LeetcodeHardGym using Success rate; pass@1 accuracy; test-generation accuracy; ablation accuracy.
- Main result: Reflexion stores verbal feedback in episodic memory and improves over baseline agents across decision-making, reasoning, and programming tasks. On code generation, Reflexion reports 91.0% pass@1 on HumanEval Python, 68.0% on HumanEval Rust, 77.1% on MBPP Python, 75.4% on MBPP Rust, and 15.0% on LeetcodeHard Python.
- Performance versus baseline: HumanEval Python improves from GPT-4 80.1% pass@1 to 91.0% (+10.9pp); HumanEval Rust improves from GPT-4 60.0% to 68.0% (+8.0pp); LeetcodeHard Python improves from GPT-4 7.5% to 15.0% (+7.5pp).
- Cost/token reporting: `nao`; NR

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0001_TA00310_reflexion-language-agents-with-verbal-reinforcement-learning.txt`
- JSON: `extraction/json/FT0001_reflexion-language-agents-with-verbal-reinforcement-learning.json`
