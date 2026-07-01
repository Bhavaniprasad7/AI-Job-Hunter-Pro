from __future__ import annotations
import smtplib
from email.message import EmailMessage
from typing import List

from ai_job_hunter_pro.domain.ports import EmailSender


class SmtpEmailSender(EmailSender):
    def __init__(
        self,
        sender: str,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        use_tls: bool = True,
    ):
        self.sender = sender
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send(self, subject: str, body: str, recipients: List[str]) -> None:
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self.sender
        message["To"] = ", ".join(recipients)
        message.set_content(body)

        with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
            if self.use_tls:
                server.starttls()
            if self.username and self.password:
                server.login(self.username, self.password)
            server.send_message(message)
