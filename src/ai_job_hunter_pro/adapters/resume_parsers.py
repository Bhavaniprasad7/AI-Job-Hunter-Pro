from __future__ import annotations
import re
from pathlib import Path
from typing import List

import pdfplumber
import docx

from ai_job_hunter_pro.domain.entities import Resume
from ai_job_hunter_pro.domain.ports import ResumeParser


class BaseResumeParser(ResumeParser):
    def parse(self, file_path: str) -> Resume:
        path = Path(file_path)
        text = self._extract_text(path)
        return Resume(
            id=str(path.name),
            file_path=str(path),
            text=text,
            name=self._extract_name(text),
            email=self._extract_email(text),
            phone=self._extract_phone(text),
            skills=self._extract_skills(text),
            experience_years=self._extract_experience(text),
        )

    def _extract_text(self, path: Path) -> str:
        if path.suffix.lower() == ".pdf":
            return self._extract_pdf(path)
        if path.suffix.lower() == ".docx":
            return self._extract_docx(path)
        return self._extract_text_file(path)

    def _extract_pdf(self, path: Path) -> str:
        with pdfplumber.open(path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text

    def _extract_docx(self, path: Path) -> str:
        document = docx.Document(path)
        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    def _extract_text_file(self, path: Path) -> str:
        return path.read_text(encoding="utf-8", errors="ignore")

    def _extract_name(self, text: str) -> str | None:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return lines[0] if lines else None

    def _extract_email(self, text: str) -> str | None:
        match = re.search(r"[\w\.-]+@[\w\.-]+", text)
        return match.group(0) if match else None

    def _extract_phone(self, text: str) -> str | None:
        match = re.search(r"\+?\d[\d\s\-()]{7,}\d", text)
        return match.group(0) if match else None

    def _extract_skills(self, text: str) -> List[str]:
        normalized = text.lower()
        candidates = [
            "python",
            "sql",
            "data analysis",
            "machine learning",
            "project management",
            "communication",
            "cloud",
            "nlp",
        ]
        return [skill for skill in candidates if skill in normalized]

    def _extract_experience(self, text: str) -> float | None:
        match = re.search(r"(\d+)\+?\s+years?", text.lower())
        return float(match.group(1)) if match else None
