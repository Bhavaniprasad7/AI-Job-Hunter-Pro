from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable, List

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from ai_job_hunter_pro.config.settings import ReportConfig
from ai_job_hunter_pro.domain.entities import MatchResult


class ReportingService:
    def __init__(self, config: ReportConfig):
        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        self.template_env = Environment(
            loader=FileSystemLoader(str(Path(__file__).parent / "templates")),
            autoescape=select_autoescape(["html"]),
        )

    def generate_reports(self, matches: Iterable[MatchResult]) -> None:
        matches_list = [self._serialize(match) for match in matches]
        self._write_json(matches_list)
        self._write_excel(matches_list)
        self._write_html(matches_list)

    def _serialize(self, match: MatchResult) -> dict:
        return {
            "resume_id": match.resume_id,
            "job_id": match.job_id,
            "score": match.score,
            "ats_score": match.ats_score,
            "summary": match.match_summary,
            "skill_matches": match.skill_matches,
            "missing_skills": match.missing_skills,
            "job_title": match.job_post.title,
            "company": match.job_post.company,
            "location": match.job_post.location,
            "url": match.job_post.url,
        }

    def _write_json(self, data: List[dict]) -> None:
        path = self.config.output_dir / self.config.json_filename
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def _write_excel(self, data: List[dict]) -> None:
        df = pd.DataFrame(data)
        path = self.config.output_dir / self.config.excel_filename
        df.to_excel(path, index=False)

    def _write_html(self, data: List[dict]) -> None:
        template = self.template_env.get_template("report.html.j2")
        html = template.render(matches=data)
        path = self.config.output_dir / self.config.html_filename
        path.write_text(html, encoding="utf-8")
