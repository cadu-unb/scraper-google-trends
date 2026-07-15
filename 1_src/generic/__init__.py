# 1_src/generic/__init__.py

_EXPORTS = {
    "CONS_VERSION_AGGREGATORS": (".values", "CONS_VERSION_AGGREGATORS"),
    "CONS_VERSION_BLOG": (".values", "CONS_VERSION_BLOG"),
    "CONS_VERSION_TASKMODEL": (".values", "CONS_VERSION_TASKMODEL"),
    "CONS_VERSION_TASKMODEL_OLD": (".values", "CONS_VERSION_TASKMODEL_OLD"),
    "CONS_VERSION_TECHNICALTAG": (".values", "CONS_VERSION_TECHNICALTAG"),
    "CONS_VERSION_TOOLMODEL": (".values", "CONS_VERSION_TOOLMODEL"),
    "CONS_VERSION_TOOLMODEL_OLD": (".values", "CONS_VERSION_TOOLMODEL_OLD"),
    "DATA": (".paths", "DATA"),
    "DIR_AGGREGATORS": (".paths", "DIR_AGGREGATORS"),
    "DIR_BLOG": (".paths", "DIR_BLOG"),
    "DIR_DYN_PIPE_INS": (".paths", "DIR_DYN_PIPE_INS"),
    "DIR_GERADOR": (".paths", "DIR_GERADOR"),
    "DIR_TASK": (".paths", "DIR_TASK"),
    "DIR_TEMPLATE": (".paths", "DIR_TEMPLATE"),
    "DIR_TOOL": (".paths", "DIR_TOOL"),
    "RAIZ": (".paths", "RAIZ"),
    "atributos_funcionais_abreviacao": (".values", "atributos_funcionais_abreviacao"),
    "atributos_funcionais_descricao": (".values", "atributos_funcionais_descricao"),
    "atributos_funcionais_ferramentas": (".values", "atributos_funcionais_ferramentas"),
    "atributos_funcionais_site": (".values", "atributos_funcionais_site"),
    "atributos_site": (".values", "atributos_site"),
    "block_funcionais_abreviacao": (".values", "block_funcionais_abreviacao"),
    "encontrar_palavra_proxima": (".utils", "encontrar_palavra_proxima"),
    "mapear_chaves_da_palavra": (".utils", "mapear_chaves_da_palavra"),
    "on_press": (".utils", "on_press"),
    "possui_palavra_proxima": (".utils", "possui_palavra_proxima"),
    "verificar_inedito": (".utils", "verificar_inedito"),
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
