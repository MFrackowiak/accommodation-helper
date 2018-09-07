from abc import ABC, abstractmethod
from typing import List, Optional

from models.property import AdvertisedProperty


class AdvertisedPropertyIRepository(ABC):
    @abstractmethod
    def save(self, advertised_property: AdvertisedProperty):
        pass

    @abstractmethod
    def update(self, advertised_property: AdvertisedProperty):
        pass

    @abstractmethod
    def get(self, property_id: int) -> Optional[AdvertisedProperty]:
        pass

    @abstractmethod
    def list_flagged(self) -> List[AdvertisedProperty]:
        pass

    @abstractmethod
    def list_all(self) -> List[AdvertisedProperty]:
        pass

    @abstractmethod
    def delete_all(self):
        pass

    @abstractmethod
    def get_last_from(self, provider) -> Optional[AdvertisedProperty]:
        pass

    @abstractmethod
    def list_ok(self) -> List[AdvertisedProperty]:
        pass