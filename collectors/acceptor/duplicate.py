from dataclasses import field, dataclass
from enum import Enum
from typing import Optional, List

from collectors.acceptor.base import Acceptor, AcceptorResponse
from collectors.scrappers.base import ParsedAccommodation
from repositories.base import AdvertisedPropertyRepository


@dataclass
class DuplicateConfig:
    cut_off_threshold: float
    verify_threshold: float = field(default=None)

class FindingType(Enum):
    URL = 1
    ADDRESS = 2


class DuplicateAcceptor(Acceptor):
    requires_repository = True
    name = 'DuplicateAcceptor'

    @dataclass
    class LastFinding:
        finding_type:FindingType
        looked_for: str
        similar_urls: List[str] = field(default=())

    def __init__(self, repository: AdvertisedPropertyRepository,
                 config: Optional[DuplicateConfig], **kwargs):
        self.repository = repository
        self.config = config or DuplicateConfig(**kwargs)
        self.last_result: Optional[self.LastFinding] = None

    def provide_reason(self) -> str:
        if self.last_result is None:
            raise ValueError('Cannot provide reason')
        elif self.last_result.finding_type == FindingType.URL:
            return f'The url {self.last_result.looked_for} was already in ' \
                   f'the database.'
        elif self.last_result.finding_type == FindingType.ADDRESS:
            return f'The address {self.last_result.looked_for} was too ' \
                   f'similar to following properties: ' \
                   f'{", ".join(self.last_result.similar_urls)}.'

    def is_ok(self, found_property: ParsedAccommodation) -> AcceptorResponse:
        if len(self.repository.list_with_url(found_property.url)) > 0:
            self.last_result = self.LastFinding(
                FindingType.URL, found_property.url)
            return AcceptorResponse.DUPLICATE
        similar_address = self.repository.list_with_similar_address(
            found_property.address, self.config.cut_off_threshold)

        if similar_address:
            self.last_result = self.LastFinding(
                FindingType.ADDRESS, found_property.address,
                [similar.url for similar in similar_address])
            if self.config.verify_threshold and all(
                    map(lambda result: result[1]
                                       <= self.config.verify_threshold,
                        similar_address)
            ):
                return AcceptorResponse.VERIFY
            else:
                return AcceptorResponse.DUPLICATE
        return AcceptorResponse.ACCEPT
