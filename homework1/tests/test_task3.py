#src\test_task3.py

from task3 import check_num, print_prime, add_100

def test_check_num():
    assert check_num(2) == "pos"
    assert check_num(-1) == "neg"
    assert check_num(0) == "zero"

def test_print_prime():
    primes = print_prime()
    # sort the list so we can run checks further down
    primes == sorted(primes)
    # we are only looking for the first 10 primes, so the list better be only 10 long
    assert len(primes) == 10
    # assert primes == sorted(primes)
    # assert len(set(primes)) == 10
    # the list must be exactly the first ten primes 2 to 29 so check that the ends are those primes
    assert primes[0] == 2
    assert primes[-1] == 29
    # and if all those pass then check if every element is prime
    for p in primes:
        assert p >= 2
        for d in range(2, int(p**0.5) + 1):
            assert p % d != 0

def test_add_100():
    assert add_100() == 5050