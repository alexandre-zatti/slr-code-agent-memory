# EXPEREPAIR: Dual-Memory Enhanced LLM-based Repository-Level Program Repair

## Identifiers

- Included ID: I021
- Full-text ID: FT0028
- Extraction key: `mu2025experepair`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Dual memory with episodic memory storing concrete repair demonstrations and semantic memory storing abstract reflective repair insights; memories are updated after repair trajectories and retrieved during test generation and patch generation.
- Evaluation: SWE-bench Lite using Pass@1 / resolved rate; average inference cost; ESR; RSR; unique resolved issues; ablation resolved rates.
- Main result: ExpeRepair achieves 47.7% pass@1 on SWE-bench Lite with Claude 3.5 Sonnet V2 at $2.07 average cost, and the abstract reports 49.3% pass@1 with Claude 3.7 Sonnet.
- Performance versus baseline: ExpeRepair surpasses PatchPilot 45.3% and DARS 47.0% on SWE-bench Lite while costing far less than DARS ($2.07 vs $12.24). Removing the experience module drops resolved rate from 47.7% to 41.3%.
- Cost/token reporting: `sim`; Average inference cost is $2.07 per SWE-bench Lite instance with Claude 3.5 Sonnet V2.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0028_TA00473_experepair-dual-memory-enhanced-llm-based-repository-level-program-repair.txt`
- JSON: `extraction/json/FT0028_experepair-dual-memory-enhanced-llm-based-repository-level-program-repair.json`
