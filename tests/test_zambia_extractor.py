from datetime import datetime
from pathlib import Path

from mailingester.models import Email
from mailingester.extractors import ZambiaExtractor
from tests.factories import create_message


def test_extract():
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
