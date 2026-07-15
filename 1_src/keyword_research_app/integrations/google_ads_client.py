"""Estrutura inicial para futura integracao com Google Ads API.

O Google Ads Keyword Planner e a fonte mais adequada para obter volume medio
mensal, competicao, indice de competicao e estimativas de lance no topo da
pagina. Esta versao nao implementa chamadas reais nem scraping.
"""

from __future__ import annotations

from typing import Iterable

from keyword_research_app.config.settings import Settings
from keyword_research_app.integrations.mock_client import (
    fetch_keyword_metrics as fetch_mock_metrics,
)


REQUIRED_CREDENTIAL_FIELDS = {
    "GOOGLE_ADS_DEVELOPER_TOKEN": "google_ads_developer_token",
    "GOOGLE_ADS_CLIENT_ID": "google_ads_client_id",
    "GOOGLE_ADS_CLIENT_SECRET": "google_ads_client_secret",
    "GOOGLE_ADS_REFRESH_TOKEN": "google_ads_refresh_token",
    "GOOGLE_ADS_CUSTOMER_ID": "google_ads_customer_id",
}


class MissingGoogleAdsCredentialsError(RuntimeError):
    """Erro usado quando credenciais obrigatorias nao foram configuradas."""


def missing_credentials(settings: Settings) -> list[str]:
    """Lista variaveis obrigatorias ausentes para Google Ads API."""
    missing: list[str] = []

    for env_name, field_name in REQUIRED_CREDENTIAL_FIELDS.items():
        if getattr(settings, field_name) is None:
            missing.append(env_name)

    return missing


def fetch_keyword_metrics(
    keywords: Iterable[str],
    settings: Settings,
    allow_mock_fallback: bool = True,
) -> list[dict[str, object]]:
    """Busca metricas futuras via Google Ads API ou usa mock como fallback.

    Args:
        keywords: Palavras-chave normalizadas.
        settings: Configuracoes carregadas do ambiente.
        allow_mock_fallback: Quando verdadeiro, usa mock se faltarem
            credenciais.

    Raises:
        MissingGoogleAdsCredentialsError: Quando faltam credenciais e o
            fallback esta desativado.
        NotImplementedError: Quando as credenciais existem, pois a chamada real
            ainda precisa ser implementada.
    """
    missing = missing_credentials(settings)

    if missing and allow_mock_fallback:
        return fetch_mock_metrics(keywords)

    if missing:
        missing_text = ", ".join(missing)
        raise MissingGoogleAdsCredentialsError(
            f"Credenciais ausentes para Google Ads API: {missing_text}."
        )

    raise NotImplementedError(
        "Integre aqui o cliente oficial da Google Ads API para buscar metricas reais."
    )
