from datetime import datetime
from enum import Enum
from typing import Optional

import can
from termcolor import colored

from communicator.common.codebook import Devices
from communicator.streams.datasource import MessageType

msgs_from_master = {
    0x24: {
        0x11: "Modules shall generate random bytes",
        0x12: "Modules shall send their random bytes",
        0x13: "Modules get their random data back anlong with an address",
        0x14: "if conflict ...",
        0x15: "Amount of modules in string in data[1]",
        0x16: "Modules shall reset their can periphery",
    },
    0x28: "Heartbeat Request",
    0x0A: "Controlboard LED Control. More info in data[1]",
    0x0B: {
        0x01: "Master Status Init",
        0x02: "Master Status Ready",
        0x03: "Master Status Idle",
        0x04: "Master Status Run",
        0x05: "Master Status Error",
        0x06: "Master Status Emergency",
    },
    0x0F: "Error triggering manual. More info in data[1]",
}

msgs_from_module = {
    "module_id": {
        0x40: "Switchmatrix CRC",
        0xF0: {"_type": "Battery Error", 0x01: "undervoltage Cell"},
        0xF9: {"_type": "RESET Condition", 0x05: "RESET_ERROR_BOR"},
        0x24: "Initialisation Step ..",
        0x0B: "State switch confirmation",
    }
}


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
        self.annotation = decode(self)
        self.type: MessageType = get_message_type(self)

    def __repr__(self) -> str:
        return visualise(self)


def decode(message: StablCanMsg) -> Optional[str]:
    if message.sender == Devices.Master:
        return msg_from_master(message)
    elif message.sender == Devices.Module:
        return msg_from_module(message)
    else:
        print("no such device")
        return None


def get_message_type(message: StablCanMsg) -> MessageType:
    msg_type = MessageType.other
    try:
        if message.arbitration_id & 0b00111000000:
            msg_type = MessageType.healthcare
        if len(message.data) == 1 and message.data[0] == 0x28:
            msg_type = MessageType.heartbeat
    except KeyError:
        pass
    return msg_type


def msg_from_master(message: StablCanMsg) -> Optional[str]:
    try:
        return msgs_from_master[message.arbitration_id][message.data[0]]
    except (KeyError, IndexError):
        return None


def msg_from_module(message: StablCanMsg) -> Optional[str]:
    try:
        if (message.arbitration_id & 0b11111000000) == 0b11111000000:
            log = "".join([chr(c) for c in message.data])
            return f"Log: {log}"

        val = msgs_from_module["module_id"][message.data[0]]
        if isinstance(val, dict):
            return f'{val["_type"]}: {val[message.data[1]]}'
        else:
            return val
    except KeyError:
        return None


def _beautify_arbitration_field(arbitration_field: int) -> str:
    raw = str(bin(arbitration_field))[2:]
    while len(raw) < 11:
        raw = "0" + raw
    direction = raw[-1]
    module_id = raw[-6:-1]
    healthcare_id = raw[2:-6]
    free_bits = raw[:2]
    hexcode = f"0x{arbitration_field:03x}"
    return f"{free_bits}-{healthcare_id}-{module_id}-{direction} ({hexcode})"


def _beautify_paylad(payload: list) -> str:
    useful = " ".join([f"{i:02x}" for i in payload])
    if len(payload) == 0:
        useful = "--"
    while len(useful) < 8 * 2 + 7:
        useful += " --"
    return useful


def visualise(message: StablCanMsg) -> str:
    timestamp = f'{message.timestamp.strftime("%H:%M:%S")}.{message.timestamp.strftime("%f")[:2]}'
    arbitration = _beautify_arbitration_field(message.arbitration_id)
    payload = _beautify_paylad(message.data)
    decoded = decode(message)
    printout = f"{timestamp} - {arbitration} - {payload} - {decoded}"
    if decoded == "Healthcare":
        return colored(printout, "yellow")
    elif decoded == "Heartbeat Response":
        return colored(printout, "green")
    else:
        return printout
