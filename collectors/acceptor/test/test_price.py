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

    def test_last_value_is_set(self):
        acceptor = PriceCheckAcceptor(
            PriceCheckConfig(accept_min=0, accept_max=10,
                             verify_min=-5, verify_max=15))
        acceptor.is_ok(mock_accommodation(5))
        self.assertEqual(acceptor.last_checked_value, 5)
        acceptor.is_ok(mock_accommodation(-6))
        self.assertEqual(acceptor.last_checked_value, -6)
        acceptor.is_ok(mock_accommodation(18))
        self.assertEqual(acceptor.last_checked_value, 18)
        acceptor.is_ok(mock_accommodation(12))
        self.assertEqual(acceptor.last_checked_value, 12)

    def test_provide_reason(self):
        acceptor = PriceCheckAcceptor(
            PriceCheckConfig(accept_min=0, accept_max=10,
                             verify_min=-5, verify_max=15))
        acceptor.is_ok(mock_accommodation(42))
        self.assertEqual(
            acceptor.provide_reason(),
            'Price may not fit in accept range: 0 to 10 or verify range: -5 to '
            '15, provided price: 42.'
        )

        acceptor = PriceCheckAcceptor(
            PriceCheckConfig(accept_max=8))
        acceptor.is_ok(mock_accommodation(42))
        self.assertEqual(
            acceptor.provide_reason(),
            'Price may not fit in accept range: n/a to 8 or verify range: n/a '
            'to n/a, provided price: 42.'
        )
