from dataclasses import dataclass
import heapq
import sys

di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

@dataclass(frozen=True, slots=True, order=True)
class P:
    i: int
    j: int

    def move(self, d):
        return P(self.i+di[d], self.j+dj[d])

@dataclass(frozen=True, slots=True, order=True)
class S:
    cost: int
    p: P
    d: int

G = [line.rstrip() for line in sys.stdin]
m = len(G)
n = len(G[0])

def getSE():
    spos = None
    epos = None
    for i, s in enumerate(G):
        for j, c in enumerate(s):
            flip = False
            if c == 'S':
                spos = P(i, j)
                flip = True
            elif c == 'E':
                epos = P(i, j)
                flip = True
            if flip:
                s = f'{s[:j]}.{s[j+1:]}'
                G[i] = s
    assert spos is not None
    assert epos is not None
    return spos, epos

u, t = getSE()
inf = 2**62
best = [[[inf] * len(di) for _ in range(m)] for _ in range(n)]
d = 1
best[u.i][u.j][d] = 0
H = [S(0, u, d)]

def update(s):
    p = s.p
    if G[p.i][p.j] != '.':
        assert G[p.i][p.j] == '#'
        return
    if best[p.i][p.j][s.d] > s.cost:
        best[p.i][p.j][s.d] = s.cost
        heapq.heappush(H, s)

while H:
    s = heapq.heappop(H)
    if s.p == t:
        print(s.cost)
        break
    if best[s.p.i][s.p.j][s.d] > s.cost:
        continue
    best[s.p.i][s.p.j][s.d] = s.cost
    update(S(s.cost+1, s.p.move(s.d), s.d))
    for dd in [-1, 1]:
        d = s.d + dd
        if d < 0:
            d += 4
        elif d >= 4:
            d -= 4
        update(S(s.cost+1000, s.p, d))
