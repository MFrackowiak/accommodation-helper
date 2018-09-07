from abc import ABC, abstractmethod
from typing import List

from models.property import AdvertisedProperty


class AdvertisedPropertyIRepository(ABC):
    @abstractmethod
    def save(self, advertised_property: AdvertisedProperty):
        pass

    @abstractmethod
    def update(self, advertised_property: AdvertisedProperty):
        pass

    @abstractmethod
    def get(self, property_id: int) -> AdvertisedProperty:
        pass

    @abstractmethod
    def list_flagged(self) -> List[AdvertisedProperty]:
        pass

    @abstractmethod
    def list_mail_sent(self) -> List[AdvertisedProperty]:
        pass

    @abstractmethod
    def list_all(self) -> List[AdvertisedProperty]:
        pass
