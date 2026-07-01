from __future__ import annotations
import os
from pathlib import Path
from typing import Any, Dict

import yaml

from ai_job_hunter_pro.config.settings import AppConfig, JobSourceConfig, FilterConfig, EmailConfig, ReportConfig


def load_config(config_path: Path | str = "config/config.yaml") -> AppConfig:
    """Load configuration from YAML file and validate with Pydantic.
    
    Environment variables override YAML values:
    - OPENAI_API_KEY: OpenAI API key for job matching
    """
    with open(config_path, "r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream) or {}

    # Convert nested config dicts to their Pydantic models
    # This ensures proper validation before passing to AppConfig
    if "job_sources" in data and isinstance(data["job_sources"], list):
        data["job_sources"] = [JobSourceConfig(**source) for source in data["job_sources"]]
    
    if "filter" in data and isinstance(data["filter"], dict):
        data["filter"] = FilterConfig(**data["filter"])
    
    if "email" in data and isinstance(data["email"], dict):
        data["email"] = EmailConfig(**data["email"])
    
    if "report" in data and isinstance(data["report"], dict):
        data["report"] = ReportConfig(**data["report"])
    
    # Convert resume_paths to Path objects if needed
    if "resume_paths" in data and isinstance(data["resume_paths"], list):
        data["resume_paths"] = [Path(p) if isinstance(p, str) else p for p in data["resume_paths"]]
    
    # Create AppConfig with validated data
    try:
        config = AppConfig(**data)
    except Exception as e:
        # Surface validation errors with context to help debug in environments
        # (Streamlit redacts pydantic errors in the UI; include keys to narrow down)
        raise RuntimeError(
            f"Configuration validation failed: {e}\nLoaded config keys: {list(data.keys())}"
        ) from e
    
    # Override with environment variables if present
    if os.getenv("OPENAI_API_KEY"):
        config.openai_api_key = os.getenv("OPENAI_API_KEY")
    
    return config
