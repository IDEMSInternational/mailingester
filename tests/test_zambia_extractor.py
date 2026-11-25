from datetime import datetime
from pathlib import Path

from mailingester.models import Email
from mailingester.extractors import ZambiaExtractor
from tests.factories import Attachment, create_message


def test_extract_html_when_no_attachments():
    ex = ZambiaExtractor(allowed=[], path_prefix="zm")
    email = Email(
        create_message(
            dt=datetime(2024, 7, 29),
            subject="ZAMBIA EVENING WEATHER FORECAST: MONDAY (29/06/2024)",
        )
    )

    items = ex.extract(email)

    assert len(items) == 1
    assert items[0].filename == Path(
        "zm/20240729/zambia-evening-weather-forecast-monday-29-06-2024.html"
    )
    assert items[0].data == "<p>Body HTML</p>\n\n".encode("utf-8")
    assert items[0].meta == {
        "sender": "Example <user@example.com>",
        "subject": "ZAMBIA EVENING WEATHER FORECAST: MONDAY (29/06/2024)",
    }


def test_extract_pdf_attachments_only():
    ex = ZambiaExtractor(allowed=[], path_prefix="zm")
    email = Email(
        create_message(
            attachments=[
                Attachment(
                    content=bytes("Content", "utf-8"),
                    filename="Weekly Weather bulletin - 03 to 9th November, 2026.pdf",
                    content_type="application/pdf",
                ),
                Attachment(
                    content=bytes("Ignored content", "utf-8"),
                    filename="ignored.docx",
                ),
                Attachment(
                    content=bytes("Extra PDF", "utf-8"),
                    filename="extra.pdf",
                ),
            ],
            dt=datetime(2026, 11, 25),
        )
    )

    items = ex.extract(email)

    assert len(items) == 2
    assert items[0].filename == Path(
        "zm/20261125/weekly-weather-bulletin-03-to-9th-november-2026.pdf"
    )
    assert items[0].data == "Content".encode("utf-8")
    assert items[1].filename == Path("zm/20261125/extra.pdf")
    assert items[1].data == "Extra PDF".encode("utf-8")
