from typing import Literal

import pandas as pd
import yfinance as yf

from ._interface import DataFetcherInterface


class YFinanceFetcher(DataFetcherInterface):
    """
    An adapter class for the yfinance package(https://github.com/ranaroussi/yfinance).

    After investing some time on this open source, we may switch to use the original
    APIs directly: see https://financeapi.net/.
    """

    def fetch_history_data(self, *, ticker: str, period: Literal["1d"]) -> pd.DataFrame:
        return yf.Ticker(ticker).history(period=period)
