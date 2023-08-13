from datetime import datetime
from enum import Enum


class Event(Enum):
    """Enum class for events."""
    PIDAY = '1'
    APRILFOOLS = '2'
    EMOJIDAY = '3'
    STARWARS = '4'
    HALLOWEEN = '5'
    NEWYEAR = '6'


class EventManager:
    """EventManager class that determines the event."""
    @staticmethod
    def determine_event():
        """Determine event."""
        today = datetime.today().date()
        if today.month == 3 and today.day == 14:
            return Event.PIDAY.value
        elif today.month == 4 and today.day == 1:
            return Event.APRILFOOLS.value
        elif today.month == 5 and today.day == 4:
            return Event.STARWARS.value
        elif today.month == 7 and today.day == 17:
            return Event.EMOJIDAY.value
        elif today.month == 10 and today.day == 31:
            return Event.HALLOWEEN.value
        elif today.month == 1 and today.day < 14:
            return Event.NEWYEAR.value
        else:
            return '0'  # in case it's not a special day
