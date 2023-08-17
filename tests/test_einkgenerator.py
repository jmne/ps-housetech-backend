import numpy as np
import pytest
from PIL import Image

from src.resources import einkgenerator


class TestEInkGenerator:

    @pytest.fixture(scope='class')
    def generator(self):
        return einkgenerator.EInkGenerator()

    @pytest.mark.parametrize(
        'rgb_array',
        ['tests/resources/picture1.npy'],
    )
    def test_color_quantization(self, generator, rgb_array):
        f = open(rgb_array, 'rb')
        result = generator.color_quantization(np.load(f))

        assert isinstance(result, list)
        assert all(
            pixel_color in ['BLACK', 'WHITE', 'RED']
            for pixel_color in result
        )

    @pytest.mark.parametrize(
        'rgb_array, rgb_color, output',
        [
            (
                'tests/resources/get_layer_input.npy', 'WHITE',
                'tests/resources/get_layer_output_WHITE.txt',
            ),
            (
                'tests/resources/get_layer_input.npy', 'RED',
                'tests/resources/get_layer_output_RED.txt',
            ),
        ],
    )
    def test_get_layer(self, generator, rgb_array, rgb_color, output):
        f = open(rgb_array, 'rb')
        o = open(output)
        result = generator.get_layer(np.load(f), rgb_color)

        assert isinstance(result, list)
        assert result == o.read().splitlines()

    @pytest.mark.skip(reason='Not working rn, needs fix')
    @pytest.mark.parametrize(
        'png, output',
        [(
            'tests/resources/get_fused_layers_input_png.png',
            'tests/resources/get_fused_layers_output.txt',
        )],
    )
    def test_fused_layers(self, generator, png, output):
        o = open(output)
        result = generator.get_fused_layers(Image.open(png))

        assert isinstance(result, str)
        assert result == ','.join(list(o.read().splitlines()))
