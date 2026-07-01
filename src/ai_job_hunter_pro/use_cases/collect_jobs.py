from __future__ import annotations
from typing import Iterable, List

from ai_job_hunter_pro.adapters.json_collector import JsonJobCollector  # noqa: F401
from ai_job_hunter_pro.adapters.rss_collector import RssJobCollector  # noqa: F401
from ai_job_hunter_pro.config.settings import AppConfig
from ai_job_hunter_pro.domain.entities import JobPost
from ai_job_hunter_pro.plugins import PluginRegistry, load_builtin_collectors


class JobCollectorService:
    def __init__(self, config: AppConfig):
        self.config = config

    def collect(self) -> List[JobPost]:
        load_builtin_collectors()
        jobs: List[JobPost] = []
        for source in self.config.job_sources:
            collector_cls = PluginRegistry.get_collector(source.plugin)
            collector = collector_cls(source.settings)
            jobs.extend(list(collector.collect()))
        return jobs
