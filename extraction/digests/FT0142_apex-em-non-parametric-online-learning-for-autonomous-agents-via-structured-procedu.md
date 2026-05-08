# APEX-EM: Non-Parametric Online Learning for Autonomous Agents via Structured Procedural-Episodic Experience Replay

## Identifiers

- Included ID: I046
- Full-text ID: FT0142
- Extraction key: `banerjee2026apexem`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Persistent Experience Memory organized as a Procedural Knowledge Graph with structured procedural-episodic traces, entities, plans, generated artifacts, iteration histories, error analyses, quality scores, and dual successful/failed outcome indexing.
- Evaluation: BigCodeBench, KGQAGen-10k, Humanity's Last Exam; planned/comparative MemRL benchmarks include Lifelong Agent Bench and ALFWorld using Last Epoch Success Rate, Cumulative Success Rate, LASM accuracy for KGQA, iteration-count reduction, transfer accuracy, ablation success rates.
- Main result: On BigCodeBench, APEX-EM with Opus judge reaches 83.3% SR / 84.0% CSR versus 53.9% no-memory baseline. On KGQAGen-10k it reaches 89.6% accuracy / 95.3% CSR, and on HLE entity graph retrieval reaches 48.0% / 53.3% CSR versus 25.2% no-memory baseline.
- Performance versus baseline: BigCodeBench improvement is +29.4pp over no memory and exceeds MemRL's reported +11.0pp gain. KGQA full-memory plus Opus judge reaches 89.6% versus 41.3% no memory. HLE entity graph retrieval improves 25.2% to 48.0%.
- Cost/token reporting: `sim_parcial`; NR as monetary/token cost; reports iteration reduction from memory accumulation, such as BCB full memory 1.50 to 1.32 iterations and KGQA Opus judge 4.40 to 2.50 iterations from epoch 1 to epoch 10.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0142_TA00484_apex-em-non-parametric-online-learning-for-autonomous-agents-via-structured-proc.txt`
- JSON: `extraction/json/FT0142_apex-em-non-parametric-online-learning-for-autonomous-agents-via-structured-procedu.json`
