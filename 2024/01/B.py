from collections import defaultdict
import sys

a = []
b = defaultdict(int)
for line in sys.stdin:
    p = line.index(' ')
    a.append(int(line[:p]))
    b[int(line[p:].strip())] += 1
print(sum(x * b[x] for x in a))
