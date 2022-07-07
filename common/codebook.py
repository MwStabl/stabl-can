from enum import Enum


class Devices(Enum):
    Master: int = 0
    Module: int = 1


msg_dict = {
    0x24: {
        0x11: "Modules shall generate random bytes"
    }
}