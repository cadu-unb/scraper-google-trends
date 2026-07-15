# 1_src/generic/paths/__init__.py

_EXPORTS = {
    "DATA": (".data", "DATA"),
    "DIR_AGGREGATORS": (".data", "DIR_AGGREGATORS"),
    "DIR_BLOG": (".data", "DIR_BLOG"),
    "DIR_DYN_PIPE_INS": (".data", "DIR_DYN_PIPE_INS"),
    "DIR_GERADOR": (".data", "DIR_GERADOR"),
    "DIR_TASK": (".data", "DIR_TASK"),
    "DIR_TEMPLATE": (".data", "DIR_TEMPLATE"),
    "DIR_TOOL": (".data", "DIR_TOOL"),
    "RAIZ": (".data", "RAIZ"),
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
