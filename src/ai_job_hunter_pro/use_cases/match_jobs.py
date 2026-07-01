from __future__ import annotations
from typing import Iterable, List

from ai_job_hunter_pro.config.settings import AppConfig
from ai_job_hunter_pro.domain.entities import JobPost, MatchResult, Resume
from ai_job_hunter_pro.adapters.ai_matcher import OpenAIAdapter
from ai_job_hunter_pro.domain.ports import Matcher


class JobMatchingService:
    def __init__(self, config: AppConfig, matcher: Matcher | None = None):
        self.config = config
        self.matcher = matcher or OpenAIAdapter(
            api_key=config.openai_api_key,
            model=config.openai_model,
        )

    def match(self, resumes: Iterable[Resume], jobs: Iterable[JobPost]) -> List[MatchResult]:
        return [self.matcher.match(resume, job) for resume in resumes for job in jobs]
