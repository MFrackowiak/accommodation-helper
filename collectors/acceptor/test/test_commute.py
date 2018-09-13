from unittest import TestCase
from mock import patch

overwritten_app_config = {
    'dublin-zip-commute-api': {
        '1': 50,
        '2': 60,
        '8': 40,
        '6': 40,
        '6w': 50,
        '18': 20
    },
}

with patch('config.config.application_config', overwritten_app_config):
    from collectors.acceptor.commute import CommuteConfig, CommuteAPI

# def patch_config(func):
#     return patch(
#         'config.config.application_config', overwritten_app_config)(func)


class CommuteAcceptorTestCase(TestCase):
    def setUp(self):
        # from collectors.acceptor.commute import CommuteConfig
        self.dummy_config = CommuteConfig(
            check_to='Heather House, Heather Road, Dublin 16',
            max_commute=30,
            max_verify=45,
            api_cls='collectors.acceptor.api.commute.dummy.DummyCommuteAPI',
        )

    # @patch_config
    def test_dont_verify_none(self):
        pass

    # @patch_config
    def test_verify_none(self):
        pass

    # @patch_config
    def test_accept(self):
        pass

    # @patch_config
    def test_reject(self):
        pass

    # @patch_config
    def test_verify(self):
        pass

    # @patch_config
    def test_last_commute(self):
        pass

    # @patch_config
    def test_provide_reason(self):
        pass