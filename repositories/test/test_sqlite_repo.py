from copy import deepcopy
from unittest import TestCase

from repositories.test.test_repo import TestRepository, create_advertised_1, \
    advertised_1_dict
from repositories.sqlite_repository import SqliteAdvertisedPropertyRepository


class TestSqliteRepository(TestRepository, TestCase):
    def setUp(self):
        self.repo = SqliteAdvertisedPropertyRepository('test-db.db', False)
        self.default = {}

    def tearDown(self):
        self.repo.finalize_session()

    def test_property_to_dict(self):
        property_dict = self.repo._property_to_dict(create_advertised_1())
        expected_dict = deepcopy(advertised_1_dict)
        expected_dict.pop('property_id')

        self.assertDictEqual(property_dict, expected_dict)

    def test_property_save(self):
        # TODO hm?
        pass