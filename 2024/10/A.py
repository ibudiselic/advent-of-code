import sys

di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

G = [line.rstrip() for line in sys.stdin]
n = len(G)
m = len(G[0])

def get(i, j):
    done = [[False]*m for _ in range(n)]
    done[i][j] = True
    head = 0
    Q = [(i, j)]
    ret = 0
    while head < len(Q):
        i, j = Q[head]
        head += 1
        for d in range(4):
            ii = i + di[d]
            jj = j + dj[d]
            if not (0 <= ii < n) or not (0 <= jj < m):
                continue
            if ord(G[i][j])+1 != ord(G[ii][jj]) or done[ii][jj]:
                continue
            done[ii][jj] = True
            if G[ii][jj] == '9':
                ret += 1
            else:
                Q.append((ii, jj))
    return ret

sol = 0
for i in range(n):
    for j in range(m):
        if G[i][j] == '0':
            sol += get(i, j)
print(sol)
