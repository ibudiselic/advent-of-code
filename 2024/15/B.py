import sys

def expand_one(c):
    match c:
        case '#': return '##'
        case 'O': return '[]'
        case '.': return '..'
        case '@': return '@.'
        case _: raise ValueError(f'unrecognized char {c}')


def expand(s):
    return ''.join(expand_one(c) for c in s)


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


def moveimpl(i, j, di, *, dryrun):
    assert G[i][j] == '[' and G[i][j+1] == ']'
    done = [[False] * m for _ in range(n)]
    done[i][j] == True
    stack = [(i, j, 0)]
    while stack:
        i, j, state = stack.pop()
        ii = i + di
        if state == 0:
            if not dryrun:
                stack.append((i, j, 1))
            if G[ii][j] == '#' or G[ii][j+1] == '#':
                assert dryrun
                return False
            if G[ii][j] == '[':
                assert G[ii][j+1] == ']'
                if not done[ii][j]:
                    done[ii][j] = True
                    stack.append((ii, j, 0))
            elif G[ii][j] == ']':
                assert G[ii][j-1] == '['
                if not done[ii][j-1]:
                    done[ii][j-1] = True
                    stack.append((ii, j-1, 0))
            if G[ii][j+1] == '[':
                assert G[ii][j+2] == ']'
                if not done[ii][j+1]:
                    done[ii][j+1] = True
                    stack.append((ii, j+1, 0))
            else:
                assert G[ii][j+1] == ']' or G[ii][j+1] == '.'
        else:
            assert state == 1
            assert not dryrun
            assert G[ii][j] == '.' and G[ii][j+1] == '.'
            G[ii] = ''.join([G[ii][:j], '[]', G[ii][j+2:]])
            G[i] = ''.join([G[i][:j], '..', G[i][j+2:]])
    return True


def canmove(i, j, di):
    return moveimpl(i, j, di, dryrun=True)


def domove(i, j, di):
    ret = moveimpl(i, j, di, dryrun=False)
    assert ret


def updown(i, j, d):
    di, _ = D[d]
    ii = i + di
    if G[ii][j] == '.':
        return ii, j
    if G[ii][j] == '#':
        return i, j
    if G[ii][j] == ']':
        assert G[ii][j-1] == '['
        i, j = updown(i, j-1, d)
        return i, j + 1
    assert G[ii][j] == '['
    if canmove(ii, j, di):
        domove(ii, j, di)
        return ii, j
    return i, j


def leftright(i, j, d):
    _, dj = D[d]
    jj = j + dj
    s = G[i]
    if s[jj] == '.':
        return i, jj
    c = jj
    while s[c] in '[]':
        c += dj
    if s[c] == '#':
        return i, j
    assert s[c] == '.'
    assert c != jj
    if d == 1:
        assert j < c
        s = ''.join([s[:j+1], '.', s[j+1:c], s[c+1:]])
    else:
        assert d == 3
        assert c < j
        s = ''.join([s[:c], s[c+1:j], '.', s[j:]])
    G[i] = s
    return i, jj

mode = 0
dirs = []
for line in sys.stdin:
    line = line.rstrip()
    if not line:
        assert mode == 0
        mode = 1
        continue
    if mode == 0:
        G.append(expand(line))
    else:
        assert mode == 1
        dirs.append(line)

dirs = ''.join(dirs)
i, j = getpos()
replace(i, j, '.')
D = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]
DMAP = {
    '^': 0,
    '>': 1,
    'v': 2,
    '<': 3,
}

n = len(G)
m = len(G[0])
for dchar in dirs:
    d = DMAP[dchar]
    if d == 0 or d == 2:
        i, j = updown(i, j, d)
    else:
        i, j = leftright(i, j, d)


sol = 0
for i in range(n):
    for j in range(m):
        if G[i][j] == '[':
            sol += 100*i+j
print(sol)
