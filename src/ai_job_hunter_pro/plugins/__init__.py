from __future__ import annotations
from typing import Dict, Type

from ai_job_hunter_pro.domain.ports import JobSourceCollector


class PluginRegistry:
    _collectors: Dict[str, Type[JobSourceCollector]] = {}

    @classmethod
    def register_collector(cls, key: str, collector: Type[JobSourceCollector]) -> None:
        cls._collectors[key] = collector

    @classmethod
    def get_collector(cls, key: str) -> Type[JobSourceCollector]:
        if key not in cls._collectors:
            raise KeyError(f"No registered collector for plugin '{key}'")
        return cls._collectors[key]


def register_collector(name: str):
    def decorator(collector: Type[JobSourceCollector]):
        PluginRegistry.register_collector(name, collector)
        return collector

    return decorator
