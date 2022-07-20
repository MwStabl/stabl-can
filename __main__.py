from cmd import Cmd

from streams.collector import Collector


class Communicator(Cmd):
    prompt = "modbus> "
    intro = "Welcome! Type ? to list commands.\nCommands not listed, will be sent via Modbus to the controller board."

    def __init__(self):
        super().__init__()
        self._collector = Collector()
        self._collector.start()

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


if __name__ == "__main__":
    communicator = Communicator()
    try:
        communicator.cmdloop()
    except KeyboardInterrupt:
        pass
    communicator.terminate()
