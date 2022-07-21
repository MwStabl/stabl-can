from serial import Serial
from yaml import safe_load

from communicator.streams.datasource import Datasource, GenericMessage, MessageType, StablDatasource


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
            baudrate=self._config.get("baudrate", 38400),
            port=self._config.get("serial_device", "/dev/ttyUOC"),
            timeout=1,
        )

    def run(self) -> None:
        self._running = True
        while self._running:
            try:
                new_msg = self._serial.read_until().decode().strip()
                if new_msg:
                    self._buffer.put(
                        GenericMessage(content=new_msg, classification=MessageType.other, datasource=Datasource.UoC)
                    )
            except TypeError as e:
                pass

    def terminate(self) -> None:
        self._running = False
