import numpy as np
from PIL import Image


class EInkGenerator:
    """E-Ink.    proxies are not included yet."""

    def __init__(self):
        """
        Initialization of E-Ink class.

        Args:
            self

        """

    def transformPNGToRGBArray(self, path):
        # Open an image file
        img = Image.open(path)
        # Convert the image data to an RGB format
        img = img.convert('RGB')
        # Convert the image into a NumPy array
        rgb_array = np.array(img)
        return rgb_array

    def transformRBGArrayToBlackWhiteRed(self, rgb_array):
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

    def getBlackWhiteLayer(self, rgb_array):
        # Write the Bit Array
        # rgb_array / 8, um 8er Bit Chunks zu erstellen
        chunk = []
        chunkCount = 0
        blackWhiteLayerBits = []
        bit = False
        for rgb_value in rgb_array:
            if rgb_value == 'WHITE':
                bit = True

            # Wenn 8 Werte geschrieben wurden
            if chunkCount == 8:
                blackWhiteLayerBits.append(chunk)
                chunkCount = 0
                chunk = []
                chunk.append(bit)
                bit = False

            else:
                chunk.append(bit)
                bit = False

            chunkCount = chunkCount + 1
        # Add last 8 Bits
        blackWhiteLayerBits.append(chunk)
        # Turn Bit Array into Hex
        blackWhiteLayerHex = []
        for bool_array in blackWhiteLayerBits:
            decimal_value = sum(
                int(b) << (7 - i)
                for i, b in enumerate(bool_array)
            )
            hex_value = format(decimal_value, '02X')
            blackWhiteLayerHex.append('0X' + hex_value)

        return blackWhiteLayerHex

    def getRedWhiteLayer(self, rgb_array):
        # Write the Bit Array
        # rgb_array / 8, um 8er Bit Chunks zu erstellen
        chunk = []
        chunkCount = 0
        redWhiteLayerBits = []
        bit = False
        for rgb_value in rgb_array:
            if rgb_value == 'RED':
                bit = True

            # Wenn 8 Werte geschrieben wurden
            if chunkCount == 8:
                redWhiteLayerBits.append(chunk)
                chunkCount = 0
                chunk = []
                chunk.append(bit)
                bit = False

            else:
                chunk.append(bit)
                bit = False

            chunkCount = chunkCount + 1

        # Add last 8 Bits
        redWhiteLayerBits.append(chunk)
        # Turn Bit Array into Hex
        redWhiteLayerHex = []
        for bool_array in redWhiteLayerBits:
            decimal_value = sum(
                int(b) << (7 - i)
                for i, b in enumerate(bool_array)
            )
            hex_value = format(decimal_value, '02X')
            redWhiteLayerHex.append('0X' + hex_value)

        return redWhiteLayerHex

    def getFuzedLayers(self, path):
        blackWhiteLayer = self.getBlackWhiteLayer(
            self.transformRBGArrayToBlackWhiteRed(
                self.transformPNGToRGBArray(path),
            ),
        )
        redWhiteLayer = self.getRedWhiteLayer(
            self.transformRBGArrayToBlackWhiteRed(
                self.transformPNGToRGBArray(path),
            ),
        )

        blackWhiteLayerString = ','.join(
            [element for element in blackWhiteLayer],
        )
        redWhiteLayerString = ','.join([element for element in redWhiteLayer])
        fuzedLayers = blackWhiteLayerString + ',' + redWhiteLayerString

        return fuzedLayers

    def get_data(self):
        """Test method returning data."""
        return self.getFuzedLayers()