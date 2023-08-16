from abc import ABC, abstractmethod
from dataclasses import dataclass


class StateInterface(ABC):
    """
    A representation of a single unit of the current entire state.
    """

    ...


@dataclass(frozen=True)
class ActionInterface(ABC):
    """
    Actions to be taken by the algorithm.
    """

    ...


@dataclass(frozen=True)
class RewardInterface(ABC):
    """
    The value of the reward earned as the result of the taken action.
    """

    ...


class RLTradingModelInterface(ABC):
    """
    The interface for RL trading models.
    """

    _state: StateInterface

    @property
    def state(self) -> StateInterface:
        ...

    @abstractmethod
    def take_action(self) -> ActionInterface:
        """
        Take an action based on the current parameters and the state given.
        """
        ...

    @abstractmethod
    def earn_reward(self, *, reward: RewardInterface) -> None:
        """
        Earn the reward as the result of the action taken, and update the parameter.
        """
        ...
