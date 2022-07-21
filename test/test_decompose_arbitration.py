import pytest

from communicator.decode import visualise


@pytest.mark.parametrize(
    "input, output",
    [
        (1, "00-000-00000-1 (0x001)"),
        (int("101", 2), "00-000-00010-1 (0x005)"),
        (int("10101010101", 2), "10-101-01010-1 (0x555)"),
    ],
)
def test_decompose_arbitration(input: int, output: str) -> None:
    decomposed_arbitration = visualise._beautify_arbitration_field(input)
    print(f"in={input}, out={decomposed_arbitration}")
    assert decomposed_arbitration == output
