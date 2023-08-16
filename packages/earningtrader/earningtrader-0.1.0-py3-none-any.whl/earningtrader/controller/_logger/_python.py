from typing import overload
import logging

from ._interface import FileLoggerInterface


class PythonFileLogger(FileLoggerInterface):
    _logger: logging.Logger
    _file_handler: logging.FileHandler
    _filepath: str

    def __init__(self, *, logger_name: str, filepath: str, message_format: str) -> None:
        self._filepath = filepath
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(level=logging.DEBUG)

        self._file_handler = logging.FileHandler(filename=filepath, encoding="utf-8")
        self._file_handler.setFormatter(fmt=logging.Formatter(fmt=message_format))
        self._file_handler.setLevel(level=logging.DEBUG)

        self._logger.addHandler(self._file_handler)

    @overload
    def log(self, *, message: str, log_level: int) -> None:
        ...

    @overload
    def log(self, *, message: Exception, log_level: int) -> None:
        ...

    def log(self, *, message, log_level=logging.INFO) -> None:
        if isinstance(message, Exception):
            self._logger.exception(msg=message, stack_info=True)

        else:
            self._logger.log(level=log_level, msg=message)

    @property
    def filepath(self) -> str:
        return self._filepath

    def close_file(self) -> None:
        self._file_handler.close()

    @staticmethod
    def shutdown() -> None:
        """
        Shutdown the entire logging system and release the file.

        Must be called when the application exits.
        """

        logging.shutdown()
