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
        username = 'room_username'
        email = 'room@wi.uni-muenster.de'
        password = 'room_password'
        server = 'mail.wiwi.uni-muenster.de/ews/exchange.asmx'

        credentials = Credentials(username=username, password=password)
        config = Configuration(server=server, credentials=credentials)

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
            # Get the required and optional attendees
            required_attendees = item.required_attendees \
                if item.required_attendees else []
            optional_attendees = item.optional_attendees \
                if item.optional_attendees else []

            # Calculate the total number of attendees
            total_attendees = len(required_attendees) + len(optional_attendees)

            items.append({
                'title': item.subject,
                'body': item.body,
                'start': item.start.isoformat(),
                'end': item.end.isoformat(),
                'duration': str(item.duration),
                'location': str(item.location),
                'organizer_name': item.organizer.name if item.organizer else '',
                'organizer_email': item.organizer.email_address if item.organizer else '',
                'conference_type': str(item.conference_type),
                'total_attendees': total_attendees,
            })

        return items
