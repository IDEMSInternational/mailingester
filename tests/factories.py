from email.message import EmailMessage


def create_message(subject: str = "Subject") -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = "Example <user@example.com>"
    msg["Subject"] = subject
    msg.set_content("Body text")
    msg.add_alternative(
        "<p>Body HTML</p>\n\n-- <br />\nFooter",
        subtype="html",
    )
    msg.add_attachment(
        bytes("Attachment content", "utf-8"),
        maintype="application",
        subtype="octet-stream",
        filename="example.txt",
    )

    return msg
