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

    def collect(self) -> tuple[List[JobPost], List[str]]:
        load_builtin_collectors()
        jobs: List[JobPost] = []
        warnings: List[str] = []
        for source in self.config.job_sources:
            collector_cls = PluginRegistry.get_collector(source.plugin)
            collector = collector_cls(source.settings)
            try:
                source_jobs = list(collector.collect())
                jobs.extend(source_jobs)
            except Exception as exc:
                warnings.append(
                    f"Source '{source.name}' ({source.plugin}) failed: {exc}"
                )
        return jobs, warnings
