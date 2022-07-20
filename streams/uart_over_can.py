from threading import Thread

from streams.datasource import StablDatasource


class StablUartOverCan(StablDatasource):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        ...

    def terminate(self) -> None:
        ...
