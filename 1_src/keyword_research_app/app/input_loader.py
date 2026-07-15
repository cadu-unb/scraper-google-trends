"""Leitura e validacao da entrada JSON de palavras-chave."""

from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path


class InputKeywordsError(ValueError):
    """Erro de entrada usado para mensagens claras ao usuario."""


def load_keywords_from_json(path: Path) -> list[str]:
    """Le palavras-chave de um arquivo JSON com a chave obrigatoria `keywords`.

    Args:
        path: Caminho do arquivo JSON de entrada.

    Returns:
        Lista validada de palavras-chave.

    Raises:
        InputKeywordsError: Quando o arquivo nao existe, esta malformado ou nao
            contem uma lista de strings na chave `keywords`.
    """
    if not path.exists():
        raise InputKeywordsError(f"Arquivo de entrada nao encontrado: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except JSONDecodeError as exc:
        raise InputKeywordsError(f"JSON invalido em {path}: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise InputKeywordsError(
            "O JSON de entrada deve ser um objeto com a chave 'keywords'."
        )

    if "keywords" not in payload:
        raise InputKeywordsError(
            "O JSON de entrada precisa conter a chave obrigatoria 'keywords'."
        )

    keywords = payload["keywords"]
    if not isinstance(keywords, list):
        raise InputKeywordsError(
            "A chave 'keywords' deve conter uma lista de strings."
        )

    invalid_items = [
        index
        for index, value in enumerate(keywords, start=1)
        if not isinstance(value, str)
    ]
    if invalid_items:
        positions = ", ".join(str(index) for index in invalid_items)
        raise InputKeywordsError(
            "Todos os itens de 'keywords' devem ser strings. "
            f"Posicoes invalidas: {positions}."
        )

    cleaned_keywords = [keyword for keyword in keywords if keyword.strip()]
    if not cleaned_keywords:
        raise InputKeywordsError(
            "A lista 'keywords' precisa conter pelo menos uma string nao vazia."
        )

    return cleaned_keywords
