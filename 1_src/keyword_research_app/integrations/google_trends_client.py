"""Adaptador da aplicação para coleta de interesse no Google Trends."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from keyword_research_app.config.settings import Settings
from keyword_research_app.utils.google_trends import (
    collect_google_trends_interest,
)


CACHE_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "google_trends_cache.json"
)


def _report_progress(
    position: int,
    total: int,
    keyword: str,
    cache_hit: bool,
) -> None:
    """Exibe progresso sem registrar conteúdo sensível."""
    status = "cache" if cache_hit else "Google Trends"
    print(f"[{position}/{total}] {keyword}: {status}")


def fetch_keyword_metrics(
    keywords: Iterable[str],
    settings: Settings,
) -> list[dict[str, object]]:
    """Coleta métricas reais de interesse relativo usando pytrends.

    Args:
        keywords: Palavras-chave normalizadas para comparação.
        settings: Configurações de idioma, região, período e retentativas.

    Returns:
        Métricas temporais serializáveis de cada palavra-chave.
    """
    return collect_google_trends_interest(
        list(keywords),
        language=settings.google_trends_language,
        timezone=settings.google_trends_timezone,
        geo=settings.google_trends_geo,
        timeframe=settings.google_trends_timeframe,
        context_filter=settings.google_trends_context_filter or None,
        max_retries=settings.google_trends_max_retries,
        backoff_seconds=settings.google_trends_backoff_seconds,
        min_delay_seconds=settings.google_trends_min_delay_seconds,
        max_delay_seconds=settings.google_trends_max_delay_seconds,
        cache_path=CACHE_PATH,
        progress_callback=_report_progress,
    )
