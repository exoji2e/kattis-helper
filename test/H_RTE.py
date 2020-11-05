from collections import *
import sys
sys.setrecursionlimit(10000)
inp = input
def ni(): return int(inp())
def nl(): return [int(v) for v in inp().split()]

N = ni()
T = nl()
best = 50, 1000
for i in range(1, N-2):
    v0 = T[i-1]
    v2 = T[i+1]
    m = max(v0, v2)
    best = min(best, (m, i))
print(bets[0], best[0])
