from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable

from ai_job_hunter_pro.domain.entities import JobPost
from ai_job_hunter_pro.domain.ports import JobSourceCollector
from ai_job_hunter_pro.plugins import register_collector


@register_collector("json")
class JsonJobCollector(JobSourceCollector):
    def __init__(self, settings: dict):
        self.path = Path(settings.get("path", "data/sample_jobs.json"))

    def collect(self) -> Iterable[JobPost]:
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as stream:
            data = json.load(stream)

        for item in data:
            yield JobPost(
                id=str(item.get("id", item.get("url", ""))),
                title=item.get("title", ""),
                description=item.get("description", ""),
                company=item.get("company", ""),
                location=item.get("location", ""),
                posted_date=item.get("posted_date"),
                url=item.get("url"),
                source="local_json",
                raw_data=item,
            )
