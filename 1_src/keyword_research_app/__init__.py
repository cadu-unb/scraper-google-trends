# 1_src/keyword_research_app/__init__.py

_EXPORTS = {
    "GoogleTrendsConnectionError": (".utils", "GoogleTrendsConnectionError"),
    "GoogleTrendsError": (".utils", "GoogleTrendsError"),
    "GoogleTrendsRateLimitError": (".utils", "GoogleTrendsRateLimitError"),
    "GoogleTrendsResponseError": (".utils", "GoogleTrendsResponseError"),
    "InputKeywordsError": (".app", "InputKeywordsError"),
    "MissingGoogleAdsCredentialsError": (".integrations", "MissingGoogleAdsCredentialsError"),
    "NormalizedKeyword": (".app", "NormalizedKeyword"),
    "Settings": (".config", "Settings"),
    "build_keyword_report": (".app", "build_keyword_report"),
    "build_report_payload": (".app", "build_report_payload"),
    "calculate_growth_rate": (".app", "calculate_growth_rate"),
    "calculate_relevance_score": (".app", "calculate_relevance_score"),
    "clamp_score": (".app", "clamp_score"),
    "collect_google_trends_interest": (".utils", "collect_google_trends_interest"),
    "convert_keywords_to_json": (".utils", "convert_keywords_to_json"),
    "copy_report_to_web_data": (".app", "copy_report_to_web_data"),
    "export_report_json": (".app", "export_report_json"),
    "fetch_google_ads_metrics": (".integrations", "fetch_google_ads_metrics"),
    "fetch_google_trends_metrics": (".integrations", "fetch_google_trends_metrics"),
    "fetch_keyword_metrics_by_source": (".main", "fetch_keyword_metrics_by_source"),
    "fetch_mock_metrics": (".integrations", "fetch_mock_metrics"),
    "generate_keyword_research_report": (".main", "generate_keyword_research_report"),
    "load_keywords_from_json": (".app", "load_keywords_from_json"),
    "load_settings": (".config", "load_settings"),
    "missing_credentials": (".integrations", "missing_credentials"),
    "normalize_keyword": (".app", "normalize_keyword"),
    "normalize_keywords": (".app", "normalize_keywords"),
    "normalize_value": (".app", "normalize_value"),
    "prompt_new_query_or_resume": (".main", "prompt_new_query_or_resume"),
    "should_start_new_google_trends_query": (".main", "should_start_new_google_trends_query"),
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
