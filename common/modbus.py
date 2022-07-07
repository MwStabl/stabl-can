from serial import Serial


class Modbus:
    def __init__(self):
        self._bus = self._create_bus()

    def _create_bus(self) -> Serial:
        return Serial(
            baudrate=38400,
            port='/dev/ttyACM0'
        )

    def cleanup(self):
        self._bus.close()

    def get_received_message(self) -> str:
        return self._bus.read_until().decode().strip()
