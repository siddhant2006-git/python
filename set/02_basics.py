# unione
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3=set1.union(set2)
print(set3)

# Intersection-The intersection() method will return a new set, that only contains the items that are present in both sets.

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1.intersection(set2)
print(set3) # apple

# Difference-The difference() method will return a new set that will contain only the items from the first set that are not present in the other set.

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set22 = set1.difference(set2)

print(set22)

# Symmetric Differences
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set4 = set1.symmetric_difference(set2)

print(set4)

# Python frozenset-frozenset is an immutable version of a set.
x = frozenset({"apple", "banana", "cherry"})
print(x)
print(type(x))
