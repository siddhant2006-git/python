# local scope - those scope which are working for inside the function.
def myfunc():
  x=100
  print(x) # local scope
myfunc()

# local variable accessed  function to function .
def variable():
  x=1000
  def localvariable():
    print(x)
  localvariable()
variable()

# global scope-those scope in which variable able in outside the function .

c=300
def globalvalue():
  c=200
  print(c)
globalvalue()
print(c)

# global keyword- local value can change the global value.
def krish():
  global x
  x=220
krish()
print(x)

# The LEGB Rule
# Local - Inside the current function
# Enclosing - Inside enclosing functions (from inner to outer)
# Global - At the top level of the module
# Built-in - In Python's built-in namespace

x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print("Inner:", x)

    inner()
    print("Outer:", x)

outer()
print("Global:", x)

# decorator-Define the decorator first, then apply it with @decorator_name above the function.
def changecase(func):
   def innerfunc():
      return func().upper()
   return innerfunc
@changecase
def myfunction():
    return "Hello Sally"
print(myfunction())

# Multiple Decorator Calls
def changecase(func):
    def myinner():
        return func().upper()
    return myinner
@changecase
def myfunction():
    return "Hello Sally"
@changecase
def otherfunction():
    return "I am speed!"
print(myfunction())
print(otherfunction())



