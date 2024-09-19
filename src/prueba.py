def pi_approximation(decimals):
    pi = 1
    for i in decimals:
        pi += i/decimals
    return pi

a = 10
value = pi_approximation(a)
print(value)

()