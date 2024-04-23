from pathlib import Path

import pytest
from mailingester.extractors import text_to_path
from mailingester.models import Config


def test_tokenize_words():
    config = Config(template="/opt/{0}/{1}/{2}.html")
    text = "One two THREE"

    assert text_to_path(config, text) == Path("/opt/one/two/three.html")


def test_reformat_date():
    config = Config(
        template="example/{date}.html",
        date_template="{0}/{1}/{2}",
        date_format_in="%Y/%m/%d",
        date_format_out="%Y%m%d",
    )
    text = "2024-04-13"

    assert text_to_path(config, text) == Path("example/20240413.html")


def test_no_subject_no_path():
    config = Config(template="{0}")
    text = ""

    with pytest.raises(Exception):
        text_to_path(config, text)


def test_invalid_date_no_path():
    config = Config(
        template="{date}",
        date_template="{1}/{2}/{3}",
        date_format_in="%d/%m/%Y",
        date_format_out="%Y_%m_%d",
    )
    text = "Subject 04/13/2024"

    with pytest.raises(Exception):
        text_to_path(config, text)


def test_too_few_tokens_no_path():
    config = Config(template="{0}/{1}/{2}.html")
    text = "Subject"

    with pytest.raises(Exception):
        text_to_path(config, text)
