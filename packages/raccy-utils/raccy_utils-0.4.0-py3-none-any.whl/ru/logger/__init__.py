"""
Copyright 2021 Daniel Afriyie

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import typing
import logging
import pathlib
import threading
import traceback
import logging.handlers as handlers
from datetime import datetime as dt

from colorama import Fore

from ru.hints import Path
from ru.constants import constants


def logger(
        name: typing.Optional[str] = None,
        fmt: typing.Optional[str] = None,
        filename: typing.Optional[Path] = None
) -> logging.Logger:
    lg = Logger(name, fmt, filename)
    return lg()


class Logger:
    __loggers: typing.Dict[str, logging.Logger] = {}

    def __init__(
            self,
            name: typing.Optional[str] = None,
            fmt: typing.Optional[str] = None,
            filename: typing.Optional[Path] = None
    ) -> None:
        self._name = name if name else __name__
        self._fmt = fmt if fmt else "%(asctime)s:%(levelname)s:%(message)s"
        self._filename = filename
        self._root_path: Path = pathlib.Path(".").absolute()

    def _get_log_file(self) -> Path:
        fn = self._filename if self._filename else "log"
        log_path = os.path.join(self._root_path, "logs")
        log_file = os.path.join(log_path, f"{fn}.log")
        if not os.path.exists(log_path):
            os.mkdir(os.path.join(log_path))
        return log_file

    def _create_logger(self) -> logging.Logger:
        _logger = logging.getLogger(self._name)
        _logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(self._fmt)
        max_bytes = 1048576 * 100  # 100mb
        file_handler = handlers.RotatingFileHandler(self._get_log_file(), maxBytes=max_bytes, encoding=constants.ENCODING, backupCount=10)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)

        _logger.addHandler(file_handler)
        _logger.addHandler(stream_handler)

        return _logger

    def __call__(self) -> logging.Logger:
        if self._name in self.__loggers:
            return self.__loggers[self._name]
        else:
            _logger = self._create_logger()
            self.__loggers[self._name] = _logger
            return _logger


class BaseColorPrint:
    mutex: threading.Lock

    def _print(self, level: str, text: str, color: str) -> None:
        with self.mutex:
            n = dt.now().strftime("%Y-%m-%d %H:%M:%S,%f")
            t1, ms = n.split(",")
            ms = ms[0:3]
            now = f"{t1},{ms}"
            t = f"{now}:{level}:{text}"
            print(color + t + Fore.RESET)

    def info(self, text: str, color: str = Fore.CYAN) -> None:
        self._print("INFO", text, color)

    def warning(self, text: str, color: str = Fore.YELLOW) -> None:
        self._print("WARNING", text, color)

    def success(self, text: str, color: str = Fore.GREEN) -> None:
        self._print("SUCCESS", text, color)

    def error(self, error: typing.Union[str, BaseException], color: str = Fore.RED) -> None:
        if isinstance(error, BaseException):
            msg = self.get_error_message(error)
            self._print("ERROR", msg, color)
        else:
            self._print("ERROR", error, color)

    @staticmethod
    def get_error_message(e: BaseException) -> str:
        msg = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        return msg


class ColorPrint(BaseColorPrint):
    mutex = threading.Lock()
