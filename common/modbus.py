from queue import Queue
from threading import Thread

from serial import Serial


class Modbus(Thread):
    def __init__(self) -> None:
        super().__init__()
        self._running = False
        self._bus = self._create_bus()
        self._buffer: Queue = Queue()
        self._new_msg: bool = False

    def _create_bus(self) -> Serial:
        return Serial(baudrate=38400, port="/dev/ttyACM0")

    @property
    def new_msg(self) -> bool:
        return self._buffer.not_empty

    def get_new_message(self) -> str:
        return self._buffer.get()

    def terminate(self) -> None:
        self._bus.close()
        self._running = False

    def run(self) -> None:
        self._running = True
        while self._running:
            try:
                self._buffer.put(self._bus.read_until().decode().strip())
            except TypeError as e:
                print(f"Modbus: Error catched: {e}")
        print("Closing Modbus")
