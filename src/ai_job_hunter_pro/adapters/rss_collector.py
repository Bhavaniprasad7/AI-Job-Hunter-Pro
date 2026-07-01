from __future__ import annotations
from datetime import datetime
from typing import Iterable

import feedparser

from ai_job_hunter_pro.domain.entities import JobPost
from ai_job_hunter_pro.domain.ports import JobSourceCollector
from ai_job_hunter_pro.plugins import register_collector


@register_collector("rss")
class RssJobCollector(JobSourceCollector):
    def __init__(self, settings: dict):
        self.url = settings.get("url", "")

    def collect(self) -> Iterable[JobPost]:
        if not self.url:
            return []

        feed = feedparser.parse(self.url)
        for entry in feed.entries:
            posted_date = None
            if getattr(entry, "published_parsed", None):
                posted_date = datetime(*entry.published_parsed[:6]).date()
            yield JobPost(
                id=str(getattr(entry, "id", entry.link)),
                title=getattr(entry, "title", ""),
                description=getattr(entry, "summary", ""),
                company=getattr(entry, "author", ""),
                location=getattr(entry, "location", ""),
                posted_date=posted_date,
                url=getattr(entry, "link", ""),
                source="rss_feed",
                raw_data={"entry": entry},
            )
