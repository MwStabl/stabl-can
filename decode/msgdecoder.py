import re
from pathlib import Path
from typing import Dict, Optional

from common.can import StablCanMsg
from common.codebook import Devices

msgs_from_master = {
    0x24: {
        0x11: "Modules shall generate random bytes",
        0x12: "Modules shall send their random bytes",
        0x13: "Modules get their random data back anlong with an address",
        0x14: "if conflict ...",
        0x15: "Amount of modules in string in data[1]",
        0x16: "Modules shall reset their can periphery",
    },
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


def decode(message: StablCanMsg) -> Optional[str]:
    if message.sender == Devices.Master:
        return msg_from_master(message)
    elif message.sender == Devices.Module:
        return msg_from_module(message)
    else:
        print("no such device")


def msg_from_master(message: StablCanMsg) -> Optional[str]:
    try:
        return msgs_from_master[message.arbitration_id][message.data[0]]
    except KeyError:
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
