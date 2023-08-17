import datetime
import hashlib
import re
from pathlib import Path

import boto3
from botocore.client import Config

from sona.core.storages.base import ShareStorageBase
from sona.settings import settings


class S3Storage(ShareStorageBase):
    def __init__(
        self,
        root_dir=settings.SONA_STORAGE_DIR,
        bucket=settings.SONA_STORAGE_S3_BUCKET,
        configs=settings.SONA_STORAGE_S3_SETTING,
    ):
        super().__init__()
        self.root_dir = root_dir
        self.bucket = bucket
        self.configs = configs

    @property
    def client(self):
        configs = self.configs or {}
        configs.update({"config": Config(signature_version="s3v4")})
        return boto3.resource("s3", **configs).meta.client

    def is_valid(self, path: str) -> bool:
        return re.match(r"^[Ss]3://.*", path)

    def on_pull(self, path: str) -> str:
        match = re.match(r"[Ss]3://([-_A-Za-z0-9]+)/(.+)", path)
        bucket = match.group(1)
        obj_key = match.group(2)
        filepath = Path(obj_key)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        self.client.download_file(bucket, obj_key, str(filepath))
        return str(filepath)

    def on_push(self, path: str) -> str:
        md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        obj_key = f"{md5.hexdigest()}{''.join(Path(path).suffixes)}"
        obj_key = (
            Path(self.root_dir) / datetime.date.today().strftime("%Y%m%d") / obj_key
        )
        self.client.upload_file(path, self.bucket, str(obj_key))
        return f"S3://{self.bucket}/{obj_key}"
