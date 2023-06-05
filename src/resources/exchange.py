from datetime import datetime
from datetime import timedelta

import pytz
from exchangelib import Account
from exchangelib import Configuration
from exchangelib import Credentials
from exchangelib import DELEGATE


class ExchangeCalendar:
    """CalendarTracker class using the exchangelib library."""

    def __init__(self):
        """Get access to exchange server."""
        # connect to server
        username = 'WIWI\\3100R022'
        email = 'wi.r022@wi.uni-muenster.de'
        password = '!esqfPmqQ6Y4KFu7re25L#'
        server = 'mail.wiwi.uni-muenster.de/ews/exchange.asmx'

        credentials = Credentials(
            username=username, password=password,
        )
        config = Configuration(
            server=server, credentials=credentials,
        )

        self.a = Account(
            primary_smtp_address=email, config=config, autodiscover=False,
            access_type=DELEGATE,
        )
        self.utc = pytz.utc

    def get_calendar_items(self):
        """
        Fetch and return calendar items from an Exchange Server.

        Returns:
            items (list): A list of dictionaries, each representing a calendar event.
        """
        start = datetime(2023, 1, 1, 0, 0, tzinfo=self.utc)
        end = datetime.now(tz=self.utc) + timedelta(days=365)
        calendar_items = self.a.calendar.view(start=start, end=end)
        items = []

        for item in calendar_items:
            items.append({
                'title': item.subject,
                'start': item.start.isoformat(),
                'end': item.end.isoformat(),
                'duration': str(item.duration),
                'location': str(item.location),
                'organizer_name': item.organizer.name,
                'organizer_email': item.organizer.email_address,
            })

        return items
