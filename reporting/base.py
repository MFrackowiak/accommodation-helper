from abc import abstractmethod, ABC

from collectors.scrappers.base import ParsedAccommodation


class CrawlingReporter(ABC):
    @abstractmethod
    def report_property_to_verify(self, advertisement: ParsedAccommodation,
                                  acceptor: str, reason: str):
        pass

    @abstractmethod
    def report_property_accepted(self, advertisement: ParsedAccommodation,
                                 sent_email: bool):
        pass