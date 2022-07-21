from pathlib import Path
from queue import Queue
from threading import Thread
from time import sleep
from typing import Dict, List

from communicator.streams.canbus import StablCanBus
from communicator.streams.datasource import Datasource, StablDatasource
from communicator.streams.modbus import StablModbus
from communicator.streams.uart_over_can import StablUartOverCan


class NoSources(Exception):
    pass


class RequiredDeviceNotAvailable(Exception):
    pass


class Collector(Thread):
    def __init__(self, logfile: Path, canbus: bool, modbus: bool, uoc: bool) -> None:
        super().__init__()
        self._logfile = logfile
        self._global_buffer: list = []
        self._sources = self._get_sources(canbus, modbus, uoc)
        self._running = False

    @staticmethod
    def _get_sources(
        require_canbus: bool, require_modbus: bool, require_uoc: bool
    ) -> Dict[Datasource, StablDatasource]:
        sources = {}
        try:
            sources[Datasource.Modbus] = StablModbus()
        except Exception as e:
            print(f"Modbus not available: {e}")
            if require_modbus:
                raise RequiredDeviceNotAvailable("modbus")
        try:
            sources[Datasource.Canbus] = StablCanBus()
        except Exception as e:
            print(f"Can Capture not available: {e}")
            if require_canbus:
                raise RequiredDeviceNotAvailable("canbus")
        try:
            sources[Datasource.UoC] = StablUartOverCan()
        except Exception as e:
            print(f"UoC Capture not available: {e}")
            if require_uoc:
                raise RequiredDeviceNotAvailable("uoc")
        if not sources:
            raise NoSources
        return sources

    def send_modbus_command(self, command: str) -> None:
        if Datasource.Modbus in self._sources.keys():
            modbus: StablModbus = self._sources[Datasource.Modbus]  # type: ignore
            modbus.send_command(command)

    def run(self) -> None:
        for source in self._sources.values():
            source.start()
        self._running = True
        while self._running:
            for source in self._sources.values():
                if source.new_msg:
                    new_msg = source.get_new_message()
                    self._global_buffer.append(new_msg)
                    self.log_message(str(new_msg))
                    print(new_msg)
            sleep(0.01)

    def log_message(self, message: str) -> None:
        with open(self._logfile, "a") as logfile:
            logfile.write(message.strip() + "\n")

    def terminate(self) -> None:
        self._running = False
        for source in self._sources.values():
            source.terminate()



class Visualisation:
    ...