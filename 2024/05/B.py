from collections import defaultdict
import sys

class G:
    def __init__(self, n):
        self.n = n
        self.edges = [[] for _ in range(n)]
        self.indeg = [0]*n

    def add(self, a, b):
        self.indeg[b] += 1
        self.edges[a].append(b)

rules = defaultdict(set)

def actives(x):
    n = len(x)
    g = G(n)
    for i in range(n):
        r = rules.get(x[i])
        if r is None:
            continue
        for j in range(n):
            if x[j] in r:
                g.add(i, j)
    return g

def fix(x):
    g = actives(x)
    ret = []
    for _ in range(g.n):
        for i in range(g.n):
            if g.indeg[i] == 0:
                added = True
                ret.append(x[i])
                g.indeg[i] = -1
                for j in g.edges[i]:
                    assert g.indeg[j] > 0
                    g.indeg[j] -= 1
                break
        else:
            assert False, 'not added'
    return ret

def ok(x):
    n = len(x)
    for i in range(1, n):
        r = rules.get(x[i])
        if r is None:
            continue
        for j in range(i):
            if x[j] in r:
                return False
    return True

mode = 0
sol = 0
for line in sys.stdin:
    line = line.rstrip()
    if not line:
        mode = 1
        continue
    if mode == 0:
        parts = line.split('|')
        assert len(parts) == 2
        rules[int(parts[0])].add(int(parts[1]))
    else:
        assert mode == 1
        x = [int(p) for p in line.split(',')]
        if not ok(x):
            x = fix(x)
            assert ok(x)
            assert len(x) % 2 == 1
            sol += x[len(x) // 2]
print(sol)
