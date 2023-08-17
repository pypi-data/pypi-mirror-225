# Dwave SONA Core

迪威智能 SONA 服務專用核心開發套件

## 安裝與使用

### 開發環境需求

- Python 3.8 或更新版本
- poetry

### 安裝與使用

1. 環境建構

```sh
$ pip install poetry
```

2. 下載與安裝

```sh
$ export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
$ poetry add git+ssh://git@github.com/DeepWaveInc/dwave-sona-core.git
```

3. 撰寫 Inferencer 模組

```python
# example/basic.py
from pathlib import Path
from typing import Dict, List

from loguru import logger
from sona.core.messages import Context, File, Job, Result
from sona.inferencers import InferencerBas


class BasicExample(InferencerBase):
    inferencer = "basic"  # Inferencer 名稱

    def on_load(self) -> None:
        """
        載入函式，Worker 啟動時呼叫
        """
        logger.info(f"Download {self.__class__.__name__} models...")

    def inference(self, params: Dict, files: List[File]) -> Result:
        """
        訊息處理函式，Worker 接受到新訊息後呼叫
        :param params: 處理參數
        :param files: 處理檔案
        :return: 處理結果
        """
        logger.info(f"Get params {params}")
        logger.info(f"Get files {files}")

        filname = "output.wav"
        Path(filname).touch(exist_ok=True)
        return Result(
            files=[File(label="output", path=filname)],
            data={"data_key": "data_val"},
        )

    def context_example(self) -> Context:
        """
        範例訊息，供 Worker 測試及 API 開發時參考使用
        :return: 範例訊息
        """
        filname = "input.wav"
        Path(filname).touch(exist_ok=True)

        params = {"param_key": "param_val"}
        files = [File(label="input", path=filname)]
        return Context(
            jobs=[
                Job(
                    name="basic_job",
                    topic=self.get_topic(),
                    params=params,
                    files=files,
                )
            ]
        )

```

4. Worker 測試

```sh
$ poetry run python -m sona inferencer test inferencer.basic.BasicExample
2023-03-22 02:52:27.392 | INFO     | sona.workers.inferencer:on_load:33 - Loading inferencer: basic
2023-03-22 02:52:27.392 | INFO     | inferencer.basic:on_load:13 - Download BasicExample models...
2023-03-22 02:52:27.392 | INFO     | sona.workers.inferencer:on_load:36 - Susbcribe on sona.worker.inferencer.basic(MockConsumer)
2023-03-22 02:52:27.392 | INFO     | sona.workers.inferencer:on_context:42 - [sona.worker.inferencer.basic] recv: {"id": "5fe59e8bcd4b4efb84462cdbcad4a3b4", "header": {}, "jobs": [{"name": "basic_job", "topic": "sona.worker.inferencer.basic", "params": {"param_key": "param_val"}, "files": [{"label": "input", "path": "input.wav"}], "extra_params": {}, "extra_files": {}}], "fallbacks": [], "results": {}, "states": []}
2023-03-22 02:52:27.392 | INFO     | inferencer.basic:inference:16 - Get params {'param_key': 'param_val'}
2023-03-22 02:52:27.392 | INFO     | inferencer.basic:inference:17 - Get files [File(label='input', path='input.wav')]
2023-03-22 02:52:27.393 | INFO     | sona.workers.inferencer:on_context:59 - [sona.worker.inferencer.basic] success: {"id": "5fe59e8bcd4b4efb84462cdbcad4a3b4", "header": {}, "jobs": [{"name": "basic_job", "topic": "sona.worker.inferencer.basic", "params": {"param_key": "param_val"}, "files": [{"label": "input", "path": "input.wav"}], "extra_params": {}, "extra_files": {}}], "fallbacks": [], "results": {"basic_job": {"files": [{"label": "output", "path": "output.wav"}], "data": {"data_key": "data_val"}}}, "states": [{"job_name": "basic_job", "exec_time": 0.00029676100000000015, "exception": {}}]}
```
