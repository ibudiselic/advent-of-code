import re

button_re = re.compile(r'Button [AB]: X\+(\d+), Y\+(\d+)')
prize_re = re.compile(r'Prize: X=(\d+), Y=(\d+)')

def get_input():
    while True:
        s = input()
        if s:
            break
    m = button_re.match(s)
    assert m is not None, s
    xa, ya = [int(t) for t in m.groups()]

    s = input()
    m = button_re.match(s)
    assert m is not None, s
    xb, yb = [int(t) for t in m.groups()]

    s = input()
    m = prize_re.match(s)
    assert m is not None, s
    x, y = [int(t) for t in m.groups()]

    return xa, ya, xb, yb, x, y

def solve():
    xa, ya, xb, yb, x, y = get_input()
    def dbg(s):
        print(xa, ya, xb, yb, x, y, '=>', s)
    if xa*yb == xb*ya:
        n = x*ya - b*xa*yb
        if n < 0:
            return 0
        d = xa*ya
        if n%d != 0:
            return 0
        a = n // d
        xx = x - a*xa
        yy = y - a*ya
        assert xx >= 0, xx
        assert yy >= 0, yy
        if xx % xb != 0 or yy % yb != 0:
            return 0
        b = xx // xb
        if b != yy // yb:
            return 0
    else:
        n = y*xa - x*ya
        d = xa*yb - xb*ya
        if n < 0 and d < 0:
            n = -n
            d = -d
        if n < 0 or d < 0 or n % d != 0:
            return 0
        b = n // d
        n = x - b*xb
        d = xa
        if n < 0 or n % d != 0:
            return 0
        a = n // d
    assert a*xa + b*xb == x
    assert a*ya + b*yb == y
    return 3*a + b

sol = 0
while True:
    try:
        sol += solve()
    except EOFError:
        break
print(sol)
