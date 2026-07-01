from __future__ import annotations
from typing import Dict, Type

from ai_job_hunter_pro.domain.ports import JobSourceCollector


class PluginRegistry:
    _collectors: Dict[str, Type[JobSourceCollector]] = {}
    _builtins_loaded: bool = False

    @classmethod
    def register_collector(cls, key: str, collector: Type[JobSourceCollector]) -> None:
        cls._collectors[key] = collector

    @classmethod
    def get_collector(cls, key: str) -> Type[JobSourceCollector]:
        if key not in cls._collectors:
            if not cls._builtins_loaded:
                load_builtin_collectors()
            if key not in cls._collectors:
                raise KeyError(f"No registered collector for plugin '{key}'")
        return cls._collectors[key]


def load_builtin_collectors() -> None:
    """Ensure built-in collector plugins are imported and registered."""
    import ai_job_hunter_pro.adapters  # noqa: F401
    PluginRegistry._builtins_loaded = True


def register_collector(name: str):
    def decorator(collector: Type[JobSourceCollector]):
        PluginRegistry.register_collector(name, collector)
        return collector

    return decorator
