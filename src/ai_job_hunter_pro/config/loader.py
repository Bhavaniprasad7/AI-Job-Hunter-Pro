from __future__ import annotations
from pathlib import Path
from typing import Any, Dict

import yaml

from ai_job_hunter_pro.config.settings import AppConfig, JobSourceConfig


def load_config(config_path: Path | str = "config/config.yaml") -> AppConfig:
    with open(config_path, "r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream) or {}

    if "job_sources" in data:
        data["job_sources"] = [JobSourceConfig(**source) for source in data["job_sources"]]
    return AppConfig(**data)
