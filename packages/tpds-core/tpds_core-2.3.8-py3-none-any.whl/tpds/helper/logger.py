from __future__ import annotations

import logging
import os
from typing import Any, Callable, Union


class LogFacility:
    """
    Logging Facility - acts as a singleton
    """

    __shared_state: dict[str, Any] = {}
    _default_log_format = "[%(levelname)s %(asctime)s %(process)-5d %(thread)-5d] %(message)s"

    def __new__(cls, **kwargs: Union[str, os.PathLike[str], None]) -> Any:
        # Only ever allow one global instance of the logger
        instance = super().__new__(cls)
        instance.__dict__ = cls.__shared_state
        return instance

    def __init__(
        self,
        logfile: Union[str, os.PathLike[str], None] = None,
        level: int = logging.DEBUG,
        logstream: bool = True,
        logformat: str = _default_log_format,
    ) -> None:
        if not hasattr(self, "_callback"):
            self._callback: Union[Callable[[str], None], None] = None
        if not hasattr(self, "_log"):
            self._log = logging.getLogger("tpds")
            self._log.setLevel(level)

        if not hasattr(self, "_formatter"):
            self._formatter = logging.Formatter(logformat)

        sh = None
        fh = None
        for h in self._log.handlers:
            if isinstance(h, logging.FileHandler):
                fh = h
            elif isinstance(h, logging.StreamHandler):
                sh = h

        if logstream and sh is None:
            sh = logging.StreamHandler()
            sh.setLevel(level)
            sh.setFormatter(self._formatter)
            self._log.addHandler(sh)

        if logfile is not None and fh is None:
            fh = logging.FileHandler(logfile, mode="w")
            fh.setLevel(level)
            fh.setFormatter(self._formatter)
            self._log.addHandler(fh)

    def log(self, message: str, logtype: int = logging.DEBUG) -> None:
        """
        Default logging mechanism which emits to all connected loggers
        """
        self._log.log(logtype, message)
        try:
            if self._callback is not None:
                self._callback(str(message).strip())
        except Exception as e:
            self._log.error(e)

    def set_logger(self, logger: Callable[[str], None]) -> None:
        """
        Add a custom logging callback that will also be used
        """
        self._callback = logger


def log(*messages: Union[str, bytes]) -> None:
    logger = LogFacility()
    message = ""
    for msg in messages:
        message += str(msg)
    logger.log(str(message).strip())


__all__ = ["LogFacility", "log"]
