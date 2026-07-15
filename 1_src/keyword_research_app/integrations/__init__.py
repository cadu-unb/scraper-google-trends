# 1_src/keyword_research_app/integrations/__init__.py

_EXPORTS = {
    "MissingGoogleAdsCredentialsError": (".google_ads_client", "MissingGoogleAdsCredentialsError"),
    "fetch_google_ads_metrics": (".google_ads_client", "fetch_keyword_metrics"),
    "fetch_google_trends_metrics": (".google_trends_client", "fetch_keyword_metrics"),
    "fetch_mock_metrics": (".mock_client", "fetch_keyword_metrics"),
    "missing_credentials": (".google_ads_client", "missing_credentials"),
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
