di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

G = []
while True:
    try:
        G.append(input())
    except:
        break

n = len(G)
m = len(G[0])

def getloc():
    for i in range(n):
        for j in range(m):
            if G[i][j] == '^':
                return i, j
    raise Exception()

done = set()
i, j = getloc()
d = 0
while True:
    done.add((i, j))
    ii = i + di[d]
    jj = j + dj[d]
    if not (0 <= ii < n) or not (0 <= jj < m):
        break
    if G[ii][jj] == '#':
        d += 1
        if d == 4:
            d = 0
    else:
        i, j = ii, jj
print(len(done))
