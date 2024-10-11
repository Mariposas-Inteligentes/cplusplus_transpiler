def outer_function(x):
    if x > 5:
        for i in range(x):
            def inner_function(y):
                if y < 3:
                    return y * 2
            print(inner_function(i))