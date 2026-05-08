#!/usr/bin/env python3
"""Build normalized search benchmark inventory."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "extraction" / "extracted-data.tsv"
OUT_INVENTORY = ROOT / "analysis" / "benchmark-inventory.tsv"
OUT_RECORDS = ROOT / "analysis" / "benchmark-records.tsv"


@dataclass(frozen=True)
class BenchmarkRule:
    label: str
    category: str
    pattern: str


BENCHMARK_RULES = [
    BenchmarkRule("SWE-bench Verified-Mini", "software_engineering", r"swe[- ]?bench[- ]?verified[- ]?mini"),
    BenchmarkRule("SWE-bench Verified", "software_engineering", r"swe[- ]?bench[- ]?(verified|v\.)(?![- ]?mini)"),
    BenchmarkRule("SWE-bench Lite", "software_engineering", r"swe[- ]?bench[- ]?(lite|lite issue|lite with)"),
    BenchmarkRule("SWE-Bench Pro", "software_engineering", r"swe[- ]?bench[- ]?pro"),
    BenchmarkRule("SWE-bench Live", "software_engineering", r"swe[- ]?bench[- ]?live"),
    BenchmarkRule("SWE-bench Multilingual", "software_engineering", r"swe[- ]?bench[- ]?multilingual"),
    BenchmarkRule("SWE-bench Multimodal", "software_engineering", r"swe[- ]?bench[- ]?multimodal"),
    BenchmarkRule("SWE-bench full training set", "software_engineering", r"swe[- ]?bench full training set"),
    BenchmarkRule("Ambiguous SWE-bench", "software_engineering", r"ambiguous swe[- ]?bench"),
    BenchmarkRule("Stateful SWE", "software_engineering", r"stateful swe"),
    BenchmarkRule("HumanEvalDafny", "code_generation", r"humanevaldafny"),
    BenchmarkRule("HumanEval-X", "code_generation", r"humaneval[- ]?x"),
    BenchmarkRule("HumanEval-Hard", "code_generation", r"humaneval[- ]?hard"),
    BenchmarkRule("HumanEval", "code_generation", r"\bhumaneval\b(?![- ]?(x|hard|dafny))"),
    BenchmarkRule("MBPP-Hard", "code_generation", r"\bmbpp[- ]?hard\b"),
    BenchmarkRule("MBPP", "code_generation", r"\bmbpp\b(?![- ]?hard)"),
    BenchmarkRule("BigCodeBench", "code_generation", r"bigcodebench"),
    BenchmarkRule("LiveCodeBench", "code_generation", r"livecodebench"),
    BenchmarkRule("LeetcodeHardGym", "code_generation", r"leetcodehardgym"),
    BenchmarkRule("APPS", "code_generation", r"(^|[;,]\s*)apps(?=,|;|$)"),
    BenchmarkRule("CODAL-Bench", "code_generation", r"codal[- ]?bench"),
    BenchmarkRule("ClassEval", "code_generation", r"classeval"),
    BenchmarkRule("Polyglot/Aider-Polyglot", "software_engineering", r"\bpolyglot\b|aider[- ]?polyglot"),
    BenchmarkRule("DS-1000", "data_science_code", r"ds[- ]?1000"),
    BenchmarkRule("DA-Code", "data_science_code", r"da[- ]?code"),
    BenchmarkRule("PandasBench", "data_science_code", r"pandasbench"),
    BenchmarkRule("EffiBench-X", "code_optimization", r"effibench[- ]?x"),
    BenchmarkRule("KernelBench", "code_optimization", r"kernelbench"),
    BenchmarkRule("NKIBench", "code_optimization", r"nkibench"),
    BenchmarkRule("FlashInfer-Bench", "code_optimization", r"flashinfer[- ]?bench"),
    BenchmarkRule("TritonBench-T", "code_optimization", r"tritonbench[- ]?t"),
    BenchmarkRule("Multi-Docker-Eval", "software_engineering", r"multi[- ]?docker[- ]?eval"),
    BenchmarkRule("Terminal-Bench", "software_engineering", r"terminal[- ]?bench"),
    BenchmarkRule("PyTorch-Bench", "software_engineering", r"pytorch[- ]?bench"),
    BenchmarkRule("StableToolBench", "general_agent", r"stabletoolbench"),
    BenchmarkRule("CyberGym", "security_or_ops", r"cybergym"),
    BenchmarkRule("DevOps-Gym", "security_or_ops", r"devops[- ]?gym"),
    BenchmarkRule("WebArena", "web_agent", r"webarena"),
    BenchmarkRule("MiniWoB++", "web_agent", r"miniwob\+\+"),
    BenchmarkRule("Mind2Web", "web_agent", r"mind2web"),
    BenchmarkRule("WebShop", "web_agent", r"webshop"),
    BenchmarkRule("ALFWorld", "web_agent", r"alfworld"),
    BenchmarkRule("AppWorld", "web_agent", r"appworld"),
    BenchmarkRule("MiniHack", "web_agent", r"minihack"),
    BenchmarkRule("GAIA", "general_agent", r"\bgaia\b"),
    BenchmarkRule("Humanity's Last Exam", "general_reasoning", r"humanity'?s last exam|\bhle\b"),
    BenchmarkRule("GPQA", "general_reasoning", r"\bgpqa\b"),
    BenchmarkRule("GSM8K", "general_reasoning", r"gsm8k"),
    BenchmarkRule("HotPotQA", "general_reasoning", r"hotpotqa"),
    BenchmarkRule("TriviaQA", "general_reasoning", r"triviaqa"),
    BenchmarkRule("StrategyQA", "general_reasoning", r"strategyqa"),
    BenchmarkRule("PopQA", "general_reasoning", r"popqa"),
    BenchmarkRule("AIME", "general_reasoning", r"\baime\b"),
    BenchmarkRule("MATH/MATH500", "general_reasoning", r"\bmath[- ]?500\b|\bmath500\b|\bmath\b"),
    BenchmarkRule("PaperBench", "research_engineering", r"paperbench"),
    BenchmarkRule("MLE-Bench", "research_engineering", r"mle[- ]?bench"),
    BenchmarkRule("ALE-Bench", "code_optimization", r"ale[- ]?bench"),
    BenchmarkRule("SUPER", "research_engineering", r"\bsuper\b"),
    BenchmarkRule("ResearchCodeBench", "research_engineering", r"researchcodebench"),
    BenchmarkRule("ScienceAgentBench", "research_engineering", r"scienceagentbench"),
    BenchmarkRule("MultiAgentBench", "multi_agent", r"multiagentbench"),
    BenchmarkRule("RedCode-Exec", "security_or_ops", r"redcode[- ]?exec"),
    BenchmarkRule("RedCode-Gen", "security_or_ops", r"redcode[- ]?gen"),
    BenchmarkRule("RMCbench", "security_or_ops", r"rmcbench"),
    BenchmarkRule("CyBench", "security_or_ops", r"cybench"),
    BenchmarkRule("BountyBench", "security_or_ops", r"bountybench"),
    BenchmarkRule("AgentSafetyBench", "security_or_ops", r"agentsafetybench"),
    BenchmarkRule("AgentHarm", "security_or_ops", r"agentharm"),
    BenchmarkRule("Agent Security Bench", "security_or_ops", r"agent security bench|\basb\b"),
    BenchmarkRule("Secure-code scenarios", "security_or_ops", r"secure[- ]?code evaluation scenarios"),
    BenchmarkRule("TAI3 toolkit APIs", "security_or_ops", r"toolkit apis|233 parameters"),
    BenchmarkRule("SRDD", "requirements_or_ui", r"\bsrdd\b"),
    BenchmarkRule("50projects50days", "software_engineering", r"50projects50days"),
    BenchmarkRule("SemFinder/CraftDroid", "requirements_or_ui", r"semfinder|craftdroid"),
    BenchmarkRule("SAT Competition", "code_optimization", r"sat competition"),
    BenchmarkRule("NLP4LP", "optimization_modeling", r"nlp4lp"),
    BenchmarkRule("NL4OPT", "optimization_modeling", r"nl4opt"),
    BenchmarkRule("IndustryOR", "optimization_modeling", r"industryor"),
    BenchmarkRule("MAMO/ComplexLP", "optimization_modeling", r"mamo|complexlp"),
    BenchmarkRule("LogiOR", "optimization_modeling", r"logior"),
    BenchmarkRule("OptiBench", "optimization_modeling", r"optibench"),
    BenchmarkRule("RustRepoTrans", "code_translation", r"rustrepotrans"),
    BenchmarkRule("BrowseComp-Plus", "web_agent", r"browsecomp[- ]?plus"),
    BenchmarkRule("IaC-Eval", "software_engineering", r"iac[- ]?eval"),
    BenchmarkRule("Weco-Kaggle Lite", "data_science_code", r"weco[- ]?kaggle lite|kaggle private leaderboard"),
    BenchmarkRule("KGQAGen-10k", "general_reasoning", r"kgqagen[- ]?10k"),
    BenchmarkRule("Lifelong Agent Bench", "general_agent", r"lifelong agent bench"),
    BenchmarkRule("Heuristic-design benchmarks", "code_optimization", r"\btsp\b|\bbpp\b|\bcaf\b|\bmis\b|\bcvrp\b|\bbbob\b|\bpmsp\b|heuristic[- ]?design"),
    BenchmarkRule("syzbot/Linux kernel repair", "software_engineering", r"syzbot|linux kernel bug"),
    BenchmarkRule("Codebase-Memory repo QA", "software_engineering", r"31 real[- ]?world repositories|structural code[- ]?question"),
    BenchmarkRule("SkillsBench", "general_agent", r"skillsbench"),
    BenchmarkRule("OpenGame-Bench", "software_engineering", r"opengame[- ]?bench"),
    BenchmarkRule("ReplicationBench", "software_engineering", r"replicationbench"),
    BenchmarkRule("MLGym-Bench", "research_engineering", r"mlgym[- ]?bench"),
    BenchmarkRule("PDDL", "planning", r"\bpddl\b"),
    BenchmarkRule("KodCode", "code_generation", r"kodcode"),
    BenchmarkRule("NdonnxEval", "code_generation", r"ndonnxeval"),
    BenchmarkRule("NumbaEval", "code_generation", r"numbaeval"),
    BenchmarkRule("FRQAD", "retrieval_memory", r"frqad"),
    BenchmarkRule("LoCoMo", "retrieval_memory", r"locomo"),
    BenchmarkRule("SLUMP", "software_engineering", r"\bslump\b"),
    BenchmarkRule("DafnyBench", "formal_methods", r"dafnybench"),
    BenchmarkRule("GSM-Symbolic", "general_reasoning", r"gsm[- ]?symbolic"),
    BenchmarkRule("tau2-bench", "general_agent", r"tau2[- ]?bench"),
    BenchmarkRule("Scientific-code optimization workloads", "code_optimization", r"landau|local tangent space|graphwave|scientific[- ]?code"),
    BenchmarkRule("nanoGPT Shakespeare", "code_generation", r"nanogpt|shakespeare"),
    BenchmarkRule("Internal RL repository", "software_engineering", r"internal expert[- ]?maintained reinforcement[- ]?learning"),
    BenchmarkRule("Truck CAN Signal", "data_science_code", r"truck can signal"),
    BenchmarkRule("Google production optimization", "software_engineering", r"google production|fleet[- ]?wide production|microbenchmark edits"),
    BenchmarkRule("Materials-science repositories", "research_engineering", r"materials[- ]?science"),
    BenchmarkRule("NAS-Bench-Suite-Zero", "code_optimization", r"nas[- ]?bench[- ]?suite[- ]?zero"),
    BenchmarkRule("STOP synthetic algorithmic tasks", "code_optimization", r"learning parity|string grid|modular quadratic|maxcut|sandbox[- ]?bypass"),
    BenchmarkRule("CORAL optimization task suite", "code_optimization", r"anthropic kernel engineering|polyominoes|vliw simd|stress[- ]?test optimization"),
    BenchmarkRule("SelfEvolve self-extension tasks", "software_engineering", r"software self[- ]?extension tasks"),
]


def load_architecture_rows() -> list[dict[str, str]]:
    with IN_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return [
        row
        for row in rows
        if row["architecture_denominator_decision"] == "include_architecture"
    ]


def normalized_benchmarks(text: str) -> list[BenchmarkRule]:
    lowered = text.lower()
    matches = [
        rule
        for rule in BENCHMARK_RULES
        if re.search(rule.pattern, lowered)
    ]
    deduped: dict[str, BenchmarkRule] = {rule.label: rule for rule in matches}
    return list(deduped.values())


def write_outputs(rows: list[dict[str, str]]) -> None:
    record_rows: list[dict[str, str]] = []
    grouped: dict[str, dict[str, object]] = {}

    for row in rows:
        matches = normalized_benchmarks(row["benchmarks_utilizados"])
        if not matches:
            matches = [BenchmarkRule("UNMATCHED", "needs_manual_review", r"")]

        for rule in matches:
            record_rows.append(
                {
                    "included_id": row["included_id"],
                    "id": row["id"],
                    "title": row["titulo"],
                    "benchmark_label": rule.label,
                    "benchmark_category": rule.category,
                    "raw_benchmarks": row["benchmarks_utilizados"],
                }
            )
            entry = grouped.setdefault(
                rule.label,
                {
                    "benchmark_label": rule.label,
                    "benchmark_category": rule.category,
                    "studies": [],
                    "raw_mentions": [],
                },
            )
            entry["studies"].append(f"{row['included_id']} {row['id']}")
            entry["raw_mentions"].append(row["benchmarks_utilizados"])

    with OUT_RECORDS.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "included_id",
            "id",
            "title",
            "benchmark_label",
            "benchmark_category",
            "raw_benchmarks",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(record_rows)

    inventory_rows = []
    for entry in grouped.values():
        studies = sorted(set(entry["studies"]))
        inventory_rows.append(
            {
                "benchmark_label": entry["benchmark_label"],
                "benchmark_category": entry["benchmark_category"],
                "n_studies": str(len(studies)),
                "studies": "; ".join(studies),
                "raw_mentions": " || ".join(sorted(set(entry["raw_mentions"]))),
            }
        )
    inventory_rows.sort(key=lambda row: (-int(row["n_studies"]), row["benchmark_label"]))

    with OUT_INVENTORY.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "benchmark_label",
            "benchmark_category",
            "n_studies",
            "studies",
            "raw_mentions",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(inventory_rows)


def main() -> None:
    rows = load_architecture_rows()
    write_outputs(rows)
    print(f"wrote {OUT_INVENTORY.relative_to(ROOT)}")
    print(f"wrote {OUT_RECORDS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
