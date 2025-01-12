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
sources = [[[set()] * len(di) for _ in range(m)] for _ in range(n)]
best[u.i][u.j][1] = 0
H = [S(0, u, 1)]

def update(s, src):
    p = s.p
    if G[p.i][p.j] != '.':
        assert G[p.i][p.j] == '#'
        return
    if best[p.i][p.j][s.d] > s.cost:
        best[p.i][p.j][s.d] = s.cost
        heapq.heappush(H, s)
        sources[p.i][p.j][s.d] = {S(-1, src.p, src.d)}
    elif best[p.i][p.j][s.d] == s.cost:
        sources[p.i][p.j][s.d].add(S(-1, src.p, src.d))

done = set()
Q = []
sol = None
while H:
    s = heapq.heappop(H)
    if s.p == t:
        if sol is None or sol == s.cost:
            sol = s.cost
            s = S(-1, t, s.d)
            Q.append(s)
            done.add(s)
            continue
        else:
            assert sol < s.cost
            break
    if best[s.p.i][s.p.j][s.d] != s.cost:
        continue
    update(S(s.cost+1, s.p.move(s.d), s.d), s)
    for dd in [-1, 1]:
        d = s.d + dd
        if d < 0:
            d += 4
        elif d >= len(di):
            d -= len(di)
        assert 0 <= d < len(di)
        update(S(s.cost+1000, s.p, d), s)

touched = {t}
head = 0
while head < len(Q):
    s = Q[head]
    head += 1
    p = s.p
    for src in sources[p.i][p.j][s.d]:
        src = S(-1, src.p, src.d)
        if src in done:
            continue
        Q.append(src)
        done.add(src)
        touched.add(src.p)
print(len(touched))
