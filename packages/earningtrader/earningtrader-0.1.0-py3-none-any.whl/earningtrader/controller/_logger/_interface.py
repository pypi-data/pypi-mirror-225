from abc import ABC, abstractmethod
from enum import Enum


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class FileLoggerInterface(ABC):
    """
    The interface of a logger attached to a file.
    """

    @abstractmethod
    def __init__(self, *, logger_name: str, filepath: str, message_format: str) -> None:
        """
        Config the logger when it is constructed.
        """
        ...

    @abstractmethod
    def log(self, *, message: str, log_level: LogLevel) -> None:
        """
        Log the message at the given log level.
        """
        ...

    @property
    @abstractmethod
    def filepath(self) -> str:
        """
        The filepath where the logs are stored.
        """
        ...

    @abstractmethod
    def close_file(self) -> None:
        """
        Close the file.
        """
