from datetime import datetime
from queue import Queue
from threading import Thread
from typing import Optional

import can

from common.codebook import Devices


def print_setupinfo() -> None:
    print("CAN Bus cannot be initialised. Check the following requirements")
    print("1. Is the PEAK Can connected? Does the red light blink?")
    print(
        "2. Check wheter pcan is initialised with 'lsmod | grep ^peak'. If not, run 'modprobe peak_usb' and check again"
    )
    print("3. Initialise the CAN: 'ip link set can0 up type can bitrate 500000'")


class StablCanMsg:
    def __init__(self, message: can.Message):
        self._message = message
        if message.arbitration_id & 1:
            self.sender = Devices.Module
        else:
            self.sender = Devices.Master
        self.arbitration_id = message.arbitration_id
        self.data = list(message.data)
        self.dlc = message.dlc
        self.timestamp: datetime = datetime.fromtimestamp(message.timestamp)


class StablCanBus(Thread):
    def __init__(self):
        super().__init__()
        try:
            self._can = can.interface.Bus(bustype="socketcan", channel=self._channel(), bitrate=self._bitrate())
        except Exception:
            print_setupinfo()
            exit()
        self._running: bool = False
        self._buffer = Queue()

    @property
    def bus(self):
        return self._can

    def _channel(self) -> str:
        """stub for a function that identifies peakcan"""
        return "can0"

    def _bitrate(self) -> int:
        """stub for a function that reads the selected bitrate from c code or some config structure"""
        return 500000

    @property
    def new_msg(self):
        return self._buffer.not_empty

    def get_new_message(self) -> StablCanMsg:
        return self._buffer.get()

    def terminate(self) -> None:
        self._can.shutdown()
        self._running = False

    def run(self) -> None:
        self._running = True
        while self._running:
            msg = self.get_received_message()
            if msg is not None:
                self._buffer.put(msg)
        print("Closing CAN Bus")

    def get_received_message(self) -> Optional[StablCanMsg]:
        try:
            msg = self._can.recv(1)
            return StablCanMsg(msg)
        except can.CanOperationError as e:
            print(f"CAN: Error catched: {e}")
