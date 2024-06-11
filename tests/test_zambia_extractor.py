from pathlib import Path

from mailingester.models import Email
from mailingester.extractors import ZambiaExtractor
from tests.factories import create_message


def test_extract():
    ex = ZambiaExtractor([])
    email = Email(create_message(subject="zero one two three four 22/04/2024"))
    items = ex.extract(email)

    assert len(items) == 2
    assert items[0].filename == Path("html/zero/threes/2024_04_22.html")
    assert items[0].data == "<p>Body HTML</p>\n\n".encode("utf-8")
    assert items[1].filename == Path("attachments/zero/threes/2024_04_22/example.txt")
