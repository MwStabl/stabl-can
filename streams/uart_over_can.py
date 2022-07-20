from serial import Serial
from yaml import safe_load

from streams.datasource import StablDatasource


def get_config() -> dict:
    with open("config.yaml", "r") as yf:
        return safe_load(yf)["stream"]["uart_over_can"]


class StablUartOverCan(StablDatasource):
    def __init__(self) -> None:
        super().__init__()
        self._config = get_config()
        self._serial = self._create_serial()
        self._running = False

    def _create_serial(self) -> Serial:
        return Serial(
            baudrate=self._config.get("baudrate", 38400), port=self._config.get("serial_device", "/dev/ttyUOC")
        )

    def run(self) -> None:
        self._running = True
        while self._running:
            try:
                self._buffer.put(self._serial.read_until().decode().strip())
            except TypeError as e:
                pass

    def terminate(self) -> None:
        self._running = False
