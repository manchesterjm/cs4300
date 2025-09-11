# src\task4.py

# need to check if the input is vaild, int or float
def _is_valid(x):
    return type(x) in (int, float)

def calculate_discount(price, discount):
    if not _is_valid(price) or not _is_valid(discount):
        return f"price or discount is not valid, please enter either an int or float value"

    if price < 0:
        return f"price is not valid, it must be a postive int or float greater than 0"
    
    if (0.00 < discount < 1.00):
        new_discount = discount
    elif (0 <= discount <= 100):
        new_discount = discount / 100
    else:
        return f"discount is invalid, it must int 0<=>100 or float 0.00<=>1.00"

    return (price * new_discount)