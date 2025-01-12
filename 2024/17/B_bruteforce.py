# For moderately complex programs where the target value has lots of digits, this brute-force
# search has no hope of finding the solution in reasonable time.

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

inputR = [get_reg_input() for _ in range(3)]
input()
inputP = get_program_input()

class Register:
    def __init__(self, m, i):
        self.m = m
        self.i = i

    def get(self):
        return self.m.R[self.i]

    def set(self, v):
        self.m.R[self.i] = v

class Machine:
    def __init__(self, R, P):
        self.R = R
        self.P = P
        self.at = 0

        self.A = Register(self, 0)
        self.B = Register(self, 1)
        self.C = Register(self, 2)

        self.sol = []

    def combo(self, k):
        if k <= 3:
            return k
        assert 4 <= k < 7
        return self.R[k-4]

    def div_impl(self, op, outreg):
        n = self.A.get()
        d = 2**self.combo(op)
        outreg.set(n // d)

    def adv(self, op):
        self.div_impl(op, self.A)

    def bxl(self, op):
        self.B.set(self.B.get() ^ op)

    def bst(self, op):
        self.B.set(self.combo(op) & 7)

    def jnz(self, op):
        if self.A.get() != 0:
            self.at = op

    def bxc(self, op):
        self.B.set(self.B.get()^self.C.get())

    def out(self, op):
        self.sol.append(self.combo(op) & 7)

    def bdv(self, op):
        self.div_impl(op, self.B)

    def cdv(self, op):
        self.div_impl(op, self.C)

    def is_quine(self):
        assert not self.sol
        F = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]
        while self.at < len(self.P):
            opcode = self.P[self.at]
            op = self.P[self.at+1]
            self.at += 2
            F[opcode](op)
            if F[opcode] == self.out and (len(self.sol) > len(self.P) or self.sol[-1] != self.P[len(self.sol) - 1]):
                return False
        return self.sol == self.P

a = 1
while True:
    R = inputR[:]
    R[0] = a
    m = Machine(R, inputP)
    if m.is_quine():
        print(a)
        break
    a += 1
