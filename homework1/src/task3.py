#src\task3.py

def check_num(num):
    if num > 0:
        return "pos"
    elif num < 0:
        return "neg"
    else:
        return "zero"

def print_prime():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    for i in primes:
        print(i)
    
    return(primes)

        

def add_100():
    i = 1
    total = 0
    while i < 101:
        total += i
        i += 1
    return(total)