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

di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

def go(i, j):
    area = 1
    perim = 0
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
            else:
                perim += 1
    return area * perim

sol = 0
for i in range(1, n-1):
    for j in range(1, m-1):
        if not done[i][j]:
            sol += go(i, j)
print(sol)
