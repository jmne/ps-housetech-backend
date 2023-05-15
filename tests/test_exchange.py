import unittest
from datetime import datetime
from datetime import timedelta
from unittest.mock import MagicMock
from unittest.mock import patch

import pytz

from src.resources.exchange import get_calendar_items


class TestExchangeServer(unittest.TestCase):

    @patch('src.resources.exchange')
    def test_get_calendar_items(self, mock_account):
        # Mock the account
        mock_account_instance = mock_account.return_value

        # Mock a calendar item
        mock_item = MagicMock()
        mock_item.subject = 'Test Meeting'
        mock_item.body = 'Test Body'
        mock_item.start = datetime(2023, 1, 1, 0, 0, tzinfo=pytz.utc)
        mock_item.end = datetime(2023, 1, 1, 1, 0, tzinfo=pytz.utc)
        mock_item.duration = timedelta(hours=1)
        mock_item.location = 'Test Location'
        mock_item.organizer = MagicMock(
            name='Test Organizer', email_address='test@uni-muenster.de',
        )
        mock_item.conference_type = 'Test Conference Type'
        mock_item.required_attendees = ['test1@uni-muenster.de']
        mock_item.optional_attendees = ['test2@uni-muenster.de']

        # Mock the calendar view method to return our mock item
        mock_account_instance.calendar.view.return_value = [mock_item]

        # Call the method we're testing
        result = get_calendar_items()

        # Check that the result is as expected
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Test Meeting')
        self.assertEqual(result[0]['body'], 'Test Body')
        self.assertEqual(result[0]['start'], '2023-01-01T00:00:00+00:00')
        self.assertEqual(result[0]['end'], '2023-01-01T01:00:00+00:00')
        self.assertEqual(result[0]['duration'], '1:00:00')
        self.assertEqual(result[0]['location'], 'Test Location')
        self.assertEqual(result[0]['organizer_name'], 'Test Organizer')
        self.assertEqual(result[0]['organizer_email'], 'test@uni-muenster.de')
        self.assertEqual(result[0]['conference_type'], 'Test Conference Type')
        self.assertEqual(result[0]['total_attendees'], 2)


if __name__ == '__main__':
    unittest.main()
