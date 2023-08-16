import logging

from earningtrader.data.acquisition.yfinance import YFinanceFetcher
from earningtrader.data.preprocessing.preprocessor import DataPreprocessor
from earningtrader.model import StateInterface
from earningtrader.model.bernoulli_ts import (
    BernTSAction,
    BernTSReward,
    BernTSState,
    BernTSTradingModel,
)
from earningtrader.trader.simulation_trader import SimulationTrader
from earningtrader.storage.shelve_storage import ShelveStorage

from ._interface import ControllerInterface, ControllerBuilderInterface
from ._logger import PythonFileLogger


class BernTSController(ControllerInterface):
    """
    A controller demonstrating a simulation using
      - Bernoulli Thompson Sampling
      - YFinance data
    """

    _data_fetcher: YFinanceFetcher
    _data_preprocessor: DataPreprocessor
    _model: BernTSTradingModel
    _trader: SimulationTrader
    _storage: ShelveStorage

    _stdout_logger: PythonFileLogger
    _stderr_logger: PythonFileLogger

    def __init__(self) -> None:
        self._stdout_logger = PythonFileLogger(
            logger_name="bern_ts_controller_stdout_logger",
            filepath="bern_ts_stdout.log",
            message_format="[log]: %(asctime)s %(message)s",
        )

        self._stderr_logger = PythonFileLogger(
            logger_name="bern_ts_controller_stderr_logger",
            filepath="bern_ts_stderr.log",
            message_format="[error]: %(asctime)s %(message)s",
        )

    def observe_state(self) -> StateInterface:
        """
        Not used in this simulator - Thompson Sampling doesn't require observation
        of the state before taking action.
        """
        raise NotImplementedError("Not required for this simulation.")

    def choose_action(self) -> BernTSAction:
        try:
            action = self._model.take_action()
            self._stdout_logger.log(
                message="complete: take_action", log_level=logging.INFO
            )
            return action

        except Exception as error:
            self._stderr_logger.log(message=error)
            raise

    def make_trade(self, *, action: BernTSAction) -> BernTSReward:
        try:
            buy_price = self._trader.make_request(tickers=[action.key]).get(
                "total_close_price"
            )

            # compare it with the previous day's price
            previous_buy_price = self._storage.load_data(key="previous_buy_price")
            self._storage.store_data(key="previous_buy_price", value=buy_price)

            increment_ratio = (
                max(buy_price - previous_buy_price, 0.0) / previous_buy_price
            )
            increment_ratio = min(increment_ratio, 1.0)
            self._stdout_logger.log(
                message="complete: make_trade", log_level=logging.INFO
            )

            return BernTSReward(action_id=action.id, reward=increment_ratio)

        except Exception as error:
            self._stderr_logger.log(message=error)
            raise

    def save_reward(self, *, reward: BernTSReward) -> None:
        try:
            reward_history = self._storage.load_data(key="reward_history")
            reward_history.append(reward)
            self._storage.store_data(key="reward_history", value=reward_history)
            self._stdout_logger.log(message="complete: save reward")

        except Exception as error:
            self._stderr_logger.log(message=error)
            raise


class BernTSControllerBuilder(ControllerBuilderInterface):
    _controller: BernTSController

    def controller(self) -> BernTSController:
        if self._controller._data_fetcher is None:
            raise AttributeError(
                "the fetcher attribute has not been setup yet: "
                "call set_data_fetcher()"
            )

        if self._controller._data_preprocessor is None:
            raise AttributeError(
                "the _data_preprocessor attribute has not been setup yet: "
                "call set_data_preprocessor()"
            )
        if self._controller._model is None:
            raise AttributeError(
                "the _model attribute has not been setup yet: "
                "call set_trading_model()"
            )

        if self._controller._trader is None:
            raise AttributeError(
                "the _trader attribute has not been setup yet: " "call set_trader()"
            )

        if self._controller._storage is None:
            raise AttributeError(
                "the _storage attribute has not been setup yet: " "call set_trader()"
            )

        return self._controller

    def initialize(self) -> None:
        self._controller = BernTSController()

    def set_data_fetcher(self) -> None:
        self._controller._data_fetcher = YFinanceFetcher()

    def set_data_preprocessor(self) -> None:
        self._controller._data_preprocessor = DataPreprocessor()

    def set_trading_model(self) -> None:
        actions = set(
            [
                BernTSAction(id="microsoft", key="MSFT"),
                BernTSAction(id="apple", key="AAPL"),
                BernTSAction(id="google", key="GOOG"),
            ]
        )

        state = BernTSState(
            parameters_with_action_ids={
                "microsoft": [2.0, 2.0],
                "apple": [2.0, 2.0],
                "google": [2.0, 2.0],
            }
        )

        model = BernTSTradingModel(actions=actions, state=state)

        self._controller._model = model

    def set_trader(self) -> None:
        self._controller._trader = SimulationTrader()

    def set_storage(self) -> None:
        storage = ShelveStorage(db_path="temp_storage.shelve")
        storage.store_data(key="previous_buy_price", value=100.0)
        storage.store_data(key="reward_history", value=[])

        self._controller._storage = storage
