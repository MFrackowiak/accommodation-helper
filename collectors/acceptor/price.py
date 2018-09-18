from dataclasses import field, dataclass, astuple
from typing import Optional

from collectors.acceptor.base import Acceptor, AcceptorResponse
from collectors.scrappers.base import ParsedAccommodation


@dataclass
class PriceCheckConfig:
    accept_min: int = field(default=None)
    accept_max: int = field(default=None)
    verify_min: int = field(default=None)
    verify_max: int = field(default=None)


class PriceCheckAcceptor(Acceptor):
    name = 'PriceAcceptor'

    def __init__(self, config: Optional[PriceCheckConfig] = None,
                 **kwargs):
        self.config = config or PriceCheckConfig(**kwargs)
        self.last_checked_value = ''

        if not any(filter(lambda c: c is not None, astuple(self.config))):
            raise ValueError('Improperly configured!')

    def is_ok(self, found_property: ParsedAccommodation) -> AcceptorResponse:
        self.last_checked_value = found_property.price
        if self._in_range(found_property.price, self.config.accept_min,
                          self.config.accept_max):
            return AcceptorResponse.ACCEPT
        elif self._in_range(found_property.price, self.config.verify_min,
                            self.config.verify_max):
            return AcceptorResponse.VERIFY
        return AcceptorResponse.REJECT

    @classmethod
    def _na_if_none(cls, value):
        return 'n/a' if value is None else value

    def provide_reason(self) -> str:
        return f'Price may not fit in accept range: ' \
               f'{self._na_if_none(self.config.accept_min)} to' \
               f' {self._na_if_none(self.config.accept_max)} or verify range:' \
               f' {self._na_if_none(self.config.verify_min)} to' \
               f' {self._na_if_none(self.config.verify_max)}, provided price:' \
               f' {self._na_if_none(self.last_checked_value)}.'

    @staticmethod
    def _in_range(value: int, min_val: Optional[int],
                  max_val: Optional[int]) -> bool:
        if min_val is None and max_val is None:
            return False
        return (min_val is None or value >= min_val) and \
               (max_val is None or value <= max_val)
