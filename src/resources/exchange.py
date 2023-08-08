from datetime import datetime
from datetime import timedelta

import pytz
from coverage.annotate import os
from dotenv import load_dotenv
from exchangelib import Account
from exchangelib import Configuration
from exchangelib import Credentials
from exchangelib import DELEGATE

# Load the .env file
load_dotenv('../secrets.env')


class ExchangeCalendar:
    """ExchangeCalendar class using the exchangelib library."""

    def __init__(self):
        """Get access to exchange server."""
        self.server = 'mail.wiwi.uni-muenster.de/ews/exchange.asmx'
        self.utc = pytz.utc
        self.a = None

    def update_credentials(self, username, password, email):
        """Update credential."""
        credentials = Credentials(
            username=username, password=password,
        )
        config = Configuration(
            server=self.server, credentials=credentials,
        )
        self.a = Account(
            primary_smtp_address=email, config=config, autodiscover=False,
            access_type=DELEGATE,
        )

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

    def get_calendar_results(self):
        """
        Fetch and return calendar results from an Exchange Server.

        Returns:
        items (list): A list of calendar items. Classified with rooms
        """
        room_emails = os.getenv('ROOM_EMAILS', '').split(',')
        rooms = os.getenv('ROOMS').split(',')
        results = []

        ex = ExchangeCalendar()
        for room_email, room_name in zip(room_emails, rooms):
            username = os.getenv('USERNAME')
            password = os.getenv('PASSWORD')

            if username and password and room_email:
                ex.update_credentials(username, password, room_email)
                results.append({
                    'room': room_name,
                    'items': ex.get_calendar_items(),
                })

        return results
