from collections import deque
from dataclasses import dataclass
from typing import Self

DIRS = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
}

@dataclass(frozen=True, slots=True)
class P:
    i: int
    j: int

    def move(self, c):
        di, dj = DIRS[c]
        return P(self.i+di, self.j+dj)
        

class Keypad:

    def __init__(self, keys):
        pad = ' ' * (len(keys[0])+2)
        self.keys = [pad]
        self.keys.extend([f' {k} ' for k in keys])
        self.keys.append(pad)
        self.n = len(self.keys)
        self.m = len(self.keys[0])

    def getA(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.keys[i][j] == 'A':
                    return P(i, j)
        raise ValueError(f'do not have A in {self.keys}')

DONE = object()
code = None

@dataclass(frozen=True, slots=True)
class CodeAt:
    at: int

    def advance(self, c):
        assert self.at < len(code)
        if code[self.at] != c:
            return None
        if self.at + 1 == len(code):
            return DONE
        return CodeAt(self.at+1)

@dataclass(frozen=True, slots=True)
class State:
    p: P
    next: Self | CodeAt

def make_keypads():
    dirK = Keypad([' ^A', '<v>'])
    numK = Keypad(['789', '456', '123', ' 0A'])
    return [dirK, dirK, numK]

K = make_keypads()

def _make_init_state(at):
    if at == len(K):
        return CodeAt(0)
    return State(K[at].getA(), _make_init_state(at+1))

def make_init_state():
    return _make_init_state(0)

def _advance(at, s, c):
    if isinstance(s, CodeAt):
        assert at == len(K)
        return s.advance(c)
    if c == 'A':
        next = _advance(at+1, s.next, K[at].keys[s.p.i][s.p.j])
        if next is DONE or next is None:
            return next
        return State(s.p, next)
    p = s.p.move(c)
    if K[at].keys[p.i][p.j] == ' ':
        return None
    return State(p, s.next)

def advance(s, c):
    return _advance(0, s, c)

def solve():
    s = make_init_state()
    Q = deque([s])
    done = {s}
    dist = -1
    distsz = 0
    while Q:
        if distsz == 0:
            distsz = len(Q)
            dist += 1
        s = Q.popleft()
        distsz -= 1
        for c in '^>v<A':
            ns = advance(s, c)
            if ns is DONE:
                return dist + 1
            if ns is not None and ns not in done:
                done.add(ns)
                Q.append(ns)
    raise AssertionError('not solvable - should never happen')

sol = 0
for i in range(5):
    code = input()
    assert code[-1] == 'A'
    sol += int(code[:-1], 10) * solve()
print(sol)
