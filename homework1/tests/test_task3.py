from task3 import check_num, print_prime, add_100

def test_check_num():
    assert check_num(2) == "pos"
    assert check_num(-1) == "neg"
    assert check_num(0) == "zero"

#def test_print_prime():

def test_add_100():
    assert add_100() == 5050