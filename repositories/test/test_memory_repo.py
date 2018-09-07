from unittest import TestCase

from repositories.in_memory_repository import \
    InMemoryAdvertisedPropertyRepository
from repositories.test.test_repo import TestRepository


class MemoryTestCase(TestRepository, TestCase):
    def setUp(self):
        self.repo = InMemoryAdvertisedPropertyRepository()
        self.default = {}

    def tearDown(self):
        self.repo.delete_all()
