from __future__ import annotations
import re
from datetime import date, timedelta
from typing import Iterable, List, Optional

from ai_job_hunter_pro.config.settings import FilterConfig
from ai_job_hunter_pro.domain.entities import JobPost


class JobFilterService:
    def __init__(self, config: FilterConfig):
        self.config = config

    def filter(self, jobs: Iterable[JobPost]) -> List[JobPost]:
        return [job for job in jobs if self._matches(job)]

    def _matches(self, job: JobPost) -> bool:
        if self.config.company and job.company.lower() not in [c.lower() for c in self.config.company]:
            return False
        if self.config.location and job.location.lower() not in [l.lower() for l in self.config.location]:
            return False
        if self.config.max_age_days and job.posted_date:
            age = date.today() - job.posted_date
            if age > timedelta(days=self.config.max_age_days):
                return False
        if self.config.experience_min is not None:
            required_years = self._extract_required_experience(job)
            if required_years is not None and required_years > self.config.experience_min:
                return False
        if self.config.skills_all or self.config.skills_any:
            job_skills = set(self._extract_skills(job))
            if self.config.skills_all and not set(self.config.skills_all).issubset(job_skills):
                return False
            if self.config.skills_any and not job_skills.intersection({s.lower() for s in self.config.skills_any}):
                return False
        return True

    def _extract_required_experience(self, job: JobPost) -> float | None:
        candidates = [job.title or "", job.description or ""]
        for text in candidates:
            match = re.search(r"(\d+)\+?\s+years?", text.lower())
            if match:
                return float(match.group(1))
        return None

    def _extract_skills(self, job: JobPost) -> List[str]:
        normalized = (job.title + " " + job.description).lower()
        keywords = [
            "python",
            "sql",
            "machine learning",
            "cloud",
            "aws",
            "azure",
            "gcp",
            "data analysis",
            "nlp",
            "devops",
        ]
        return [keyword for keyword in keywords if keyword in normalized]
