# loads-json convert into python
import json

x = '{ "name":"John", "age":30, "city":"New York"}'
y=json.loads(x)
print(y["age"])

# dumps-python convert to json string
import json

# a Python object (dict):
x = {"name": "John", "age": 30, "city": "New York"}
y = json.dumps(x)
print(y)

import json

print(json.dumps({"name": "John", "age": 30}))
print(json.dumps(["apple", "bananas"]))
print(json.dumps(("apple", "bananas")))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))
