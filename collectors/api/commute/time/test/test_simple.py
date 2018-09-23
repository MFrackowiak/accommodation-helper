from unittest import TestCase
from datetime import date, datetime
from mock import MagicMock, patch
from pytz import UTC

from collectors.api.commute.time.simple import SimpleConfigurationTimeParser


class SimpleTimeParserTestCase(TestCase):
    def _mock_now(self, date_time: datetime = datetime(
        2018, 9, 20, 12, 0, 0, tzinfo=UTC)):
        dt_mock = MagicMock()
        dt_mock.now.return_value = date_time
        dt_mock.combine = datetime.combine
        return patch('collectors.api.commute.time.simple.datetime', dt_mock)

    def test_no_tz_same_day(self):
        with self._mock_now():
            self.time_parser = SimpleConfigurationTimeParser()
            self.assertEqual(self.time_parser.parse_time('3 13:00'),
                             datetime(2018, 9, 20, 13, tzinfo=UTC))

    def test_no_tz_day_earlier(self):
        with self._mock_now():
            self.time_parser = SimpleConfigurationTimeParser()
            self.assertEqual(self.time_parser.parse_time('2 19:00'),
                             datetime(2018, 9, 26, 19, tzinfo=UTC))

    def test_no_tz_monday(self):
        with self._mock_now():
            self.time_parser = SimpleConfigurationTimeParser()
            self.assertEqual(self.time_parser.parse_time('0 8:00'),
                             datetime(2018, 9, 24, 8, tzinfo=UTC))

    def test_no_tz_sunday(self):
        with self._mock_now():
            self.time_parser = SimpleConfigurationTimeParser()
            self.assertEqual(self.time_parser.parse_time('6 14:00'),
                             datetime(2018, 9, 23, 14, tzinfo=UTC))

    def test_no_tz_hour_does_not_change_day(self):
        with self._mock_now():
            self.time_parser = SimpleConfigurationTimeParser()
            self.assertEqual(self.time_parser.parse_time('3 7:00'),
                             datetime(2018, 9, 20, 7, tzinfo=UTC))