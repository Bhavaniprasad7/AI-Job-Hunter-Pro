from __future__ import annotations
from typing import Iterable

from ai_job_hunter_pro.config.settings import EmailConfig
from ai_job_hunter_pro.domain.entities import MatchResult
from ai_job_hunter_pro.domain.ports import EmailSender


class DailySummaryService:
    def __init__(self, email_config: EmailConfig, sender: EmailSender):
        self.email_config = email_config
        self.sender = sender

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
        self.sender.send(self.email_config.daily_summary_subject, body, self.email_config.recipients)
