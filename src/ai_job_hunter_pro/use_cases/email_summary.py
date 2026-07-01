from __future__ import annotations
from pathlib import Path
from typing import Iterable, List

from ai_job_hunter_pro.config.settings import EmailConfig, ReportConfig
from ai_job_hunter_pro.domain.entities import MatchResult
from ai_job_hunter_pro.domain.ports import EmailSender


class DailySummaryService:
    def __init__(
        self,
        email_config: EmailConfig,
        sender: EmailSender,
        report_config: ReportConfig | None = None,
    ):
        self.email_config = email_config
        self.sender = sender
        self.report_config = report_config

    def send_summary(self, matches: Iterable[MatchResult]) -> None:
        if not self.email_config.enabled or not self.email_config.recipients:
            return

        lines = [
            f"Resume: {match.resume_id}",
            f"Job: {match.job_post.title} @ {match.job_post.company}",
            f"Score: {match.score:.1f}, ATS: {match.ats_score:.1f}",
            f"Link: {match.job_post.url}",
            "",
        ]
        body = "\n".join(lines)
        attachments: List[Path] = []
        if self.report_config:
            excel_path = self.report_config.output_dir / self.report_config.excel_filename
            if excel_path.exists():
                attachments.append(excel_path)

        self.sender.send(
            self.email_config.daily_summary_subject,
            body,
            self.email_config.recipients,
            attachments=attachments if attachments else None,
        )
