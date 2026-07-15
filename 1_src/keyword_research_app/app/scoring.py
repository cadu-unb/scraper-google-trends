"""Calculo de crescimento e relevancia das palavras-chave."""

from __future__ import annotations


def clamp_score(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    """Limita um valor numerico ao intervalo configurado."""
    return max(minimum, min(maximum, value))


def normalize_value(value: float, minimum: float, maximum: float) -> float:
    """Normaliza um valor para a escala de 0 a 100."""
    if maximum <= minimum:
        return 0.0
    return clamp_score(((value - minimum) / (maximum - minimum)) * 100)


def calculate_growth_rate(monthly_volumes: list[int]) -> float:
    """Calcula crescimento percentual entre o primeiro e o ultimo mes."""
    if len(monthly_volumes) < 2:
        return 0.0

    first_month = monthly_volumes[0]
    last_month = monthly_volumes[-1]

    if first_month <= 0:
        return 0.0

    return ((last_month - first_month) / first_month) * 100


def calculate_relevance_score(
    normalized_search_volume: float,
    normalized_growth: float,
    normalized_competition: float,
) -> float:
    """Calcula a pontuacao de relevancia em escala de 0 a 100.

    Formula inicial:
    `0.60 * volume + 0.30 * crescimento - 0.10 * competicao`.
    """
    score = (
        0.60 * normalized_search_volume
        + 0.30 * normalized_growth
        - 0.10 * normalized_competition
    )
    return round(clamp_score(score), 2)
