# Lambda Functions- A lambda function can take any number of arguments, but can only have one expression.

# addition
x = lambda a: a + 10
print(x(5))

# multiplication

x1=lambda b,a :b*a
print(x1(5,6))

# Lambda Functions-The power of lambda is better shown when you use them as an anonymous function inside another function.


def myfunc(n):
    return lambda a: a * n
mydoubler = myfunc(2)
print(mydoubler(11))

# map -The map() function applies a function to every item in an iterable:

number=[1,2,3,4,5,6]
double=list(map(lambda x:x*2,number))
print(double)

# filter-The filter() function creates a list of items for which a function returns True:

numbers=[1,2,3,4,5,6,7,8]
doubles=list(filter(lambda x:x%2!=0,numbers))
print(doubles)

# sorted-The sorted() function can use a lambda as a key for custom sorting
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

