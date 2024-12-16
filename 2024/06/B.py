di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

G = []
while True:
    try:
        G.append([c for c in input()])
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

def nextdir(d):
    return 0 if d == 3 else d+1

def ok(i, j, d, done):
    while True:
        if (i, j, d) in done:
            return True
        done.add((i, j, d))
        ii = i + di[d]
        jj = j + dj[d]
        if not (0 <= ii < n) or not (0 <= jj < m):
            return False
        if G[ii][jj] == '#':
            d = nextdir(d)
        else:
            i, j = ii, jj
    raise Exception()

done = set()
i, j = getloc()
sol = 0
d = 0
while True:
    done.add((i, j, d))
    ii = i + di[d]
    jj = j + dj[d]
    if not (0 <= ii < n) or not (0 <= jj < m):
        break
    if G[ii][jj] == '#':
        d = nextdir(d)
    else:
        if G[ii][jj] == '.':
            G[ii][jj] = '#'
            if ok(i, j, nextdir(d), set(done)):
                sol += 1
            G[ii][jj] = '^'
        i, j = ii, jj
print(sol)
