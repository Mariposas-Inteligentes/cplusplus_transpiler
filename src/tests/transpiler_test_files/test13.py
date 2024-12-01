# +=_____________
print('+=_____________')
x = 'Angie, Emilia y '
x += 'luis'
print(x)

y = 5*10
y += 250*9
print(y)

z = (1,2,3)
z+= (4,5)+(6,7)
print(z)

a = [4,3,2] + [1]
a += [-1, -2]
print(a)

b = 5.0
b += 1
print(b)

# -=_____________
print('-=_____________')
y = 5*10
y -= 51
print(y)

b = 5.0*10
b -= 51
print(b)

c = {1,2,890}
c -= {890}
print(c)

# *=_____________
print('*=_____________')
y = 5*5-1+1
y *= 5
print(y)

x = 'string'
x *= 5
print(x)

x = 5
x *= 'luis es humilde\n'
print(x)

a = [1,2,3] * 2
print(a)

a = 2 * [1,2,3]
print(a)