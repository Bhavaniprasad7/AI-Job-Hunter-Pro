from __future__ import annotations
from typing import Iterable, List

from ai_job_hunter_pro.config.settings import AppConfig
from ai_job_hunter_pro.domain.entities import JobPost
from ai_job_hunter_pro.plugins import PluginRegistry


class JobCollectorService:
    def __init__(self, config: AppConfig):
        self.config = config

    def collect(self) -> List[JobPost]:
        jobs: List[JobPost] = []
        for source in self.config.job_sources:
            collector_cls = PluginRegistry.get_collector(source.plugin)
            collector = collector_cls(source.settings)
            jobs.extend(list(collector.collect()))
        return jobs
