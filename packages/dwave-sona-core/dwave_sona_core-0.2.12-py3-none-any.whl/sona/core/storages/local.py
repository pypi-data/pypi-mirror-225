import hashlib
import os
import shutil
from pathlib import Path

from sona.core.storages.base import ShareStorageBase
from sona.settings import settings


class LocalStorage(ShareStorageBase):
    def __init__(self,
                 local_root=settings.SONA_STORAGE_LOCAL_ROOT,
                 storage_dir=settings.SONA_STORAGE_DIR):
        super().__init__()
        self.local_root = local_root
        self.storage_dir = storage_dir

    def is_valid(self, path: str) -> bool:
        return path.startswith(self.local_root)

    def on_pull(self, path: str) -> str:
        tmp_path = os.path.relpath(path, self.local_root)
        Path(tmp_path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "rb") as f_in, open(tmp_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        return str(tmp_path)

    def on_push(self, path: str) -> str:
        md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        filename = f"{md5.hexdigest()}{''.join(Path(path).suffixes)}"
        local_path = Path(self.local_root) / self.storage_dir / filename
        local_path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "rb") as f_in, open(local_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        return str(local_path)
