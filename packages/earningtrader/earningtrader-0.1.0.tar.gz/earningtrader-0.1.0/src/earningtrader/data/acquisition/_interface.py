from abc import ABC, abstractmethod

import pandas as pd


class DataFetcherInterface(ABC):
    """
    The interface for the data fetchers.
    """

    @abstractmethod
    def fetch_history_data(self, *, ticker: str, period: str) -> pd.DataFrame:
        """
        Fetch the data according to a given list of options.
        """
        ...
