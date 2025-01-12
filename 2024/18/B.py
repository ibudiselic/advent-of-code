import random
import sys

random.seed(123)

n = 71

dy8 = [-1, -1, 0, 1, 1, 1, 0, -1]
dx8 = [0, 1, 1, 1, 0, -1, -1, -1]

UF = {}

def root(p):
    r = UF.get(p, -1)
    if r == -1:
        return p
    r = root(UF[p])
    UF[p] = r
    return r

def join(p, q):
    p = root(p)
    q = root(q)
    if p != q:
        if random.random() <= 0.5:
            UF[p] = q
        else:
            UF[q] = p

border1 = (-1, 0)
border2 = (0, -1)

blocked = set()
for k in range(n):
    for p in [(-1, k), (k, n)]:
        blocked.add(p)
        join(p, border1)
    for p in [(n, k), (k, -1)]:
        blocked.add(p)
        join(p, border2)

assert root(border1) != root(border2)

while True:
    x, y = [int(v) for v in input().split(',')]
    p = (x, y)
    if p in blocked:
        continue
    blocked.add(p)
    for d in range(8):
        xx = x + dx8[d]
        yy = y + dy8[d]
        q = (xx, yy)
        if q in blocked:
            join(p, q)
    if root(border1) == root(border2):
        print(f'{x},{y}')
        break
