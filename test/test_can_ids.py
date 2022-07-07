import pytest

import compose.can_id as ci


@pytest.mark.parametrize('arbitration_field, implemented')
def test_information_requests(arbitration_field: int, implemented: int):
    ...


@pytest.mark.parametrize('hc_msg, module_id, implemented',
                         [
                            (ci.SwitchMatrixMessages, 1, 1000010),
                             (ci.SwitchMatrixMessages, 2, 1000100),
                             (ci.SwitchMatrixMessages, 3, 1000110),
                             (ci.SwitchMatrixMessages, 4, 1001000),
                             (ci.SwitchMatrixMessages, 5, 1001010),
                             (ci.SwitchMatrixMessages, 6, 1001100),
                             (ci.SwitchMatrixMessages, 7, 1001110),
                             (ci.SwitchMatrixMessages, 8, 1010000),
                             (ci.SwitchMatrixMessages, 9, 1010010),
                             (ci.SwitchMatrixMessages, 10, 1010100),
                             (ci.SwitchMatrixMessages, 11, 1010110),
                             (ci.SwitchMatrixMessages, 12, 1011000),
                             (ci.SwitchMatrixMessages, 13, 1011010),
                             (ci.SwitchMatrixMessages, 14, 1011100),
                             (ci.SwitchMatrixMessages, 15, 1011110),
                             (ci.SwitchMatrixMessages, 16, 1100000),
                             (ci.SwitchMatrixMessages, 17, 1100010),  # Todo: why does this module id correspond to nonexisting nr. 17?

                         ]
                         )
def test_switchmatrix_messages(hc_msg: ci.HealthcareSwitchmatrixMessage, module_id: int, implemented: str) -> None:
    result = ci.CanId(hc_msg, module_id)
    assert result.__repr__() == implemented
    if result._message.direction == ci.Direction.master_to_module:
        assert result._message.direction.value == 0
    else:
        assert result._message.direction.value == 1



@pytest.mark.parametrize('hc_msg, module_id, implemented',
                         [
                             (ci.HealthcareMessages.update_msg1, None, '10000000'),
                                 (ci.HealthcareMessages.msg1, 1, '10000011'),
                                 (ci.HealthcareMessages.msg1, 2, '10000101'),
                                 (ci.HealthcareMessages.msg1, 3, '10000111'),
                                 (ci.HealthcareMessages.msg1, 4, '10001001'),
                                 (ci.HealthcareMessages.msg1, 5, '10001011'),
                                 (ci.HealthcareMessages.msg1, 6, '10001101'),
                                 (ci.HealthcareMessages.msg1, 7, '10001111'),
                                 (ci.HealthcareMessages.msg1, 8, '10010001'),
                                 (ci.HealthcareMessages.msg1, 9, '10010011'),
                                 (ci.HealthcareMessages.msg1, 10, '10010101'),
                                 (ci.HealthcareMessages.msg1, 11, '10010111'),
                                 (ci.HealthcareMessages.msg1, 12, '10011001'),
                                 (ci.HealthcareMessages.msg1, 13, '10011011'),
                                 (ci.HealthcareMessages.msg1, 14, '10011101'),
                                 (ci.HealthcareMessages.msg1, 15, '10011111'),
                                 (ci.HealthcareMessages.msg1, 16, '10100001'),
                                 (ci.HealthcareMessages.update_msg2, None, '11000000'),
                                 (ci.HealthcareMessages.msg2, 1, '11000011'),
                                 (ci.HealthcareMessages.msg2, 2, '11000101'),
                                 (ci.HealthcareMessages.msg2, 3, '11000111'),
                                 (ci.HealthcareMessages.msg2, 4, '11001001'),
                                 (ci.HealthcareMessages.msg2, 5, '11001011'),
                                 (ci.HealthcareMessages.msg2, 6, '11001101'),
                                 (ci.HealthcareMessages.msg2, 7, '11001111'),
                                 (ci.HealthcareMessages.msg2, 8, '11010001'),
                                 (ci.HealthcareMessages.msg2, 9, '11010011'),
                                 (ci.HealthcareMessages.msg2, 10, '11010101'),
                                 (ci.HealthcareMessages.msg2, 11, '11010111'),
                                 (ci.HealthcareMessages.msg2, 12, '11011001'),
                                 (ci.HealthcareMessages.msg2, 13, '11011011'),
                                 (ci.HealthcareMessages.msg2, 14, '11011101'),
                                 (ci.HealthcareMessages.msg2, 15, '11011111'),
                                 (ci.HealthcareMessages.msg2, 16, '11100001'),
                                 (ci.HealthcareMessages.update_msg3, None, '100000000'),
                                 (ci.HealthcareMessages.msg3, 1, '100000011'),
                                 (ci.HealthcareMessages.msg3, 2, '100000101'),
                                 (ci.HealthcareMessages.msg3, 3, '100000111'),
                                 (ci.HealthcareMessages.msg3, 4, '100001001'),
                                 (ci.HealthcareMessages.msg3, 5, '100001011'),
                                 (ci.HealthcareMessages.msg3, 6, '100001101'),
                                 (ci.HealthcareMessages.msg3, 7, '100001111'),
                                 (ci.HealthcareMessages.msg3, 8, '100010001'),
                                 (ci.HealthcareMessages.msg3, 9, '100010011'),
                                 (ci.HealthcareMessages.msg3, 10, '100010101'),
                                 (ci.HealthcareMessages.msg3, 11, '100010111'),
                                 (ci.HealthcareMessages.msg3, 12, '100011001'),
                                 (ci.HealthcareMessages.msg3, 13, '100011011'),
                                 (ci.HealthcareMessages.msg3, 14, '100011101'),
                                 (ci.HealthcareMessages.msg3, 15, '100011111'),
                                 (ci.HealthcareMessages.msg3, 16, '100100001'),
                                 (ci.HealthcareMessages.update_msg4, None, '101000000'),
                                 (ci.HealthcareMessages.msg4, 1, '101000011'),
                                 (ci.HealthcareMessages.msg4, 2, '101000101'),
                                 (ci.HealthcareMessages.msg4, 3, '101000111'),
                                 (ci.HealthcareMessages.msg4, 4, '101001001'),
                                 (ci.HealthcareMessages.msg4, 5, '101001011'),
                                 (ci.HealthcareMessages.msg4, 6, '101001101'),
                                 (ci.HealthcareMessages.msg4, 7, '101001111'),
                                 (ci.HealthcareMessages.msg4, 8, '101010001'),
                                 (ci.HealthcareMessages.msg4, 9, '101010011'),
                                 (ci.HealthcareMessages.msg4, 10, '101010101'),
                                 (ci.HealthcareMessages.msg4, 11, '101010111'),
                                 (ci.HealthcareMessages.msg4, 12, '101011001'),
                                 (ci.HealthcareMessages.msg4, 13, '101011011'),
                                 (ci.HealthcareMessages.msg4, 14, '101011101'),
                                 (ci.HealthcareMessages.msg4, 15, '101011111'),
                                 (ci.HealthcareMessages.msg4, 16, '101100001'),
                                 (ci.HealthcareMessages.update_msg5, None, '110000000'),
                                 (ci.HealthcareMessages.msg5, 1, '110000011'),
                                 (ci.HealthcareMessages.msg5, 2, '110000101'),
                                 (ci.HealthcareMessages.msg5, 3, '110000111'),
                                 (ci.HealthcareMessages.msg5, 4, '110001001'),
                                 (ci.HealthcareMessages.msg5, 5, '110001011'),
                                 (ci.HealthcareMessages.msg5, 6, '110001101'),
                                 (ci.HealthcareMessages.msg5, 7, '110001111'),
                                 (ci.HealthcareMessages.msg5, 8, '110010001'),
                                 (ci.HealthcareMessages.msg5, 9, '110010011'),
                                 (ci.HealthcareMessages.msg5, 10, '110010101'),
                                 (ci.HealthcareMessages.msg5, 11, '110010111'),
                                 (ci.HealthcareMessages.msg5, 12, '110011001'),
                                 (ci.HealthcareMessages.msg5, 13, '110011011'),
                                 (ci.HealthcareMessages.msg5, 14, '110011101'),
                                 (ci.HealthcareMessages.msg5, 15, '110011111'),
                                 (ci.HealthcareMessages.msg5, 16, '110100001'),
                                 (ci.HealthcareMessages.update_msg6, None, '111000000'),
                                 (ci.HealthcareMessages.msg6, 1, '111000011'),
                                 (ci.HealthcareMessages.msg6, 2, '111000101'),
                                 (ci.HealthcareMessages.msg6, 3, '111000111'),
                                 (ci.HealthcareMessages.msg6, 4, '111001001'),
                                 (ci.HealthcareMessages.msg6, 5, '111001011'),
                                 (ci.HealthcareMessages.msg6, 6, '111001101'),
                                 (ci.HealthcareMessages.msg6, 7, '111001111'),
                                 (ci.HealthcareMessages.msg6, 8, '111010001'),
                                 (ci.HealthcareMessages.msg6, 9, '111010011'),
                                 (ci.HealthcareMessages.msg6, 10, '111010101'),
                                 (ci.HealthcareMessages.msg6, 11, '111010111'),
                                 (ci.HealthcareMessages.msg6, 12, '111011001'),
                                 (ci.HealthcareMessages.msg6, 13, '111011011'),
                                 (ci.HealthcareMessages.msg6, 14, '111011101'),
                                 (ci.HealthcareMessages.msg6, 15, '111011111'),
                                 (ci.HealthcareMessages.msg6, 16, '111100001')
])
def test_healthcare_messages(hc_msg: ci.HealthcareSwitchmatrixMessage, module_id: int, implemented: str) -> None:
    result = ci.CanId(hc_msg, module_id)
    assert result.__repr__() == implemented
    if result._message.direction == ci.Direction.master_to_module:
        assert result._message.direction.value == 0
    else:
        assert result._message.direction.value == 1
