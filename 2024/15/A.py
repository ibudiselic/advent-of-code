import sys

def replace_impl(s, i, c):
    return ''.join([s[:i], c, s[i+1:]])

G = []

def replace(i, j, c):
    G[i] = replace_impl(G[i], j, c)

def getpos():
    for i, s in enumerate(G):
        for j, c in enumerate(s):
            if c == '@':
                return i, j
    raise ValueError('initial position not found')

mode = 0
dirs = []
for line in sys.stdin:
    line = line.rstrip()
    if not line:
        assert mode == 0
        mode = 1
        continue
    if mode == 0:
        G.append(line)
    else:
        assert mode == 1
        dirs.append(line)

dirs = ''.join(dirs)
i, j = getpos()
replace(i, j, '.')
D = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
}

n = len(G)
m = len(G[0])
for d in dirs:
    di, dj = D[d]
    ii = i + di
    jj = j + dj
    if G[ii][jj] == '.':
        i = ii
        j = jj
        continue
    r = ii
    c = jj
    while G[r][c] == 'O':
        r += di
        c += dj
    if G[r][c] == '#':
        continue
    assert G[r][c] == '.'
    assert r != ii or c != jj
    replace(r, c, 'O')
    replace(ii, jj, '.')
    i = ii
    j = jj

sol = 0
for i in range(n):
    for j in range(m):
        if G[i][j] == 'O':
            sol += 100*i+j
print(sol)
