import os

from flask import render_template
from markupsafe import Markup

from .cris import CrisTracker


class HTMLFactory:
    """Class that generates html string."""

    def __init__(self):
        """
        Initialization of E-Ink class.

        Args:
            self
        """

    def get_cris_data(self, address, room_number):
        """Import CRIS module and filter for room."""
        cris = CrisTracker()
        cris.get_cris_data()
        data = {
            'room': room_number,
            'person': [],
            'globalRoomNumber': room_number,
        }
        for person in cris.result:
            if person['address'] == address and person['roomNumber'] == room_number:
                data['person'].append(
                    {
                        'name': f"{person['cfFirstNames']} {person['cfFamilyNames']}",
                        'degree': (
                            person['academicTitle']
                            if person['academicTitle'] else ''
                        ),
                    },
                )

        return data

    def return_html(self, room_number):
        """Return html which is later on converted to SC."""
        # Example room data
        backend_data = self.get_cris_data('Leonardo-Campus 3', room_number)

        path = os.path.dirname(os.path.abspath(__file__))
        svg = open(os.path.join(path, 'template', 'ercis.svg')).read()

        html_string = render_template(
            'index.html', roomData=backend_data, svg=Markup(svg),
        )

        return html_string
