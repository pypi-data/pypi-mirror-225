from typing import Sequence, Any
from abc import ABC, abstractmethod


class TraderInterface(ABC):
    """
    The interface for the trader component that actually
    makes trading API request to the external service vendors.
    """

    _api_base_url: str

    @abstractmethod
    def make_request(self, *, items: Sequence[str]) -> dict[str, Any]:
        """
        Make API requests to the external API vendor(s) and get the actual response.
        """
        ...
