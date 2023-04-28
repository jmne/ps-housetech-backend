import pytest

from src.backend.Example import fibonacci_recursive


@pytest.mark.parametrize('n, expected', [(3, 2), (5, 5), (7, 13)])
def test_fibonacci_recursive(n, expected):
    assert fibonacci_recursive(n) == expected
