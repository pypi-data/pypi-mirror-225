from earningtrader.data.acquisition.yfinance import YFinanceFetcher


def test_yfinance_fetch_history_data():
    """
    Remark: currently this test is for the documentation purpose.

    However, when we implement our own yfinance API adaptor,
    this test will be used in the refactoring process.
    """

    ticker = "MSFT"

    fetcher = YFinanceFetcher()

    one_day = fetcher.fetch_history_data(ticker=ticker, period="1d")
    columns_set = set(map(lambda x: x.lower(), one_day.columns.values.tolist()))

    assert len(one_day) == 1
    assert len(set(["open", "close", "high", "low", "volume"]) - columns_set) == 0
