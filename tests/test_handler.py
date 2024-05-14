from mailbox import Maildir
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from mailingester.extractors import ZambiaExtractor
from mailingester.handlers import MailServer
from mailingester.storage import GoogleCloudStorage, LocalFileSystem
from tests.factories import create_message


def test_handle_message():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        handler = MailServer(
            root,
            LocalFileSystem(root),
            [ZambiaExtractor(["Example <user@example.com>"])],
        )
        msg = create_message(subject="zero one two three four 14/04/2024")

        handler.handle_message(msg)

        assert (root / "html/zero/threes/2024_04_14.html").exists()
        assert (root / "attachments/zero/threes/2024_04_14/example.txt").exists()
        assert len(list((root / "archive").iterdir())) == 1
        assert not Maildir(root / "Maildir").items()


def test_incoming_message_always_saved():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        handler = MailServer(root, None, [])

        handler.handle_message(create_message())

        assert not (root / "archive").exists()
        assert len(Maildir(root / "Maildir").items()) == 1


@pytest.mark.skip()
def test_google_storage():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        handler = MailServer(
            root,
            GoogleCloudStorage(Path("test"), "zambia_pdf_forecasts"),
        )
        msg = create_message()

        handler.handle_message(msg)

        assert not Maildir(root / "Maildir").items()
