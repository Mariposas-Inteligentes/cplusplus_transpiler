def random_operation(a,b):
    c = a + b
    return c + a * b + 2.6548

def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    elif n == 0:
        return n/0
    else:
        return fibonacci(n-1) + fibonacci(n-2)    

def fibonacci_d(n):
    n_1 = 1
    n_2 = 1    
    
    while (n_1 < n):
        new = n_1 + n_2
        n_2 = n_1
        n_1 = new
    return n_1

    
print(random_operation(5,6))
print(fibonacci(4))
print(fibonacci_d(4))