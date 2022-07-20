import logging
from cmd import Cmd
from datetime import datetime
from pathlib import Path

import click

from streams.collector import Collector


class Communicator(Cmd):
    prompt = "modbus> "
    intro = "Welcome! Type ? to list commands.\nCommands not listed, will be sent via Modbus to the controller board."

    def __init__(self, require_canbus, require_modbus, require_uoc):
        super().__init__()
        self.logfile = Path(f"{datetime.now().strftime('%Y_%m_%d-%H_%M_%S')}.log")
        self._collector = Collector(self.logfile, require_canbus, require_modbus, require_uoc)
        self._collector.start()
        self._configure_filelogger()

    def _configure_filelogger(self) -> None:
        logging.basicConfig(
            filename="error.log",
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s: %(name)s: %(message)s",
            datefmt="%m.%d.%Y %H:%M:%S",
        )

    def terminate(self) -> None:
        self._collector.terminate()

    def do_exit(self, inp: str):
        print("Byebye")
        return True

    def do_hc(self, inp: str):
        if inp == "on":
            print("Show HC Messages")
        else:
            print("supressing HC Messages")

    def help_exit(self):
        print("exit the application. Shorthand: x q Ctrl-D.")

    def default(self, inp: str):
        if inp == "x" or inp == "q":
            return self.do_exit(inp)
        else:
            self._collector.send_modbus_command(inp)


@click.command()
@click.option(
    "--canbus",
    "-c",
    is_flag=True,
    default=False,
    help="insist on capturing CAN outputs (will raise if device is not available)",
)
@click.option(
    "--modbus",
    "-m",
    is_flag=True,
    default=False,
    help="insist on capturing Modbus outputs (will raise if device is not available)",
)
@click.option(
    "--uoc",
    "-u",
    is_flag=True,
    default=False,
    help="insist on capturing Uart Over Can (UoC) outputs (will raise if device is not available)",
)
def main(canbus: bool, modbus: bool, uoc: bool) -> None:
    communicator = Communicator(canbus, modbus, uoc)
    try:
        communicator.cmdloop()
    except KeyboardInterrupt:
        pass
    communicator.terminate()
    safe = input("Safe Logfile? [Y/n]")
    if safe == "n":
        communicator.logfile.unlink()
    else:
        new_name = input("Rename it to something fancy? (leave empty for boring timestamp)")
        if not new_name == "":
            communicator.logfile.rename(f"{new_name}.log")


if __name__ == "__main__":
    main()
