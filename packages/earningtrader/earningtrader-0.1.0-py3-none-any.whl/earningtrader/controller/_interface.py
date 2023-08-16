from abc import ABC, abstractmethod

from earningtrader.model import (
    StateInterface,
    ActionInterface,
    RewardInterface,
)


class ControllerInterface(ABC):
    """
    The interface for the central component controlling the other components.
    """

    @abstractmethod
    def observe_state(self) -> StateInterface:
        """
        A factory method for converting external data into a defined state.
        """
        ...

    @abstractmethod
    def choose_action(self, *, observed_state: StateInterface) -> ActionInterface:
        """
        Given the observed state, choose the action using the RL model.
        """
        ...

    @abstractmethod
    def make_trade(self, *, action: ActionInterface) -> RewardInterface:
        """
        Take the action determined from the model, and
        return the reward from the actual trading.
        """
        ...

    @abstractmethod
    def save_reward(self, *, reward: RewardInterface) -> None:
        """
        Save the reward to assess the performance of the model.
        """
        ...


class ControllerBuilderInterface(ABC):
    @abstractmethod
    def initialize(self) -> None:
        ...

    @abstractmethod
    def set_data_fetcher(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def set_data_preprocessor(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def set_trading_model(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def set_trader(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def set_storage(self, *args, **kwargs) -> None:
        ...
