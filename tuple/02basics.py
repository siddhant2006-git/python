# unpacked tuple

fruits=("apple","mango","cherry")
(green,yellow,red)=fruits

print(green)
print(yellow)
print(red)

# loop of tuple
x=("bat", "set","mark")
for i in x:
    print(i)


# len for loop
l = ("cricket", "ball", "ball")
for i in range(len(l)):
    print(l[i])

# join tuple
a=("cricket","car","bus")
b=("set","mat","bat")
c=a+b
print(c)

# multiple tuple
l1 =  ("cricket", "car", "bus")
l2=l1*3
print(l2)

# count - how many element present in tuple
l3 = ("cricket", "car", "bus","car")
l4=l3.count("car")
print(l4)

# index-only show the index on first time only 
l5= ("cricket", "car", "bus", "car")
l6 = l3.index("car")
print(l6)