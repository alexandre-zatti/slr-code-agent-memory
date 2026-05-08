# Self-Defining Systems

## Identifiers

- Included ID: I034
- Full-text ID: FT0080
- Extraction key: `anderson2025selfdefining`
- Role: `boundary_case_study`
- Architecture status: `boundary_not_final_architecture`
- Architecture denominator decision: `exclude_contextual`

## Evidence Role

Boundary case study.
Boundary case-study evidence for agent-authored reusable operational/deployment artifacts in software-system development.

## Key Extracted Facts

- SDS describes an agentic workflow for infrastructure/system design where specifications, artifacts, code, and evaluation results are kept in sync.
- The LLM runtime case reports allmos v2 at about 1.7k tokens/s, near nano-vLLM at 1.76k, and a monolithic runtime at 1.2k tokens/s.
- A reusable agent-authored key-solutions playbook cut fresh-VM deployment from about 90 minutes with human debugging to about 6 minutes without human intervention.
- Denominator review keeps SDS outside the architecture-study count because the paper reports a broad workflow/case study and an agent-authored playbook, not a dedicated persistence architecture evaluated as the main study contribution.

## Denominator Notes

- Controlled-comparison status: `not_applicable_contextual`.
- Extraction verification status: `verified_from_full_text`.
- Notes: Boundary include retained as contextual systems-development evidence. Do not count as an architecture study because the paper reports a broad SDS workflow/case study and an agent-authored playbook, not a dedicated persistence architecture evaluated as the study contribution.

## Source Files

- PDF text: `search/full-texts/text/FT0080_TA01629_self-defining-systems.txt`
- JSON: `extraction/json/FT0080_self-defining-systems.json`
