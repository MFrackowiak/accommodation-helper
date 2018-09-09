from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class ParsedAccommodation:
    url: str
    address: str
    entered: datetime
    price: int
    provider: str
    description: str = field(default='')


class AccommodationScrapper(ABC):
    @abstractmethod
    def next_page(self):
        pass

    @abstractmethod
    def read_from_page(self) -> List[ParsedAccommodation]:
        pass

    def generate_pages(self):
        while True:
            for advertised_property in self.read_from_page():
                yield advertised_property
            self.next_page()

    @abstractmethod
    def contact_advertiser(self):
        pass
