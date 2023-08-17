from __future__ import annotations

from typing import Dict, List

from loguru import logger

from sona.core.messages.result import Result
from sona.core.utils.dict_utils import find_value_from_nested_keys

from .base import MessageBase
from .file import File


class Job(MessageBase):
    name: str
    topic: str
    params: Dict = {}
    files: List[File] = []
    extra_params: Dict[str, str] = {}  # TODO: Deprecate in 1.0.0
    extra_files: Dict[str, str] = {}  # TODO: Deprecate in 1.0.0
    required_result_params: Dict[str, str] = {}
    required_result_files: Dict[str, str] = {}

    @property
    def required_params(self):
        if self.extra_params:
            logger.warning("extra_params will be deprecated in version 1.0.0")
        return {**self.extra_params, **self.required_result_params}

    @property
    def required_files(self):
        if self.extra_files:
            logger.warning("extra_files will be deprecated in version 1.0.0")
        return {**self.extra_files, **self.required_result_files}

    def prepare_params(self, results: Dict[str, Result]):
        params = {**self.params}
        for key, target in self.required_params.items():
            targets = target.split("__")
            job_name, keys = targets[0], targets[1:]
            params[key] = find_value_from_nested_keys(keys, results[job_name].data)
        return params

    def prepare_files(self, results: Dict[str, Result]):
        file_map = {file.label: file for file in self.files}
        for label, target in self.required_files.items():
            job, files_label = target.split("__")
            file = results[job].find_file(files_label).mutate(label=label)
            file_map[label] = file
        return list(file_map.values())
