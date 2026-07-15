# 1_src/keyword_research_app/app/__init__.py

_EXPORTS = {
    "InputKeywordsError": (".input_loader", "InputKeywordsError"),
    "NormalizedKeyword": (".normalizer", "NormalizedKeyword"),
    "build_keyword_report": (".report_builder", "build_keyword_report"),
    "build_report_payload": (".json_exporter", "build_report_payload"),
    "calculate_growth_rate": (".scoring", "calculate_growth_rate"),
    "calculate_relevance_score": (".scoring", "calculate_relevance_score"),
    "clamp_score": (".scoring", "clamp_score"),
    "copy_report_to_web_data": (".json_exporter", "copy_report_to_web_data"),
    "export_report_json": (".json_exporter", "export_report_json"),
    "load_keywords_from_json": (".input_loader", "load_keywords_from_json"),
    "normalize_keyword": (".normalizer", "normalize_keyword"),
    "normalize_keywords": (".normalizer", "normalize_keywords"),
    "normalize_value": (".scoring", "normalize_value"),
}

__all__ = list(_EXPORTS)


def __getattr__(name: str):
    from importlib import import_module

    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module_name, attribute_name = _EXPORTS[name]
    value = getattr(import_module(module_name, __name__), attribute_name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))
