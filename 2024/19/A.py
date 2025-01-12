from functools import cache

have = input().split(', ')
input()

def matches(s, at, h):
    assert at + len(h) <= len(s)
    for i in range(len(h)):
        if s[at+i] != h[i]:
            return False
    return True

def can(s):
    n = len(s)
    ok = [False] * (n+1)
    ok[0] = True
    for at in range(n):
        if not ok[at]:
            continue
        for h in have:
            nn = at + len(h)
            if nn > n or ok[nn]:
                continue
            if matches(s, at, h):
                ok[nn] = True
    return ok[n]

sol = 0
while True:
    try:
        s = input()
    except EOFError:
        break
    if can(s):
        sol += 1
print(sol)
