#test\test_task4.py

from task4 import calculate_discount

def test_valid_inputs():
    # test integer price with integer discounts
    assert calculate_discount(100, 10) == 90
    assert calculate_discount(100, 50) == 50
    assert calculate_discount(100, 80) == 20

    # test with assorted float and int price and discount
    assert calculate_discount(80.0, 12.5) == 70.0
    assert calculate_discount(200.0, 25) == 150.0
    assert calculate_discount(200, 12.5) == 175.0

    # test no discount
    assert calculate_discount(80.0, 0) == 80.0
    assert calculate_discount(80, 0.00) == 80

    # test full discount
    assert calculate_discount(80.0, 100) == 0.00
    assert calculate_discount(80, 100) == 0
    assert calculate_discount(80.0, 1.00) == 0.00
    assert calculate_discount(80, 1.00) == 0

def test_invalid_discounts():
    # test with invalid discount ranges
    assert "discount is invalid" in calculate_discount(10, 101)
    assert "discount is invalid" in calculate_discount(10, -101)
    assert "discount is invalid" in calculate_discount(10, -1.01)
    assert "discount is invalid" in calculate_discount(10, 100.01)

def test_invalid_prices():
    # test with invalid price ranges
    assert "price is not valid" in calculate_discount(0, 10)
    assert "price is not valid" in calculate_discount(-10, 10)

def test_with_strings():
    # test with strings
    assert "price or discount is not valid" in calculate_discount("100", 10)
    assert "price or discount is not valid" in calculate_discount(100, "10")

def test_with_boolean():
    # test that bools are rejected
    assert "price or discount is not valid" in calculate_discount(True, 10)
    assert "price or discount is not valid" in calculate_discount(100, False)
