from dataclasses import field, dataclass
from typing import Optional

from collectors.acceptor.base import Acceptor, AcceptorResponse
from collectors.scrappers.scrapper import ParsedAccommodation
from repositories.property import AdvertisedPropertyIRepository


@dataclass
class DuplicateConfig:
    cut_off_threshold: float
    verify_threshold: float = field(default=None)


class DuplicateAcceptor(Acceptor):
    requires_repository = True
    name = 'DuplicateAcceptor'

    def __init__(self, repository: AdvertisedPropertyIRepository,
                 config: Optional[DuplicateConfig], **kwargs):
        self.repository = repository
        self.config = config or DuplicateConfig(**kwargs)

    def is_ok(self, found_property: ParsedAccommodation) -> AcceptorResponse:
        if len(self.repository.list_with_url(found_property.url)) > 0:
            return AcceptorResponse.DUPLICATE
        similar_address = self.repository.list_with_similar_address(
                found_property.address, self.config.cut_off_threshold)

        if similar_address:
            if self.config.verify_threshold and all(
                map(lambda result: result[1] <= self.config.verify_threshold,
                    similar_address)
            ):
                return AcceptorResponse.VERIFY
            else:
                return AcceptorResponse.DUPLICATE
        return AcceptorResponse.ACCEPT
