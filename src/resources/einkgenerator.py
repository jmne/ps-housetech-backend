import os
import tempfile

import numpy as np
from flask import render_template
from html2image import Html2Image
from markupsafe import Markup
from PIL import Image

from .cris import CrisTracker


tempfile.tempdir = tempfile.TemporaryDirectory(
    dir=os.path.dirname(os.path.abspath(__file__)),
).name


class EInkGenerator:
    """Generate E-Ink image in HEX Format."""

    def __init__(self):
        """
        Initialization of E-Ink class.

        Args:
            self

        """

    def transform_png_to_rgb_array(self, png):
        """Turn png into numpy array."""
        # Convert the image into a NumPy array
        return np.array(png)

    def color_quantization(self, rgb_array):
        """Turn numpy rgb array into black/white/red."""
        result = []
        for row in rgb_array:
            for pixel in row:
                red, green, blue = pixel  # Access individual RGB values
                # Check the color value and convert it to black, red, or white
                if red == 133 and green == 35 and blue == 57:
                    result.append('RED')
                elif red < 5 and green < 5 and blue < 5:
                    result.append('BLACK')
                elif red == 135 and green == 151 and blue == 163:
                    result.append('BLACK')
                elif red == 145 and green == 160 and blue == 170:
                    result.append('BLACK')
                else:
                    result.append('BLACK')
        return result

    def get_layer(self, rgb_array, rgb_color):
        """Turn a black/white/red array into black/white or red/white."""
        # Write the Bit Array
        # rgb_array / 8, to get chunks of 8
        chunk = []
        chunk_count = 0
        layer_bits = []
        bit = False
        for rgb_value in rgb_array:
            if rgb_value == rgb_color:
                bit = True

            # If 8 values are appended
            if chunk_count == 8:
                layer_bits.append(chunk)
                chunk_count = 0
                chunk = [bit]
                bit = False

            else:
                chunk.append(bit)
                bit = False

            chunk_count = chunk_count + 1
        # Add last 8 Bits
        layer_bits.append(chunk)
        # Turn Bit Array into Hex
        layer_hex = []
        for bool_array in layer_bits:
            decimal_value = sum(
                int(b) << (7 - i)
                for i, b in enumerate(bool_array)
            )
            hex_value = format(decimal_value, '02X')
            layer_hex.append('0X' + hex_value)

        return layer_hex

    def get_fused_layers(self, png):
        """Fuze the black/white and the red/white layer together."""
        black_white_layer = self.get_layer(
            self.color_quantization(
                self.transform_png_to_rgb_array(png),
            ),
            'WHITE',
        )
        red_white_layer = self.get_layer(
            self.color_quantization(
                self.transform_png_to_rgb_array(png),
            ),
            'RED',
        )

        black_white_layer_string = ','.join(list(black_white_layer))
        red_white_layer_string = ','.join(list(red_white_layer))

        fused_layers = black_white_layer_string + ',' + red_white_layer_string

        return fused_layers

    def get_data(self, room_number):
        """Return a hex array with bases on the png of a given room number."""
        img = self.get_image(room_number)
        return self.get_fused_layers(img)

    def get_cris_data(self, address, room_number):
        """Import CRIS module and filter for room."""
        cris = CrisTracker()
        cris.get_cris_data('de')
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
        svg = open(os.path.join(path, '../templates', 'ercis.svg')).read()

        html_string = render_template(
            'index.html', roomData=backend_data, svg=Markup(svg),
        )

        return html_string

    def get_image(self, room_number: str):
        """Return PNG door-sign for the correct room number."""
        tempdir = tempfile.gettempdir()

        hti = Html2Image(
            size=(648, 480), temp_path=tempdir, custom_flags=[
                '--default-background-color=ffffff',
                '--hide-scrollbars',
                '--headless',
                '--disable-gpu',
                '--disable-audio-output',
                '--run-all-compositor-stages-before-draw',
                '--virtual-time-budget=10000',
            ],
        )
        """making it the display size of the Eink
        calling the link for the respective room number to crate a png screenshot from it

        alternatively with a HTML and CSS file"""
        hti.output_path = tempdir

        html = self.return_html(room_number)

        screenshot_path = hti.screenshot(
            html_str=html,
            save_as='Raum-' + room_number + '.png',
        )

        image = Image.open(screenshot_path[0])
        image = image.convert('RGB')
        if os.path.exists(screenshot_path[0]):
            os.remove(screenshot_path[0])
        if os.path.exists(screenshot_path[0].replace('.png', '.html')):
            os.remove(screenshot_path[0].replace('.png', '.html'))
        return image
