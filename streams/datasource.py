from enum import Enum
from queue import Queue
from threading import Thread


class Datasource(Enum):
    Canbus = "canbus"
    Modbus = "modbus"
    UoC = "uoc"


class StablDatasource(Thread):
    def __init__(self) -> None:
        super().__init__()
        self._buffer: Queue = Queue()

    def terminate(self) -> None:
        raise NotImplementedError

    @property
    def new_msg(self) -> bool:
        return not self._buffer.empty()

    def get_new_message(self):  # type: ignore
        return self._buffer.get()

    def run(self) -> None:
        raise NotImplementedError
