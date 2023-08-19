# Geeeks - A simple and helpful package
Install our package using
```
pip install geeeks
```

## String Functions
1. Reverse String
```
import geeeks
strFunc = geeeks.StringFunctions()

my_string = "AnyRandomString"
rev = strFunc.reverse_str(my_string)

print(rev)
# Output: gnirtSmodnaRynA
```

2. Make Link
```
import geeeks
strFunc = geeeks.StringFunctions()

my_string = "Any Random String"
link = strFunc.make_link(my_string)

print(link)
# Output: any-random-string
```