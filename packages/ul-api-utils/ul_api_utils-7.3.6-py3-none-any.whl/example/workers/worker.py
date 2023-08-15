from unipipeline.message.uni_message import UniMessage
from unipipeline.worker.uni_worker import UniWorker
from unipipeline.worker.uni_worker_consumer_message import UniWorkerConsumerMessage

from ul_api_utils.modules.worker_context import WorkerContext
from ul_api_utils.modules.worker_sdk import WorkerSdk
from ul_api_utils.modules.worker_sdk_config import WorkerSdkConfig

initialized_worker = WorkerSdk(WorkerSdkConfig())


class Msg(UniMessage):
    pass


class HttpNbfiParserWorker(UniWorker[Msg, None]):

    @initialized_worker.handle_message()  # type: ignore
    def handle_message(self, ctx: WorkerContext, message: UniWorkerConsumerMessage[Msg]) -> None:
        pass
