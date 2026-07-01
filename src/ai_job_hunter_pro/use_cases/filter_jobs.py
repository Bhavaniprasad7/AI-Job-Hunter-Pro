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
        text = f"{job.title or ''} {job.description or ''} {job.company or ''} {job.location or ''}".lower()
        if getattr(self.config, "role", ""):
            role = self.config.role.strip().lower()
            role_tokens = [token for token in re.split(r"\W+", role) if token]
            if role_tokens and not all(token in text for token in role_tokens):
                return False

        if getattr(self.config, "keywords", []):
            keywords = [keyword.strip().lower() for keyword in self.config.keywords if keyword.strip()]
            if keywords and not any(keyword in text for keyword in keywords):
                return False

        if self.config.company and job.company:
            if job.company.lower() not in [c.lower() for c in self.config.company]:
                return False

        if self.config.location:
            if not self._matches_location(job.location, self.config.location):
                return False

        if self.config.last_24_hours:
            if not job.posted_date:
                return False
            age = date.today() - job.posted_date
            if age > timedelta(days=1):
                return False

        if self.config.max_age_days and job.posted_date:
            age = date.today() - job.posted_date
            if age > timedelta(days=self.config.max_age_days):
                return False

        if self.config.experience_min is not None:
            required_years = self._extract_required_experience(job)
            if required_years is not None and required_years > self.config.experience_min:
                return False

        if self.config.fortune_500_only:
            if not self._is_fortune_500_company(job.company):
                return False

        if self.config.skills_all or self.config.skills_any:
            job_skills = set(self._extract_skills(job))
            if self.config.skills_all and not set(self.config.skills_all).issubset(job_skills):
                return False
            if self.config.skills_any and not job_skills.intersection({s.lower() for s in self.config.skills_any}):
                return False
        return True

    def _is_fortune_500_company(self, company_name: str) -> bool:
        normalized = company_name.strip().lower()
        winners = [c.lower() for c in self.config.fortune_500_companies]
        return any(normalized == company or normalized.endswith(f" {company}") for company in winners)

    def _extract_required_experience(self, job: JobPost) -> float | None:
        candidates = [job.title or "", job.description or ""]
        for text in candidates:
            match = re.search(r"(\d+)\+?\s+years?", text.lower())
            if match:
                return float(match.group(1))
        return None

    def _matches_location(self, job_location: str | None, filters: List[str]) -> bool:
        if not job_location:
            return False

        normalized_job_location = re.sub(r"\s+", " ", job_location.lower()).strip()
        for loc in filters:
            query = re.sub(r"\s+", " ", loc.lower()).strip()
            if not query:
                continue
            tokens = [token for token in query.split(" ") if token]
            if any(token in normalized_job_location for token in tokens):
                return True
        return False

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
            "logic apps",
        ]
        return [keyword for keyword in keywords if keyword in normalized]
