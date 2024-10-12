def outer_function(x):
    if x > 5:
        for i in range(x):
            while i < 4:
                if i < 3:
                    print(inner_function(i))
                    return y * 2
            