from __future__ import annotations
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field



def _default_fortune_500_companies() -> List[str]:
    return [
        "Apple",
        "Microsoft",
        "Amazon",
        "Alphabet",
        "Meta",
        "Berkshire Hathaway",
        "Walmart",
        "Exxon Mobil",
        "JPMorgan Chase",
        "Chevron",
        "Pfizer",
        "PepsiCo",
        "Coca-Cola",
        "Intel",
        "IBM",
        "Cisco",
        "Oracle",
        "Salesforce",
        "Adobe",
        "Accenture",
        "Deloitte",
        "FedEx",
        "UPS",
        "Verizon",
        "AT&T",
        "Boeing",
        "Honeywell",
        "Tesla",
        "Procter & Gamble",
        "Nike",
    ]

class JobSourceConfig(BaseModel):
    name: str
    plugin: str
    settings: Dict[str, Any] = Field(default_factory=dict)

class FilterConfig(BaseModel):
    experience_min: float = 0.0
    skills_all: List[str] = Field(default_factory=list)
    skills_any: List[str] = Field(default_factory=list)
    company: List[str] = Field(default_factory=list)
    location: List[str] = Field(default_factory=list)
    max_age_days: int = 30
    fortune_500_only: bool = False
    fortune_500_companies: List[str] = Field(default_factory=_default_fortune_500_companies)

class EmailConfig(BaseModel):
    enabled: bool = False
    sender: str = "no-reply@example.com"
    recipients: List[str] = Field(default_factory=list)
    smtp_server: str = "smtp.example.com"
    smtp_port: int = 587
    username: str = ""
    password: str = ""
    use_tls: bool = True
    daily_summary_subject: str = "AI Job Hunter Pro Daily Summary"

class ReportConfig(BaseModel):
    output_dir: Path = Path("reports")
    excel_filename: str = "job_matches.xlsx"
    html_filename: str = "job_matches.html"
    json_filename: str = "job_matches.json"

class AppConfig(BaseModel):
    environment: str = "development"
    database_url: str = "sqlite:///ai_job_hunter_pro.db"
    resume_paths: List[Path] = Field(default_factory=lambda: [Path("resumes")])
    job_sources: List[JobSourceConfig] = Field(default_factory=list)
    filter: FilterConfig = FilterConfig()
    email: EmailConfig = EmailConfig()
    report: ReportConfig = ReportConfig()
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"

    class Config:
        extra = "ignore"
