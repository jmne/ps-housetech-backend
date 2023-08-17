import pytest

from src.resources import cris


class TestCris:

    @pytest.fixture(scope='class')
    def tracker(self):
        return cris.CrisTracker()

    @pytest.mark.parametrize(
        'input_list, max_length, result',
        [([1, 2, 3, 4, 5, 6, 7, 8, 9], 3, ([1, 2, 3], [4, 5, 6], [7, 8, 9]))],
    )
    def test_split_list(self, tracker, input_list, max_length, result):
        result = tracker.split_list(input_list, max_length)

        assert isinstance(result, list)
        assert all(isinstance(sublist, list) for sublist in result)
        assert all(len(sublist) <= max_length for sublist in result)
        assert (len(result) <= len(input_list)/max_length)
