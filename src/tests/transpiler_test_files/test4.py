def slices_ex():
    l = [1,2,3,4,5,6,7,7,8,9]
    print(l[-2])
    print(l[1:-2])    
    k = l[1:2] + l[-3:-4]
    return (k)
    
def string_ex():
    print("profe"[2:4])
    print("profe"[2:4] + "profe"[0:2] + "profe"[-1])

print(slices_ex())
string_ex()