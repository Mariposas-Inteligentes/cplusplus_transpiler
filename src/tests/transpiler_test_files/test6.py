l = [1, 2, 3, 4, 5]

print("List")
for i in l:
  print(i)

s = {1, 2, 3, 4, 5}

print("set")
for i in s:
  print(i)

angie = 2
d = {1: 2, "holi": 4, (1, 2): {1, 2, 3}, angie:"wii"}
print("Dict keys")
for i in d:
  print(i)

print("Dict values")
for i in d.keys():
  print(i)

t = (1, 2, 3, "angie", {1:2, 5: "holi"}, { 1, 2, 3}, {})
print("Tuple")
for i in t:
  print(i)