from collections import OrderedDict
from dataclasses import asdict
from typing import List, Dict, Optional

from models.property import AdvertisedProperty
from repositories.property import AdvertisedPropertyIRepository


class InMemoryAdvertisedPropertyRepository(AdvertisedPropertyIRepository):
    _repo: Dict[int, Dict] = OrderedDict()
    _last_id = 0

    def _property_to_dict(self, advertised_property: AdvertisedProperty):
        return asdict(advertised_property)

    def save(self, advertised_property: AdvertisedProperty):
        self._last_id = self._last_id + 1

        advertised_property.property_id = self._last_id
        self._repo[self._last_id] = self._property_to_dict(advertised_property)

    def update(self, advertised_property: AdvertisedProperty):
        self._repo[advertised_property.property_id] = \
            self._property_to_dict(advertised_property)

    def get(self, property_id: int) -> Optional[AdvertisedProperty]:
        stored_dict = self._repo.get(property_id)

        if stored_dict:
            return AdvertisedProperty(**stored_dict)
        return stored_dict

    def list_flagged(self) -> List[AdvertisedProperty]:
        return list(map(lambda d: AdvertisedProperty(**d),
                        filter(lambda d: d['flagged'], self._repo.values())))

    def list_all(self) -> List[AdvertisedProperty]:
        return list(map(lambda d: AdvertisedProperty(**d), self._repo.values()))

    def get_last_from(self, provider) -> Optional[AdvertisedProperty]:
        from_provider = sorted(
            filter(lambda d: d['provided_by'] == provider,
                   self._repo.values()),
            key=lambda d: d['entered'],
            reverse=True,
        )
        if not from_provider:
            return None
        return AdvertisedProperty(**from_provider[0])

    def delete_all(self):
        InMemoryAdvertisedPropertyRepository._repo = OrderedDict()
        InMemoryAdvertisedPropertyRepository._last_id = 0

    def list_ok(self):
        return list(map(lambda d: AdvertisedProperty(**d),
                        filter(lambda d: d['ok'], self._repo.values())))

    def list_with_url(self, url: str) -> List[AdvertisedProperty]:
        return list(map(lambda d: AdvertisedProperty(**d),
                        filter(lambda d: d['url'] == url, self._repo.values())))

    def list_with_similar_address(
            self, address: str, similarity_threshold: float = 0.5
    ) -> List[AdvertisedProperty]:
        # TODO proper distance
        address = address.lower()
        return list(
            map(lambda d: AdvertisedProperty(**d),
                filter(lambda d: address in d['address'].lower(),
                       self._repo.values())))
