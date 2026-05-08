# Systematic Literature Review Protocol

## Administrative Information

- Title: Knowledge Persistence Architectures for AI-Based Coding Agents: A
  Systematic Literature Review
- Protocol date: March 2026, amended through May 2026
- Methodological framework: Kitchenham and Charters (2007), updated by
  Kitchenham and Brereton (2013)
- Reporting guideline: SEGRESS, adapted from PRISMA 2020 for software
  engineering secondary studies
- Reporting checklist: PRISMA 2020

## Research Questions

PICo framework:

- Population: AI-based coding agents with mechanisms for knowledge persistence
  across sessions, tasks, repositories, or agent lifecycles
- Interest: persistence architectures, empirical evidence, cost evidence, and
  operational risks
- Context: empirical evaluations, benchmarks, case studies, tools, and
  frameworks in software engineering or coding-agent settings

Main RQ:

> How does the literature address knowledge persistence in AI-based coding
> agents, and what empirical evidence exists regarding the effectiveness,
> cost, and operational risks of different persistence architectures?

Secondary questions:

- SQ1: Which persistence architectures are proposed, and how are they
  classified by temporal scope, representational substrate, and control policy?
- SQ2: Which evaluation methods and benchmarks are used, and how comparable are
  the reported results?
- SQ3: What performance evidence is reported relative to strict or broad
  baselines?
- SQ4: What cost and efficiency evidence is reported?
- SQ5: What evidence exists about memory-induced degradation, operational
  complexity, security risk, or contextual failure?

## Eligibility Criteria

Inclusion criteria:

- CI1: proposes or evaluates an explicit mechanism to store, retrieve, update,
  reuse, or govern knowledge, memory, experience, context, skills, cases,
  trajectories, policies, or agent state across sessions, tasks, repositories,
  or agent lifecycles.
- CI2: reports empirical results, a benchmark, a case study, or an evaluated
  tool/framework.
- CI3: published or posted between 2023 and the final search cutoff.
- CI4: written in English or Portuguese.
- CI5: peer-reviewed publication or identifiable preprint/technical report.

Exclusion criteria:

- CE1: only intra-session retrieval, prompt stuffing, file selection, context
  compression, or generic RAG without a persistence mechanism.
- CE2: not evaluated on software development, coding, program repair,
  repository work, code optimization, software operations, or closely related
  agentic engineering tasks.
- CE3: no evaluation beyond anecdotal examples.
- CE4: tutorial, editorial, opinion, or purely descriptive nontechnical item.
- CE5: duplicate or superseded publication record; keep the most complete or
  most recent version from the same authors.

Boundary rule:

- Systems that externalize procedural state into executable artifacts during
  task execution may be retained as boundary evidence only when the artifact is
  created, invoked, and reused by the agent during task execution.
  They are not treated as cross-session persistence unless the artifact
  persists across tasks or sessions.

## Information Sources

The final search uses:

- Scopus
- arXiv
- Semantic Scholar citation chasing
- documented manual full-text retrieval for records already identified by the
  reproducible search routes

The final search strategy is recorded in `search/search-strategy.md`.
Screening ledgers are `screening/title-abstract-screening.tsv` and
`screening/full-text-screening.tsv`.

## Extraction

Extraction follows `extraction/extraction-form.md`.
The canonical compiled table is `extraction/extracted-data.tsv`.
Per-study JSON files are stored in `extraction/json/`, and factual digests are
stored in `extraction/digests/`.

## Synthesis

The synthesis is narrative and tabular.
No pooled effect size is computed because benchmark, model, scaffold,
repository, task, and budget settings are heterogeneous.

Denominators:

- 95 included studies.
- 85 architecture studies.
- 10 contextual/boundary studies.
- 56 strict controlled-comparison studies.
- 76 broad controlled-comparison studies.

Supporting synthesis files are stored under `analysis/`.

## Amendments

Protocol amendments are recorded in `protocol/amendments.md`.
