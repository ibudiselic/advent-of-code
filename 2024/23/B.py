from collections import defaultdict
import sys

# The input contains 520 nodes with degree 13 each.

E = []
A = defaultdict(set)
for line in sys.stdin:
    line = line.rstrip()
    a, b = line.split('-')
    E.append((a, b))
    A[a].add(b)
    A[b].add(a)

for a, bs in A.items():
    bs.add(a)

best = set()
nodes = list(A.keys())
nodes.sort()
where = {node:i for i, node in enumerate(nodes)}

mask = [set()]
for a in nodes:
    s = set(mask[-1])
    s.add(a)
    mask.append(s)

def bad(at, cur):
    for i in range(at):
        a = nodes[i]
        if a not in cur:
            continue
        bs = A[a]
        for j in range(i+1, at+1):
            b = nodes[j]
            if b not in cur:
                continue
            if b not in bs:
                return True
    return False

def go(at, cur):
    global best
    if len(cur) <= len(best) or bad(at, cur):
        return
    cand = cur & mask[at+1]
    if len(cand) > len(best):
        best = cand
    for k in range(at+1, len(nodes)):
        b = nodes[k]
        if b in cur:
            go(k, A[b] & cur)
    

for i, a in enumerate(nodes):
    bs = A[a]
    if len(bs & mask[i+1]) == 1:
        go(i, bs)

print(','.join(sorted(best)))
