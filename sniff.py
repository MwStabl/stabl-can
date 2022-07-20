from time import sleep

import click
from termcolor import cprint

from common.modbus import Modbus
from decode.visualise import visualise
from streams.canbus import StablCanBus


@click.command()
@click.option("--canbus", "-c", is_flag=True, default=True, help="Capture CAN outputs")
@click.option("--modbus", "-m", is_flag=True, default=False, help="Capture Modbus (over uart) outputs")
def main(canbus: bool, modbus: bool) -> None:
    if canbus:
        cprint("can message", "red")
        can = StablCanBus()
        can.start()
    if modbus:
        cprint("modbus message", "green")
        mod = Modbus()
        mod.start()
    print("\n")
    try:
        while True:
            if canbus and can.new_msg:
                visualise(can.get_new_message())
            if modbus and mod.new_msg:
                cprint(mod.get_new_message(), "green")
            sleep(0.001)
    except KeyboardInterrupt:
        print("End")
    finally:
        if canbus:
            can.terminate()
        if modbus:
            mod.terminate()


if __name__ == "__main__":
    main()
