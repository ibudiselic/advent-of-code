from collections import defaultdict
import sys

rules = defaultdict(set)

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
        if ok(x):
            assert len(x) % 2 == 1
            sol += x[len(x) // 2]
print(sol)
