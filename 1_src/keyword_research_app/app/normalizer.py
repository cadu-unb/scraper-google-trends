"""Normalizacao e rastreabilidade das palavras-chave de entrada."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class NormalizedKeyword:
    """Representa uma palavra normalizada com sua posicao original."""

    input_order: int
    keyword: str


def normalize_keyword(keyword: str) -> str:
    """Remove espacos excedentes e converte a palavra para minusculas.

    Acentos sao preservados porque podem ser relevantes em buscas em
    portugues.
    """
    return " ".join(keyword.strip().lower().split())


def normalize_keywords(keywords: Iterable[str]) -> list[NormalizedKeyword]:
    """Normaliza palavras-chave preservando ordem e primeira ocorrencia.

    Duplicatas normalizadas sao ignoradas depois da primeira aparicao para que
    a ordem original continue rastreavel.
    """
    normalized_items: list[NormalizedKeyword] = []
    seen: set[str] = set()

    for input_order, raw_keyword in enumerate(keywords, start=1):
        keyword = normalize_keyword(str(raw_keyword))
        if not keyword or keyword in seen:
            continue

        normalized_items.append(
            NormalizedKeyword(input_order=input_order, keyword=keyword)
        )
        seen.add(keyword)

    return normalized_items
