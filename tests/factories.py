from collections import namedtuple
from datetime import datetime

from email.message import EmailMessage
from email.utils import format_datetime

Attachment = namedtuple("Attachment", ["content", "filename"])


def create_message(
    attachments: list[Attachment] = [],
    dt=None,
    subject: str = "Subject",
) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = "Example <user@example.com>"
    msg["Subject"] = subject
    msg["Date"] = format_datetime(dt or datetime.now())
    msg.set_content("Body text")
    msg.add_alternative(
        "<p>Body HTML</p>\n\n-- <br />\nYou received this message because",
        subtype="html",
    )

    if not attachments:
        attachments = [
            Attachment(
                content=bytes("Attachment content", "utf-8"),
                filename="example.txt",
            )
        ]

    for attachment in attachments:
        msg.add_attachment(
            attachment.content,
            maintype="application",
            subtype="octet-stream",
            filename=attachment.filename,
        )

    return msg
