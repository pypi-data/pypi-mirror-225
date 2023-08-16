from typing import Any, Sequence

import random

from ._interface import TraderInterface


class SimulationTrader(TraderInterface):
    """
    A trader component simulating the actual tradings.
    """

    def make_request(self, *, tickers: Sequence[str]) -> dict[str, Any]:
        # measure the close price of yesterday
        return {"total_close_price": random.uniform(100, 300)}
