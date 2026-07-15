# 1_src/generic/utils/__init__.py

_EXPORTS = {
    "encontrar_palavra_proxima": (".analise_nomes", "encontrar_palavra_proxima"),
    "mapear_chaves_da_palavra": (".analise_nomes", "mapear_chaves_da_palavra"),
    "on_press": (".coordenadas", "on_press"),
    "possui_palavra_proxima": (".analise_nomes", "possui_palavra_proxima"),
    "verificar_inedito": (".analise_nomes", "verificar_inedito"),
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
