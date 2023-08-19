import numpy as np
import pandas as pd
import math
import heapq

INF = 999

# Divide & Conquer Algorithms


class DnC_Algo:
    def __init__(self):
        pass

    # Binary Search
    def binary_search(arr, x, low=0, high=0):
        if high >= low:
            mid = low + (high - low) // 2
            if arr[mid] == x:
                return mid
            elif arr[mid] > x:
                return DnC_Algo.binary_search(arr, x, low, mid-1)
            else:
                return DnC_Algo.binary_search(arr, x, mid + 1, high)
        else:
            return -1

    def bubble_sort(arr):
        for i in range(0, len(arr)):
            for j in range(i):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    # Merge Sort
    def merge(arr, low, mid, high):

        left = arr[low:mid+1]
        right = arr[mid+1:high+1]
        i = 0
        j = 0
        k = low
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    def merge_sort(arr, left, right):
        if right > left:
            mid = (right + left) // 2
            DnC_Algo.merge_sort(arr, left, mid)
            DnC_Algo.merge_sort(arr, mid+1, right)
            DnC_Algo.merge(arr, left, mid, right)

    # Min-Max
    def min_max(arr, start, end):
        if (start == end):
            return arr[start], arr[end]
        if (start == end-1):
            if (arr[start] < arr[end]):
                return arr[start], arr[end]
            else:
                return arr[end], arr[start]
        if (start < end-1):
            mid = (start+end)//2
            min1, max1 = DnC_Algo.min_max(arr, start, mid)
            min2, max2 = DnC_Algo.min_max(arr, mid+1, end)
            return (min(min1, min2), max(max1, max2))

    # Quick Sort
    def quick_sort(arr, l, h):
        if l < h:
            p = DnC_Algo.partition(arr, l, h)
            DnC_Algo.quick_sort(arr, l, p-1)
            DnC_Algo.quick_sort(arr, p+1, h)

    def partition(arr, l, h):
        pivot = arr[h]
        i = l-1
        for j in range(l, h):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[h] = arr[h], arr[i+1]
        return i+1

# Dynamic Programming Algorithms


class DP_Algo:
    def __init__(self):
        pass

    # 0-1 Knapsack Problem
    def zero_one_knapsack(capacity, weight, profit):
        counter = 0
        n = len(profit)
        ans_list = list()
        table = np.zeros([n+1, capacity+1], dtype=int)

        for i in range(n + 1):
            for w in range(capacity + 1):
                if i == 0 or w == 0:
                    counter += 1
                    table[i][w] = 0
                elif weight[i - 1] <= w:
                    counter += 1
                    table[i][w] = max(profit[i - 1] + table[i - 1]
                                      [w - weight[i - 1]], table[i - 1][w])
                else:
                    counter += 1
                    table[i][w] = table[i - 1][w]

        print("\nTable: \n", table)
        res = table[n][capacity]
        print("Max. Profit: ", res)

        w = capacity
        for i in range(n, 0, -1):
            counter += 1
            if res <= 0:
                break

            if res == table[i - 1][w]:
                continue
            else:
                if i == 1:
                    res = res - profit[i - 1]
                    w = w - weight[i - 1]
                    temp = str(i)+"st"
                    ans_list.append(temp)
                elif i == 2:
                    res = res - profit[i - 1]
                    w = w - weight[i - 1]
                    temp = str(i)+"nd"
                    ans_list.append(temp)
                else:
                    res = res - profit[i - 1]
                    w = w - weight[i - 1]
                    temp = str(i)+"th"
                    ans_list.append(temp)

        print("Products Selected: ", ans_list)
        print("Time Complexity (counter): ", counter)

    # Coin Change Problem
    def coin_change(coins, amount):
        no_of_coins = len(coins)
        dp = np.zeros((no_of_coins+1, amount+1))

        for i in range(1, no_of_coins+1):
            dp[i][0] = 0
            for j in range(1, amount+1):
                dp[0][j] = 0
                if i == 1:
                    if j-coins[i-1] < 0:
                        dp[i][j] = math.inf
                    else:
                        dp[i][j] = 1+dp[i][j-coins[i-1]]

                elif j < coins[i-1]:
                    dp[i][j] = dp[i-1][j]

                else:
                    dp[i][j] = min(dp[i-1][j], 1+dp[i][j-coins[i-1]])
        print(dp)
        print("Minimum Number of coins required : ", dp[no_of_coins][amount])

        i, k = no_of_coins, amount
        req_coins = list()
        while i > 0 and k > 0:
            if dp[i][k] != dp[i-1][k]:
                req_coins.append(coins[i-1])
                k -= coins[i-1]
            else:
                i -= 1
        print("Coins making sum up:", req_coins)

    # Longest Common Subsequence
    def longest_common_subsequence(str_a, str_b):
        res = list()
        flag = 0
        len_a = len(str_a)
        len_b = len(str_b)
        table = np.zeros([len_a+1, len_b+1])
        str_a.insert(0, " ")
        str_b.insert(0, " ")
        for i in range(len_a+1):
            flag = 0
            for j in range(len_b+1):
                if i == 0 and j == 0:
                    table[i][j] = 0
                if str_a[i] == str_b[j] and i != 0 and j != 0:
                    table[i][j] = (table[i-1][j-1])+1
                    x = str_b[j]
                    if flag == 0:
                        res.append(x)
                        flag += 1
                    else:
                        flag = 0

                else:
                    table[i][j] = max(table[i-1][j], table[i][j-1])
        print(table)
        print("Length of LCS", table[-1][-1])
        return res

    # Matrix Chain Multiplication
    def matrix_multiplication(arr):
        n = len(arr)
        dp = np.zeros((n, n))
        for i in range(0, n-1):
            dp[i][i+1] = 0
        for gap in range(2, n):
            for i in range(0, n-gap):
                j = i+gap
                dp[i][j] = float('inf')
                for k in range(i+1, j):
                    dp[i][j] = min(dp[i][j], dp[i][k]+dp[k]
                                   [j]+(arr[i]*arr[k]*arr[j]))

        print(dp)
        return dp[0][n-1]

# Graph Algorithms


class Graph_Algo:
    def __init__(self):
        pass

    # Dijkstra's Algorithm
    def dijkstra_func(graph, src):
        V = len(graph)
        dist = [float('inf') for i in range(V)]
        dist[src] = 0
        fin = [False for i in range(V)]
        for count in range(V-1):
            u = -1
            for i in range(V):
                if fin[i] == False and (u == -1 or dist[i] < dist[u]):
                    u = i
            fin[u] = True
            for v in range(V):
                if fin[v] == False and graph[u][v] != 0:
                    dist[v] = min(dist[v], dist[u]+graph[u][v])
        return dist

    # Printing the output of Dijkstra's Algorithm
    def dijkstra(graph):
        for i in range(0, len(graph)):
            print("Distance from {}th node to other nodes: {}".format(
                i+1, Graph_Algo.dijkstra_func(graph, i)))

    # Floyd Warshall Algorithm
    def floyd(graph):
        num_vertices = len(graph)
        dist = list(map(lambda p: list(map(lambda q: q, p)), graph))

        # Adding vertices individually
        for r in range(num_vertices):
            for p in range(num_vertices):
                for q in range(num_vertices):
                    dist[p][q] = min(dist[p][q], dist[p][r] + dist[r][q])
        Graph_Algo.print_floyd(dist,num_vertices)

    # Printing the output of Floyd Warshall Algorithm
    def print_floyd(dist,num_vertices):
        for p in range(num_vertices):
            for q in range(num_vertices):
                if (dist[p][q] == INF):
                    print("INF", end=" ")
                else:
                    print(dist[p][q], end="  ")
            print(" ")


# Greedy Algorithms
class Greedy_Algo:
    def __init__(self):
        pass

    # Fractional Knapsack
    def fractional_knapsack(values, weight, max_capacity):
        item_name = list()
        res = list()
        v_by_w = list()
        counter = 0
        weightTaken = 0
        profit = 0

        # length exception handling
        if len(values) != len(weight):
            print(".....Values & Weight are not of same length.....")
            print(".....Exiting system.....")
            exit(0)
        else:
            # calculating values/weight ratio
            for i in range(len(values)):
                item_name.append(i+1)
                v_by_w.append(values[i]/weight[i])

            # creating dataframe
            data = {'name': item_name, 'values': values,
                    'weight': weight, 'v/w': v_by_w}
            df = pd.DataFrame(data)

            # final dataframe
            sorted_df = df.sort_values(by=['v/w'], ascending=False)

            # applying greedy approach for fractional knapsack problem
            for i in sorted_df.index:
                if (weightTaken+sorted_df['weight'][i] <= max_capacity):
                    weightTaken += sorted_df['weight'][i]
                    profit += sorted_df['values'][i]
                    temp = str(sorted_df['name'][i])+str("= full")
                    res.append(temp)
                    counter += 1
                else:
                    remaining = max_capacity - weightTaken
                    profit = profit + (remaining * sorted_df['v/w'][i])
                    temp = str(sorted_df['name'][i])+" = " + \
                        str((remaining/sorted_df['weight'][i]))
                    res.append(temp)
                    counter += 1
                    break

            # printing result
            print("Given Data: \n {}".format(sorted_df))
            print("Maximum Profit gained: {}".format(profit))
            print("Items Taken: {}".format(res))
            print("Time complexity: {}".format(counter))

    # Huffman Encoding
    def build_huffman_tree(arr, freq):
        h = []
        for i in range(len(arr)):
            heapq.heappush(h, Node(freq[i], arr[i], None, None))

        while len(h) > 1:
            l = heapq.heappop(h)
            r = heapq.heappop(h)
            heapq.heappush(h, Node(l.freq+r.freq, '$', l, r))

        print("Encoded Values: \n")
        return Greedy_Algo.printCodes(h[0])

    def printCodes(root, s=''):
        if root == None:
            return
        if root.ch != '$':
            print(root.ch+': '+s)
            return
        Greedy_Algo.printCodes(root.left, s+'0')
        Greedy_Algo.printCodes(root.right, s+'1')

    # Job Schedulling
    '''
    arr = [['j1', 5, 200],
       ['j2', 3, 180],
       ['j3', 3, 190],
       ['j4', 2, 300],
       ['j5', 4, 120],
       ['j6', 2, 100]
       ]
    '''

    def job_scheduling(arr):
        t = 0
        n = len(arr)

        for i in range(len(arr)):
            if t < arr[i][1]:
                t = arr[i][1]

        for i in range(n):
            for j in range(n - 1 - i):
                if arr[j][2] < arr[j + 1][2]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

        result = [False] * t
        job = ['-1'] * t

        for i in range(len(arr)):
            for j in range(min(t - 1, arr[i][1] - 1), -1, -1):
                if result[j] is False:
                    result[j] = True
                    job[j] = arr[i][0]
                    break
        print(job)

    # Prim's Algorithm
    def prims_mst(graph):
        V = len(graph)
        key = [float('inf') for i in range(V)]
        key[0] = 0
        res = 0
        mSet = [False for i in range(V)]

        for count in range(V):
            u = -1
            for i in range(V):
                if mSet[i] == False and (u == -1 or key[i] < key[u]):
                    u = i
            mSet[u] = True
            res += key[u]
            for v in range(V):
                if mSet[v] == False and graph[u][v] != 0 and graph[u][v] < key[v]:
                    key[v] = graph[u][v]
        return res


class Node:
    def __init__(self, freq, ch, left, right):
        self.freq = freq
        self.ch = ch  # '$' for non-leaf nodes
        self.left = left
        self.right = right

    def __lt__(self, n):  # used by heapq [lessthan()]
        return self.freq < n.freq
