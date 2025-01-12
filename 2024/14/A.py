import re
import sys

RE = re.compile(r'p=([^,]+?),([^ ]+?) v=([^,]*?),(\S+)')

def modfix(x, X):
    if x < 0:
        x += (-x+X-1) // X * X
    elif x >= X:
        x %= X
    assert 0 <= x < X, f'{x=} {X=}'
    return x

def coord(x, X):
    x = modfix(x, X)
    if x == X // 2:
        return -1
    return 0 if x < X//2 else 1

X = 101
Y = 103
nsteps = 100
cnt = [[0] * 2 for _ in range(2)]

for line in sys.stdin:
    m = RE.match(line)
    assert m is not None, line
    x, y, dx, dy = [int(p) for p in m.groups()]
    x += nsteps * dx
    y += nsteps * dy
    x = coord(x, X)
    y = coord(y, Y)
    if x != -1 and y != -1:
        cnt[x][y] += 1

sol = 1
for i in range(2):
    for j in range(2):
        sol *= cnt[i][j]
print(sol)
