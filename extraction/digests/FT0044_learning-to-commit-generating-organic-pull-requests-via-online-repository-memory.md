# Learning to Commit: Generating Organic Pull Requests via Online Repository Memory

## Identifiers

- Included ID: I068
- Full-text ID: FT0044
- Extraction key: `li2026learningcommit`
- Role: `architecture`
- Architecture status: `arch_repository_memory`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_repository_memory`.
- Storage: continuously updated repository-specific skill document learned from chronological historical commits through contrastive reflection against oracle diffs.
- Evaluation: held-out future pull-request tasks from an expert-maintained repository, deterministic metrics, pairwise LLM judging, and case study.
- Main result: skill-conditioned agents improve localization, reduce patch bloat, and win more pairwise comparisons in three of four settings.
- Performance versus baseline: File IoU reaches 80% versus 61% in seq-all and 80% versus 68% in par-bycat; pairwise win rates reach 54%/57% in par-bycat and 55%/58% in seq-all.
- Cost/token reporting: `sim_parcial`; trajectory steps are reported, but no monetary or token cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0044_TA00235_learning-to-commit-generating-organic-pull-requests-via-online-repository-memory.txt`
- JSON: `extraction/json/FT0044_learning-to-commit-generating-organic-pull-requests-via-online-repository-memory.json`
