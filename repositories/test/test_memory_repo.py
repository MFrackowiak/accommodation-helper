from unittest import TestCase

from repositories.in_memory_repository import \
    InMemoryAdvertisedPropertyRepository
from .test_repo import BaseTestRepository


class MemoryTestCase(BaseTestRepository, TestCase):
    def setUp(self):
        self.repo = InMemoryAdvertisedPropertyRepository()
        self.default = {}

    def tearDown(self):
        self.repo.delete_all()
