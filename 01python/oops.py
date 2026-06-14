# python is object orient programing language allowing th structured code using class and object

# advantage of oops
# 1. structure of code and clean of code .
# 2.make a maintain code reuse debug the error

# what is class and object?
# class- is blue print from the  object create .
# object -An object is a concrete instance of a class.

# create a class
class Myclass:
  x=5
  print(x)


# create a object
p1=Myclass()
print(p1.x)

# pass statement - it is use to avoid error .

# python _init_method-All classes have a built-in method called __init__()., which is always executed when the class is being initiated
# The __init__() method is used to assign values to object properties, or to perform operations that are necessary when the object is being created.


# init
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


p3 = Person("email", 36)

print(p3.age)
