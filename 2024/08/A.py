from collections import defaultdict
import sys

G = [line.rstrip() for line in sys.stdin]
pos = defaultdict(list)
n = len(G)
m = len(G[0])
for i in range(n):
    for j in range(m):
        if G[i][j] != '.':
            pos[G[i][j]].append((i, j))

hit = set()
for _, p in pos.items():
    for k in range(len(p)):
        i, j = p[k]
        for kk in range(len(p)):
            if k == kk: continue
            r, c = p[kk]
            x = 2*r-i
            y = 2*c-j
            if 0 <= x < n and 0 <= y < m:
                hit.add((x, y))
print(len(hit))
