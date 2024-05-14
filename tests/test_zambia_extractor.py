from pathlib import Path

from mailingester.models import Email
from mailingester.extractors import ZambiaExtractor
from tests.factories import create_message


def test_can_extract_from_allowed_addresses():
    class MockEmail:
        def __init__(self, sender):
            self.sender = sender

    ex = ZambiaExtractor(["sender_1@example.com", "sender_2@example.com"])

    assert ex.can_extract(MockEmail("sender_1@example.com"))
    assert ex.can_extract(MockEmail("Example sender <sender_2@example.com>"))
    assert not ex.can_extract(MockEmail("Not allowed <sender_3@example.com>"))


def test_extract():
    ex = ZambiaExtractor([])
    email = Email(create_message(subject="zero one two three four 22/04/2024"))
    items = ex.extract(email)

    assert len(items) == 2
    assert items[0].filename == Path("html/zero/threes/2024_04_22.html")
    assert items[0].data == "<p>Body HTML</p>\n".encode("utf-8")
    assert items[1].filename == Path("attachments/zero/threes/2024_04_22/example.txt")
