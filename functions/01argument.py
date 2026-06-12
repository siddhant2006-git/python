def myargument(fname):# fname is parameter 
  print(fname + " Rename")

myargument("Email")
myargument("phone")
myargument("instagram") # argument 

# default parameter
def default(name="siddhant" ,rollno=11): # default parameter 
  print(name + "class" )
default()

# args - The *args parameter allows a function to accept any number of positional arguments.
def my_function(*kids):
    print("The youngest child is " + kids[1])


my_function("Emil", "Tobias", "Linus")

