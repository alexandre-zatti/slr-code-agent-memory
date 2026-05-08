# Complementary Reinforcement Learning

## Identifiers

- Included ID: I052
- Full-text ID: FT0153
- Extraction key: `muhtar2026complementaryrl`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Evolving experience bank managed by a centralized MemoryManager; the experience extractor distills, merges, deduplicates, retrieves, and maintains structured experience entries while co-evolving with the policy actor.
- Evaluation: MiniHack Room, WebShop, ALFWorld, SWE-Bench Verified, multi-task mixtures using Success rate, validation score, number of actions per task, multi-task evaluation average, performance gain versus baseline.
- Main result: Complementary RL consistently outperforms no-experience baselines. In single-task training it reports about a 1.3x performance margin on MiniHack Room and ALFWorld and a +3.0% gain on SWE-Bench; in multi-task evaluation, Complementary RL with experience averages 0.82 versus 0.75 baseline.
- Performance versus baseline: Multi-task table reports baseline average 0.75, Complementary RL evaluated with experience 0.82, and Complementary RL without experience 0.78. Static Online Experience with experience averages 0.59 and without experience 0.54, showing that static experience alone is insufficient.
- Cost/token reporting: `sim_parcial`; NR monetary cost; reports action-count efficiency such as 1.5x fewer actions on MiniHack and 2x fewer actions on ALFWorld.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0153_TA01075_complementary-reinforcement-learning.txt`
- JSON: `extraction/json/FT0153_complementary-reinforcement-learning.json`
