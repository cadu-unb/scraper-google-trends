"""Exportacao do relatorio em JSON para Python e mini-aplicacao web."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


STANDARD_REPORT_COLUMNS: list[dict[str, str]] = [
    {"key": "input_order", "label": "Ordem"},
    {"key": "keyword", "label": "Palavra-chave"},
    {"key": "avg_monthly_searches", "label": "Buscas mensais"},
    {"key": "competition", "label": "Competição"},
    {"key": "competition_index", "label": "Índice de competição"},
    {"key": "low_top_bid", "label": "Lance baixo"},
    {"key": "high_top_bid", "label": "Lance alto"},
    {"key": "growth_rate", "label": "Crescimento"},
    {"key": "relevance_score", "label": "Relevância"},
    {"key": "source", "label": "Fonte"},
]

GOOGLE_TRENDS_REPORT_COLUMNS: list[dict[str, str]] = [
    {"key": "keyword", "label": "Palavra-chave"},
    {"key": "average_interest", "label": "Interesse médio"},
    {"key": "latest_interest", "label": "Interesse recente"},
    {"key": "peak_interest", "label": "Pico"},
    {"key": "trend_direction", "label": "Tendência"},
    {"key": "trend_change", "label": "Variação da curva"},
    {"key": "relevance_score", "label": "Relevância"},
    {"key": "source", "label": "Fonte"},
]


def _report_columns(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    """Seleciona colunas compatíveis com a fonte presente nas linhas."""
    if rows and all(row.get("source") == "GOOGLE_TRENDS" for row in rows):
        return GOOGLE_TRENDS_REPORT_COLUMNS
    return STANDARD_REPORT_COLUMNS


def build_report_payload(rows: list[dict[str, object]]) -> dict[str, object]:
    """Monta a estrutura final obrigatoria do arquivo JSON."""
    sources = sorted({str(row.get("source", "")) for row in rows if row.get("source")})
    source = ", ".join(sources) if sources else "UNKNOWN"

    return {
        "metadata": {
            "generated_at": datetime.now().replace(microsecond=0).isoformat(),
            "source": source,
            "total_keywords": len(rows),
            "description": "Keyword research report generated from JSON input.",
        },
        "columns": _report_columns(rows),
        "rows": rows,
    }


def export_report_json(payload: dict[str, object], path: Path) -> Path:
    """Salva o relatorio JSON com indentacao legivel."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
        file.write("\n")
    return path


def copy_report_to_web_data(output_path: Path, web_data_path: Path) -> Path:
    """Copia o JSON gerado para a pasta consumida pela interface web."""
    web_data_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_path, web_data_path)
    return web_data_path
