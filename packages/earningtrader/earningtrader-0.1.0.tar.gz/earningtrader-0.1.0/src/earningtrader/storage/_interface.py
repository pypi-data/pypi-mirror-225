from typing import Any
from abc import ABC, abstractmethod


class StorageInterface(ABC):
    """
    The interface for the storage components.

    A storage component assumes a key-value database as its backend.
    """

    @abstractmethod
    def load_data(self, *, key: str) -> Any:
        """
        Load the (key, value) pair from the database backend corresponding
        to the given key.
        """
        ...

    @abstractmethod
    def store_data(self, *, key: str, value: Any) -> Any:
        """
        Store the (key, value) pair(including new and updated ones altogether)
        into the database backend.
        """
        ...

    @abstractmethod
    def delete_data(self, *, key: str) -> Any:
        """
        Delete the (key, value) pair in the database.
        """
        ...

    @abstractmethod
    def clear(self) -> None:
        """
        Clear the database; i.e. delete all the (key, value) pairs in it.
        """
        ...
