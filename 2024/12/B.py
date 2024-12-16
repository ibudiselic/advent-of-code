import sys

G_ = [f'@{line.rstrip()}@' for line in sys.stdin]
n = len(G_) + 2
m = len(G_[0])
top_ = '@'*m
G = [top_]
G.extend(G_)
G.append(top_)
del G_, top_

done = [[False]*m for _ in range(n)]
side_counted = [[[False]*4 for _ in range(m)] for _ in range(n)]

di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

def record_side(i, j, d):
    for delta in [1, 3]:
        dd = d + delta
        if dd >= 4:
            dd -= 4
        assert 0 <= dd < 4
        r = i
        c = j
        while G[r][c] == G[i][j] and G[r+di[d]][c+dj[d]] != G[i][j]:
            side_counted[r][c][d] = True
            r += di[dd]
            c += dj[dd]

def go(i, j):
    area = 1
    nsides = 0
    head = 0
    Q = [(i, j)]
    v = G[i][j]
    done[i][j] = True
    while head < len(Q):
        i, j = Q[head]
        head += 1
        for d in range(4):
            ii = i + di[d]
            jj = j + dj[d]
            if G[ii][jj] == v:
                if not done[ii][jj]:
                    done[ii][jj] = True
                    area += 1
                    Q.append((ii, jj))
            elif not side_counted[i][j][d]:
                nsides += 1
                record_side(i, j, d)
    return area * nsides

sol = 0
for i in range(1, n-1):
    for j in range(1, m-1):
        if not done[i][j]:
            sol += go(i, j)
print(sol)
