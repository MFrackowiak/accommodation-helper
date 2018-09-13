from unittest import TestCase

from collectors.api.commute.dublin_postcode import DublinPostcodeCommuteAPI
from collectors.api.commute.test.test_dummy import mock_request


class DublinPostcodeCommuteAPITestCase(TestCase):
    def setUp(self):
        self.commute_api = DublinPostcodeCommuteAPI({
            'dublin-zip-commute-api': {
                '1': 50,
                '6W': 45,
                '6': 40,
                '18': 5,
                '16': 23,
            },
        })

    def test_unknown(self):
        self.assertIsNone(self.commute_api.check_commute_time(
            mock_request('12 Ave, Monkstown, Co. Dublin')))
        self.assertIsNone(self.commute_api.check_commute_time(
            mock_request('12 Sea, Bray, Co. Wicklow')))

    def test_not_in_config(self):
        self.assertIsNone(self.commute_api.check_commute_time(
            mock_request('13 Xd, Center, Dublin 3')))
        self.assertIsNone(self.commute_api.check_commute_time(
            mock_request('Red Line, Watch Yourself, Dublin 7')))

    def test_in_config(self):
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Doblin 18, Dublin 1')), 50)
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Somewhere in Dublin 16')), 23)
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Dublin 18, D18XC72')), 5)

    def test_6_and_6w(self):
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Doblin 18, Dublin 6')), 40)
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Somewhere in Dublin 6W')), 45)
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Somewhere in dublin 6w')), 45)
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Dublin 6 w')), 40)

    def test_grab_first_group(self):
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Doblin 18, Dublin 1, Dublin 6')), 50)
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Somewhere in Dublin 16, Dublin 1')), 23)
        self.assertEqual(self.commute_api.check_commute_time(
            mock_request('Dublin 18, D18XC72, Dublin 6w')), 5)