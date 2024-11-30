y = 0
print(type(y))

y = float(y)
print(type(y))
print(y)

y = str(y)
print(type(y))
print(y)

x = y
x = bool(x)
print(x) # false because y is a string

y = float(y)
y = bool(y)
print(y) # true because y is a number


