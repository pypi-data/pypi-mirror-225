from pathlib import Path
from typing import List

from sona.core.messages.file import File


class ShareStorageBase:
    def __init__(self):
        self.cached_path = []

    def pull_all(self, files: List[File]) -> List[File]:
        return [self.pull(file) for file in files]

    def pull(self, file: File) -> File:
        if Path(file.path).is_file():
            return file
        if not self.is_valid(file.path):
            raise Exception("Invalid share storage path")
        path = self.on_pull(file.path)
        self.cached_path.append(path)
        return file.mutate(path=path)

    def push_all(self, files: List[File]) -> List[File]:
        return [self.push(file) for file in files]

    def push(self, file: File) -> File:
        if self.is_valid(file.path):
            return file
        if not Path(file.path).is_file():
            raise Exception(f"Missing file: {file}")
        self.cached_path.append(file.path)
        return file.mutate(path=self.on_push(file.path))

    def clean(self) -> None:
        for path in self.cached_path:
            file_path = Path(path)
            if file_path.exists():
                file_path.unlink()

    def create_storage(self):
        return self.__class__()

    # Callbacks
    def is_valid(self, path) -> bool:
        return NotImplemented

    def on_pull(self, path) -> str:
        return NotImplemented

    def on_push(self, path) -> str:
        return NotImplemented
