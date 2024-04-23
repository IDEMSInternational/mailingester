import re
from datetime import datetime
from pathlib import Path

from mailingester.models import Config, Content, Email


class ZambiaExtractor:
    def __init__(self, allowed: list[str]):
        self.allowed_addresses = allowed

    def can_extract(self, email: Email) -> bool:
        return any(address in email.sender for address in self.allowed_addresses)

    def extract(self, email: Email) -> list[Content]:
        items = []
        config = Config(
            template="{0}/{3}s/{date}",
            date_template="{5}/{6}/{7}",
            date_format_in="%d/%m/%Y",
            date_format_out="%Y_%m_%d",
        )
        path = text_to_path(config, email.subject)
        html: Content = email.html

        if html:
            html.filename = "html" / path.with_suffix(".html")
            items.append(html)

        for item in email.attachments:
            item.filename = "attachments" / path / item.filename
            items.append(item)

        return items


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
