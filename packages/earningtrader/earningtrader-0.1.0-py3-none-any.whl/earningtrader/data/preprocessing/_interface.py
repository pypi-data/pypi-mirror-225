from typing import Literal, Any
from abc import ABC, abstractmethod

import pandas as pd


class DataPreprocessorInterface(ABC):
    """
    The interface for the data preprocessing components.
    """

    @abstractmethod
    def rearrange_raw_data(
        *, self, input: pd.DataFrame, data_schema: pd.Index
    ) -> pd.DataFrame:
        """
        Check whether the input data satisfies the schema provided.

        Otherwise, it will raise ValidationError.
        """
        ...

    @abstractmethod
    def handle_missing_values(
        *,
        self,
        input: pd.DataFrame,
        option: Literal["exclude", "replace"],
        replace_value: Any,
    ) -> pd.DataFrame:
        """
        Handles missing values in the pd.DataFrame(NaN).

        So this function is a wrapper of the more general APIs explained here
        in this guide: https://pandas.pydata.org/docs/user_guide/missing_data.html.

        Note that when the option is 'exclude', any value passed to
        'replace_value' parameter will be ignored.
        """
        ...
