from dataclasses import dataclass
from enum import Enum
from queue import Queue
from threading import Thread


class Datasource(Enum):
    Canbus = "can"
    Modbus = "mod"
    UoC = "uoc"


class MessageType(Enum):
    healthcare = "healthcare"
    heartbeat = "heartbeat"
    logging = "logging"
    other = "other"


@dataclass
class GenericMessage:
    content: str
    classification: MessageType
    datasource: Datasource


class StablDatasource(Thread):
    def __init__(self) -> None:
        super().__init__()
        self._buffer: Queue = Queue()

    def terminate(self) -> None:
        raise NotImplementedError

    @property
    def new_msg(self) -> bool:
        return not self._buffer.empty()

    def get_new_message(self) -> GenericMessage:
        return self._buffer.get()

    def run(self) -> None:
        raise NotImplementedError
