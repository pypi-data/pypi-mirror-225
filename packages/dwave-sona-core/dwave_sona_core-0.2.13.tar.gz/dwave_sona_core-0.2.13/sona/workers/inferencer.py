import asyncio

from loguru import logger

from sona.core.messages import Context, Job, State
from sona.inferencers import InferencerBase
from sona.settings import settings

from .base import WorkerBase

TOPIC_PREFIX = settings.SONA_INFERENCER_TOPIC_PREFIX
INFERENCER_CLASS = settings.SONA_INFERENCER


class InferencerWorker(WorkerBase):
    def __init__(self, inferencer: InferencerBase):
        super().__init__()
        self.inferencer = inferencer

    async def on_load(self):
        logger.info(f"Loading inferencer: {self.inferencer.inferencer}")
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.inferencer.on_load)

    async def on_context(self, context: Context):
        try:
            logger.info(f"[{self.topic}] recv: {context.to_message()}")

            # Prepare process data
            current_job: Job = context.current_job
            current_state: State = State.start(current_job.name)
            params = current_job.prepare_params(context.results)
            files = current_job.prepare_files(context.results)
            files = self.storage.pull_all(files)

            # Process
            # TODO: Make process cancelable
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None, self.inferencer.inference, params, files
            )
            result = result.mutate(files=self.storage.push_all(result.files))

            # Create success context
            current_state = current_state.complete()
            next_context = context.next_context(current_state, result)
            logger.info(f"[{self.topic}] success: {next_context.to_message()}")

            # Emit message
            next_job = next_context.current_job
            if next_job:
                self.producer.emit(next_job.topic, next_context.to_message())
            else:
                for topic in next_context.reporters:
                    self.producer.emit(topic, next_context.to_message())
            return next_context

        except Exception as e:
            # Create fail context
            current_state = current_state.fail(e)
            next_context = context.next_context(current_state)
            logger.exception(f"[{self.topic}] error: {next_context.to_message()}")

            # Emit message
            for topic in next_context.fallbacks:
                self.producer.emit(topic, next_context.to_message())
            return next_context

    def context_example(self):
        return self.inferencer.context_example()

    def get_topic(self):
        return self.inferencer.get_topic()
