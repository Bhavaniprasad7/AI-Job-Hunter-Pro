from __future__ import annotations
from pathlib import Path
from typing import Iterable, List

from ai_job_hunter_pro.adapters.resume_parsers import BaseResumeParser
from ai_job_hunter_pro.config.settings import AppConfig
from ai_job_hunter_pro.domain.entities import Resume


class ResumeParsingService:
    def __init__(self, config: AppConfig):
        self.config = config
        self.parser = BaseResumeParser()

    def parse_all(self) -> List[Resume]:
        resumes: List[Resume] = []
        for resume_path in self.config.resume_paths:
            path = Path(resume_path)
            if not path.exists():
                continue
            for file_path in path.rglob("*"):
                if file_path.suffix.lower() not in {".pdf", ".docx", ".txt"}:
                    continue
                resumes.append(self.parser.parse(str(file_path)))
        return resumes
