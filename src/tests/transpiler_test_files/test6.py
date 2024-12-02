l = [1, 2, "holas", (1, 2, 3), 5]

print("List")
for i in l:
  print(i)

s = {1, ("holiwispiwis", 3), (1,3), ("h","luis"), 5}

print("set")
for i in s:
  print(i)

angie = 2
d = {1: 2, "holi": 4, ("compilanding", 2): {1, 2, 3}, angie:"wii", (1, 2):"wii", (2, 3):"wuuu"}
print("Dict keys")
for i in d:
  print(i)

print("Dict values")
for i in d.keys():
  print(d[i])

t = (1, 2, 3, "angie", {1:2, 5: "holi"}, { 1, 2, 3}, {})
print("Tuple")
for i in t:
  print(i)


setin = {(1,2), (2,3,1), (5,6)}
print('Set')
for i in setin:
  print(i)
