from copy import deepcopy
from unittest import TestCase

from .test_repo import BaseTestRepository, create_advertised_1, \
    advertised_1_dict
from repositories.sql_repository import SqlAdvertisedPropertyRepository


class TestSqliteRepository(BaseTestRepository, TestCase):
    def setUp(self):
        self.repo = SqlAdvertisedPropertyRepository('test-db.db', False)
        self.default = {}

    def tearDown(self):
        self.repo.finalize_session()

    def test_property_to_dict(self):
        property_dict = self.repo._property_to_dict(create_advertised_1())
        expected_dict = deepcopy(advertised_1_dict)
        expected_dict.pop('property_id')

        self.assertDictEqual(property_dict, expected_dict)

    def test_property_save(self):
        advertised_1 = create_advertised_1()
        self.repo.save(advertised_1)
        self.assertIsNotNone(advertised_1.property_id)