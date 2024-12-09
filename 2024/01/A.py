import sys

a = []
b = []
for line in sys.stdin:
    p = line.index(' ')
    a.append(int(line[:p]))
    b.append(int(line[p:].strip()))
a.sort()
b.sort()
print(sum(abs(x-y) for x, y in zip(a, b)))
