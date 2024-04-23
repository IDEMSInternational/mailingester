from email.message import EmailMessage

from mailingester.models import Email
from tests.factories import create_message


def test_alternative_text_html():
    msg = create_message()
    email = Email(msg)

    assert email.sender == "Example <user@example.com>"
    assert email.subject == "Subject"
    assert "Body HTML" in str(email.html.data, "utf-8")
    assert str(email.attachments[0].data, "utf-8") == "Attachment content"
