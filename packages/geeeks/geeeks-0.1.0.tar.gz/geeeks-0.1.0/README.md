# Geeeks - A simple and helpful package
Install/Upgrade our package
```
pip install geeeks # install
pip install --upgrade geeeks # upgrade
```

## String Functions  
1. Reverse String: reverse_str(string)
```
from geeeks import StringFunctions as sf

my_string = "AnyRandomString"
rev = sf.reverse_str(my_string)

print(rev)
# Output: gnirtSmodnaRynA
```

2. Make Link: make_link(string)
```
from geeeks import StringFunctions as sf

my_string = "Any Random String"
link = sf.make_link(my_string)

print(link)
# Output: any-random-string
```

## Advance Algorithms  
### Divide & Conquer Algorithms  
This package (geeeks.DnC_Algo) contains the following functions:
* binary_search(arr, x, low, high)
* bubble_sort(arr)
* merge_sort(arr, low, high)
* min_max(arr, low, high)
* quick_sort(arr, low, high)

1. Binary Search  
```
from geeeks import DnC_Algo as dnc

arr = [1,2,3,4,5]
x = 4 # Element to search
low = 0 # lowest index
high = len(arr)-1 # maximum index

res = dnc.binary_search(arr, x, low, high)
if res != -1:
    print(f"Element is present at index: {res}")
else:
    print("Element is not present in array!")
```

2. Bubble Sort
```
from geeeks import DnC_Algo as dnc

arr = [12,9,87,6,43,55,34]
print(dnc.bubble_sort(arr))
```

3. Merge Sort
```
from geeeks import DnC_Algo as dnc

arr = [1,2,3,4,5]
low = 0 # lowest index
high = len(arr) # maximum index

print(arr)
dnc.merge_sort(arr, low, high)
print(arr)
```

4. Minimum & Maximum
```
from geeeks import DnC_Algo as dnc

arr = [34, 67, 78, 45]
low = 0
high = len(arr) - 1 # maximum index
minimum, maximum = dnc.min_max(arr, low, high)
print(f"Maximum: {maximum}\nMinimum: {minimum}")
```

5. Quick Sort
```
from geeeks import DnC_Algo as dnc

arr = [10,9,8,7,6]
low = 0
high = len(arr)-1

print("Before quick sort: {}".format(arr))
dnc.quick_sort(arr, low, high)
print("After quick sort: {}".format(arr))
```

### Dynamic Programming Algorithms
This package (geeeks.DP_Algo) contains the following functions:
* zero_one_knapsack(capacity, weight, profit)
* coin_change(coins, amount)
* longest_common_subsequence(str_a, str_b)
* matrix_multiplication(arr)

1. 0-1 Knapsack Problem
```
from geeeks import DP_Algo as dp

weight = [2, 3, 4, 5]
profit = [1, 2, 5, 6]
capacity = 8

dp.zero_one_knapsack(capacity, weight, profit)
```

2. Coin Change Problem
```
from geeeks import DP_Algo as dp

coins = [2,5,10]
amount = 25
dp.coin_change(coins, amount)
```

3. Longest Common Subsequence
```
from geeeks import DP_Algo as dp

A,B = list("algorithm"), list("analysis")
print(dp.longest_common_subsequence(A,B))
```

4. Matrix Multiplication
```
from geeeks import DP_Algo as dp

arr=[1,2,3,4,1]
print(dp.matrix_multiplication(arr))
```

### Graph Algorithms
This package (geeeks.Graph_Algo) contains the following functions:
* dijkstra(graph)
* floyd(graph, num_vertices)

1. Dijkstra's Algorithm
```
from geeeks import Graph_Algo as gp

graph = [[0, 5, 8, 0], [5, 0, 10, 0], [8, 10, 0, 20], [0, 15, 20, 0]]
gp.dijkstra(graph)
```

2. Floyd-Warshall Algorithm
```
from geeeks import Graph_Algo as gp
INF = 999
graph = [    [0, 3, INF, 7],
         [8, 0, 2, INF],
         [5, INF, 0, 1],
         [2, INF, INF, 0]]

gp.floyd(graph)
```

### Greedy Algorithms
This package (geeeks.Greedy_Algo) contains the following functions:
* fractional_knapsack(values, weight, max_capacity)
* build_huffman_tree(arr, freq)
* job_scheduling(arr)
* prims_mst(graph)

1. Fractional Knapsack
```
from geeeks import Greedy_Algo as gd

values = [280, 100, 120, 120]
weight = [40, 10, 20, 24]
max_capacity = 60
gd.fractional_knapsack(values, weight, max_capacity)
```

2. Huffman Encoding Technique
```
from geeeks import Greedy_Algo as gd

arr = ['a','b','c','d','e','f']
freq = [40,30,20,5,3,2]
gd.build_huffman_tree(arr, freq)
```

3. Job Scheduling
```
from geeeks import Greedy_Algo as gd

# follow this structure for the data
arr = [['j1', 5, 200],
       ['j2', 3, 180],
       ['j3', 3, 190],
       ['j4', 2, 300],
       ['j5', 4, 120],
       ['j6', 2, 100]
       ]

gd.job_scheduling(arr)
```

4. Prim's Algorithm
```
from geeeks import Greedy_Algo as gd

graph = [[0,5,8,0],[5,0,10,0],[8,10,0,20],[0,15,20,0]]
print("MST acc. to Prim's is: {}".format(gd.prims_mst(graph)))
```