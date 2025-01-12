import sys

def get_reg_input():
    parts = input().split(': ')
    assert len(parts) == 2
    assert parts[0].startswith('Register')
    return int(parts[1])

def get_program_input():
    parts = input().split(': ')
    assert len(parts) == 2
    assert parts[0].startswith('Program')
    return [int(x) for x in parts[1].split(',')]

R = [get_reg_input() for _ in range(3)]
input()
P = get_program_input()

at = 0

def combo(k):
    if k <= 3:
        return k
    assert 4 <= k < 7
    return R[k-4]

class Register:
    def __init__(self, i):
        self.i = i

    def get(self):
        return R[self.i]

    def set(self, v):
        R[self.i] = v

A = Register(0)
B = Register(1)
C = Register(2)

def div_impl(op, outreg):
    n = A.get()
    d = 2**combo(op)
    outreg.set(n // d)

def adv(op):
    div_impl(op, A)

def bxl(op):
    B.set(B.get() ^ op)

def bst(op):
    B.set(combo(op) & 7)

def jnz(op):
    global at
    if A.get() != 0:
        at = op

def bxc(op):
    B.set(B.get()^C.get())

sol = []

def out(op):
    global sol
    sol.append(str(combo(op) & 7))

def bdv(op):
    div_impl(op, B)

def cdv(op):
    div_impl(op, C)

F = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

while at < len(P):
    opcode = P[at]
    op = P[at+1]
    at += 2
    F[opcode](op)
print(','.join(sol))
