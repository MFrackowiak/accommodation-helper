from datetime import datetime
from unittest import TestCase

from collectors.acceptor.base import AcceptorResponse
from collectors.acceptor.description import DescriptionAcceptor, \
    DescriptionConfig
from collectors.scrappers.base import ParsedAccommodation


def mocked_found_property(description):
    return ParsedAccommodation(
        url='http://found.co',
        address='Good one 2, Dublin 18',
        entered=datetime.now(),
        price=1200,
        provider='daft',
        description=description
    )


class DescriptionAcceptorTestCase(TestCase):
    def setUp(self):
        self.acceptor = DescriptionAcceptor(DescriptionConfig(
            reject_if_found=[
                {'phrase': 'single person'},
                {'is_reg': True, 'phrase': 'no (dog|pet)s? (are|is)? allowed'},
                {'is_reg': True, 'phrase': 'no (dog|pet)s? allowed'},
                {'is_reg': True, 'phrase': '(dog|pet)s? (is|are) not allowed'},
            ],
            verify_if_found=[
                {'phrase': 'shared'},
            ],
        ))

    def test_simple_clean(self):
        cleaned = self.acceptor._simple_clean(
            'PEts **are** not! Allowed\n nice clean bathroom.....')
        self.assertEqual(
            'pets are not allowed nice clean bathroom', cleaned
        )

    def test_simple_tokenize(self):
        cleaned = self.acceptor._simple_clean(
            'PEts **are** not! Allowed\n nice clean bathroom.....')
        tokenized = self.acceptor._simple_tokenize(cleaned)
        self.assertEqual(
            ['pets', 'are', 'not', 'allowed', 'nice', 'clean', 'bathroom'],
            tokenized
        )

    def test_is_sublist(self):
        test_list = ['hey', 'kitchen', 'single', 'person', 'and', 'bed']
        check_list = ['single', 'person']

        self.assertTrue(self.acceptor._is_sublist(check_list, test_list))
        self.assertFalse(self.acceptor._is_sublist(test_list, check_list))
        self.assertTrue(self.acceptor._is_sublist(['1', '2'], ['1', '2']))
        self.assertFalse(self.acceptor._is_sublist(['1', '2'], ['2', '1']))
        self.assertTrue(self.acceptor._is_sublist(
            ['1', '2'], ['3', '4', '1', '2']))

    def test_improperly_configured(self):
        with self.assertRaises(ValueError):
            DescriptionAcceptor(DescriptionConfig())

    def test_accepted_not_found(self):
        response = self.acceptor.is_ok(mocked_found_property(
            'Really nice. Extra kitchen. Pets are welcome. Two people.'
        ))
        self.assertEqual(response, AcceptorResponse.ACCEPT)

    def test_rejected_found(self):
        response = self.acceptor.is_ok(mocked_found_property(
            'Really nice. Extra kitchen. No pets allowed. Two people.'
        ))
        self.assertEqual(response, AcceptorResponse.REJECT)
        response = self.acceptor.is_ok(mocked_found_property(
            'Really nice. Extra kitchen. No dog is allowed. Two people.'
        ))
        self.assertEqual(response, AcceptorResponse.REJECT)
        response = self.acceptor.is_ok(mocked_found_property(
            'Really nice. Pet is not allowed.'
        ))
        self.assertEqual(response, AcceptorResponse.REJECT)
        response = self.acceptor.is_ok(mocked_found_property(
            'Really nice. Dogs are not allowed.'
        ))
        self.assertEqual(response, AcceptorResponse.REJECT)
        response = self.acceptor.is_ok(mocked_found_property(
            'Really nice. Dogs are allowed. SINGLE PERSON ONLY.'
        ))
        self.assertEqual(response, AcceptorResponse.REJECT)

    def test_verify_found(self):
        response = self.acceptor.is_ok(mocked_found_property(
            'Really nice. Extra kitchen. Shared bathroom.'
        ))
        self.assertEqual(response, AcceptorResponse.VERIFY)

    def test_rejected_before_verify(self):
        response = self.acceptor.is_ok(mocked_found_property(
            'Really nice. No pets allowed. Shared bathroom.'
        ))
        self.assertEqual(response, AcceptorResponse.REJECT)

    def test_founded_rules_are_saved(self):
        self.acceptor.is_ok(mocked_found_property(
            'shared something in fact is.'
        ))
        self.assertEqual(self.acceptor.found_rules, ['shared'])
        self.acceptor.is_ok(mocked_found_property(
            'dogs are not allowed'
        ))
        self.assertEqual(self.acceptor.found_rules,
                         ['(dog|pet)s? (is|are) not allowed'])
        self.acceptor.is_ok(mocked_found_property(
            'no dogs allowed. only for single person.'
        ))
        self.assertEqual(self.acceptor.found_rules,
                         ['no (dog|pet)s? allowed', 'single person'])
        self.acceptor.is_ok(mocked_found_property(
            'Perfect property. Come and live here.'
        ))
        self.assertEqual(self.acceptor.found_rules, [])