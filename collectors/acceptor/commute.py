from dataclasses import field, dataclass
from typing import Optional

from collectors.acceptor.base import Acceptor, AcceptorResponse
from collectors.api.commute.base import CommuteAPI, CommuteRequest
from collectors.scrappers.base import ParsedAccommodation
from config.config import application_config
from utils.dynamic_loading import import_string


@dataclass
class CommuteConfig:
    check_to: str
    max_commute: int
    api_cls: str = field(default='collectors.api.commute.dummy.DummyCommuteAPI')
    max_verify: Optional[int] = field(default=None)
    verify_unknown: bool = field(default=True)
    allow_normalize_from: bool = field(default=True)
    allow_normalize_to: bool = field(default=True)


class CommuteAcceptor(Acceptor):
    name = 'CommuteTimeAcceptor'

    def __init__(self, config: Optional[CommuteConfig] = None, **kwargs):
        self.config = config or CommuteConfig(**kwargs)
        self.api: CommuteAPI = import_string(
            self.config.api_cls)(application_config)
        self.last_commute = None

    def is_ok(self, found_property: ParsedAccommodation) -> AcceptorResponse:
        request = CommuteRequest(
            to_address=self.config.check_to,
            from_address=found_property.address,
            clean_from=self.config.allow_normalize_from,
            clean_to=self.config.allow_normalize_to,
        )
        self.last_commute = self.api.check_commute_time(request)
        if self.last_commute is None:
            return AcceptorResponse.VERIFY if self.config.verify_unknown \
                else AcceptorResponse.REJECT
        elif self.last_commute <= self.config.max_commute:
            return AcceptorResponse.ACCEPT
        elif self.config.max_verify and \
                self.last_commute <= self.config.max_verify:
            return AcceptorResponse.VERIFY
        return AcceptorResponse.REJECT

    def provide_reason(self):
        return f'The {self.config.api_cls} return commute time ' \
               f'{self.last_commute}; max commute time to accept is ' \
               f'{self.config.max_commute} and to verify is ' \
               f'{self.config.max_verify}'
