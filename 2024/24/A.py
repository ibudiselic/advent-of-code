from dataclasses import dataclass
from collections import defaultdict, deque
import sys

@dataclass(frozen=True, slots=True)
class Gate:
    a: str
    b: str
    c: str
    op: str

def compute(a, b, op):
    match op:
        case 'AND': return a&b
        case 'OR': return a|b
        case 'XOR': return a^b
        case _: assert False

wires = {}
gates = []
# str -> [int] (indices of the gates)
wire_out_gates = defaultdict(list)


inmode = 0
Q = deque()
for line in sys.stdin:
    line = line.rstrip()
    if not line:
        assert inmode == 0
        inmode = 1
    elif inmode == 0:
        wire, val = line.split(': ')
        val = int(val)
        assert 0 <= val <= 1
        wires[wire] = val
        Q.append(wire)
    else:
        assert inmode == 1
        a, op, b, _, c = line.split(' ')
        assert _ == '->'
        wire_out_gates[a].append(len(gates))
        wire_out_gates[b].append(len(gates))
        gates.append(Gate(a, b, c, op))

while Q:
    a = Q.popleft()
    for gi in wire_out_gates[a]:
        g = gates[gi]
        if g.a not in wires or g.b not in wires:
            continue
        assert a == g.a or a == g.b
        aval = wires[g.a]
        bval = wires[g.b]
        wires[g.c] = compute(aval, bval, g.op)
        Q.append(g.c)

z = 0
for w, val in wires.items():
    if w[0] == 'z':
        z |= val<<int(w[1:])
print(z)
