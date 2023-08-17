import asyncio

import typer
from loguru import logger

from sona.core.consumers import create_consumer
from sona.core.messages.context import Context
from sona.core.producers import MockProducer, create_producer
from sona.core.storages import LocalStorage, ShareStorageBase, create_storage
from sona.inferencers import InferencerBase
from sona.settings import settings
from sona.workers import *

worker_app = typer.Typer()
inference_app = typer.Typer()


@worker_app.command()
def run(
    inferencer: str = settings.SONA_INFERENCER,
    worker: str = settings.SONA_WORKER,
):
    try:
        worker_cls = WorkerBase.load_class(worker)
        if worker_cls == InferencerWorker:
            worker: WorkerBase = worker_cls(InferencerBase.load_class(inferencer)())
        else:
            worker: WorkerBase = worker_cls()
        worker.set_storage(create_storage())
        worker.set_producer(create_producer())
        worker.set_consumer(create_consumer())
        asyncio.run(worker.start())
    except Exception as e:
        logger.exception(e)


@worker_app.command("test")
def worker_test(worker_class: str, file: str = None):
    worker: WorkerBase = WorkerBase.load_class(worker_class)()
    _test(worker, file)


@inference_app.command("test")
def inferencer_test(inferencer_class: str, file: str = None):
    worker: WorkerBase = InferencerWorker(InferencerBase.load_class(inferencer_class)())
    _test(worker, file)


def _test(worker: WorkerBase, file: str):
    storage: ShareStorageBase = LocalStorage()
    if file:
        context: Context = Context.parse_file(file)
    else:
        context: Context = worker.context_example()
    worker.set_storage(storage)
    worker.set_producer(MockProducer())
    asyncio.run(worker.test(context))


app = typer.Typer()
app.add_typer(worker_app, name="worker")
app.add_typer(inference_app, name="inferencer")
