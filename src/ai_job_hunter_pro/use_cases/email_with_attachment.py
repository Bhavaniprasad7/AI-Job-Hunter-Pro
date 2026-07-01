from __future__ import annotations
import mimetypes
from email.message import EmailMessage
from pathlib import Path
from typing import List

from ai_job_hunter_pro.domain.ports import EmailSender


class AttachmentEmailSender(EmailSender):
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

    def send(self, subject: str, body: str, recipients: List[str], attachments: List[Path] | None = None) -> None:
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self.sender
        message["To"] = ", ".join(recipients)
        message.set_content(body)

        attachments = attachments or []
        for attachment in attachments:
            ctype, encoding = mimetypes.guess_type(str(attachment))
            if ctype is None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)
            with attachment.open("rb") as file:
                message.add_attachment(file.read(), maintype=maintype, subtype=subtype, filename=attachment.name)

        with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
            if self.use_tls:
                server.starttls()
            if self.username and self.password:
                server.login(self.username, self.password)
            server.send_message(message)
