# tuple - it is collection of the unchangeable elements
# tuple can used for unchangeable.
a=("1","2","3","4")

# length of tuple
b=("apple","banan","cat","rat")
print(len(b))

# update value
c= ("apple", "banan", "cat", "rat")
d1=list(c)
d1[1]="siddhant"
c=tuple(d1)
print(c)

# add the element
e = ("apple", "banan", "cat", "rat")
e1=list(e)
e1.append("krish")
e=tuple(e1)
print(e)

# remove the element
f = ("apple", "banan", "cat", "rat")
f1 = list(e)
f1.remove("cat")
f = tuple(f1)
print(f)

