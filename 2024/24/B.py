from dataclasses import dataclass
from collections import defaultdict, deque
from functools import reduce
import random
import sys
from typing import Self

OPMAP = {
    'AND': '&',
    'OR': '|',
    'XOR': '^',
}

@dataclass(frozen=True, slots=True)
class Gate:
    a: str
    b: str
    c: str
    op: str

def andop(a, b): return a & b
def orop(a, b): return a | b
def xorop(a, b): return a ^ b

def getop(op):
    match op:
        case '&': return andop
        case '|': return orop
        case '^': return xorop
        case _: assert False

def applyop(op, vals):
    op = getop(op)
    assert vals
    return reduce(op, vals)

def addvals(mask, v, bits):
    b = 1
    while b <= mask:
        if mask & b:
            bits.append(1 if (v&b) else 0)
        b <<= 1

@dataclass(frozen=True, slots=True)
class Expr:
    op: str
    x: int  # Mask of bits from the x variable that get operated on by op.
    y: int
    other: list[Self]  # Other operands.

    def eval(self, x, y):
        vals = [o.eval(x, y) for o in self.other]
        addvals(self.x, x, vals)
        addvals(self.y, y, vals)
        return applyop(self.op, vals)

    def __str__(self):
        if self.x == 0 and self.y == 0 and not self.other:
            return '(***0***)'
        # assert int.bit_count(self.x) <= 1, self.x
        parts = []
        if self.x == self.y:
            if self.x:
                parts.append(f'[{self.x}_{self.op}]')
        else:
            if self.x:
                parts.append(f'***DIFF***x_{self.x}')
            if self.y:
                parts.append(f'***DIFF***y_{self.y}')
        parts.extend(str(o) for o in self.other)
        if len(parts) == 1:
            return parts[0]
        inner = f'{self.op}'.join(sorted(parts, key=lambda s: (len(s), s)))
        return f'({inner})'

def opmerge(a, b, op):
    match op:
        case '&' | '|': return a|b
        case '^': return a^b
        case _: assert False

def merge(a, b, op):
    if a.op == 'id' and b.op == 'id':
        return Expr(op, opmerge(a.x, b.x, op), opmerge(a.y, b.y, op), [])
    if b.op == 'id':
        a, b = b, a
    if a.op == 'id':
        if op == b.op:
            return Expr(op, opmerge(a.x, b.x, op), opmerge(a.y, b.y, op), b.other)
        else:
            return Expr(op, a.x, a.y, [b])
    assert a.op != 'id' and b.op != 'id'
    if a.op == b.op:
        if op == a.op:
            return Expr(op, opmerge(a.x, b.x, op), opmerge(a.y, b.y, op), a.other + b.other)
        else:
            return Expr(op, 0, 0, [a, b])
    if b.op == op:
        a, b = b, a
    if a.op == op:
        return Expr(op, a.x, a.y, a.other + [b])
    return Expr(op, 0, 0, [a, b])

wires = {}
gates = []
# str -> [int] (indices of the gates)
wire_out_gates = defaultdict(list)
formulas = {}

_rewires = [
    ('gwh', 'z09'),
    ('jct', 'z39'),
    ('rcb', 'z21'),
    ('wbw', 'wgb'),
]
rewires = {a: b for a, b in _rewires}
rewires.update({b: a for a, b in _rewires})

# pcAB stands for "partial carry for bit AB", and this is the part of the carry without the xAB&yAB part.
# cAB stands for the "carry bit from bit AB"
# Formulas:
#   pcAB = c[AB-1]&{^AB} where {^AB} stands for xAB^yAB.
#   cAB == pcAB|{&AB} where {&AB} stands for xAB&yAB.
#   zAB == c[AB-1]^{^AB}
renames = {
    'jcq': 'c00',
    'hnj': '{&01}',
    'sqk': '{^01}',
    'tng': '{&02}',
    'qpd': '{^02}',
    'rtt': '{&03}',
    'npk': '{^03}',
    'dtn': '{&04}',
    'ptv': '{^04}',
    'fkt': '{&05}',
    'sfn': '{^05}',
    'knd': '{&06}',
    'hsn': '{^06}',
    'vjc': '{&07}',
    'gjv': '{^07}',
    'qpg': '{&08}',
    'jhr': '{^08}',
    'ptc': '{&09}',
    'mnm': '{^09}',
    'bcw': '{&10}',
    'cvv': '{^10}',
    'cbm': '{&11}',
    'ksb': '{^11}',
    'njd': '{&12}',
    'htr': '{^12}',
    'wgb': '{&13}',
    'wbw': '{^13}',
    'ktg': '{&14}',
    'tfh': '{^14}',
    'vch': '{&15}',
    'pvj': '{^15}',
    'fhn': '{&16}',
    'vgb': '{^16}',
    'fpk': '{&17}',
    'tdb': '{^17}',
    'gpq': '{&18}',
    'jbp': '{^18}',
    'hhb': '{&19}',
    'mcv': '{^19}',
    'vwh': '{&20}',
    'vdc': '{^20}',
    'knb': '{&21}',
    'sbs': '{^21}',
    'dpg': '{&22}',
    'qgd': '{^22}',
    'nrw': '{&23}',
    'gcj': '{^23}',
    'frv': '{&24}',
    'kdn': '{^24}',
    'dbt': '{&25}',
    'nfm': '{^25}',
    'jck': '{&26}',
    'jkt': '{^26}',
    'fjr': '{&27}',
    'qrw': '{^27}',
    'shp': '{&28}',
    'rtb': '{^28}',
    'bqn': '{&29}',
    'wtw': '{^29}',
    'rvc': '{&30}',
    'qgc': '{^30}',
    'gpp': '{&31}',
    'tkw': '{^31}',
    'ttt': '{&32}',
    'wrd': '{^32}',
    'hbn': '{&33}',
    'pmg': '{^33}',
    'rkq': '{&34}',
    'bgg': '{^34}',
    'qph': '{&35}',
    'prn': '{^35}',
    'pfc': '{&36}',
    'dkj': '{^36}',
    'nbc': '{&37}',
    'vjg': '{^37}',
    'crp': '{&38}',
    'spg': '{^38}',
    'jct': '{&39}',
    'ksf': '{^39}',
    'qhf': '{&40}',
    'qwt': '{^40}',
    'kfp': '{&41}',
    'krk': '{^41}',
    'qjp': '{&42}',
    'sbn': '{^42}',
    'bmf': '{&43}',
    'nsb': '{^43}',
    'cvk': '{&44}',
    'jrb': '{^44}',
    'bmc': 'pc01',
    'kpf': 'c01',
    'pwk': 'pc02',
    'tpv': 'c02',
    'hrr': 'pc03',
    'bdk': 'c03',
    'nnq': 'pc04',
    'svk': 'c04',
    'wnq': 'pc05',
    'cjh': 'c05',
    'hds': 'pc06',
    'wcs': 'c06',
    'nbb': 'pc07',
    'bwm': 'c07',
    'tvw': 'pc08',
    'gqb': 'c08',
    'dsk': 'pc09',
    'gwh': 'c09',
    'pgn': 'pc10',
    'jbk': 'c10',
    'hgb': 'pc11',
    'jgf': 'c11',
    'dmc': 'pc12',
    'qwr': 'c12',
    'dqm': 'pc13',
    'nkd': 'c13',
    'jrd': 'pc14',
    'bgh': 'c14',
    'vcd': 'pc15',
    'nhh': 'c15',
    'btr': 'pc16',
    'ctv': 'c16',
    'ffh': 'pc17',
    'wtc': 'c17',
    'pfh': 'pc18',
    'ppf': 'c18',
    'gvt': 'pc19',
    'tjc': 'c19',
    'vvc': 'pc20',
    'kgk': 'c20',
    'rcb': 'pc21',
    'tvj': 'c21',
    'vsb': 'pc22',
    'grk': 'c22',
    'cdw': 'pc23',
    'pbv': 'c23',
    'mhd': 'pc24',
    'vsw': 'c24',
    'dfq': 'pc25',
    'kgs': 'c25',
    'wtd': 'pc26',
    'mjf': 'c26',
    'jgh': 'pc27',
    'whc': 'c27',
    'jsf': 'pc28',
    'vmj': 'c28',
    'nbw': 'pc29',
    'bqb': 'c29',
    'nth': 'pc30',
    'mwg': 'c30',
    'vmq': 'pc31',
    'mrg': 'c31',
    'vcm': 'pc32',
    'rnc': 'c32',
    'dmp': 'pc33',
    'kvw': 'c33',
    'gwm': 'pc34',
    'bhd': 'c34',
    'drv': 'pc35',
    'dmj': 'c35',
    'vnw': 'pc36',
    'jgc': 'c36',
    'mqh': 'pc37',
    'bwb': 'c37',
    'wjg': 'pc38',
    'wjf': 'c38',
    'hvf': 'pc39',
    'nhk': 'c39',
    'qwh': 'pc40',
    'sgk': 'c40',
    'qvv': 'pc41',
    'pwt': 'c41',
    'qwg': 'pc42',
    'gdt': 'c42',
    'dnc': 'pc43',
    'tdh': 'c43',
    'pjg': 'pc44',
}

# Make sure there are no duplicates in the renames.
rename_vals = set()
for a, b in renames.items():
    assert a not in rename_vals, a
    rename_vals.add(a)
    assert b not in rename_vals, b
    rename_vals.add(b)

def maybe_rewire(a):
    r = rewires.get(a, None)
    if r is not None:
        return r
    return a

def maybe_rename(a):
    r = renames.get(a, None)
    if r is not None:
        return r
    return a

# for a, b in sorted(renames.items(), key=lambda p: (p[1][2:], p[1])):
#     print(f"    '{a}': '{b}',")

inmode = 0
Q = deque()
for line in sys.stdin:
    line = line.rstrip()
    if not line:
        assert inmode == 0
        inmode = 1
    elif inmode == 0:
        wire, _ = line.split(': ')
        if wire[0] == 'x':
            x = 1<<int(wire[1:])
            y = 0
        else:
            assert wire[0] == 'y'
            x = 0
            y = 1<<int(wire[1:])
        wires[wire] = Expr('id', x, y, [])
        Q.append(wire)
    else:
        assert inmode == 1
        a, op, b, _, c = line.split(' ')
        assert _ == '->'
        op = OPMAP[op]
        a = maybe_rename(a)
        b = maybe_rename(b)
        # Rewires only apply to gate outputs (not to inputs)!
        c = maybe_rename(maybe_rewire(c))
        if b.startswith(('x', 'c', 'pc', 'z')):
            a, b = b, a
        wire_out_gates[a].append(len(gates))
        wire_out_gates[b].append(len(gates))
        gates.append(Gate(a, b, c, op))
        f = f'{a}{op}{b}'
        formulas[c] = f
        # if a[0] == 'x' and c[0] != 'z':
        #     try:
        #         k = int(a[1:])
        #     except:
        #         continue
        #     if f == f'x{k:02d}{op}y{k:02d}':
        #         # Generate renames for formulas operating on one bit of x and y.
        #         print(f"    '{c}': '{{{op}{k:02d}}}',")

while Q:
    a = Q.popleft()
    for gi in wire_out_gates[a]:
        g = gates[gi]
        if g.a not in wires or g.b not in wires:
            continue
        assert a == g.a or a == g.b
        aval = wires[g.a]
        bval = wires[g.b]
        wires[g.c] = merge(aval, bval, g.op)
        # if g.c == 'jcq':
        #     print(aval, g.op, bval)
        #     print(wires[g.c])
        #     exit(0)
        Q.append(g.c)

resolved = []
for w in wires:
    if w.startswith(('x', 'y')):
        continue
    resolved.append((str(wires[w]), w))
resolved.sort(key=lambda p: (len(p[0]), p[1], p[0]))
for r, w in resolved:
    f = formulas[w]
    print(w, formulas[w], r[:110])
    match w[0]:
        case 'z':
            k = int(w[1:])
            if w not in ('z00', 'z09', 'z10', 'z45'):
                assert f == f'c{k-1:02d}^{{^{k:02d}}}'
        case 'c':
            k = int(w[1:])
            if w != 'c00' and w != 'c09':
                assert f == f'pc{k:02d}|{{&{k:02d}}}'
        case 'p':
            if w not in ():
                assert w.startswith('pc')
                k = int(w[2:])
                assert f == f'c{k-1:02d}&{{^{k:02d}}}'
        case _: pass

# for i in range(45):
#     z = f'z{i:02d}'
#     print(z, formulas[z], wires[z])

# print()
# for w in ['kfp', 'qpd']:
#     print(w, formulas[w], wires[w])

print()
nbit = 45
nums = [2**nbit-1]
random.seed(123)
for _ in range(50):
    nums.append(random.randint(2**max(0, nbit-3), 2**nbit))
for x in nums:
    for y in nums:
        z = x+y
        zcomp = 0
        for b in range(nbit+1):
            zcomp |= wires[f'z{b:02d}'].eval(x, y)<<b
        if z != zcomp:
            print('FAILURE')
            print(f'for {x=} {y=} {z=} != {zcomp=}')
            print(f'{z:b}\n{zcomp:b}')
            exit(0)
print(f'{nbit=} OK')

print(','.join(sorted([p[0] for p in _rewires] + [p[1] for p in _rewires])))
