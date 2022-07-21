import logging
from datetime import datetime
from pathlib import Path
from typing import Any


class StablLogfileHandler(logging.StreamHandler):
    __at_least_one_log: bool = False

    def __init__(self, parent: logging.Logger, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(name)s: %(message)s")
        formatter.datefmt = "%d.%m.%Y %H:%M:%S"
        self.setFormatter(formatter)
        parent.addHandler(self)

    @property
    def existing(self):
        return self.__at_least_one_log

    def emit(self, record: logging.LogRecord):
        self.__at_least_one_log = True
        super().emit(record)


LOG = logging.getLogger(__name__)


class StablLogger:
    def __init__(self, log_path: Path = Path("logs")) -> None:
        LOG = logging.getLogger("STABL")
        self.logfile = Path(f"{log_path}/error.log")
        handler = logging.FileHandler(self.logfile)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(name)s: %(message)s")
        formatter.datefmt = "%d.%m.%Y %H:%M:%S"
        handler.setFormatter(formatter)
        LOG.addHandler(handler)
