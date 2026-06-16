# list are build the data structure the serve the dynamic array.
# a=[1,2,3,4,56,6,"krish"]
# append the element in the list
a=[1,2,4,4,24,3]
a.append(5)
print(a)
# sorted data
a.sort()
print(a)

# Create an algorithm to find the lowest value in a list

a=[1,2,34,5,3,23343,432]
minval=a[0]
for i in a:
    if i < minval:
        minval = i

print(minval)

# time complexity-the amount of computer time can be run to them.
# 1. O(1) — Constant Time- the run time can be exactly to there input .

# 2.O(logn) — Logarithmic Time-the run time can be increase if the input size can be increase .
# ex - binary search is example of o(logn).

# 3. o(n)- linear time - run time is directly propstional to input size .
# linear search

# 4.  o(nlogn)-Linearithmic Time- slight slower then linear time but still very large efficent datasets .
# Merge Sort, Heap Sort, Quick Sort.

# 5. o(n**)-run time is propostional to square of input size .
# Bubble Sort, Selection Sort,


# o(2**n)-runtime is double every addition of input .
# Calculating the n-th Fibonacci number

# o(n!)-run time with factorial .

