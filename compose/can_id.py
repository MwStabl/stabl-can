from enum import Enum
from typing import Optional

import pretty_tables
from collections import namedtuple


CanMessage = namedtuple("healthcare_message", "hc_id direction update_interval type information")


class Direction(Enum):
    master_to_module: int = 0
    module_to_master: int = 1


class SwitchMatrixMessages:
    msg = CanMessage(hc_id=1, direction=Direction.module_to_master, update_interval=1, type="Error/Info/Ack", information="")


class HealthcareMessages:
    msg1 = CanMessage(hc_id=2, direction=Direction.module_to_master, update_interval=10, type="Healthcare Message 1", information="voltage, soc, current, le temperature")
    msg2 = CanMessage(hc_id=3, direction=Direction.module_to_master, update_interval=10, type="Healthcare Message 2", information="voltage, soc, current, le temperature")
    msg3 = CanMessage(hc_id=4, direction=Direction.module_to_master, update_interval=10, type="Healthcare Message 3", information="voltage, soc, current, le temperature")
    msg4 = CanMessage(hc_id=5, direction=Direction.module_to_master, update_interval=10, type="Healthcare Message 4", information="voltage, soc, current, le temperature")
    msg5 = CanMessage(hc_id=6, direction=Direction.module_to_master, update_interval=10, type="Healthcare Message 5", information="voltage, soc, current, le temperature")
    msg6 = CanMessage(hc_id=7, direction=Direction.module_to_master, update_interval=10, type="Healthcare Message 6", information="voltage, soc, current, le temperature")
    update_msg1 = CanMessage(hc_id=2, direction=Direction.master_to_module, update_interval=None, type="Update Trigger for Healthcare Message 1", information="voltage, soc, current, le temperature")
    update_msg2 = CanMessage(hc_id=3, direction=Direction.master_to_module, update_interval=None, type="Update Trigger for Healthcare Message 2", information="voltage, soc, current, le temperature")
    update_msg3 = CanMessage(hc_id=4, direction=Direction.master_to_module, update_interval=None, type="Update Trigger for Healthcare Message 3", information="voltage, soc, current, le temperature")
    update_msg4 = CanMessage(hc_id=5, direction=Direction.master_to_module, update_interval=None, type="Update Trigger for Healthcare Message 4", information="voltage, soc, current, le temperature")
    update_msg5 = CanMessage(hc_id=6, direction=Direction.master_to_module, update_interval=None, type="Update Trigger for Healthcare Message 5", information="voltage, soc, current, le temperature")
    update_msg6 = CanMessage(hc_id=7, direction=Direction.master_to_module, update_interval=None, type="Update Trigger for Healthcare Message 6", information="voltage, soc, current, le temperature")


class CanId:
    def __init__(self, message: CanMessage, module_id: Optional[int] = None) -> None:
        self._message = message
        self._module_id = module_id

    def __repr__(self) -> str:
        return dec2bin(self.compose_arbitration_field())

    def compose_arbitration_field(self) -> int:
        arbitration_field = self._message.direction.value + (self._message.hc_id << 6)
        if self._message.direction == Direction.module_to_master:
            arbitration_field += (self._module_id << 1)
        return arbitration_field


def dec2bin(n: int) -> str:
    return "{0:b}".format(int(n))
