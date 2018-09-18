from datetime import datetime
from unittest import TestCase

from collectors.accomodation import AccommodationCollector
from collectors.scrappers.dummy import DummyAccommodationScrapper
from collectors.scrappers.base import ParsedAccommodation
from models.advertised_property import AdvertisedProperty
from reporting.json_file import JsonCrawlingReporter, JsonCrawlingReporterConfig
from repositories.in_memory_repository import \
    InMemoryAdvertisedPropertyRepository


def mock_parsed_accomodation(
        entered: datetime, url: str) -> ParsedAccommodation:
    return ParsedAccommodation(
        url=url,
        address='Some nice address in Dublin',
        entered=entered,
        price=1100,
        provider='test',
        description='Oh god yes',
    )


def mock_advertised(url):
    return AdvertisedProperty(
        url=url,
        address='Some nice address in Dublin',
        price=1200,
        provided_by='test',
        entered=datetime(2018, 9, 1, 19, 32, 10),
        flagged=False,
        sent_email=True,
        ok=True,
    )


accomodations = [
    mock_parsed_accomodation(
        datetime(2018, 9, 9, 20, 0, 0),
        'http://first.dum'),
    mock_parsed_accomodation(
        datetime(2018, 9, 9, 19, 30, 0),
        'http://second.dum'),
    mock_parsed_accomodation(
        datetime(2018, 9, 9, 19, 0, 0),
        'http://let.dum'),
    mock_parsed_accomodation(
        datetime(2018, 9, 9, 18, 0, 0),
        'http://first.rent'),
    mock_parsed_accomodation(
        datetime(2018, 9, 9, 16, 45, 0),
        'http://first.rent.x'),
    mock_parsed_accomodation(
        datetime(2018, 9, 9, 13, 0, 0),
        'http://damn.dum'),
    mock_parsed_accomodation(
        datetime(2018, 9, 9, 12, 0, 0),
        'http://tested.dum'),
    mock_parsed_accomodation(
        datetime(2018, 9, 9, 8, 0, 0),
        'http://yup.dum'),
    mock_parsed_accomodation(
        datetime(2018, 9, 8, 22, 0, 0),
        'http://nah.dum'),
    mock_parsed_accomodation(
        datetime(2018, 9, 8, 21, 0, 0),
        'http://kek.dum'),
    mock_parsed_accomodation(
        datetime(2018, 9, 8, 20, 0, 0),
        'http://cd.dum'),
]


class AccomodationCollectorStopTestCase(TestCase):
    def setUp(self):
        self.collector = AccommodationCollector(
            DummyAccommodationScrapper([]),
            InMemoryAdvertisedPropertyRepository(),
            JsonCrawlingReporter(
                JsonCrawlingReporterConfig('test.json', False)),
        )

    def test_stop_limit(self):
        stop_func = self.collector._create_stop_condition(limit=5)

        for i, accom in enumerate(accomodations[:5]):
            self.assertFalse(stop_func(i, accom))
        self.assertTrue(stop_func(5, accomodations[5]))
        self.assertTrue(stop_func(6, accomodations[6]))

    def test_stop_date(self):
        stop_func = self.collector._create_stop_condition(
            entered=datetime(2018, 9, 9, 15, 0, 0))
        for i, accom in enumerate(accomodations[:5]):
            self.assertFalse(stop_func(i, accom))
        for i, accom in enumerate(accomodations[5:]):
            self.assertTrue(stop_func(i + 5, accom))

        stop_func = self.collector._create_stop_condition(
            entered=datetime(2018, 9, 9, 0, 0, 0))
        for i, accom in enumerate(accomodations[:8]):
            self.assertFalse(stop_func(i, accom))
        for i, accom in enumerate(accomodations[8:]):
            self.assertTrue(stop_func(i + 8, accom))

    def test_stop_till_known(self):
        stop_func = self.collector._create_stop_condition(
            last_from_provider=mock_advertised('http://kek.dum'))
        for i, accom in enumerate(accomodations[:9]):
            self.assertFalse(stop_func(i, accom))
        self.assertTrue(stop_func(9, accomodations[9]))

    def test_stop_multiple(self):
        pass
