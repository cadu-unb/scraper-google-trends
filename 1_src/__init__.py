# 1_src/__init__.py

_EXPORTS = {
    "CONS_VERSION_AGGREGATORS": (".generic", "CONS_VERSION_AGGREGATORS"),
    "CONS_VERSION_BLOG": (".generic", "CONS_VERSION_BLOG"),
    "CONS_VERSION_TASKMODEL": (".generic", "CONS_VERSION_TASKMODEL"),
    "CONS_VERSION_TASKMODEL_OLD": (".generic", "CONS_VERSION_TASKMODEL_OLD"),
    "CONS_VERSION_TECHNICALTAG": (".generic", "CONS_VERSION_TECHNICALTAG"),
    "CONS_VERSION_TOOLMODEL": (".generic", "CONS_VERSION_TOOLMODEL"),
    "CONS_VERSION_TOOLMODEL_OLD": (".generic", "CONS_VERSION_TOOLMODEL_OLD"),
    "DATA": (".generic", "DATA"),
    "DIR_AGGREGATORS": (".generic", "DIR_AGGREGATORS"),
    "DIR_BLOG": (".generic", "DIR_BLOG"),
    "DIR_DYN_PIPE_INS": (".generic", "DIR_DYN_PIPE_INS"),
    "DIR_GERADOR": (".generic", "DIR_GERADOR"),
    "DIR_TASK": (".generic", "DIR_TASK"),
    "DIR_TEMPLATE": (".generic", "DIR_TEMPLATE"),
    "DIR_TOOL": (".generic", "DIR_TOOL"),
    "GoogleTrendsConnectionError": (".keyword_research_app", "GoogleTrendsConnectionError"),
    "GoogleTrendsError": (".keyword_research_app", "GoogleTrendsError"),
    "GoogleTrendsRateLimitError": (".keyword_research_app", "GoogleTrendsRateLimitError"),
    "GoogleTrendsResponseError": (".keyword_research_app", "GoogleTrendsResponseError"),
    "InputKeywordsError": (".keyword_research_app", "InputKeywordsError"),
    "MissingGoogleAdsCredentialsError": (".keyword_research_app", "MissingGoogleAdsCredentialsError"),
    "NormalizedKeyword": (".keyword_research_app", "NormalizedKeyword"),
    "RAIZ": (".generic", "RAIZ"),
    "Settings": (".keyword_research_app", "Settings"),
    "atributos_funcionais_abreviacao": (".generic", "atributos_funcionais_abreviacao"),
    "atributos_funcionais_descricao": (".generic", "atributos_funcionais_descricao"),
    "atributos_funcionais_ferramentas": (".generic", "atributos_funcionais_ferramentas"),
    "atributos_funcionais_site": (".generic", "atributos_funcionais_site"),
    "atributos_site": (".generic", "atributos_site"),
    "block_funcionais_abreviacao": (".generic", "block_funcionais_abreviacao"),
    "build_keyword_report": (".keyword_research_app", "build_keyword_report"),
    "build_report_payload": (".keyword_research_app", "build_report_payload"),
    "calculate_growth_rate": (".keyword_research_app", "calculate_growth_rate"),
    "calculate_relevance_score": (".keyword_research_app", "calculate_relevance_score"),
    "clamp_score": (".keyword_research_app", "clamp_score"),
    "collect_google_trends_interest": (".keyword_research_app", "collect_google_trends_interest"),
    "convert_keywords_to_json": (".keyword_research_app", "convert_keywords_to_json"),
    "copy_report_to_web_data": (".keyword_research_app", "copy_report_to_web_data"),
    "encontrar_palavra_proxima": (".generic", "encontrar_palavra_proxima"),
    "export_report_json": (".keyword_research_app", "export_report_json"),
    "fetch_google_ads_metrics": (".keyword_research_app", "fetch_google_ads_metrics"),
    "fetch_google_trends_metrics": (".keyword_research_app", "fetch_google_trends_metrics"),
    "fetch_keyword_metrics_by_source": (".keyword_research_app", "fetch_keyword_metrics_by_source"),
    "fetch_mock_metrics": (".keyword_research_app", "fetch_mock_metrics"),
    "generate_keyword_research_report": (".keyword_research_app", "generate_keyword_research_report"),
    "load_keywords_from_json": (".keyword_research_app", "load_keywords_from_json"),
    "load_settings": (".keyword_research_app", "load_settings"),
    "mapear_chaves_da_palavra": (".generic", "mapear_chaves_da_palavra"),
    "missing_credentials": (".keyword_research_app", "missing_credentials"),
    "normalize_keyword": (".keyword_research_app", "normalize_keyword"),
    "normalize_keywords": (".keyword_research_app", "normalize_keywords"),
    "normalize_value": (".keyword_research_app", "normalize_value"),
    "on_press": (".generic", "on_press"),
    "possui_palavra_proxima": (".generic", "possui_palavra_proxima"),
    "prompt_new_query_or_resume": (".keyword_research_app", "prompt_new_query_or_resume"),
    "should_start_new_google_trends_query": (".keyword_research_app", "should_start_new_google_trends_query"),
    "verificar_inedito": (".generic", "verificar_inedito"),
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
