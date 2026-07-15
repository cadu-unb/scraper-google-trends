"""Cliente simulado para executar o pipeline sem APIs externas."""

from __future__ import annotations

import hashlib
from typing import Iterable


COMPETITION_LEVELS = ("LOW", "MEDIUM", "HIGH")


def _seed_from_keyword(keyword: str) -> int:
    """Gera uma semente deterministica a partir da palavra-chave."""
    digest = hashlib.sha256(keyword.encode("utf-8")).hexdigest()
    return int(digest[:12], 16)


def _monthly_volumes(seed: int, keyword: str) -> list[int]:
    """Gera uma serie mensal coerente e repetivel para testes."""
    base = 250 + (seed % 7_500)
    trend_step = ((seed >> 4) % 23) - 7
    seasonality = (len(keyword) % 6) * 8

    volumes: list[int] = []
    for month in range(12):
        wave = ((month % 4) - 1) * seasonality
        value = base + month * trend_step * 12 + wave
        volumes.append(max(20, int(value)))

    return volumes


def fetch_keyword_metrics(keywords: Iterable[str]) -> list[dict[str, object]]:
    """Retorna metricas simuladas para cada palavra-chave.

    Os valores sao deterministicos para facilitar testes e comparacoes entre
    execucoes.
    """
    results: list[dict[str, object]] = []

    for keyword in keywords:
        seed = _seed_from_keyword(keyword)
        monthly_volumes = _monthly_volumes(seed, keyword)
        competition_index = float(15 + (seed % 81))
        competition = COMPETITION_LEVELS[min(2, int(competition_index // 34))]
        low_top_bid = round(0.35 + ((seed >> 6) % 450) / 100, 2)
        high_top_bid = round(low_top_bid + 0.75 + ((seed >> 11) % 650) / 100, 2)

        results.append(
            {
                "keyword": keyword,
                "avg_monthly_searches": round(
                    sum(monthly_volumes) / len(monthly_volumes)
                ),
                "competition": competition,
                "competition_index": competition_index,
                "low_top_bid": low_top_bid,
                "high_top_bid": high_top_bid,
                "monthly_volumes": monthly_volumes,
                "source": "MOCK",
            }
        )

    return results
