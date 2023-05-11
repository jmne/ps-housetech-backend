from datetime import datetime, timedelta
from exchangelib import DELEGATE, Account, Credentials, Configuration
import pytz
from flask import Flask, jsonify, render_template

# ****this file used JSON and FullCalendar**** #

# app = Flask(__name__)

# connect to server
username = 'username'  # username of each room exchange server
email = 'email'  # email of each room exchange server
password = 'password'  # password of each room exchange server
server = 'mail.wiwi.uni-muenster.de/ews/exchange.asmx'

credentials = Credentials(username=username, password=password)
config = Configuration(server=server, credentials=credentials)

a = Account(primary_smtp_address=email, config=config, autodiscover=False,
            access_type=DELEGATE)
utc = pytz.utc

# get calendar events
def get_calendar_items():
    start = datetime(2023, 1, 1, 0, 0, tzinfo=utc)
    end = datetime.now(tz=utc) + timedelta(days=365)
    calendar_items = a.calendar.view(start=start, end=end)
    items = []
    for item in calendar_items:
        # Get the required and optional attendees
        required_attendees = item.required_attendees if item.required_attendees else []
        optional_attendees = item.optional_attendees if item.optional_attendees else []
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
            'total_attendees': total_attendees
        })

    return items


# return JSON response data
@app.route('/api/events', methods=['GET'])
def events():
    return jsonify(get_calendar_items())


# bind URL to function
@app.route('/')
def index():
    return render_template('index.html')


# get the application to run on the local server
if __name__ == '__main__':
    app.run(debug=True, port=5004)