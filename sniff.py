from time import sleep

import click
from termcolor import cprint

from common.can import StablCanBus
from common.modbus import Modbus
from decode.visualise import visualise


@click.command()
@click.option("--canbus", is_flag=True, help="Capture CAN outputs")
@click.option("--modbus", is_flag=True, help="Capture Modbus (over uart) outputs")
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
                cprint(visualise(can.get_new_message()), "red")
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
