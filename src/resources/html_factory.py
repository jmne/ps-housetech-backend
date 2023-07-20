from flask import Markup
from flask import render_template


class HTMLFactory:
    """Class that generates html string."""

    def __init__(self):
        """
        Initialization of E-Ink class.

        Args:
            self
        """

    def return_html(self):
        """Return html which is later on converted to SC."""
        # Assuming specialRoomNumber is 'B202'
        specialRoomNumber = 'B202'

        # Example room data
        backendData = {
            'room': 'B202',
            'person': [
                {
                    'name': 'Prof. Dr. Hans Schmid',
                    'degree': 'M.Sc',
                },
                {
                    'name': 'Prof. Dr. Julia Wagne',
                    'degree': 'Ph.D',
                },
                {
                    'name': 'Prof. Dr. Julia Wagne',
                    'degree': 'Ph.D',
                },
            ],
            'globalRoomNumber': '120.202',
        }
        # More room data...

        svg = open('resources/template/ercis.svg').read()

        html_string = render_template(
            'index.html', roomData=backendData,
            specialRoomNumber=specialRoomNumber,
            svg=Markup(svg),
        )

        return html_string
