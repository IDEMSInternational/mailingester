import json
from pathlib import Path

from google.cloud import storage

from mailingester.models import Content


class LocalFileSystem:

    def __init__(self, root: Path):
        self.root = root

    def save(self, item: Content) -> None:
        path = self.root / item.filename
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "wb") as f:
            f.write(item.data)

        if item.meta:
            with open(path.with_name(path.name + ".meta.json"), "w") as f:
                json.dump(item.meta, f, indent=2)


class GoogleCloudStorage:

    def __init__(self, bucket: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket)

    def save(self, item: Content):
        blob = self.bucket.blob(str(item.filename))
        blob.metadata = item.meta
        blob.upload_from_string(item.data, item.content_type)
