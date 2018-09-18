from datetime import datetime
from unittest import TestCase
from mock import patch

from collectors.acceptor.base import AcceptorResponse
from collectors.scrappers.base import ParsedAccommodation

overwritten_app_config = {
    'dublin-zip-commute-api': {
        '1': 50,
        '2': 60,
        '8': 30,
        '6': 40,
        '6w': 45,
        '18': 20
    },
}

with patch('config.config.application_config', overwritten_app_config):
    from collectors.acceptor.commute import CommuteConfig, CommuteAcceptor

def mock_accommodation(address: str) -> ParsedAccommodation:
    return ParsedAccommodation('dummy.url', address, datetime.now(),
                               1200, 'test')


class CommuteAcceptorTestCase(TestCase):
    def setUp(self):
        # from collectors.acceptor.commute import CommuteConfig
        self.dummy_config = CommuteConfig(
            check_to='Heather House, Heather Road, Dublin 16',
            max_commute=30,
            max_verify=45,
            api_cls='collectors.api.commute.'
                    'dublin_postcode.DublinPostcodeCommuteAPI',
        )

    def test_dont_verify_none(self):
        self.dummy_config.verify_unknown = False
        self.acceptor = CommuteAcceptor(self.dummy_config)
        self.assertEqual(
            self.acceptor.is_ok(mock_accommodation('Some street, Dublin 49')),
            AcceptorResponse.REJECT)
        self.assertEqual(
            self.acceptor.is_ok(mock_accommodation('Some Place, Co. Wicklow')),
            AcceptorResponse.REJECT)

    def test_verify_none(self):
        self.acceptor = CommuteAcceptor(self.dummy_config)
        self.assertEqual(
            self.acceptor.is_ok(mock_accommodation('Some street, Dublin 49')),
            AcceptorResponse.VERIFY)
        self.assertEqual(
            self.acceptor.is_ok(mock_accommodation('Some Place, Co. Wicklow')),
            AcceptorResponse.VERIFY)

    def test_accept(self):
        self.acceptor = CommuteAcceptor(self.dummy_config)
        self.assertEqual(
            self.acceptor.is_ok(mock_accommodation('Wild Place, Dublin 18')),
            AcceptorResponse.ACCEPT)
        self.assertEqual(
            self.acceptor.is_ok(mock_accommodation('Nice one, Dublin 8')),
            AcceptorResponse.ACCEPT)

    def test_reject(self):
        self.acceptor = CommuteAcceptor(self.dummy_config)
        self.assertEqual(
            self.acceptor.is_ok(
                mock_accommodation('You Don\'t Want, Dublin 1')),
            AcceptorResponse.REJECT)
        self.assertEqual(
            self.acceptor.is_ok(
                mock_accommodation('Not Worth It, Dublin 2, Co. Dublin')),
            AcceptorResponse.REJECT)

    def test_verify(self):
        self.acceptor = CommuteAcceptor(self.dummy_config)
        self.assertEqual(
            self.acceptor.is_ok(
                mock_accommodation('Kenilworth, Dublin 6W')),
            AcceptorResponse.VERIFY)
        self.assertEqual(
            self.acceptor.is_ok(
                mock_accommodation('Kenilworth, Dublin 6w')),
            AcceptorResponse.VERIFY)
        self.assertEqual(
            self.acceptor.is_ok(
                mock_accommodation('Rathmines, Dublin 6')),
            AcceptorResponse.VERIFY)

    def test_last_commute(self):
        pass

    def test_provide_reason(self):
        pass