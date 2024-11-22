   
def default_ex(a='hola'):
    return (a)

def set_ex():    
    a = {1,2,"hola",4,5}    
    return 2 in a

def tuple_ex():    
    a = (5,6,'joseph')
    b = (1,2, 'valverde')
    return a + b

print(default_ex())
print(tuple_ex())
print(set_ex()) 