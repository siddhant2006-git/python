# set-is collection of unordered ,unchangeable,unindexing

# unordered-set order cannot be fixed.
s = {"apple", "mango", "rat"}
print(s)

# unchangeable-set  item cannot be  directly change . not changeable
# s1={"chai","code","class"}
# s1[0]="class"
# print(s1)

# set item can  be add and remove the new element with any indexing .
d = {"siddhant", "krish", "yash", "sarthak"}
# d.add(1)
d.add("hello")
print(d)

# Duplicates Not Allowed
thisset = {"apple", "banana", "cherry", "apple"}
print(thisset)  # apple can be print only 1 time .

# some condition is same true and 1 is same .
a = {"blue", "car", "red", "green", 1, True}
print(a)

# false and 0 is also same .
v1 = {"red", "blue", "black", 0, False}
print(v1)

# get length of set
q1 = {"flag", "red", "blue"}

print(len(q1))

# add the element

q2 = {"flag", "red", "blue"}
q2.add("orange")
print(q2)

# iterable
thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange"]

thisset.update(mylist)

print(thisset)

# update
thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}

thisset.update(tropical)

print(thisset)

