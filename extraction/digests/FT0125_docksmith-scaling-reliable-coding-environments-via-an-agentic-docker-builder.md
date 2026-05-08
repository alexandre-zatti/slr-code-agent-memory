# DockSmith: Scaling Reliable Coding Environments via an Agentic Docker Builder

## Identifiers

- Included ID: I057
- Full-text ID: FT0125
- Extraction key: `zhang2026docksmith`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: SWE-Factory global memory pool of validated Dockerfile and evaluation-script pairs, augmented for cross-task retrieval as demonstrations for new repository environments.
- Evaluation: Multi-Docker-Eval, SWE-bench Verified, SWE-bench Multilingual, Terminal-Bench 2.0, ablations, error analysis, and case studies.
- Main result: DockSmith reaches 39.72% Fail-to-Pass and 58.28% Commit Rate on Multi-Docker-Eval, exceeding evaluated open- and closed-source baselines and the prior reported upper bound of 37.7% F2P.
- Performance versus baseline: improves +20.3 absolute F2P points over Qwen3-Coder-30B-A3B-Instruct and reduces total errors from 3,757 to 2,161.
- Cost/token reporting: `sim_parcial`; reports average input/output tokens and training-token mixing ratios, but no monetary cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0125_TA00187_docksmith-scaling-reliable-coding-environments-via-an-agentic-docker-builder.txt`
- JSON: `extraction/json/FT0125_docksmith-scaling-reliable-coding-environments-via-an-agentic-docker-builder.json`
