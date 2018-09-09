from typing import List

from collectors.scrappers.base import AccommodationScrapper, \
    ParsedAccommodation


class DummyAccommodationScrapper(AccommodationScrapper):
    def __init__(self, list_to_return: List[ParsedAccommodation],
                 page_size: int=10):
        self.page = 0
        self.list_to_return = list_to_return
        self.page_size = page_size

    def next_page(self):
        self.page += 1

    def read_from_page(self) -> List[ParsedAccommodation]:
        return self.list_to_return[
               self.page * self.page_size:(self.page + 1) * self.page_size]

    def contact_advertiser(self):
        return True

