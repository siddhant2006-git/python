# Recursion is when a function calls itself.
def countdown(n):
    if n <= 0:
        print("done")
    else:
        print(n)
        countdown(n - 1)


countdown(5)

# A base case - A condition that stops the recursion
# A recursive case - The function calling itself with a modified argument

# factorial
def factorial(n):
    # Base case
    if n == 0 or n == 1:
        return 1
    # Recursive case
    else:
        return n * factorial(n - 1)


print(factorial(5))

# fibonacci sequence

def fibonacci(n):
    if(n<=1):
        return n
    else:
      return  fibonacci(n-1) +fibonacci(n-2)

print(fibonacci(7))


# Recursion with Lists
def sum_list(numbers):
    if len(numbers) == 0:
        return 0
    else:
        return numbers[0] + sum_list(numbers[1:])


my_list = [1, 2, 3, 4, 5]
print(sum_list(my_list))

# limit
import sys
print(sys.getrecursionlimit()) # 1000 limit

import sys
sys.setrecursionlimit(2000)
print(sys.getrecursionlimit())

# send
def echo_generator():
    while True:
        received = yield
        print("Received:", received)


gen = echo_generator()
next(gen)  # Prime the generator
gen.send("Hello")
gen.send("World")


# close() Method
def my_gen():
    try:
        yield 1
        yield 2
        yield 3
    finally:
        print("Generator closed")


gen = my_gen()
print(next(gen))
gen.close()
