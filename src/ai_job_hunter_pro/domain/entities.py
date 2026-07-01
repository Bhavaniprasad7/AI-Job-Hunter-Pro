from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional

@dataclass(frozen=True)
class JobPost:
    id: str
    title: str
    description: str
    company: str
    location: str
    posted_date: Optional[date]
    url: Optional[str]
    source: str
    raw_data: dict = field(default_factory=dict)

@dataclass(frozen=True)
class Resume:
    id: str
    file_path: str
    text: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    experience_years: Optional[float] = None

@dataclass(frozen=True)
class MatchResult:
    resume_id: str
    job_id: str
    score: float
    ats_score: float
    match_summary: str
    skill_matches: List[str]
    missing_skills: List[str]
    job_post: JobPost
    resume: Resume
