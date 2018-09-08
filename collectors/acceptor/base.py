from abc import abstractmethod, ABC
from enum import Enum

from collectors.scrapper import ParsedAccommodation


class AcceptorResponse(Enum):
    REJECT = 1
    VERIFY = 2
    ACCEPT = 3


class Acceptor(ABC):
    @abstractmethod
    def is_ok(self, found_property: ParsedAccommodation) -> AcceptorResponse:
        pass