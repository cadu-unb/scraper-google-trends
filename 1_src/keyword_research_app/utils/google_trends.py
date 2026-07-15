"""Coleta resiliente do interesse individual por meio do pytrends."""

from __future__ import annotations

import hashlib
import json
import random
import time
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pandas import DataFrame
from pytrends.exceptions import ResponseError, TooManyRequestsError
from pytrends.request import TrendReq
from requests.exceptions import RequestException


CACHE_VERSION = 1


class GoogleTrendsError(RuntimeError):
    """Erro base para falhas durante a consulta ao Google Trends."""


class GoogleTrendsConnectionError(GoogleTrendsError):
    """Indica falha de conexão ou tempo limite ao consultar o serviço."""


class GoogleTrendsRateLimitError(GoogleTrendsError):
    """Indica bloqueio temporário por excesso de requisições HTTP 429."""


class GoogleTrendsResponseError(GoogleTrendsError):
    """Indica resposta inesperada ou inválida devolvida pelo Google Trends."""


def _validate_keywords(keywords: Sequence[str]) -> list[str]:
    """Valida os termos sem alterar sua ordem."""
    cleaned_keywords = [keyword.strip() for keyword in keywords]
    if not cleaned_keywords or any(not keyword for keyword in cleaned_keywords):
        raise ValueError("Informe ao menos uma palavra-chave não vazia.")
    return cleaned_keywords


def _request_interest_over_time(
    keywords: list[str],
    *,
    language: str,
    timezone: int,
    geo: str,
    timeframe: str,
    max_retries: int,
    backoff_seconds: float,
    sleeper: Callable[[float], None],
) -> DataFrame:
    """Executa uma consulta com retentativas controladas pela aplicação."""
    for attempt in range(max_retries + 1):
        try:
            client = TrendReq(
                hl=language,
                tz=timezone,
                timeout=(10, 30),
            )
            client.build_payload(
                keywords,
                timeframe=timeframe,
                geo=geo,
            )
            return client.interest_over_time()
        except TooManyRequestsError as exc:
            if attempt == max_retries:
                raise GoogleTrendsRateLimitError(
                    "O Google Trends bloqueou temporariamente as consultas "
                    "com HTTP 429. Aguarde antes de tentar novamente."
                ) from exc
        except RequestException as exc:
            if attempt == max_retries:
                raise GoogleTrendsConnectionError(
                    "Não foi possível conectar ao Google Trends após "
                    f"{max_retries + 1} tentativas."
                ) from exc
        except ResponseError as exc:
            status_code = getattr(exc.response, "status_code", None)
            if status_code is not None and status_code >= 500:
                if attempt == max_retries:
                    raise GoogleTrendsResponseError(
                        "O Google Trends permaneceu indisponível após "
                        f"{max_retries + 1} tentativas."
                    ) from exc
            else:
                raise GoogleTrendsResponseError(
                    "O Google Trends devolveu uma resposta inválida "
                    f"(HTTP {status_code or 'desconhecido'})."
                ) from exc
        except (KeyError, ValueError) as exc:
            raise GoogleTrendsResponseError(
                "O Google Trends devolveu dados em formato inesperado."
            ) from exc

        sleeper(backoff_seconds * (2**attempt))

    raise GoogleTrendsError("A consulta terminou sem resposta.")


def _remove_partial_periods(frame: DataFrame) -> DataFrame:
    """Remove períodos ainda incompletos sinalizados pelo Google Trends."""
    if "isPartial" not in frame.columns:
        return frame
    return frame.loc[~frame["isPartial"].astype(bool)].drop(columns="isPartial")


def _get_series(frame: DataFrame, keyword: str):
    """Obtém uma série numérica obrigatória da resposta."""
    if keyword not in frame.columns:
        raise GoogleTrendsResponseError(
            f"A resposta não contém dados para o termo: {keyword}."
        )
    return frame[keyword].fillna(0).astype(int)


def _analyze_curve(values: list[int]) -> dict[str, float | str]:
    """Resume direção e variação de uma série por regressão linear simples."""
    if len(values) < 2:
        return {
            "trend_slope": 0.0,
            "trend_change": 0.0,
            "trend_direction": "ESTÁVEL",
        }

    mean_x = (len(values) - 1) / 2
    mean_y = sum(values) / len(values)
    numerator = sum(
        (index - mean_x) * (value - mean_y)
        for index, value in enumerate(values)
    )
    denominator = sum(
        (index - mean_x) ** 2
        for index in range(len(values))
    )
    slope = numerator / denominator if denominator else 0.0
    projected_change = slope * (len(values) - 1)

    if projected_change >= 5:
        direction = "CRESCENTE"
    elif projected_change <= -5:
        direction = "DECRESCENTE"
    else:
        direction = "ESTÁVEL"

    return {
        "trend_slope": round(slope, 2),
        "trend_change": round(projected_change, 2),
        "trend_direction": direction,
    }


def _curve_relevance_score(
    average_interest: float,
    latest_interest: int,
    trend_change: float,
) -> float:
    """Combina interesse sustentado, valor recente e direção da curva."""
    trend_component = max(0.0, min(100.0, 50 + trend_change))
    score = (
        0.5 * average_interest
        + 0.3 * latest_interest
        + 0.2 * trend_component
    )
    return round(max(0.0, min(100.0, score)), 2)


def _build_keyword_metric(
    frame: DataFrame,
    *,
    keyword: str,
) -> dict[str, Any]:
    """Transforma a série individual do termo em métrica serializável."""
    complete_frame = _remove_partial_periods(frame)
    if complete_frame.empty:
        raise GoogleTrendsResponseError(
            "O Google Trends não retornou períodos completos para os termos."
        )

    keyword_series = _get_series(complete_frame, keyword)
    values = keyword_series.tolist()
    keyword_average = round(float(keyword_series.mean()), 2)
    latest_interest = int(keyword_series.iloc[-1])
    curve = _analyze_curve(values)

    return {
        "keyword": keyword,
        "average_interest": keyword_average,
        "peak_interest": int(keyword_series.max()),
        "latest_interest": latest_interest,
        "interest_values": values,
        **curve,
        "relevance_score": _curve_relevance_score(
            keyword_average,
            latest_interest,
            float(curve["trend_change"]),
        ),
        "timeline": [
            {
                "date": timestamp.isoformat(),
                "interest": int(value),
            }
            for timestamp, value in keyword_series.items()
        ],
        "source": "GOOGLE_TRENDS",
    }


def _null_metric(keyword: str) -> dict[str, Any]:
    """Métrica vazia usada quando uma consulta é pulada por bloqueio 429."""
    return {
        "keyword": keyword,
        "average_interest": 0.0,
        "peak_interest": 0,
        "latest_interest": 0,
        "interest_values": [],
        "trend_slope": 0.0,
        "trend_change": 0.0,
        "trend_direction": "ESTÁVEL",
        "relevance_score": 0.0,
        "timeline": [],
        "source": "GOOGLE_TRENDS",
        "cache_hit": False,
        "skipped": True,
    }


def _new_cache() -> dict[str, Any]:
    """Cria a estrutura vazia do cache persistente."""
    return {"version": CACHE_VERSION, "entries": {}}


def _load_cache(cache_path: Path | None) -> dict[str, Any]:
    """Carrega o cache ou retorna uma estrutura vazia quando indisponível."""
    if cache_path is None or not cache_path.exists():
        return _new_cache()
    try:
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return _new_cache()
    if cache.get("version") != CACHE_VERSION:
        return _new_cache()
    if not isinstance(cache.get("entries"), dict):
        return _new_cache()
    return cache


def _cache_key(
    keyword: str,
    *,
    language: str,
    timezone: int,
    geo: str,
    timeframe: str,
) -> str:
    """Identifica uma consulta e todos os parâmetros que alteram seu resultado."""
    payload = {
        "geo": geo,
        "keyword": keyword,
        "language": language,
        "timeframe": timeframe,
        "timezone": timezone,
    }
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _cached_metric(
    cache: dict[str, Any],
    key: str,
) -> dict[str, Any] | None:
    """Retorna a métrica em cache para a chave, sem expiração automática.

    O cache só é limpo quando o usuário escolhe explicitamente iniciar uma
    nova consulta (ver prompt em `main.py`), evitando que uma expiração por
    tempo force novas requisições e estoure o limite do Google Trends.
    """
    entry = cache["entries"].get(key)
    if not isinstance(entry, dict):
        return None
    metric = entry.get("metric")
    if not isinstance(metric, dict):
        return None
    return {**metric, "cache_hit": True}


def _save_cached_metric(
    cache: dict[str, Any],
    key: str,
    metric: dict[str, Any],
    cache_path: Path | None,
) -> None:
    """Atualiza o cache em disco após cada consulta concluída."""
    if cache_path is None:
        return
    cache["entries"][key] = {
        "cached_at": datetime.now(UTC).isoformat(),
        "metric": {**metric, "cache_hit": False},
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = cache_path.with_suffix(f"{cache_path.suffix}.tmp")
    temporary_path.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(cache_path)


def collect_google_trends_interest(
    keywords: Sequence[str],
    *,
    language: str = "pt-BR",
    timezone: int = 180,
    geo: str = "BR",
    timeframe: str = "today 12-m",
    context_filter: str | None = None,
    max_retries: int = 3,
    backoff_seconds: float = 5.0,
    min_delay_seconds: float = 5.0,
    max_delay_seconds: float = 20.0,
    cache_path: Path | None = None,
    sleeper: Callable[[float], None] = time.sleep,
    random_delay: Callable[[float, float], float] = random.uniform,
    progress_callback: Callable[[int, int, str, bool], None] | None = None,
) -> list[dict[str, Any]]:
    """Coleta cada palavra-chave individualmente com filtro contextual AND opcional.

    O Google Trends normaliza cada consulta na própria escala de 0 a 100. Por
    isso, a pontuação representa a média temporal do termo e não seu volume
    absoluto nem sua popularidade contra outras consultas.

    Args:
        keywords: Termos originais processados sequencialmente.
        language: Idioma da sessão do Google Trends.
        timezone: Diferença em minutos entre o fuso local e UTC.
        geo: Código geográfico consultado, como ``BR``.
        timeframe: Intervalo aceito pelo pytrends.
        context_filter: Termo de nicho concatenado via AND (``+``) a cada
            palavra-chave para restringir o contexto da busca. Quando ``None``
            ou vazio, a consulta é feita sem modificador.
        max_retries: Novas tentativas após a primeira falha.
        backoff_seconds: Espera inicial após falhas remotas.
        min_delay_seconds: Menor espera entre consultas concluídas.
        max_delay_seconds: Maior espera entre consultas concluídas.
        cache_path: Arquivo usado para retomar e reutilizar resultados.
        sleeper: Função de espera substituível em testes.
        random_delay: Gerador do intervalo entre consultas.
        progress_callback: Função opcional chamada após cada palavra processada.

    Returns:
        Métricas individuais e séries temporais por palavra-chave.

    Raises:
        ValueError: Quando termos ou parâmetros são inválidos.
        GoogleTrendsError: Quando uma consulta remota não pode ser concluída.
    """
    cleaned_keywords = _validate_keywords(keywords)
    if max_retries < 0 or backoff_seconds < 0:
        raise ValueError("Retentativas e backoff não podem ser negativos.")
    if min_delay_seconds < 0 or max_delay_seconds < min_delay_seconds:
        raise ValueError("O intervalo de espera configurado é inválido.")

    cache = _load_cache(cache_path)
    metrics: list[dict[str, Any]] = []
    total = len(cleaned_keywords)
    rate_limited = False

    for position, keyword in enumerate(cleaned_keywords, start=1):
        query_keyword = (
            f"{keyword} + {context_filter}"
            if context_filter and context_filter.strip()
            else keyword
        )
        key = _cache_key(
            query_keyword,
            language=language,
            timezone=timezone,
            geo=geo,
            timeframe=timeframe,
        )
        metric = _cached_metric(cache, key)
        cache_hit = metric is not None

        if metric is None:
            if rate_limited:
                print(
                    f"  ↷ [{position}/{total}] {keyword}: "
                    "pulado (sessão bloqueada por HTTP 429)"
                )
                metric = _null_metric(keyword)
            else:
                try:
                    frame = _request_interest_over_time(
                        [query_keyword],
                        language=language,
                        timezone=timezone,
                        geo=geo,
                        timeframe=timeframe,
                        max_retries=max_retries,
                        backoff_seconds=backoff_seconds,
                        sleeper=sleeper,
                    )
                    metric = _build_keyword_metric(
                        frame,
                        keyword=query_keyword,
                    )
                    metric["keyword"] = keyword
                    metric["cache_hit"] = False
                    _save_cached_metric(cache, key, metric, cache_path)
                except GoogleTrendsRateLimitError:
                    print(
                        f"  ✗ [{position}/{total}] {keyword}: "
                        "bloqueado por HTTP 429"
                    )
                    rate_limited = True
                    metric = _null_metric(keyword)

        metrics.append(metric)
        if not metric.get("skipped"):
            if progress_callback is not None:
                progress_callback(position, total, keyword, cache_hit)
            if not cache_hit:
                sleeper(random_delay(min_delay_seconds, max_delay_seconds))

    skipped_count = sum(1 for m in metrics if m.get("skipped"))
    if skipped_count:
        done_count = total - skipped_count
        print(
            f"\n⚠ {done_count}/{total} palavras concluídas; "
            f"{skipped_count} ignoradas por HTTP 429. "
            "Execute novamente para tentar as restantes "
            "(concluídas estão em cache)."
        )
        if done_count == 0:
            raise GoogleTrendsRateLimitError(
                "O Google Trends bloqueou temporariamente as consultas "
                "com HTTP 429. Aguarde antes de tentar novamente."
            )

    return metrics
