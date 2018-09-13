from unittest import TestCase

from collectors.api.commute.dummy import DummyCommuteAPI
from collectors.api.commute.base import CommuteRequest

def mock_request(from_address):
    return CommuteRequest(
        from_address=from_address,
        to_address='some random address',
    )



class DummyCommuteAPITestCase(TestCase):
    def setUp(self):
        self.commute_api = DummyCommuteAPI()

    def test_nice_location(self):
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('nice location somewhere')
        ), 50)
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Nice Address, Dublin 42')
        ), 50)

    def test_rathmines_location(self):
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Rathmines Ave, Rathmines, Dublin 6')
        ), 40)
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Next to this pub in Rathmines')
        ), 40)

    def test_expensive_location(self):
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Quite Expensive, Dublin 16')
        ), 20)
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('expensive studio, Dundrum')
        ), 20)

    def test_close_location(self):
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Really close to the office, Dublin 18')
        ), 10)
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Closest, Heather Road, Dublin 18')
        ), 10)

    def test_unknown_location(self):
        self.assertIsNone(self.commute_api.check_commute_time(
            mock_request('oh where is it')))
        self.assertIsNone(self.commute_api.check_commute_time(
            mock_request('no one nows')))
