from functools import cache

have = input().split(', ')
input()

def matches(s, at, h):
    assert at + len(h) <= len(s)
    for i in range(len(h)):
        if s[at+i] != h[i]:
            return False
    return True

def ways(s):
    n = len(s)
    w = [0] * (n+1)
    w[0] = 1
    for at in range(n):
        if not w[at]:
            continue
        for h in have:
            nn = at + len(h)
            if nn > n:
                continue
            if matches(s, at, h):
                w[nn] += w[at]
    return w[n]

sol = 0
while True:
    try:
        s = input()
    except EOFError:
        break
    sol += ways(s)
print(sol)
