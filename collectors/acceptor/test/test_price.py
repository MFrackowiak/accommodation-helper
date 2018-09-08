from dataclasses import field, dataclass
from datetime import datetime
from unittest import TestCase

from collectors.acceptor.base import AcceptorResponse
from collectors.acceptor.price import PriceCheckAcceptor, PriceCheckConfig


@dataclass
class MockedProperty:
    price: int
    provider: str = field(default='')
    url: str = field(default='')
    address: str = field(default='')
    entered: datetime = field(default=datetime.now())


class PriceAcceptorTestCase(TestCase):
    def test_invalid_config(self):
        with self.assertRaises(ValueError):
            PriceCheckAcceptor(PriceCheckConfig())

    def test_in_accept(self):
        acceptor = PriceCheckAcceptor(PriceCheckConfig(accept_min=0,
                                                       accept_max=10))
        self.assertEqual(acceptor.is_ok(MockedProperty(5)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(MockedProperty(0)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(MockedProperty(10)),
                         AcceptorResponse.ACCEPT)

    def test_not_in_accept(self):
        acceptor = PriceCheckAcceptor(PriceCheckConfig(accept_min=0,
                                                       accept_max=2))
        self.assertEqual(acceptor.is_ok(MockedProperty(-1)),
                         AcceptorResponse.REJECT)
        self.assertEqual(acceptor.is_ok(MockedProperty(3)),
                         AcceptorResponse.REJECT)

    def test_in_accept_and_verify(self):
        acceptor = PriceCheckAcceptor(
            PriceCheckConfig(accept_min=0, accept_max=10,
                             verify_min=-5, verify_max=15))

        self.assertEqual(acceptor.is_ok(MockedProperty(5)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(MockedProperty(0)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(MockedProperty(10)),
                         AcceptorResponse.ACCEPT)
        self.assertEqual(acceptor.is_ok(MockedProperty(-5)),
                         AcceptorResponse.VERIFY)
        self.assertEqual(acceptor.is_ok(MockedProperty(11)),
                         AcceptorResponse.VERIFY)
        self.assertEqual(acceptor.is_ok(MockedProperty(15)),
                         AcceptorResponse.VERIFY)

    def test_out_of_verify(self):
        acceptor = PriceCheckAcceptor(
            PriceCheckConfig(accept_min=0, accept_max=10,
                             verify_min=-5, verify_max=15))

        self.assertEqual(acceptor.is_ok(MockedProperty(-6)),
                         AcceptorResponse.REJECT)
        self.assertEqual(acceptor.is_ok(MockedProperty(16)),
                         AcceptorResponse.REJECT)
