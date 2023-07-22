import numpy as np

from .eink_image import EinkImage


class EInkGenerator:
    """E-Ink.    proxies are not included yet."""

    def __init__(self):
        """
        Initialization of E-Ink class.

        Args:
            self

        """

    def transform_png_to_rgb_array(self, png):
        """Turn png into numpy ."""
        # Convert the png to an RGB format
        img = png.convert('RGB')
        # Convert the image into a NumPy array
        rgb_array = np.array(img)
        return rgb_array

    def transform_rgb_array_to_black_white_red(self, rgb_array):
        """Turn numpy rgb array into black/white/red."""
        result = []
        for row in rgb_array:
            for pixel in row:
                red, green, blue = pixel  # Access individual RGB values
                # Check the color value and convert it to black, red, or white
                if red > 240 and green < 50 and blue < 50:
                    result.append('RED')
                elif red > 180 and green > 180 and blue > 180:
                    result.append('WHITE')
                else:
                    result.append('BLACK')
        return result

    def get_black_white_layer(self, rgb_array):
        """Turn black/white/red array into black/white."""
        # Write the Bit Array
        # rgb_array / 8, to get chunks of 8
        chunk = []
        chunk_count = 0
        black_white_layer_bits = []
        bit = False
        for rgb_value in rgb_array:
            if rgb_value == 'WHITE':
                bit = True

            # If 8 values are appended
            if chunk_count == 8:
                black_white_layer_bits.append(chunk)
                chunk_count = 0
                chunk = []
                chunk.append(bit)
                bit = False

            else:
                chunk.append(bit)
                bit = False

            chunk_count = chunk_count + 1
        # Add last 8 Bits
        black_white_layer_bits.append(chunk)
        # Turn Bit Array into Hex
        black_white_layer_hex = []
        for bool_array in black_white_layer_bits:
            decimal_value = sum(
                int(b) << (7 - i)
                for i, b in enumerate(bool_array)
            )
            hex_value = format(decimal_value, '02X')
            black_white_layer_hex.append('0X' + hex_value)

        return black_white_layer_hex

    def get_red_white_layer(self, rgb_array):
        """Turn black/white/red array into red/white."""
        # Write the Bit Array
        # rgb_array / 8, to get chunks of 8
        chunk = []
        chunk_count = 0
        red_white_layer_bits = []
        bit = False
        for rgb_value in rgb_array:
            if rgb_value == 'RED':
                bit = True

            # If 8 values are appended
            if chunk_count == 8:
                red_white_layer_bits.append(chunk)
                chunk_count = 0
                chunk = []
                chunk.append(bit)
                bit = False

            else:
                chunk.append(bit)
                bit = False

            chunk_count = chunk_count + 1

        # Add last 8 Bits
        red_white_layer_bits.append(chunk)
        # Turn Bit Array into Hex
        red_white_layer_hex = []
        for bool_array in red_white_layer_hex:
            decimal_value = sum(
                int(b) << (7 - i)
                for i, b in enumerate(bool_array)
            )
            hex_value = format(decimal_value, '02X')
            red_white_layer_hex.append('0X' + hex_value)

        return red_white_layer_hex

    def get_fuzed_layers(self, png):
        """Fuze the black/white and the red/white layer together."""
        black_white_layer = self.get_black_white_layer(
            self.transform_rgb_array_to_black_white_red(
                self.transform_png_to_rgb_array(png),
            ),
        )
        red_white_layer = self.get_red_white_layer(
            self.transform_rgb_array_to_black_white_red(
                self.transform_png_to_rgb_array(png),
            ),
        )

        black_white_layer_string = ','.join(list(black_white_layer))
        red_white_layer_string = ','.join(list(red_white_layer))

        fuzed_layers = black_white_layer_string + ',' + red_white_layer_string

        return fuzed_layers

    def get_data(self, room_number: str):
        """Return a hex array with bases on the png of a given room number."""
        eink_image = EinkImage()
        png = eink_image.get_image(room_number)
        return self.get_fuzed_layers(png)
