from datetime import datetime
from pathlib import Path

from mailingester.models import Email
from mailingester.extractors import MalawiExtractor
from tests.factories import Attachment, create_message


def test_extract():
    ex = MalawiExtractor(allowed=[], path_prefix="mw")
    content = bytes("Content", "utf-8")
    attachments = [
        Attachment(
            content=content,
            filename="WEATHER FORECAST FOR TONIGHT AND TOMORROW 11TH JUNE, 2024.pdf",
        ),
        Attachment(
            content=content,
            filename="Morning weather bulletin issued on 10th June, 2024.pdf",
        ),
        Attachment(
            content=content,
            filename="Evening Weather Bulletin issued on 10TH_June, 2024.pdf",
        ),
    ]
    email = Email(create_message(attachments=attachments, dt=datetime(2024, 6, 10)))

    items = ex.extract(email)

    assert len(items) == 3
    assert items[0].filename == Path(
        "mw/20240610/weather-forecast-for-tonight-and-tomorrow-11th-june-2024.pdf"
    )
    assert items[1].filename == Path(
        "mw/20240610/morning-weather-bulletin-issued-on-10th-june-2024.pdf"
    )
    assert items[2].filename == Path(
        "mw/20240610/evening-weather-bulletin-issued-on-10th-june-2024.pdf"
    )
    assert all(i.data == "Content".encode("utf-8") for i in items)
