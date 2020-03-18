#백준 11279 우선순위 큐 문제 답안
from sys import *
from heapq import *

h = []

for _ in range(int(stdin.readline())):
    a = int(stdin.readline())

    if a == 0:
        print(0 if len(h) == 0 else -heappop(h))
    else:
        heappush(h, -a)