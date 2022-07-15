from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union


# CanMessage = namedtuple("healthcare_message", "hc_id direction update_interval type payload information")
class Direction(Enum):
    master_to_module: int = 0
    module_to_master: int = 1


@dataclass
class CanMessage:
    update_interval: Optional[int]
    type: str
    payload_length: int
    direction: int
    payload: List[Union[str, int]]


@dataclass
class CanMessageHardcodedArbitrationField(CanMessage):
    arbitration_field: int


@dataclass
class HealthcareSwitchmatrixMessage(CanMessage):
    hc_id: int


class InformationRequests:
    status = CanMessageHardcodedArbitrationField(
        arbitration_field=0x00,
        direction=Direction.master_to_module,
        update_interval=1,
        type="Error/Info",
        payload_length=1,
        payload=[],
    )
    acknowledgement = HealthcareSwitchmatrixMessage(
        hc_id=0,
        direction=Direction.module_to_master,
        update_interval=1,
        type="Error/Info/Ack",
        payload_length=2,
        payload=[],
    )
    cycletime_config = CanMessageHardcodedArbitrationField(
        arbitration_field=0x22,
        direction=Direction.master_to_module,
        update_interval=None,
        type="cycletime_config",
        payload_length=4,
        payload=[],
    )
    initialisation = CanMessageHardcodedArbitrationField(
        arbitration_field=0x24,
        direction=Direction.master_to_module,
        update_interval=None,
        type="initialisation",
        payload_length=1,
        payload=[],
    )
    # ota_update = CanMessageHardcodedArbitrationField(arbitration_field=0x26, direction=Direction.master_to_module, update_interval=None, type="ota_update", payload_length=0, payload=[]s
    heartbeat = CanMessageHardcodedArbitrationField(
        arbitration_field=0x28,
        direction=Direction.master_to_module,
        update_interval=None,
        type="heartbeat",
        payload_length=0,
        payload=[],
    )


class SwitchMatrixMessages:
    msg = HealthcareSwitchmatrixMessage(
        hc_id=1,
        direction=Direction.module_to_master,
        update_interval=1,
        type="Error/Info/Ack",
        payload_length=2,
        payload=[],
    )


class HealthcareMessages:
    msg1_v_soc_i_temp = HealthcareSwitchmatrixMessage(
        hc_id=2,
        direction=Direction.module_to_master,
        update_interval=10,
        type="Healthcare Message 1",
        payload_length=2,
        payload=[],
    )
    msg2_cell_voltages_1to4 = HealthcareSwitchmatrixMessage(
        hc_id=3,
        direction=Direction.module_to_master,
        update_interval=10,
        type="Healthcare Message 2",
        payload_length=2,
        payload=[],
    )
    msg3_cell_voltages_5to8 = HealthcareSwitchmatrixMessage(
        hc_id=4,
        direction=Direction.module_to_master,
        update_interval=10,
        type="Healthcare Message 3",
        payload_length=2,
        payload=[],
    )
    msg4_cell_voltages_9to12 = HealthcareSwitchmatrixMessage(
        hc_id=5,
        direction=Direction.module_to_master,
        update_interval=10,
        type="Healthcare Message 4",
        payload_length=2,
        payload=[],
    )
    msg5_cell_voltages_13to16 = HealthcareSwitchmatrixMessage(
        hc_id=6,
        direction=Direction.module_to_master,
        update_interval=10,
        type="Healthcare Message 5",
        payload_length=2,
        payload=[],
    )
    msg6_cell_bms_temperature = HealthcareSwitchmatrixMessage(
        hc_id=7,
        direction=Direction.module_to_master,
        update_interval=10,
        type="Healthcare Message 6",
        payload_length=2,
        payload=[],
    )
    update_msg1_v_soc_i_temp = HealthcareSwitchmatrixMessage(
        hc_id=2,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Update Trigger for Healthcare Message 1",
        payload_length=2,
        payload=[],
    )
    update_msg2_cell_voltages_1to4 = HealthcareSwitchmatrixMessage(
        hc_id=3,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Update Trigger for Healthcare Message 2",
        payload_length=2,
        payload=[],
    )
    update_msg3_cell_voltages_5to8 = HealthcareSwitchmatrixMessage(
        hc_id=4,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Update Trigger for Healthcare Message 3",
        payload_length=2,
        payload=[],
    )
    update_msg4_cell_voltages_9to12 = HealthcareSwitchmatrixMessage(
        hc_id=5,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Update Trigger for Healthcare Message 4",
        payload_length=2,
        payload=[],
    )
    update_msg5_cell_voltages_13to16 = HealthcareSwitchmatrixMessage(
        hc_id=6,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Update Trigger for Healthcare Message 5",
        payload_length=2,
        payload=[],
    )
    update_msg6_cell_bms_temperature = HealthcareSwitchmatrixMessage(
        hc_id=7,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Update Trigger for Healthcare Message 6",
        payload_length=2,
        payload=[],
    )


class FirmwareUpdateMessages:
    ota_announce_update = CanMessageHardcodedArbitrationField(
        arbitration_field=0x26,
        direction=Direction.master_to_module,
        update_interval=None,
        type="",
        payload_length=2,
        payload=[0x01, 0x00],
    )
    ota_confirm_ready = HealthcareSwitchmatrixMessage(
        hc_id=0,
        direction=Direction.module_to_master,
        update_interval=None,
        type="state readiness for ota fw update",
        payload_length=2,
        payload=[0x26, 0x01],
    )
    ota_success = HealthcareSwitchmatrixMessage(
        hc_id=0,
        direction=Direction.module_to_master,
        update_interval=None,
        type="",
        payload_length=2,
        payload=[0x26, 0x02],
    )
    ota_fail = HealthcareSwitchmatrixMessage(
        hc_id=0,
        direction=Direction.module_to_master,
        update_interval=None,
        type="",
        payload_length=2,
        payload=[0x26, 0xFF],
    )


class Color(Enum):
    white: int = 0x03
    red: int = 0x04
    green: int = 0x05
    blue: int = 0x06
    magenta: int = 0x07
    cyan: int = 0x08
    yellow: int = 0x09


@dataclass
class ModuleLedSetMessage(CanMessageHardcodedArbitrationField):
    def __init__(self, module_id: int, color: Color) -> None:
        self.arbitration_field = 0
        self.direction = Direction.master_to_module
        self.update_interval = None
        self.payload_length = 4
        self.payload = [0x0A, module_id, color.value, 0x00]


module_id = 500


class MasterInfoMessages:
    off = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[0x0A, module_id, 0x00, 0x00],
    )
    show_address = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    show_soc = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    pulse_white = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    pulse_red = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    pulse_green = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    pulse_blue = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    pulse_magenta = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    pulse_cyan = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    pulse_yellow = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    warning_blink_yellow = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    error_blink_red = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    master_status_init = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    master_status_ready = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    master_status_idle = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    master_status_run = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    master_status_error = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    master_status_emergency = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    can_softwatchdog_fail = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    uoc_softwatchdog_fail = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    can_heartbeat_response_error = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )
    hw_watchdog_error = CanMessageHardcodedArbitrationField(
        arbitration_field=0,
        direction=Direction.master_to_module,
        update_interval=None,
        type="Master Info Message",
        payload_length=4,
        payload=[],
    )


class CanId:
    def __init__(self, message: HealthcareSwitchmatrixMessage, module_id: Optional[int] = None) -> None:
        self._message = message
        self._module_id = module_id

    def __repr__(self) -> str:
        return dec2bin(self.compose_arbitration_field())

    def compose_arbitration_field(self) -> int:
        arbitration_field = self._message.direction.value + (self._message.hc_id << 6)
        if self._message.direction == Direction.module_to_master:
            arbitration_field += self._module_id << 1
        return arbitration_field


def dec2bin(n: int) -> str:
    return "{0:b}".format(int(n))
