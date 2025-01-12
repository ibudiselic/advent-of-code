from dataclasses import dataclass
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

X = 101
Y = 103
badlim = 32

@dataclass()
class Robot:
    x: int
    y: int
    dx: int
    dy: int

    def step(self):
        self.x += self.dx
        self.x = modfix(self.x, X)
        self.y += self.dy
        self.y = modfix(self.y, Y)

robots = []
for line in sys.stdin:
    m = RE.match(line)
    assert m is not None, line
    x, y, dx, dy = [int(p) for p in m.groups()]
    robots.append(Robot(x, y, dx, dy))

for steps in range(100000):
    for r in robots:
        r.step()
    grid = [['.'] * X for _ in range(Y)]
    for r in robots:
        grid[r.y][r.x] = '*'
    nbad = 0
    prevcnt = 0
    for row in grid:
        cnt = sum(g == '*' for g in row)
        if cnt > 0:
            if cnt < prevcnt:
                nbad += 1
                if nbad > badlim:
                    break
            prevcnt = cnt
    if nbad <= badlim:
        print(steps + 1, '->', nbad)
        for row in grid:
            print(''.join(row))
        print()

