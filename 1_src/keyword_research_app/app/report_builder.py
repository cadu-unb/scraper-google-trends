"""Montagem dos dados finais de palavras-chave para exportacao JSON."""

from __future__ import annotations

from keyword_research_app.app.normalizer import NormalizedKeyword, normalize_keyword
from keyword_research_app.app.scoring import (
    calculate_growth_rate,
    calculate_relevance_score,
    normalize_value,
)


REPORT_COLUMNS = [
    "input_order",
    "keyword",
    "avg_monthly_searches",
    "competition",
    "competition_index",
    "low_top_bid",
    "high_top_bid",
    "growth_rate",
    "relevance_score",
    "source",
]


def _metrics_by_keyword(
    metrics: list[dict[str, object]],
) -> dict[str, dict[str, object]]:
    """Indexa metricas por palavra-chave normalizada."""
    return {
        normalize_keyword(str(item["keyword"])): item
        for item in metrics
    }


def _build_rows(
    normalized_keywords: list[NormalizedKeyword],
    metrics: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Combina palavras normalizadas com metricas coletadas."""
    indexed_metrics = _metrics_by_keyword(metrics)
    rows: list[dict[str, object]] = []

    for item in normalized_keywords:
        keyword_metrics = indexed_metrics[item.keyword]
        monthly_volumes = [int(value) for value in keyword_metrics["monthly_volumes"]]
        rows.append(
            {
                "input_order": item.input_order,
                "keyword": item.keyword,
                "avg_monthly_searches": int(keyword_metrics["avg_monthly_searches"]),
                "competition": str(keyword_metrics["competition"]),
                "competition_index": float(keyword_metrics["competition_index"]),
                "low_top_bid": float(keyword_metrics["low_top_bid"]),
                "high_top_bid": float(keyword_metrics["high_top_bid"]),
                "growth_rate": round(calculate_growth_rate(monthly_volumes), 2),
                "source": str(keyword_metrics["source"]),
            }
        )

    return rows


def _build_google_trends_rows(
    normalized_keywords: list[NormalizedKeyword],
    metrics: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Monta linhas próprias para índices relativos do Google Trends."""
    indexed_metrics = _metrics_by_keyword(metrics)
    rows: list[dict[str, object]] = []

    for item in normalized_keywords:
        keyword_metrics = indexed_metrics[item.keyword]
        average_interest = float(keyword_metrics["average_interest"])
        rows.append(
            {
                "input_order": item.input_order,
                "keyword": item.keyword,
                "average_interest": average_interest,
                "peak_interest": int(keyword_metrics["peak_interest"]),
                "latest_interest": int(keyword_metrics["latest_interest"]),
                "trend_direction": str(
                    keyword_metrics["trend_direction"]
                ),
                "trend_change": float(keyword_metrics["trend_change"]),
                "relevance_score": float(keyword_metrics["relevance_score"]),
                "timeline": keyword_metrics["timeline"],
                "cache_hit": bool(keyword_metrics.get("cache_hit", False)),
                "skipped": bool(keyword_metrics.get("skipped", False)),
                "source": "GOOGLE_TRENDS",
            }
        )

    return rows


def build_keyword_report(
    normalized_keywords: list[NormalizedKeyword],
    metrics: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Cria as linhas finais com crescimento e pontuacao de relevancia."""
    if metrics and all(
        metric.get("source") == "GOOGLE_TRENDS" for metric in metrics
    ):
        return _build_google_trends_rows(normalized_keywords, metrics)

    rows = _build_rows(normalized_keywords, metrics)

    if not rows:
        return []

    volumes = [float(row["avg_monthly_searches"]) for row in rows]
    growth_rates = [float(row["growth_rate"]) for row in rows]
    min_volume = min(volumes)
    max_volume = max(volumes)
    min_growth = min(growth_rates)
    max_growth = max(growth_rates)

    for row in rows:
        row["relevance_score"] = calculate_relevance_score(
            normalized_search_volume=normalize_value(
                float(row["avg_monthly_searches"]), min_volume, max_volume
            ),
            normalized_growth=normalize_value(
                float(row["growth_rate"]),
                min_growth,
                max_growth,
            ),
            normalized_competition=float(row["competition_index"]),
        )

    return sorted(rows, key=lambda row: int(row["input_order"]))
