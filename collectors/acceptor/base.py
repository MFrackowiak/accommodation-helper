from abc import abstractmethod, ABC
from enum import Enum

from collectors.scrappers.base import ParsedAccommodation


class AcceptorResponse(Enum):
    REJECT = 1
    VERIFY = 2
    ACCEPT = 3
    DUPLICATE = 4


class Acceptor(ABC):
    requires_repository = False
    name = 'BaseAbstractAcceptor'

    @abstractmethod
    def is_ok(self, found_property: ParsedAccommodation) -> AcceptorResponse:
        pass

    @abstractmethod
    def provide_reason(self) -> str:
        pass