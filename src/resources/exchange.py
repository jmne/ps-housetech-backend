from datetime import datetime
from datetime import timedelta

import pytz
from coverage.annotate import os
from exchangelib import Account
from exchangelib import Configuration
from exchangelib import Credentials
from exchangelib import DELEGATE


class ExchangeCalendar():
    """ExchangeCalendar class using the exchangelib library."""

    # Define the rooms and email addresses directly in the class
    ROOMS = [
        {'name': 'R022', 'email': 'WI.R022@wi.uni-muenster.de'},
        {'name': 'R115', 'email': 'WI.R115@wi.uni-muenster.de'},
        {'name': 'Leo2', 'email': 'WI.LEO2@wi.uni-muenster.de'},
        {'name': 'Leo18', 'email': 'WI.LEO18@wi.uni-muenster.de'},
        {'name': 'WI-Pool', 'email': 'wi.pool@wi.uni-muenster.de'},
    ]

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

    def get_calendar_items(self, room_email):
        """
        Fetch and return calendar items from an Exchange Server.

        Args:
            room_email (str): The email of the room.

        Returns:
            items (list): A list of dictionaries, each representing a calendar event.
        """
        start = datetime(2023, 1, 1, 0, 0, tzinfo=self.utc)
        end = datetime.now(tz=self.utc) + timedelta(days=365)

        username = os.getenv('CAL_USERNAME')
        password = os.getenv('CAL_PASSWORD')

        print(username)
        print(password)

        if username and password:
            self.update_credentials(username, password, room_email)

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

    def get_calendar_results(self, room_name):
        """
        Fetch and return calendar results from an Exchange Server.

        Args:
            room_name (str): The name of the room.

        Returns:
        items (list): A list of calendar items. Classified with rooms
        """
        results = []

        for room in self.ROOMS:
            if room['name'] == room_name:
                room_email = room['email']

                username = os.getenv('CAL_USERNAME')
                password = os.getenv('CAL_PASSWORD')

                if username and password and room_email:
                    self.update_credentials(username, password, room_email)
                    return self.get_calendar_items(room['email'])

        return results
        # return an empty list if room not found or no calendar items in the room
