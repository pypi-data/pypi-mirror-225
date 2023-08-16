import pathlib

import pytest

from earningtrader.storage.shelve_storage import ShelveStorage


class TestObject:
    ...


@pytest.fixture
def test_object() -> object:
    return TestObject()


@pytest.fixture
def storage(tmp_path: pathlib.Path) -> ShelveStorage:
    return ShelveStorage(db_path=str(tmp_path / "test.shelve"))


def test_init_shelve_storage_with_wrong_file_extension():
    with pytest.raises(ValueError) as exc_info:
        ShelveStorage(db_path="test.db")
        assert "exist" in exc_info.value


def test_load_data_properly(test_object: object, storage: ShelveStorage):
    storage.store_data(key="test", value=test_object)
    assert (
        storage.load_data(key="test").__class__.__name__
        == test_object.__class__.__name__
    )


def test_load_data_with_nonexist_key(storage: ShelveStorage):
    with pytest.raises(KeyError):
        storage.load_data(key="non_exists")


def test_store_possible_objects(storage: ShelveStorage):
    import pandas as pd
    import numpy as np

    pd_dataframe = pd.DataFrame([[1, 2]])
    np_array = np.array([1, 2, 3])

    assert isinstance(
        storage.store_data(key="pd_dataframe", value=pd_dataframe), pd.DataFrame
    )
    assert isinstance(storage.store_data(key="np_array", value=np_array), np.ndarray)


def test_delete_data_properly(storage: ShelveStorage, test_object: object):
    storage.store_data(key="test", value=test_object)

    assert (
        storage.delete_data(key="test").__class__.__name__
        == test_object.__class__.__name__
    )

    with pytest.raises(KeyError):
        storage.load_data(key="test")


def test_clear_db_properly(storage: ShelveStorage):
    storage.store_data(key="str", value="42")
    storage.store_data(key="int", value=42)

    assert storage.load_data(key="str") == "42"
    assert storage.load_data(key="int") == 42

    storage.clear()

    with pytest.raises(KeyError):
        storage.load_data(key="str")
        storage.load_data(key="int")
