# Git Context Controller: Manage the Context of LLM-based Agents like Git

## Identifiers

- Included ID: I023
- Full-text ID: FT0021
- Extraction key: `wu2025gcc`
- Role: `architecture`
- Architecture status: `arch_persistent_workspace_state`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `git_metafora`.
- Storage format: .GCC/ directory versionado: main.md (roadmap global, milestones, to-do list compartilhado entre branches), branches/{name}/commit.md (sumários de progresso: Branch Purpose + Previous Progress + This Commit's Contribution), log.md (traces OTA fine-grained), metadata.yaml (file structure, dependencies, configs). Tudo plain-text, checkpointed via git commits reais.
- Retrieval method: `hibrido`.
- Evaluation method: `benchmark`.
- Benchmarks: BrowseComp-Plus (150 instâncias), SWE-Bench Verified (500 instâncias), SWE-Benchlite (300 instâncias)
- Main result: SOTA em SWE-Bench Verified (Pass@1 0.802 com Claude 4 Sonnet, +13.6% vs baseline) e BrowseComp-Plus (0.834 com GPT-5). Em SWE-Benchlite, resolve 48.00% (144/300), superando 26 sistemas existentes incluindo agentes comerciais.
- Performance versus baseline: +6.2pp Pass@1 vs Folding Agent (melhor baseline) com Claude 4 Sonnet em SWE-Bench Verified (0.802 vs 0.740); +1.9pp BrowseComp-Plus com GPT-5 (0.834 vs 0.815)
- Cost reporting: `sim_detalhado`; $1.21/task vs $1.62 SWE-Agent, $2.51 Agentless em SWE-Benchlite (Claude 3.5 S); custo comparável aos melhores open-source apesar de performance muito superior

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0021_TA00361_git-context-controller-manage-the-context-of-llm-based-agents-like-git.txt`
- JSON: `extraction/json/FT0021_git-context-controller-manage-the-context-of-llm-based-agents-like-git.json`
