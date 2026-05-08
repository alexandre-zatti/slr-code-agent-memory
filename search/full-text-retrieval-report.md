# Search Full-Text Retrieval Report

Date: 2026-04-28

Status: automated retrieval plus targeted public-URL rescue complete.
Two records still lack retrieved PDFs/texts; one of them was excluded from a
recovered publisher abstract, and one is finalized as not retrieved.

## Inputs

- Full-text screening ledger:
  `screening/full-text-screening.tsv`.
- Retrieval manifest:
  `search/full-text-retrieval.tsv`.
- Retrieval status ledger:
  `search/full-text-retrieval-status.tsv`.
- PDF/text directory:
  `search/full-texts/`.

## Retrieval Counts

- Records sought for full-text retrieval: 165.
- PDFs retrieved: 163.
- Text files converted with `pdftotext`: 163.
- Retrieval failures: 2.
- Retrieval failures still requiring eligibility decision: 0.

Retrieval source distribution:

- arXiv: 155.
- Manual public URL: 7.
- Unpaywall/open-access DOI: 1.
- Failed/no automated/manual route: 2.

## Failed Retrieval Records

| Full-text ID | Screening ID | Title | Failure reason | Screening status |
| --- | --- | --- | --- | --- |
| FT0073 | TA00776 | MAAP: A Self-Evolving Multi-Agent Automated Vulnerability Repair Framework for Python | `not_open_access` | Marked `not_retrieved`; not an eligibility exclusion. |
| FT0076 | TA00822 | SEED-APR: A closed-loop self-evolving framework for automated program repair | `no_pdf_url` | Excluded under CE1 from recovered publisher abstract after PDF/full-text route remained unavailable. |

MAAP public access checks covered Researchr, DBLP/OpenAlex, Unpaywall, and
ResearchGate metadata; none exposed a public PDF or full text as of
2026-04-28.

## Manual Resolutions

| Full-text ID | Screening ID | Resolution |
| --- | --- | --- |
| FT0078 | TA00857 | Malformed citation resolved to an ETASR browser-visualization optimization paper; public PDF retrieved. |
| FT0080 | TA01629 | *Self-Defining Systems* resolved to a December 2025 University of Washington white paper; public PDF retrieved. |

## Notes

- The two retrieval failures remain `retrieval_status=failed` in retrieval
  accounting.
  SEED-APR no longer requires eligibility screening because the recovered
  publisher abstract was decisive under CE1.
  MAAP is reported as not retrieved because public metadata is not sufficient
  for a final criterion-level decision.
- Seven initially failed records were recovered through documented public URLs
  in `search/full-text-manual-urls.tsv`.
- Missing-abstract records that did retrieve successfully should still be
  checked carefully at full text because the title/abstract decision was made
  from title/metadata only.
- `screening/full-text-screening.tsv` has been synchronized with retrieval
  status and planned PDF/text paths.
