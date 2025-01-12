from collections import deque
from dataclasses import dataclass
import sys

G = [line.rstrip() for line in sys.stdin]
n = len(G)
m = len(G[0])

di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

@dataclass(frozen=True, slots=True)
class P:
    i: int
    j: int

    def move(self, d):
        return P(self.i+di[d], self.j+dj[d])

def valid(p):
    return 0 <= p.i < n and 0 <= p.j < m

def getSE():
    s = None
    e = None
    for i in range(n):
        for j in range(m):
            if G[i][j] == 'S':
                assert s is None
                s = P(i, j)
            elif G[i][j] == 'E':
                assert e is None
                e = P(i, j)
    assert s is not None
    assert e is not None
    return s, e

def replace(p, c):
    s = G[p.i]
    s = ''.join([s[:p.j], c, s[p.j+1:]])
    G[p.i] = s

def solve(s):
    Q = deque([s])
    cost = {s: 0}
    def update(p, c):
        if not p in cost:
            cost[p] = c
            Q.append(p)

    while Q:
        p = Q.popleft()
        c = cost[p]
        for d in range(4):
            q = p.move(d)
            if not valid(q):
                continue
            if G[q.i][q.j] == '.':
                update(q, c+1)
    return cost

s, e = getSE()
replace(s, '.')
replace(e, '.')
inf = 2**63

from_s = solve(s)
from_e = solve(e)
nocheat = from_s[e]
sol = 0
for i in range(n):
    for j in range(m):
        p = P(i, j)
        if p not in from_s:
            continue
        for r in range(-20, 21):
            if not (0 <= p.i+r < n):
                continue
            rem = 20 - abs(r)
            for c in range(-rem, rem+1):
                if not (0 <= p.j+c < m) or (r == 0 and c == 0):
                    continue
                q = P(p.i+r, p.j+c)
                if q not in from_e:
                    continue
                if from_s[p] + from_e[q] + abs(r) + abs(c) + 100 <= nocheat:
                    sol += 1
print(sol)
