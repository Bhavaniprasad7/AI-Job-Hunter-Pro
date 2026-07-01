"""Domain layer for AI Job Hunter Pro."""
from ai_job_hunter_pro.domain.entities import JobPost, MatchResult, Resume
from ai_job_hunter_pro.domain.ports import (
    ConfigProvider,
    EmailSender,
    JobRepository,
    JobSourceCollector,
    MatchRepository,
    Matcher,
    ResumeParser,
)

__all__ = [
    "JobPost",
    "MatchResult",
    "Resume",
    "JobSourceCollector",
    "ResumeParser",
    "Matcher",
    "JobRepository",
    "MatchRepository",
    "ConfigProvider",
    "EmailSender",
]
