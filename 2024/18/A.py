from collections import deque
import sys

n = 71

def valid(x):
    return 0 <= x < n

dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]

blocked = set()
for _ in range(1024):
    x, y = [int(v) for v in input().split(',')]
    blocked.add((x, y))
    
done = {(0, 0): 0}
Q = deque([(0, 0)])
while Q:
    x, y = Q.popleft()
    dist = done[(x, y)]
    for d in range(len(dx)):
        xx = x + dx[d]
        yy = y + dy[d]
        p = (xx, yy)
        if not valid(xx) or not valid(yy) or p in blocked or p in done:
            continue
        if p == (n-1, n-1):
            print(dist + 1)
            exit(0)
        Q.append(p)
        done[p] = dist + 1
raise AssertionError('unrechable')
