from dataclasses import field, dataclass, astuple
from typing import Optional

from collectors.acceptor.base import Acceptor, AcceptorResponse
from collectors.scrappers.scrapper import ParsedAccommodation


@dataclass
class PriceCheckConfig:
    accept_min: int = field(default=None)
    accept_max: int = field(default=None)
    verify_min: int = field(default=None)
    verify_max: int = field(default=None)


class PriceCheckAcceptor(Acceptor):
    def __init__(self, config: Optional[PriceCheckConfig] = None,
                 **kwargs):
        self.config = config or PriceCheckConfig(**kwargs)

        if not any(filter(lambda c: c is not None, astuple(config))):
            raise ValueError('Improperly configured!')

    def is_ok(self, found_property: ParsedAccommodation) -> AcceptorResponse:
        if self._in_range(found_property.price, self.config.accept_min,
                          self.config.accept_max):
            return AcceptorResponse.ACCEPT
        elif self._in_range(found_property.price, self.config.verify_min,
                            self.config.verify_max):
            return AcceptorResponse.VERIFY
        return AcceptorResponse.REJECT

    def _in_range(self, value: int, min_val: Optional[int],
                  max_val: Optional[int]) -> bool:
        if min_val is None and max_val is None:
            return False
        return (min_val is None or value >= min_val) and \
               (max_val is None or value <= max_val)
