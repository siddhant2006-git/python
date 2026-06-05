# access list
a = ["apple", "banana", "mango"]
print(a[1])

# negative item
d = ["cat", "dog", "rat"]
print(d[-2])

# range of index
e = ["cat", "bat", "rat", "krish", "bhatnagar"]
print(e[2:4])

# change list
v = ["bat", "kartik", "krish"]
v[1] = "bhatnagar"
print(v)

# change list two or more variable
n = ["nat", "set", "bat", "krish"]
n[1:3] = ["ball", "mall"]
print(n)

# insert element in list - add the element with index
m = ["krish", "sarthak", "karyik"]
m.insert(2, "amma ")
print(m)

# append element -add the element in last of element
k = ["sidd", "chai", "rat"]
k.append("shivkant")
print(k)

# extened the list
i=["rat","mat","chai"]
o=["set","chat","made"]
i.extend(o)
print(i)

# extened list to tuple
l1 = ["rat", "mat", "chai"]
o1=("sidd","cat")
l1.extend(o1)
print(l1)


# remove list item- is used remove specfic item
l2 = ["rat", "mat", "chai"]
l2.remove("mat")
print(l2)

# pop list item- delete the element in last
l3 = ["rat", "mat", "chai"]
l3.pop()
print(l3)

# del - delete the element with index value to delete
l4 = ["rat", "mat", "chai"]
del l4[1]
print(l4)

# clear
l6= ["rat", "mat", "chai"]
l6.clear()
print(l6)


