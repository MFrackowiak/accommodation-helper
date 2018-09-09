from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Callable, List

from collectors.acceptor.base import Acceptor, AcceptorResponse
from collectors.scrappers.scrapper import AccommodationScrapper, \
    ParsedAccommodation
from models.property import AdvertisedProperty
from config.config import application_config
from repositories.property import AdvertisedPropertyIRepository
from utils.dynamic_loading import import_string


@dataclass
class AcceptorsDecision:
    decision: AcceptorResponse
    voted_verify: List[str]
    verify_reason: List[str]
    voted_reject: str
    reject_reason: str


class AccommodationCollector:
    def __init__(self, scrapper: AccommodationScrapper,
                 repository: AdvertisedPropertyIRepository):
        self.scrapper: AccommodationScrapper = scrapper
        self.repository = repository
        self.acceptors: List[Acceptor] = []

        for acceptor in application_config.collector.acceptors:
            acceptor_cls = import_string(acceptor.cls)
            kwargs = acceptor.config
            if acceptor_cls.requires_repository:
                kwargs.update(repository=repository)
            self.acceptors.append(acceptor_cls(**kwargs))

    def find_till(self, last_from_provider: Optional[AdvertisedProperty] = None,
                  limit: int = 100, entered: Optional[datetime] = None):
        stop_func = self._create_stop_condition(
            last_from_provider, limit, entered)

        for i, scrapped in enumerate(self.scrapper.generate_pages()):

            decision = self._check_decision(scrapped)

            if stop_func(i, scrapped):
                break

    def _check_decision(self, parsed_accommodation: ParsedAccommodation
                        ) -> AcceptorsDecision:
        decision = AcceptorsDecision(AcceptorResponse.ACCEPT, [], [], [], [])

        for acceptor in self.acceptors:
            acceptor_vote = acceptor.is_ok(parsed_accommodation)

            if acceptor_vote == AcceptorResponse.REJECT or \
                    AcceptorResponse.DUPLICATE:
                decision.decision = acceptor_vote
                decision.reject_reason = acceptor.provide_reason()
                decision.voted_reject = acceptor.name
                break
            elif acceptor_vote == AcceptorResponse.VERIFY:
                decision.decision = acceptor_vote
                decision.verify_reason.append(acceptor.provide_reason())
                decision.voted_verify.append(acceptor.name)

        return decision

    def _create_stop_condition(
            self, last_from_provider: Optional[AdvertisedProperty] = None,
            limit: int = 100, entered: Optional[datetime] = None) -> Callable:
        if not any([last_from_provider, limit, entered]):
            raise ValueError('At least one condition is required!')

        conditions = []

        if last_from_provider:
            def equals_last_checked(_: int, scrapped: ParsedAccommodation):
                return scrapped.url == last_from_provider.url

            conditions.append(equals_last_checked)
        if limit:
            conditions.append(lambda i, _: i >= limit)
        if entered:
            def older_than(_: int, scrapped: ParsedAccommodation):
                return scrapped.entered < entered

            conditions.append(older_than)

        return lambda i, scrapped: any(
            map(lambda func: func(i, scrapped), conditions))
