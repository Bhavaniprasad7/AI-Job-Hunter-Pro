from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings

class JobSourceConfig(BaseSettings):
    name: str
    plugin: str
    settings: Dict[str, Any] = Field(default_factory=dict)

class FilterConfig(BaseSettings):
    experience_min: float = 0.0
    skills_all: List[str] = Field(default_factory=list)
    skills_any: List[str] = Field(default_factory=list)
    company: List[str] = Field(default_factory=list)
    location: List[str] = Field(default_factory=list)
    max_age_days: int = 30

class EmailConfig(BaseSettings):
    enabled: bool = False
    sender: str = "no-reply@example.com"
    recipients: List[str] = Field(default_factory=list)
    smtp_server: str = "smtp.example.com"
    smtp_port: int = 587
    username: str = ""
    password: str = ""
    use_tls: bool = True
    daily_summary_subject: str = "AI Job Hunter Pro Daily Summary"

class ReportConfig(BaseSettings):
    output_dir: Path = Path("reports")
    excel_filename: str = "job_matches.xlsx"
    html_filename: str = "job_matches.html"
    json_filename: str = "job_matches.json"

class AppConfig(BaseSettings):
    environment: str = "development"
    database_url: str = "sqlite:///ai_job_hunter_pro.db"
    resume_paths: List[Path] = Field(default_factory=lambda: [Path("resumes")])
    job_sources: List[JobSourceConfig] = Field(default_factory=list)
    filter: FilterConfig = FilterConfig()
    email: EmailConfig = EmailConfig()
    report: ReportConfig = ReportConfig()
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"
        env_prefix = "AI_JOB_HUNTER_PRO_"
        extra = "ignore"
