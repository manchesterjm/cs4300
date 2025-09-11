#src\test_task3.py

from task3 import check_num, print_prime, add_100

def test_check_num():
    assert check_num(2) == "pos"
    assert check_num(-1) == "neg"
    assert check_num(0) == "zero"

def test_print_prime():
    primes = print_prime()

    # first thing, we are only looking for the first 10 primes, so the list better be only 10 long
    assert len(primes) == 10

    # sort the list so we can run checks further down
    primes == sorted(primes)

    # the list must be exactly the first ten primes 2 to 29 so check that the ends are those primes after being sorted
    assert primes[0] == 2
    assert primes[-1] == 29
    
    # and if all those pass then check if every element is prime
    for p in primes:
        # primes start at 2 and are all larger after two, no negative numbers
        assert p >= 2
        for d in range(2, int(p**0.5) + 1): # we only need to check numbers up to the square root of the prime candidate ( +1 because of rounding ) to say it is prime
            assert p % d != 0

def test_add_100():
    # the total for adding 1 to 100 is 5050
    assert add_100() == 5050