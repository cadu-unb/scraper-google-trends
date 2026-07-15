"""Carregamento de configuracoes por variaveis de ambiente."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Configuracoes usadas pelas fontes de dados e pelo pipeline."""

    data_source: str
    google_ads_developer_token: str | None
    google_ads_client_id: str | None
    google_ads_client_secret: str | None
    google_ads_refresh_token: str | None
    google_ads_customer_id: str | None
    default_language_id: str
    default_geo_target_id: str
    google_trends_language: str = "pt-BR"
    google_trends_timezone: int = 180
    google_trends_geo: str = "BR"
    google_trends_timeframe: str = "today 12-m"
    google_trends_max_retries: int = 3
    google_trends_backoff_seconds: float = 5.0
    google_trends_min_delay_seconds: float = 5.0
    google_trends_max_delay_seconds: float = 20.0
    google_trends_context_filter: str = "inteligência artificial"


def _empty_to_none(value: str | None) -> str | None:
    """Converte strings vazias em `None` para facilitar validacoes."""
    if value is None or value.strip() == "":
        return None
    return value.strip()


def load_settings(base_dir: Path | None = None) -> Settings:
    """Carrega `.env`, quando existir, e retorna configuracoes tipadas.

    Args:
        base_dir: Pasta onde o arquivo `.env` deve ser procurado.

    Returns:
        Instancia imutavel com as configuracoes da aplicacao.
    """
    if base_dir is not None:
        load_dotenv(base_dir / ".env")
    else:
        load_dotenv()

    return Settings(
        data_source=os.getenv("DATA_SOURCE", "GOOGLE_TRENDS").strip().upper(),
        google_ads_developer_token=_empty_to_none(
            os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
        ),
        google_ads_client_id=_empty_to_none(os.getenv("GOOGLE_ADS_CLIENT_ID")),
        google_ads_client_secret=_empty_to_none(os.getenv("GOOGLE_ADS_CLIENT_SECRET")),
        google_ads_refresh_token=_empty_to_none(os.getenv("GOOGLE_ADS_REFRESH_TOKEN")),
        google_ads_customer_id=_empty_to_none(os.getenv("GOOGLE_ADS_CUSTOMER_ID")),
        default_language_id=os.getenv("DEFAULT_LANGUAGE_ID", "1014").strip(),
        default_geo_target_id=os.getenv("DEFAULT_GEO_TARGET_ID", "2076").strip(),
        google_trends_language=os.getenv(
            "GOOGLE_TRENDS_LANGUAGE",
            "pt-BR",
        ).strip(),
        google_trends_timezone=int(os.getenv("GOOGLE_TRENDS_TIMEZONE", "180")),
        google_trends_geo=os.getenv("GOOGLE_TRENDS_GEO", "BR").strip(),
        google_trends_timeframe=os.getenv(
            "GOOGLE_TRENDS_TIMEFRAME",
            "today 12-m",
        ).strip(),
        google_trends_max_retries=int(
            os.getenv("GOOGLE_TRENDS_MAX_RETRIES", "3")
        ),
        google_trends_backoff_seconds=float(
            os.getenv("GOOGLE_TRENDS_BACKOFF_SECONDS", "5")
        ),
        google_trends_min_delay_seconds=float(
            os.getenv("GOOGLE_TRENDS_MIN_DELAY_SECONDS", "5")
        ),
        google_trends_max_delay_seconds=float(
            os.getenv("GOOGLE_TRENDS_MAX_DELAY_SECONDS", "20")
        ),
        google_trends_context_filter=os.getenv(
            "GOOGLE_TRENDS_CONTEXT_FILTER",
            "inteligência artificial",
        ).strip(),
    )
