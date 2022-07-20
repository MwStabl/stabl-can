from queue import Queue
from threading import Thread
from time import sleep
from typing import Dict, List

from streams.canbus import StablCanBus
from streams.datasource import Datasource, StablDatasource
from streams.modbus import StablModbus
from streams.uart_over_can import StablUartOverCan


class NoSources(Exception):
    pass


class Collector(Thread):
    def __init__(self) -> None:
        super().__init__()
        self._global_buffer = []
        self._sources = self._get_sources()
        self._running = False

    def _get_sources(self) -> Dict[Datasource, StablDatasource]:
        sources = {}
        try:
            sources[Datasource.Modbus] = StablModbus()
        except Exception as e:
            print(f"Modbus not available: {e}")
        try:
            sources[Datasource.Canbus] = StablCanBus()
        except Exception as e:
            print(f"Can Capture not available: {e}")
        try:
            sources[Datasource.UoC] = StablUartOverCan()
        except Exception as e:
            print(f"UoC Capture not available: {e}")
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
                    print(new_msg)
            sleep(0.01)

    def terminate(self) -> None:
        self._running = False
        for source in self._sources.values():
            source.terminate()
