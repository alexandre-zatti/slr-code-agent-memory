# Beyond Crash-to-Patch: Patch Evolution for Linux Kernel Repair

## Identifiers

- Included ID: I048
- Full-text ID: FT0046
- Extraction key: `bai2026patchadvisor`
- Role: `architecture`
- Architecture status: `arch_repository_memory`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_repository_memory`.
- Storage: Three-layer PatchAdvisor memory from syzbot-linked patch evolution: instance memory with crash evidence, fix characterization, final merged diff, and patch-evolution summary; pattern memory with FixStrategy and ReviewLesson records; embedding memory over crash reports and patch artifacts for semantic retrieval.
- Evaluation: 6,946 syzbot-linked Linux kernel bug-fix lifecycles, 100 temporally held-out crash cases for diagnostic evaluation, and six recent syzbot bugs for end-to-end repair using Diagnostic Coverage Rate, precision, recall, F1, fix rate, CodeBERTScore, compilation success rate, average AI-assessed quality rank.
- Main result: PatchAdvisor improves reviewer-alignment and repair quality. Memory raises diagnostic F1 by 21.8% (0.330 vs 0.271), and end-to-end memory guidance raises repair success from 1/6 to 4/6; the fine-tuned Gemma-3-12B advisor reaches 5/6 fixes, CodeBERTScore 0.91, and 100% compilation success.
- Performance versus baseline: Baseline repair succeeds on 1/6 bugs with CodeBERTScore 0.42 and 83.3% compile success. Memory-guided repair succeeds on 4/6 with CodeBERTScore 0.74. Fine-tuned Gemma-3-12B PatchAdvisor succeeds on 5/6 with average rank 2.7.
- Cost/token reporting: `nao`; NR; advisor fine-tuning used LoRA on one NVIDIA A100 80GB GPU, but no monetary/token cost per task is reported.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0046_TA00246_beyond-crash-to-patch-patch-evolution-for-linux-kernel-repair.txt`
- JSON: `extraction/json/FT0046_beyond-crash-to-patch-patch-evolution-for-linux-kernel-repair.json`
