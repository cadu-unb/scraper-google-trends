"""Registra execucoes do keyword research disparadas pelo n8n."""

from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


DEFAULT_REPORT_PATH = Path(
    "/workspace/1_src/keyword_research_app/data/keyword_trends_report.json"
)
DEFAULT_LOG_PATH = Path(
    "/workspace/1_src/keyword_research_app/data/n8n_execution_log.json"
)


def load_json_file(path: Path, fallback: Any) -> Any:
    """Carrega um JSON existente ou retorna um valor padrao."""
    if not path.exists():
        return fallback

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def build_run_entry(status: str, note: str, report_path: Path) -> dict[str, Any]:
    """Monta um registro de execucao com dados do relatorio mais recente."""
    report = load_json_file(report_path, {})
    metadata = report.get("metadata", {}) if isinstance(report, dict) else {}
    rows = report.get("rows", []) if isinstance(report, dict) else []

    return {
        "executed_at": datetime.now(UTC).isoformat(),
        "status": status,
        "note": note,
        "source": metadata.get("source"),
        "report_generated_at": metadata.get("generated_at"),
        "total_keywords": metadata.get("total_keywords", len(rows)),
        "report_path": str(report_path),
        "workflow_execution_id": os.getenv("N8N_EXECUTION_ID"),
    }


def append_run_log(log_path: Path, entry: dict[str, Any]) -> Path:
    """Adiciona um item ao historico local de execucoes."""
    payload = load_json_file(log_path, {"runs": []})
    if not isinstance(payload, dict):
        payload = {"runs": []}

    runs = payload.get("runs")
    if not isinstance(runs, list):
        runs = []

    runs.append(entry)
    payload["runs"] = runs
    payload["total_runs"] = len(runs)
    payload["updated_at"] = entry["executed_at"]

    log_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = log_path.with_suffix(f"{log_path.suffix}.tmp")
    temporary_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(log_path)
    return log_path


def parse_args() -> argparse.Namespace:
    """Le os argumentos enviados pelo node Execute Command."""
    parser = argparse.ArgumentParser(
        description="Registra execucoes do keyword research em JSON."
    )
    parser.add_argument(
        "--status",
        default="success",
        choices=("success", "failed", "manual"),
        help="Status que sera gravado no historico.",
    )
    parser.add_argument(
        "--note",
        default="Execucao registrada pelo n8n.",
        help="Observacao curta sobre a execucao.",
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=DEFAULT_REPORT_PATH,
        help="Caminho do relatorio JSON gerado pelo keyword research.",
    )
    parser.add_argument(
        "--log-path",
        type=Path,
        default=DEFAULT_LOG_PATH,
        help="Caminho do historico local de execucoes.",
    )
    return parser.parse_args()


def main() -> None:
    """Ponto de entrada do script."""
    args = parse_args()
    entry = build_run_entry(args.status, args.note, args.report_path)
    output_path = append_run_log(args.log_path, entry)
    print(f"Execucao registrada em: {output_path}")


if __name__ == "__main__":
    main()
