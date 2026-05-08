# PRISMA 2020 Checklist

Verification of PRISMA 2020 reporting coverage for the current manuscript.

Reference: Page MJ, McKenzie JE, Bossuyt PM, et al.
The PRISMA 2020 statement.
BMJ. 2021;372:n71.

Status: `[x]` complete | `[~]` partial | `[ ]` absent.

## Checklist

| # | Item | Status | Current Evidence |
| --- | --- | --- | --- |
| 1 | Title identifies the report as a systematic review. | [x] | `manuscript/main.tex`; title contains "Systematic Literature Review". |
| 2 | Abstract is structured and reports context, objective, method, results, and conclusion. | [x] | `manuscript/main.tex`. |
| 3 | Introduction explains rationale. | [x] | `manuscript/sections/introduction.tex`. |
| 4 | Introduction states objectives and research questions. | [x] | `manuscript/sections/introduction.tex`. |
| 5 | Eligibility criteria are specified. | [x] | `manuscript/sections/method.tex`; `screening/criteria.md`. |
| 6 | Information sources are specified. | [x] | `manuscript/sections/method.tex`; `search/search-strategy.md`. |
| 7 | Search strategy is reproducible. | [x] | `search/search-strategy.md`; `search/arxiv-query-chunks.tsv`; `search/scopus-query-branches.tsv`. |
| 8 | Selection process is reported. | [x] | `screening/title-abstract-screening.tsv`; `screening/full-text-screening.tsv`. |
| 9 | Data collection process is reported. | [x] | `extraction/extraction-form.md`; `extraction/compile_extracted_data.py`. |
| 10 | Data items are defined. | [x] | `extraction/extraction-form.md`. |
| 11 | Quality assessment is reported. | [x] | `analysis/quality-assessment.tsv`; manuscript method/results. |
| 12 | Effect measures are described. | [x] | Narrative synthesis; performance deltas are descriptive and not pooled effect sizes. |
| 13a-f | Synthesis eligibility, preparation, tabulation, methods, heterogeneity, and sensitivity are reported. | [x] | `analysis/synthesis-matrix.md`; `analysis/certainty-sensitivity-summary.md`; manuscript method/results. |
| 14 | Reporting-bias constraints are discussed. | [x] | Manuscript limitations; preprint and single-reviewer constraints. |
| 15 | Certainty assessment is reported. | [x] | `analysis/certainty-sensitivity-records.tsv`; `analysis/certainty-sensitivity-summary.md`. |
| 16a | Study selection flow is reported. | [x] | `analysis/prisma-flow.md`; `manuscript/figures/fig-01-prisma.pdf`. |
| 16b | Excluded full texts and reasons are available. | [x] | `screening/full-text-screening.tsv`. |
| 17 | Included-study characteristics are reported. | [x] | `extraction/extracted-data.tsv`; manuscript results tables. |
| 18 | Quality/risk information is reported. | [x] | `analysis/quality-assessment.tsv`; manuscript results. |
| 19 | Results of individual studies are available. | [x] | `extraction/digests/*.md`; `analysis/performance-normalized.tsv`. |
| 20a-d | Synthesis results, heterogeneity, and sensitivity are reported. | [x] | `analysis/synthesis-matrix.md`; manuscript results. |
| 21 | Reporting-bias limits are discussed per synthesis where relevant. | [x] | Manuscript results/discussion. |
| 22 | Certainty of evidence is reported. | [x] | `analysis/certainty-sensitivity-summary.md`; manuscript results. |
| 23a-d | Discussion interprets findings, evidence limitations, review limitations, and implications. | [x] | `manuscript/sections/discussion.tex`. |
| 24a | Registration status is stated. | [x] | Manuscript method. |
| 24b | Protocol availability is stated. | [~] | Public DOI pending; use repository path until fresh release is minted. |
| 24c | Protocol amendments are recorded. | [x] | `protocol/amendments.md`. |
| 25 | Support/funding is stated. | [x] | Manuscript declarations. |
| 26 | Competing interests are stated. | [x] | Manuscript declarations. |
| 27 | Data, code, and materials availability is stated. | [~] | Fresh replication package and DOI pending. |

## Open Items Before Submission

1. Mint and verify the fresh replication-package DOI.
2. Update manuscript data-availability text with the DOI.
3. Recheck line references after the final venue template is selected.
