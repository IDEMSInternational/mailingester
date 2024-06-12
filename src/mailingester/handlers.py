import logging
import traceback
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from aiosmtpd.handlers import Mailbox
from pydantic import BaseModel, ImportString
from pydantic_core import from_json
from pydantic_settings import BaseSettings

from mailingester import version
from mailingester.models import Content, Email

logger = logging.getLogger(__name__)


class CallableConfig(BaseModel):
    name: ImportString
    args: dict[str, Any] = list()


class Settings(BaseSettings):
    mail_dir: Path = Path()
    storage: CallableConfig
    extractors: list[CallableConfig]


class MailServer(Mailbox):
    def __init__(self, root: Path, storage, extractors):
        root.mkdir(parents=True, exist_ok=True)
        super().__init__(root / "Maildir", EmailMessage)
        self.storage = storage
        self.extractors = extractors

    def handle_message(self, message: EmailMessage) -> None:
        key = self.mailbox.add(message)

        try:
            email = Email(message)
            extractor = self.find_extractor(email)

            for item in extractor.extract(email):
                self.storage.save(item)

            self.archive(key, message)
            self.mailbox.remove(key)
            logger.info(
                {
                    "msg": "Extraction succeeded",
                    "key": key,
                    "sender": email.sender,
                    "subject": email.subject,
                    "extractor": type(extractor),
                }
            )
        except Exception as ex:
            traceback.print_exc()
            logger.error({"msg": "Extraction failed", "key": key, "error": ex})

    def find_extractor(self, email: Email):
        return next(e for e in self.extractors if e.can_extract(email))

    def archive(self, key: str, message: EmailMessage) -> None:
        self.storage.save(
            Content(
                content_type="application/octet-stream",
                data=bytes(message),
                filename=Path("archive") / key,
            )
        )

    @classmethod
    def from_cli(cls, parser, *args):
        logging.basicConfig(
            datefmt="%Y-%m-%dT%H:%M:%S",
            format="%(asctime)s.%(msecs)03d %(levelname)s %(name)s %(message)s",
            level=logging.INFO,
        )
        config_file = args[0] if args else "config.json"
        logger.info({"msg": "Started", "version": version()})
        logger.info({"msg": "Config file identified", "path": config_file})

        with open(config_file, "r") as f:
            settings = Settings(**from_json(f.read()))

        logger.info({"msg": "Config file loaded", "settings": settings})

        return cls(
            settings.mail_dir,
            settings.storage.name(**settings.storage.args),
            [e.name(**e.args) for e in settings.extractors],
        )
