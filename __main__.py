import logging
from cmd import Cmd
from datetime import datetime
from pathlib import Path
from typing import Optional

import click

from communicator.common.logger import StablLogger
from communicator.streams.collector import Collector
from communicator.streams.filter import MsgFilters


class Communicator(Cmd):
    prompt = "modbus> "
    intro = "Welcome! Type ? to list commands.\nCommands not listed, will be sent via Modbus to the controller board."

    def __init__(self, require_canbus, require_modbus, require_uoc):
        super().__init__()
        self.logger = StablLogger()
        self.output_file = Path("logs") / f"{datetime.now().strftime('%Y_%m_%d-%H_%M_%S')}.log"
        self._collector = Collector(self.logger.logfile, require_canbus, require_modbus, require_uoc)
        self._collector.start()
        self._command_map = {
            "x": self.do_exit,
            "p": self.do_exit,
            ":hc on": self._hc_on,
            ":hc off": self._hc_off,
            ":can on": self._can_on,
            ":can off": self._can_off,
            ":uoc on": self._uoc_on,
            ":uoc off": self._uoc_off,
            ":modbus on": self._modbus_on,
            ":modbus off": self._modbus_off,
            ":log on": self._log_on,
            ":log off": self._log_off,
            ":c": self._clear_output,
        }

    def run_until_terminated(self):
        try:
            self.cmdloop()
        except KeyboardInterrupt:
            pass

    def _hc_on(self, inp) -> Optional[bool]:
        self._collector.message_filter.deactivate_filter(MsgFilters.suppress_hc)
        return None

    def _hc_off(self, inp) -> Optional[bool]:
        self._collector.message_filter.activate_filter(MsgFilters.suppress_hc)
        return None

    def _can_on(self, inp) -> Optional[bool]:
        self._collector.message_filter.deactivate_filter(MsgFilters.suppress_can)
        return None

    def _can_off(self, inp) -> Optional[bool]:
        self._collector.message_filter.activate_filter(MsgFilters.suppress_can)
        return None

    def _uoc_on(self, inp) -> Optional[bool]:
        self._collector.message_filter.deactivate_filter(MsgFilters.suppress_uoc)
        return None

    def _uoc_off(self, inp) -> Optional[bool]:
        self._collector.message_filter.activate_filter(MsgFilters.suppress_uoc)
        return None

    def _modbus_on(self, inp) -> Optional[bool]:
        self._collector.message_filter.deactivate_filter(MsgFilters.suppress_modbus)
        return None

    def _modbus_off(self, inp) -> Optional[bool]:
        self._collector.message_filter.activate_filter(MsgFilters.suppress_modbus)
        return None

    def _log_on(self, inp) -> Optional[bool]:
        self._collector.message_filter.deactivate_filter(MsgFilters.suppress_logging)
        return None

    def _log_off(self, inp) -> Optional[bool]:
        self._collector.message_filter.activate_filter(MsgFilters.suppress_logging)
        return None

    def _clear_output(self, inp) -> Optional[bool]:
        print(chr(27) + "[2J")
        return None

    def terminate(self) -> None:
        self._collector.terminate()
        self._collector.join()
        self.fancyfy_saving()

    def fancyfy_saving(self) -> None:
        safe = input("Safe Logfile? [Y/n]: ")
        if safe == "n":
            self.output_file.unlink(missing_ok=True)
        else:
            new_name = input("Rename it to something fancy? (leave empty for boring timestamp): ")
            if not new_name == "":
                self.output_file.rename(f"{new_name}.log")

    def do_exit(self, inp: str):
        print("Byebye")
        return True

    def help_exit(self):
        print("exit the application. Shorthand: x q Ctrl-D.")

    def default(self, inp: str):
        if inp in self._command_map.keys():
            return self._command_map[inp](inp)
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
    communicator.run_until_terminated()
    communicator.terminate()


if __name__ == "__main__":
    main()
