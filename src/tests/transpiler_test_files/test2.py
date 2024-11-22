def iter_example():
    l = [1,2.5,3,"hola",5,"mundo"]
    it = iter(l)
    for i in l:
        print(next(it))
    return True
        
def map_ex():    
    d = {
        "hola": "mundo",
        1: [1,2,3,4,5],        
        "dict": {'adios': ':D'}
    }    

    for k in d.keys():        
        print(d[k])
        
    return "hola" + "mundo"  

print(iter_example())
print(map_ex())