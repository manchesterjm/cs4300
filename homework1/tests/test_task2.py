from task2 import add, multiply, greet_name, is_positive

def test_add_integers():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_multiply_floats():
    assert multiply(0.5, 0.5) == 0.25
    assert multiply(2.0, 1.5) == 3.0
    assert multiply(4.0, 0.0) == 0.0

def test_greet_name():
    assert greet_name("CS") == "Hello, CS"
    assert greet_name("World") == "Hello, World"

def test_is_positive():
    assert is_positive(5) is True
    assert is_positive(0) is False
    assert is_positive(-3) is False