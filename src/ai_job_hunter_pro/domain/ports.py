from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from typing import Iterable, List, Optional

from ai_job_hunter_pro.domain.entities import JobPost, Resume, MatchResult

class JobSourceCollector(ABC):
    @abstractmethod
    def collect(self) -> Iterable[JobPost]:
        pass

class ResumeParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> Resume:
        pass

class Matcher(ABC):
    @abstractmethod
    def match(self, resume: Resume, job_post: JobPost) -> MatchResult:
        pass

class JobRepository(ABC):
    @abstractmethod
    def save_jobs(self, jobs: Iterable[JobPost]) -> None:
        pass

    @abstractmethod
    def list_jobs(self, source: Optional[str] = None) -> List[JobPost]:
        pass

class MatchRepository(ABC):
    @abstractmethod
    def save_matches(self, matches: Iterable[MatchResult]) -> None:
        pass

    @abstractmethod
    def list_matches(self, resume_id: Optional[str] = None) -> List[MatchResult]:
        pass

class ConfigProvider(ABC):
    @abstractmethod
    def get(self, key: str, default=None):
        pass

class EmailSender(ABC):
    @abstractmethod
    def send(
        self,
        subject: str,
        body: str,
        recipients: List[str],
        attachments: List[Path] | None = None,
    ) -> None:
        pass
