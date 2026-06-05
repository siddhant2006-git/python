# for loop
l3 = ["rat", "mat", "chai"]
for x in l3:
    print(x)

# loop with len
l4 = ["rat", "mat", "chai"]
for x in range(len(l4)):# index can be show 
    print(l4[x])

# while loop
l1 = ["1", "2", "3"]
i=0
while i<len(l1):
    print(l1[i])
    i=i+1

# list comprehension -in shortest syntax comprehension
l5=["1","22","33"]
[print(x) for x in l5]

# core concept
l0=["11","22","33","44","rat","banana","apple"]
newlist=[]

for x in l0:
    if "a" in x:
        newlist.append(x)

print(newlist)        

# upper condition in loop
a1=["apple","set","mat"]
newlist2=[x.upper() for x  in a1 if "a" in x  ]
print(newlist2)


