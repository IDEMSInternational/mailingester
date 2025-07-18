import json
import os
from datetime import datetime
from mailbox import Maildir
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from google.cloud import storage
from mailingester.extractors import ZambiaExtractor
from mailingester.handlers import MailServer
from mailingester.storage import GoogleCloudStorage, LocalFileSystem

from tests.factories import create_message

bucket_name = os.getenv("MAILINGESTER_TEST_BUCKET_NAME")


def test_handle_message():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        handler = MailServer(
            root,
            LocalFileSystem(root),
            [
                ZambiaExtractor(
                    allowed=["Example <user@example.com>"],
                    path_prefix="zm",
                )
            ],
        )
        msg = create_message(dt=datetime(2024, 7, 29), subject="subject")

        handler.handle_message(msg)

        assert (root / "zm/20240729/subject.html").exists()
        assert (root / "zm/20240729/subject.html.meta.json").exists()
        with open(root / "zm/20240729/subject.html.meta.json", "r") as f:
            assert json.load(f) == {
                "sender": "Example <user@example.com>",
                "subject": "subject",
            }
        assert len(list((root / "archive").iterdir())) == 1
        assert not Maildir(root / "Maildir").items()


def test_incoming_message_always_saved():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        handler = MailServer(root, None, [])

        handler.handle_message(create_message())

        assert not (root / "archive").exists()
        assert len(Maildir(root / "Maildir").items()) == 1


@pytest.mark.skipif(not bucket_name, reason="Test bucket name not set")
def test_google_storage():
    bucket = storage.Client().bucket(bucket_name)
    bucket.delete_blobs(list(bucket.list_blobs()))

    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        handler = MailServer(
            root,
            GoogleCloudStorage(bucket_name),
            [ZambiaExtractor(["Example <user@example.com>"])],
        )
        msg = create_message(subject="zero one two three four 14/04/2024")

        handler.handle_message(msg)

        assert not Maildir(root / "Maildir").items()

    names = sorted([b.name for b in bucket.list_blobs()])
    assert len(names) == 2
    assert names[1].startswith("archive/")

    today = datetime.now().strftime("%Y%m%d")
    assert names[0] == f"{today}/zero-one-two-three-four-14-04-2024.html"
    assert bucket.get_blob(names[0]).metadata == {
        "sender": "Example <user@example.com>",
        "subject": "zero one two three four 14/04/2024",
    }
