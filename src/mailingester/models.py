from dataclasses import dataclass
from email.message import EmailMessage
from email.utils import parsedate_to_datetime
from pathlib import Path


@dataclass
class Content:
    content_type: str
    data: bytes
    filename: Path = None


class Email:
    def __init__(self, message: EmailMessage):
        self.msg = message
        self.path = None

    @property
    def attachments(self) -> list[Content]:
        return [
            Content(
                content_type=part.get_content_type(),
                data=part.get_payload(decode=True),
                filename=Path(part.get_filename()),
            )
            for part in self.msg.walk()
            if part.get_content_disposition() == "attachment"
        ]

    @property
    def date(self):
        return parsedate_to_datetime(self.msg["Date"])

    @property
    def html(self) -> Content:
        return next(
            Content(
                content_type=part.get_content_type(),
                data=part.get_payload(decode=True),
            )
            for part in self.msg.walk()
            if part.get_content_type() == "text/html"
        )

    @property
    def sender(self) -> str:
        return self.msg["From"]

    @property
    def subject(self) -> str:
        return self.msg["Subject"]
