# 1_src/generic/values/__init__.py

_EXPORTS = {
    "CONS_VERSION_AGGREGATORS": (".constants", "CONS_VERSION_AGGREGATORS"),
    "CONS_VERSION_BLOG": (".constants", "CONS_VERSION_BLOG"),
    "CONS_VERSION_TASKMODEL": (".constants", "CONS_VERSION_TASKMODEL"),
    "CONS_VERSION_TASKMODEL_OLD": (".constants", "CONS_VERSION_TASKMODEL_OLD"),
    "CONS_VERSION_TECHNICALTAG": (".constants", "CONS_VERSION_TECHNICALTAG"),
    "CONS_VERSION_TOOLMODEL": (".constants", "CONS_VERSION_TOOLMODEL"),
    "CONS_VERSION_TOOLMODEL_OLD": (".constants", "CONS_VERSION_TOOLMODEL_OLD"),
    "atributos_funcionais_abreviacao": (".variaveis", "atributos_funcionais_abreviacao"),
    "atributos_funcionais_descricao": (".variaveis", "atributos_funcionais_descricao"),
    "atributos_funcionais_ferramentas": (".variaveis", "atributos_funcionais_ferramentas"),
    "atributos_funcionais_site": (".variaveis", "atributos_funcionais_site"),
    "atributos_site": (".variaveis", "atributos_site"),
    "block_funcionais_abreviacao": (".variaveis", "block_funcionais_abreviacao"),
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
