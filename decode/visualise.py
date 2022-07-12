from common.can import StablCanMsg
from decode.msgdecoder import decode


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
    while len(useful) < 8*2+7:
        useful += " --"
    return useful


def visualise(message: StablCanMsg) -> str:
    return f'{message.timestamp.strftime("%H:%M:%S")}.{message.timestamp.strftime("%f")[:2]} - {_beautify_arbitration_field(message.arbitration_id)} - {_beautify_paylad(message.data)} - {decode(message)}'
