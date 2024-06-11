import re
from datetime import datetime
from pathlib import Path

from mailingester.models import Config, Content, Email


class Extractor:

    def __init__(self, allowed: list[str]):
        self.allowed_addresses = allowed

    def can_extract(self, email: Email) -> bool:
        return any(address in email.sender for address in self.allowed_addresses)


class ZambiaExtractor(Extractor):

    def extract(self, email: Email) -> list[Content]:
        items = []
        config = Config(
            template="{0}/{3}s/{date}",
            date_template="{5}/{6}/{7}",
            date_format_in="%d/%m/%Y",
            date_format_out="%Y_%m_%d",
            footer_start="-- <br />\nYou received this message",
        )
        path = text_to_path(config, email.subject)
        html = email.html

        if html:
            html.filename = "html" / path.with_suffix(".html")
            html.data = bytes(
                strip_footer(
                    config.footer_start,
                    convert_line_endings(str(html.data, "utf-8")),
                ),
                "utf-8",
            )
            items.append(html)

        for item in email.attachments:
            item.filename = "attachments" / path / item.filename
            items.append(item)

        return items


class MalawiExtractor(Extractor):

    def extract(self, email: Email) -> list[Content]:
        items = []

        for item in email.attachments:
            path = email.date.strftime("%Y_%m_%d")
            filename = self.translate_filename(str(item.filename))

            item.filename = Path("attachments") / path / filename
            items.append(item)

        return items

    def translate_filename(self, filename: str):
        translation_map = {
            "forecast": "forecast",
            "morning": "bulletin_morning",
            "evening": "bulletin_evening",
        }
        lower = filename.lower()

        for key, stem in translation_map.items():
            if key in lower:
                return stem + ".pdf"

        raise Exception("Filename translation failed")


def text_to_path(config: Config, text: str) -> Path:
    tokens = [t.lower() for t in re.findall(config.regex, text) if t]

    if not tokens:
        raise Exception(
            {
                "msg": "No tokens produced",
                "subject": text,
                "regex": config.regex,
            }
        )

    date = datetime.strptime(
        config.date_template.format(*tokens),
        config.date_format_in,
    ).strftime(config.date_format_out)

    return Path(config.template.format(*tokens, date=date))


def convert_line_endings(text: str):
    return text.replace("\r\n", "\n")


def strip_footer(start: str, text: str):
    try:
        i = text.index(start)
        return text[:i]
    except Exception:
        return text
