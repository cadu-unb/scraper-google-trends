"""Orquestra a geração do relatório de pesquisa de palavras-chave."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from keyword_research_app.app.input_loader import (
    InputKeywordsError,
    load_keywords_from_json,
)
from keyword_research_app.app.json_exporter import (
    build_report_payload,
    copy_report_to_web_data,
    export_report_json,
)
from keyword_research_app.app.normalizer import normalize_keywords
from keyword_research_app.app.report_builder import build_keyword_report
from keyword_research_app.config.settings import Settings, load_settings
from keyword_research_app.integrations import (
    fetch_google_ads_metrics,
    fetch_google_trends_metrics,
    fetch_mock_metrics,
)
from keyword_research_app.integrations.google_trends_client import CACHE_PATH
from keyword_research_app.utils import GoogleTrendsError


BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "data" / "input_keywords.json"
REPORT_DATA_PATH = BASE_DIR / "data" / "keyword_trends_report.json"
WEB_DATA_PATH = BASE_DIR / "web" / "data" / "keywords_report.json"


def should_start_new_google_trends_query() -> bool:
    """Decide se o cache do Google Trends deve ser apagado.

    Em execucoes automatizadas, como n8n e Docker, use
    `GOOGLE_TRENDS_NEW_QUERY=true` para forcar uma nova consulta. Quando a
    variavel nao existe, o terminal interativo continua perguntando ao usuario;
    processos sem TTY preservam o cache para evitar travamento em `input()`.
    """
    env_value = os.getenv("GOOGLE_TRENDS_NEW_QUERY")
    if env_value is not None:
        return env_value.strip().lower() in ("1", "true", "yes", "y", "sim", "s")

    if not sys.stdin.isatty():
        print("Execucao sem terminal interativo. Cache do Google Trends preservado.")
        return False

    answer = input(
        "Iniciar nova consulta? Digite Y/yes para nova ou pressione "
        "Enter para continuar a anterior: "
    ).strip().lower()
    return answer in ("y", "yes", "s", "sim")


def prompt_new_query_or_resume(cache_path: Path = CACHE_PATH) -> None:
    """Apaga ou preserva o cache do Google Trends antes da coleta.

    `GOOGLE_TRENDS_NEW_QUERY=true` apaga o cache em execucoes automatizadas.
    Sem essa variavel, o usuario escolhe em terminal interativo; em processos
    sem TTY, o cache e preservado.
    """
    if should_start_new_google_trends_query():
        cache_path.unlink(missing_ok=True)
        print("Cache apagado. Iniciando nova consulta.")
    else:
        print("Continuando a consulta anterior (cache preservado).")


def fetch_keyword_metrics_by_source(
    settings: Settings,
    keywords: list[str],
) -> list[dict[str, object]]:
    """Busca métricas usando a fonte configurada para a aplicação.

    Args:
        settings: Configurações que definem a fonte de dados.
        keywords: Palavras-chave normalizadas para consulta.

    Returns:
        Métricas coletadas para cada palavra-chave.

    Raises:
        ValueError: Quando a fonte configurada não é reconhecida.
    """
    source = settings.data_source.upper()

    if source == "MOCK":
        return fetch_mock_metrics(keywords)
    if source == "GOOGLE_ADS":
        return fetch_google_ads_metrics(
            keywords,
            settings=settings,
            allow_mock_fallback=True,
        )
    if source == "GOOGLE_TRENDS":
        return fetch_google_trends_metrics(
            keywords,
            settings=settings,
        )

    allowed_sources = "MOCK, GOOGLE_ADS, GOOGLE_TRENDS"
    raise ValueError(
        f"DATA_SOURCE inválido: {settings.data_source}. Use: {allowed_sources}."
    )


def generate_keyword_research_report() -> None:
    """Gera e publica o relatório completo de pesquisa de palavras-chave.

    Carrega a entrada JSON, normaliza as palavras-chave, coleta métricas,
    calcula o relatório e grava os arquivos consumidos pela aplicação web.

    Raises:
        SystemExit: Quando o arquivo de entrada é inválido.
    """
    settings = load_settings(BASE_DIR)

    if settings.data_source == "GOOGLE_TRENDS":
        prompt_new_query_or_resume()

    try:
        raw_keywords = load_keywords_from_json(INPUT_PATH)
        normalized_keywords = normalize_keywords(raw_keywords)
        keywords = [item.keyword for item in normalized_keywords]
        print(f"Fonte selecionada: {settings.data_source}")
        if settings.data_source == "GOOGLE_TRENDS":
            average_delay = (
                settings.google_trends_min_delay_seconds
                + settings.google_trends_max_delay_seconds
            ) / 2
            estimated_minutes = (average_delay * len(keywords)) / 60
            print(
                "Tempo médio estimado somente para pausas: "
                f"{estimated_minutes:.1f} minutos."
            )
        metrics = fetch_keyword_metrics_by_source(settings, keywords)
        rows = build_keyword_report(normalized_keywords, metrics)
        payload = build_report_payload(rows)
        output_path = export_report_json(payload, REPORT_DATA_PATH)
        web_path = copy_report_to_web_data(output_path, WEB_DATA_PATH)
    except (GoogleTrendsError, InputKeywordsError) as exc:
        print(f"Erro ao gerar o relatório: {exc}")
        raise SystemExit(1) from exc

    print("\nRelatorio JSON gerado com sucesso.")
    print(f"Total de palavras-chave: {len(rows)}")
    print(f"Arquivo principal: {output_path}")
    print(f"Arquivo para a web app: {web_path}")
    print("\nPrimeiras linhas:")
    for row in rows[:5]:
        metric_label = "interesse médio"
        metric_value = row.get("average_interest")
        if metric_value is None:
            metric_label = "buscas"
            metric_value = row.get("avg_monthly_searches")
        print(
            f"- {row['input_order']}. {row['keyword']} | "
            f"{metric_label}: {metric_value} | "
            f"relevancia: {row['relevance_score']}"
        )


if __name__ == "__main__":
    generate_keyword_research_report()
