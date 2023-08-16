from typing import Literal, Any

import pandas as pd

from earningtrader.common.exceptions import ValidationError
from ._interface import DataPreprocessorInterface


class DataPreprocessor(DataPreprocessorInterface):
    def rearrange_raw_data(
        self, *, input: pd.DataFrame, data_schema: pd.Index
    ) -> pd.DataFrame:
        if not data_schema.difference(input.columns).empty:
            raise ValidationError(
                "There are missing fields in the returned dataframe "
                "compared to the provided schema"
            )

        input.drop(columns=input.columns.difference(data_schema), inplace=True)
        return input

    def handle_missing_values(
        self,
        *,
        input: pd.DataFrame,
        option: Literal["exclude", "replace"],
        replace_value: Any = None,
    ) -> pd.DataFrame:
        if option == "exclude":
            input.dropna(axis=0, inplace=True)  # axis=0: drop raws
        elif option == "replace":
            input.fillna(value=replace_value, inplace=True)
        else:
            raise NotImplementedError(f"The option {option} is not implemented.")

        return input
