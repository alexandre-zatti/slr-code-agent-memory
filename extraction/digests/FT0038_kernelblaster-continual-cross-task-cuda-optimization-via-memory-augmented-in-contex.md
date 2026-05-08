# KernelBlaster: Continual Cross-Task CUDA Optimization via Memory-Augmented In-Context Reinforcement Learning

## Identifiers

- Included ID: I064
- Full-text ID: FT0038
- Extraction key: `dong2026kernelblaster`
- Role: `architecture`
- Architecture status: `arch_structured_knowledge_base`
- Architecture denominator decision: `include_architecture`

## Recheck Status

This digest was verified against the current full-text record and extraction JSON.

## Key Extracted Facts

- Architecture type: `grafo_conhecimento`.
- Storage format: Persistent CUDA Knowledge Base (~50KB JSON): hierarquia de estados de performance (memory-bound, compute-bound, hybrid) → listas de otimizações candidatas com scores de desempenho esperado. Cada entrada ⟨state, (optimization, score)⟩. Atualizada via PolicyEvaluation (compara resultado vs predição), PerfGapAnalysis (analisa discrepância), ParameterUpdate (reescreve KB).
- Retrieval method: `outro`.
- Evaluation method: `benchmark`.
- Benchmarks: KernelBench Level 1, Level 2, Level 3 (NVIDIA A6000, H100, L40S GPUs)
- Main result: KernelBlaster atinge speedups geométricos médios de 1.43×, 2.50× e 1.50× nos KernelBench Level 1-3 vs PyTorch. Knowledge Base persistente permite transferência cross-task e cross-GPU, com 1.67× ganho sobre agente sem memória.
- Performance versus baseline: GeoMean 1.43× (L1), 2.50× (L2), 1.50× (L3) vs PyTorch; 1.67× vs no_mem_agent; supera AI CUDA Engineer em fast_p para speedups moderados a altos
- Cost reporting: `sim_parcial`; 2.4× menos tokens que minimal agent sem KB; KB reutilizável entre GPUs (~50KB compacta)

## Denominator Notes

- Controlled-comparison status: `yes_prefilled_prior`.
- Extraction verification status: `verified_prior_extraction`.
- Notes: Controlled-comparison and quality fields are carried from prior and must be recomputed after all architecture records are extracted.

## Source Files

- PDF text: `search/full-texts/text/FT0038_TA00200_kernelblaster-continual-cross-task-cuda-optimization-via-memory-augmented-in-con.txt`
- JSON: `extraction/json/FT0038_kernelblaster-continual-cross-task-cuda-optimization-via-memory-augmented-in-contex.json`
