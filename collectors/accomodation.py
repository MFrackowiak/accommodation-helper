from datetime import datetime
from typing import Optional, Callable

from collectors.scrapper import AccommodationScrapper, accomodation_generator, \
    ParsedAccommodation
from models.property import AdvertisedProperty


class AccommodationCollector:
    def __init__(self, scrapper: AccommodationScrapper):
        self.scrapper = scrapper

    def find_till(self, last_from_provider: Optional[AdvertisedProperty] = None,
                  limit: int = 100, entered: Optional[datetime] = None):
        stop_func = self._create_stop_condition(
            last_from_provider, limit, entered)

        for i, scrapped in enumerate(accomodation_generator(self.scrapper)):
            # do something with scrapped
            if stop_func(i, scrapped):
                break

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
            conditions.append(lambda i, _: i == limit)
        if entered:
            def older_than(_: int, scrapped: ParsedAccommodation):
                return scrapped.entered < entered
            conditions.append(older_than)

        return lambda i, scrapped: any(
            map(lambda func: func(i, scrapped), conditions))
