from pathlib import Path
from typing import Dict, List

from loguru import logger

from sona.core.messages import Context, File, Job, Result
from sona.inferencers import InferencerBase
from sona.settings import settings


class MockInferencer(InferencerBase):
    inferencer = "mock"

    def on_load(self) -> None:
        logger.info(f"Download {self.__class__.__name__} models...")

    def inference(self, params: Dict, files: List[File]) -> Result:
        logger.info(f"Get params {params}")
        logger.info(f"Get files {files}")
        filepath = "output.wav"
        Path(filepath).touch(exist_ok=True)
        return Result(
            files=[File(label="output", path=filepath)],
            data={"output_key": "output_val"},
        )

    def context_example(self) -> Context:
        storage = settings.SONA_STORAGE_LOCAL_ROOT
        filepath1 = f"{storage}/input1.wav"
        filepath2 = f"{storage}/input2.wav"
        Path(storage).mkdir(exist_ok=True, parents=True)
        Path(filepath1).touch(exist_ok=True)
        Path(filepath2).touch(exist_ok=True)

        return Context(
            jobs=[
                Job(
                    name="input1",
                    topic=self.get_topic(),
                    params={"input1_key": "input1_val"},
                    files=[
                        File(
                            label="input1",
                            path=filepath1,
                        )
                    ],
                    required_result_params={
                        "input2_key": "input2__input2_key1__input2_key2"
                    },
                    required_result_files={"input2": "input2__input2_r"},
                )
            ],
            results={
                "input2": Result(
                    files=[
                        File(
                            label="input2_r",
                            path=filepath2,
                        )
                    ],
                    data={"input2_key1": {"input2_key2": "input2_val"}},
                )
            },
        )
