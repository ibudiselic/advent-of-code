from collections import defaultdict
import sys

E = []
A = defaultdict(set)
for line in sys.stdin:
    line = line.rstrip()
    a, b = line.split('-')
    E.append((a, b))
    A[a].add(b)
    A[b].add(a)

def special(node):
    return node.startswith('t')

# [i] - number of counted triplets with i+1 nodes that start with a t.
cnts = [0] * 3
for a, bs in A.items():
    if not special(a):
        continue
    for b, c in E:
        if a == b or a == c:
            continue
        if b not in bs or c not in bs:
            continue
        k = sum(special(x) for x in [b, c])
        cnts[k] += 1

assert cnts[1] % 2 == 0
assert cnts[2] % 3 == 0
print(cnts[0] + cnts[1]//2 + cnts[2]//3)
