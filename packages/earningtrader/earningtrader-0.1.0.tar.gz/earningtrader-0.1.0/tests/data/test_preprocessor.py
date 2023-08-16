import pytest

import pandas as pd
import numpy as np

from earningtrader.data.preprocessing.preprocessor import DataPreprocessor
from earningtrader.common.exceptions import ValidationError


@pytest.fixture
def preprocessor() -> DataPreprocessor:
    return DataPreprocessor()


@pytest.mark.parametrize(
    ["input_index", "data_schema"],
    [(["a", "b", "c"], ["a", "b"]), (["a", "b", "c"], ["a", "b", "c"])],
)
def test_rearranged_correctly_done(
    preprocessor: DataPreprocessor, input_index: list[str], data_schema: list[str]
):
    preprocessor.rearrange_raw_data(
        input=pd.DataFrame([[0] * len(input_index)], columns=input_index),
        data_schema=pd.Index(data_schema),
    )


@pytest.mark.parametrize(
    ["input_index", "data_schema"],
    [(["a", "b"], ["b", "c"]), (["d"], ["a", "b", "c"])],
)
def test_rearranged_raises_error(
    preprocessor: DataPreprocessor, input_index: list[str], data_schema: list[str]
):
    with pytest.raises(ValidationError):
        preprocessor.rearrange_raw_data(
            input=pd.DataFrame([[0] * len(input_index)], columns=input_index),
            data_schema=pd.Index(data_schema),
        )


def test_excluding_missing_values(preprocessor: DataPreprocessor):
    input = pd.DataFrame([[1, None], [np.nan, 2], [3, 4]], columns=["a", "b"])

    handled_data = preprocessor.handle_missing_values(input=input, option="exclude")
    handled_data
    assert handled_data.to_dict(orient="list") == pd.DataFrame(
        [[3.0, 4.0]], columns=["a", "b"]
    ).to_dict(orient="list")


def test_replacing_missing_values(preprocessor: DataPreprocessor):
    input = pd.DataFrame([[1, None], [np.nan, 2], [3, 4]], columns=["a", "b"])

    handled_data = preprocessor.handle_missing_values(
        input=input, option="replace", replace_value=0
    )
    assert handled_data.to_dict(orient="list") == pd.DataFrame(
        [[1.0, 0.0], [0.0, 2.0], [3.0, 4.0]], columns=["a", "b"]
    ).to_dict(orient="list")
