from enum import Enum
from pathlib import Path
from re import findall
from typing import Dict


class Devices(Enum):
    Master: int = 0
    Module: int = 1


MAX_CAN_INFO_DEFAULT_LOCATION = Path("/home/max/Workspaces/clion/Stabl-Master/peripherals/can_info_messages.h")


class Codebook:
    def __init__(self, can_messages_h_location: Path = MAX_CAN_INFO_DEFAULT_LOCATION) -> None:
        self._can_messages_h = self._load_can_messages_h(can_messages_h_location)

    @staticmethod
    def _load_can_messages_h(location: Path) -> list:
        with open(location, "r") as f:
            return [l.strip() for l in f.readlines()]

    def _decode_codebook(self) -> Dict[int, str]:
        codebook = {}
        for line in self._can_messages_h:
            try:
                key = int(findall("0x[A-Fa-f0-9]+", line)[0], 16)
                value = str(findall("can\w*", line)[0])
                codebook[key] = value
            except IndexError:
                pass
        return codebook
