#!/usr/bin/env python3
"""Compile search extraction JSON files into a TSV."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_DIR = ROOT / "extraction" / "json"
OUT_PATH = ROOT / "extraction" / "extracted-data.tsv"

FIELDS = [
    "included_id",
    "full_text_id",
    "screening_id",
    "dedup_group",
    "study_role",
    "architecture_status",
    "controlled_comparison_status",
    "classification_status",
    "architecture_denominator_decision",
    "contextual_role",
    "full_text_rationale",
    "source_routes",
    "source_files",
    "route_provenance",
    "extraction_verification_status",
    "extractor_notes",
    "id",
    "autores",
    "ano",
    "titulo",
    "venue",
    "tipo_venue",
    "tipo_arquitetura",
    "escopo_temporal",
    "substrato_representacional",
    "politica_controle",
    "formato_armazenamento",
    "metodo_recuperacao",
    "granularidade_memoria",
    "compartilhamento_entre_agentes",
    "framework_agente",
    "llm_utilizado",
    "nivel_autonomia",
    "codigo_aberto",
    "metodo_avaliacao",
    "benchmarks_utilizados",
    "metricas_desempenho",
    "metricas_cl",
    "baseline_comparado",
    "tokens_entrada_por_tarefa",
    "tokens_saida_por_tarefa",
    "tamanho_memoria_ao_longo_tempo",
    "custo_por_tarefa",
    "reducao_tokens",
    "reporta_dados_custo",
    "resultado_principal",
    "desempenho_vs_baseline",
    "custo_vs_baseline",
    "resultado_negativo",
    "pontuacao_qualidade",
    "limitacoes",
    "ameacas_validade",
    "relevancia_gaps",
]


def clean(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError(f"all JSON values must be strings, got {type(value)!r}")
    return value.replace("\t", " ").replace("\r", " ").replace("\n", "; ")


def main() -> None:
    rows = []
    for path in sorted(JSON_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        missing = [field for field in FIELDS if field not in data]
        extra = [field for field in data if field not in FIELDS]
        if missing or extra:
            raise SystemExit(
                f"{path}: schema mismatch; missing={missing}; extra={extra}"
            )
        rows.append({field: clean(data[field]) for field in FIELDS})

    rows.sort(key=lambda row: (row["included_id"], row["full_text_id"], row["id"]))
    with OUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
