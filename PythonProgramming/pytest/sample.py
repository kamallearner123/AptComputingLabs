# Example: test_calculator.py
import pytest

def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

@pytest.fixture
def numbers():
    return {"a": 2, "b": 3}

def test_add_with_fixture(numbers):
    assert add(numbers["a"], numbers["b"]) == 5

@pytest.mark.parametrize("a, b, expected", [(1, 1, 2), (0, 5, 5), (-2, 2, 0)])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected