# KernelEvolve: Scaling Agentic Kernel Coding for Heterogeneous AI Accelerators at Meta

## Identifiers

- Included ID: I026
- Full-text ID: FT0075
- Extraction key: `kernelevolve2025`
- Role: `architecture`
- Architecture status: `arch_experience_bank`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_experience_bank`.
- Storage: Persistent knowledge base of hardware-specific constraints and optimization patterns plus metadata/object stores for kernel candidates, parent-child relationships, fitness scores, correctness flags, artifacts, profiling reports, and checkpointed search state.
- Evaluation: KernelBench, 160 PyTorch ATen operators across NVIDIA GPUs, AMD GPUs, and MTIA v3, Meta production recommendation-model workloads using Pass rate/correctness; speedup over PyTorch baselines; development time; operator-platform correctness; metadata query scalability; production deployment outcomes.
- Main result: KernelEvolve achieves 100% pass rate on all 250 KernelBench problems and 100% correctness over 480 operator-platform configurations, while reducing development time from weeks to hours and achieving up to 17x speedup over PyTorch baselines.
- Performance versus baseline: Reports 1.2x to 17x speedups over PyTorch baselines across production use cases and competitive performance with expert manual implementations.
- Cost/token reporting: `sim`; NR as per-task monetary cost; reports development time reduced from weeks to hours and production speedups up to 17x.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0075_TA01303_kernelevolve-scaling-agentic-kernel-coding-for-heterogeneous-ai-accelerators-at.txt`
- JSON: `extraction/json/FT0075_kernelevolve-scaling-agentic-kernel-coding-for-heterogeneous-ai-accelerators-at-met.json`
