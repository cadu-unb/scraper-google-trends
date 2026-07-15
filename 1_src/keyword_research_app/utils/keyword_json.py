"""Gravação de listas de palavras-chave na entrada JSON da aplicação."""

from __future__ import annotations

import json
from pathlib import Path


DEFAULT_INPUT_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "input_keywords.json"
)


def convert_keywords_to_json(
    keywords: list[str],
    output_path: Path | None = None,
) -> Path:
    """Converte palavras-chave e grava o JSON de entrada da aplicação.

    Args:
        keywords: Lista de palavras-chave não vazias.
        output_path: Destino opcional. Por padrão, usa o arquivo de entrada
            localizado em ``data/input_keywords.json``.

    Returns:
        Caminho do arquivo JSON gravado.

    Raises:
        TypeError: Quando a entrada não é uma lista de strings.
        ValueError: Quando a lista está vazia ou contém strings vazias.
    """
    if not isinstance(keywords, list) or any(
        not isinstance(keyword, str) for keyword in keywords
    ):
        raise TypeError("keywords deve ser uma lista de strings.")

    cleaned_keywords = [keyword.strip() for keyword in keywords]
    if not cleaned_keywords:
        raise ValueError("keywords deve conter pelo menos uma palavra-chave.")
    if any(not keyword for keyword in cleaned_keywords):
        raise ValueError("keywords não pode conter strings vazias.")

    destination = output_path or DEFAULT_INPUT_PATH
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as json_file:
        json.dump(
            {"keywords": cleaned_keywords},
            json_file,
            ensure_ascii=False,
            indent=2,
        )
        json_file.write("\n")

    return destination
