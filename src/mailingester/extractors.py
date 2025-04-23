from pathlib import Path

from slugify import slugify

from mailingester.models import Content, Email


class Extractor:

    def __init__(self, allowed: list[str], path_prefix: str = ""):
        self.allowed_addresses = allowed
        self.path_prefix = Path(path_prefix)

    def can_extract(self, email: Email) -> bool:
        return any(address in email.sender for address in self.allowed_addresses)


    def extract_meta(self, email: Email) -> dict:
        return {
            "sender": email.sender,
            "subject": email.subject,
        }


class ZambiaExtractor(Extractor):
    FOOTER_START = "-- <br />\nYou received this message"

    def extract(self, email: Email) -> list[Content]:
        html = email.html

        if html:
            html.filename = (
                self.path_prefix
                / email.date.strftime("%Y%m%d")
                / slugify(email.subject)
            ).with_suffix(".html")
            html.data = bytes(
                strip_footer(
                    self.FOOTER_START,
                    convert_line_endings(str(html.data, "utf-8")),
                ),
                "utf-8",
            )
            html.meta = self.extract_meta(email)

        return [html]


class MalawiExtractor(Extractor):

    def extract(self, email: Email) -> list[Content]:
        meta = self.extract_meta(email)
        items = []

        for item in email.attachments:
            item.filename = (
                self.path_prefix
                / email.date.strftime("%Y%m%d")
                / item.filename.with_stem(slugify(item.filename.stem))
            )
            item.meta = meta
            items.append(item)

        return items


def convert_line_endings(text: str):
    return text.replace("\r\n", "\n")


def strip_footer(start: str, text: str):
    try:
        i = text.index(start)
        return text[:i]
    except Exception:
        return text
