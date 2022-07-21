import logging
from typing import Optional

import can

from communicator.decode.msgdecoder import StablCanMsg
from communicator.streams.datasource import Datasource, GenericMessage, StablDatasource

LOG = logging.getLogger(__name__)


def print_setupinfo() -> None:
    print("CAN Bus cannot be initialised. Check the following requirements")
    print("1. Is the PEAK Can connected? Does the red light blink?")
    print(
        "2. Check wheter pcan is initialised with 'lsmod | grep ^peak'. If not, run 'modprobe peak_usb' and check again"
    )
    print("3. Initialise the CAN: 'ip link set can0 up type can bitrate 500000'")


class StablCanBus(StablDatasource):
    def __init__(self):
        LOG.debug("init can")
        super().__init__()
        self._can = can.interface.Bus(bustype="socketcan", channel=self._channel(), bitrate=self._bitrate())
        self._running: bool = False

    @property
    def bus(self):
        return self._can

    def _channel(self) -> str:
        """stub for a function that identifies peakcan"""
        return "can0"

    def _bitrate(self) -> int:
        """stub for a function that reads the selected bitrate from c code or some config structure"""
        return 500000

    def terminate(self) -> None:
        self._running = False
        self._can.shutdown()

    def run(self) -> None:
        self._running = True
        while self._running:
            msg = self.get_received_message()
            if msg is not None:
                self._buffer.put(msg)
        print("Closing CAN Bus")

    def get_received_message(self) -> Optional[GenericMessage]:
        try:
            msg = self._can.recv(1)
            if msg is not None:
                canmsg = StablCanMsg(msg)
                return GenericMessage(
                    content=canmsg.__repr__(), classification=canmsg.type, datasource=Datasource.Canbus
                )
        except can.CanOperationError as e:
            print(f"CAN: Error catched: {e}")
            return None
