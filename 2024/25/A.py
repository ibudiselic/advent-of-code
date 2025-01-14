import sys

H = 7
W = 5

def mklock(g):
    ret = []
    n = len(g)
    assert n == H
    m = len(g[0])
    assert m == W
    for j in range(m):
        i = 0
        while i<n and g[i][j] == '#':
            i += 1
        ret.append(i - 1)
    assert len(ret) == W
    return ret

def get_input():
    locks = []
    keys = []
    for part in sys.stdin.read().split('\n\n'):
        g = part.strip().split('\n')
        k = len(g[0])
        if g[0] == '#'*k:
            locks.append(mklock(g))
        else:
            g.reverse()
            keys.append(mklock(g))
    return locks, keys

def ok(lock, key):
    return all(a+b+2 <= H for a, b in zip(lock, key))

locks, keys = get_input()
sol = 0
for lock in locks:
    for k in keys:
        if ok(lock, k):
            sol += 1
print(sol)
