from datetime import datetime
from unittest import TestCase

from collectors.acceptor.base import AcceptorResponse
from collectors.acceptor.price import PriceCheckAcceptor, PriceCheckConfig
from collectors.scrappers.base import ParsedAccommodation


def mock_accommodation(price: int) -> ParsedAccommodation:
    return ParsedAccommodation('dummy.url', 'somewhere', datetime.now(),
                               price, 'test')


class PriceAcceptorTestCase(TestCase):
    def test_invalid_config(self):
        with self.assertRaises(ValueError):
            PriceCheckAcceptor(PriceCheckConfig())

    def test_in_accept(self):
        acceptor = PriceCheckAcceptor(PriceCheckConfig(accept_min=0,
                                                       accept_max=10))
        self.assertEqual(acceptor.is_ok(mock_accommodation(5)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(mock_accommodation(0)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(mock_accommodation(10)),
                         AcceptorResponse.ACCEPT)

    def test_only_one(self):
        acceptor = PriceCheckAcceptor(PriceCheckConfig(accept_max=10))

        self.assertEqual(acceptor.is_ok(mock_accommodation(5)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(mock_accommodation(0)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(mock_accommodation(10)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(mock_accommodation(12)),
                         AcceptorResponse.REJECT)

    def test_not_in_accept(self):
        acceptor = PriceCheckAcceptor(PriceCheckConfig(accept_min=0,
                                                       accept_max=2))
        self.assertEqual(acceptor.is_ok(mock_accommodation(-1)),
                         AcceptorResponse.REJECT)
        self.assertEqual(acceptor.is_ok(mock_accommodation(3)),
                         AcceptorResponse.REJECT)

    def test_in_accept_and_verify(self):
        acceptor = PriceCheckAcceptor(
            PriceCheckConfig(accept_min=0, accept_max=10,
                             verify_min=-5, verify_max=15))

        self.assertEqual(acceptor.is_ok(mock_accommodation(5)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(mock_accommodation(0)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(mock_accommodation(10)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(mock_accommodation(-5)),
                         AcceptorResponse.VERIFY)
        self.assertEqual(acceptor.is_ok(mock_accommodation(11)),
                         AcceptorResponse.VERIFY)
        self.assertEqual(acceptor.is_ok(mock_accommodation(15)),
                         AcceptorResponse.VERIFY)

    def test_out_of_verify(self):
        acceptor = PriceCheckAcceptor(
            PriceCheckConfig(accept_min=0, accept_max=10,
                             verify_min=-5, verify_max=15))

        self.assertEqual(acceptor.is_ok(mock_accommodation(-6)),
                         AcceptorResponse.REJECT)
        self.assertEqual(acceptor.is_ok(mock_accommodation(16)),
                         AcceptorResponse.REJECT)
