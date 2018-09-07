from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ParsedAccommodation:
    url: str
    address: str
    entered: datetime
    price: int
    provider: str


class AccommodationScrapper:
    def next_page(self):
        pass

    def read_from_page(self) -> List[ParsedAccommodation]:
        pass


def accomodation_generator(scraper: AccommodationScrapper):
    while True:
        for advertised_property in scraper.read_from_page():
            yield advertised_property
        scraper.next_page()
