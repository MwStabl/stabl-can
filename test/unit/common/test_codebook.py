from pathlib import Path
from typing import Generator

import pytest

from communicator.common import Codebook

can_info_messages_h = """
//
// Created by max on 14.07.22.
//

#ifndef STABL_MASTER_CAN_INFO_MESSAGES_H
#define STABL_MASTER_CAN_INFO_MESSAGES_H

typedef enum {
    canMsgStateConfirmation=0x10,
    // Fw Update Messages
    canMsgFwUpdate=0x26,
    // Battery Operating Limit Messages
    canMsgCellUnderVoltage=0x30,
    canMsgCellOvervoltage=0x31,
    canMsgBatteryNotDetected=0x32,
    canMsgBatteryUnderVoltage=0x33,
    canMsgBatteryOverVoltage=0x34,
    canMsgBatteryOverCurrent=0x35,
    canMsgCellOverTemp=0x36,
    canMsgCellUnderTemp=0x37,
    // STABL Module (PCB) Limit Messages
    canMsgPCBOverTemp=0x40,
    canMsgPCBShortCircuit=0x41,

    // BMS Limit Messages
    canMsgBMSNotConnected=0x50,
    canMsgBMSNoDataRCV=0x51,
    // STABL Module Watchdog Errors
    canMsgWatchdogHardwareTriggered=0x60,
    canMsgWatchdogCANTriggered=0x61,
    canMsgWatchdogUOCTriggered=0x62,
    canMsgWatchdogIwdgTriggered=0x63,
    canMsgWatchdogWwdgTriggered=0x64,
    // STABL Module Mosfet Driver Errors
    canMsgMosfetDriverDisabled=0x70,
    canMsgMosfetDriverBatteryDisabled=0x71,
    // STABL Module Power Errors
    canMsgPowerVdd=0x80,
    canMsgPowerVdda=0x81,
    canMsgPower5v=0x82,

    // Switchmatrix Responses
    canMsgSwitchMat=0x90,
    canMsgSwitchMatrixIDUseTe=0x91,
    canMsgSwitchMatrixIDCopyTempMatrixToPrima=0x92,
    canMsgSwitchMatrixIDUsePrima=0x93,
    canMsgSwitchMatrixIDDeleteTe=0x94,
    // Reveice Heartbeat Messages

    canMsgHeartbeat=0xA0,

    // Receive Manual Error
    canMsgManualError=0xB0,

    // Receive Reset condition
    canMsgResetConditionErrorUnknown=0xC0,
    canMsgResetConditionErrorLowPower=0xC1,
    //formerly 0xC2 and 0xC3 were Iwdg and Wwdg Callbacks (now with their fellow watchdogs in the 0x6n area)
    canMsgResetConditionErrorSoftware=0xC4,
    canMsgResetConditionErrorBor=0xC5,
    canMsgResetConditionErrorByteloader=0xC6,
    canMsgResetConditionErrorFirewall=0xC7,
    canMsgResetConditionErrorNrst=0xC8,

    // invalid lines
    dfgdf=df,
    sdf=0x4t,
    hjklö=0x56
} _canInfoMessages_t;

#endif //STABL_MASTER_CAN_INFO_MESSAGES_H
"""


@pytest.fixture
def codebook() -> Generator[Codebook, None, None]:
    msg_h_file = Path("test/unit/common/can_info_messages.h")
    with open(msg_h_file, "w") as f:
        f.write(can_info_messages_h)
    yield Codebook(msg_h_file)
    msg_h_file.unlink()


def test_fixture(codebook: Codebook) -> None:
    can_info_messages = codebook._decode_codebook()
    assert len(can_info_messages) == 38
    for key, value in can_info_messages.items():
        assert isinstance(key, int)
        assert isinstance(value, str)
