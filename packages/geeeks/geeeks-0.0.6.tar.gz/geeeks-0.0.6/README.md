# Geeeks - A simple and helpful package
Install/Upgrade our package
```
pip install geeeks # install
pip install --upgrade geeeks # upgrade
```

## String Functions
1. Reverse String
```
from geeeks import StringFunctions as sf

my_string = "AnyRandomString"
rev = sf.reverse_str(my_string)

print(rev)
# Output: gnirtSmodnaRynA
```

2. Make Link
```
from geeeks import StringFunctions as sf

my_string = "Any Random String"
link = sf.make_link(my_string)

print(link)
# Output: any-random-string
```