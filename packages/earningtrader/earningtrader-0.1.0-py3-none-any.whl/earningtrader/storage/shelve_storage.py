import re
import shelve
from typing import Any

from ._interface import StorageInterface


class ShelveStorage(StorageInterface):
    """
    The adapter of the shelve library(https://docs.python.org/3/library/shelve.html)
    that conforms to the common StorageInterface.
    """

    _db_path: str

    def __init__(self, *, db_path: str) -> None:
        if re.match(r"^[\/\w\-]+\.shelve$", db_path) is None:
            raise ValueError("The DB path must be in the format '*.shelve'.")

        self._db_path = db_path

    def load_data(self, *, key: str) -> Any:
        with self._open_db() as db:
            return db[key]

    def store_data(self, *, key: str, value: Any) -> Any:
        with self._open_db() as db:
            db[key] = value
            return db[key]

    def delete_data(self, *, key: str) -> Any:
        temp = None
        try:
            with self._open_db() as db:
                temp = db[key]
                del db[key]

        except KeyError:
            # do nothing if there is no data to be removed
            ...

        else:
            return temp

    def clear(self) -> None:
        with self._open_db() as db:
            for key in db.keys():
                del db[key]

    def _open_db(self) -> shelve.Shelf[Any]:
        return shelve.open(filename=self._db_path, writeback=True)
