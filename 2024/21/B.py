from dataclasses import dataclass

NLAYERS = 25

ALL_SYM = '^>v<A'
# The order must match `ALL_SYM`.
DIRS = [ 
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]

@dataclass(frozen=True, slots=True)
class P:
    i: int
    j: int

    def move(self, d):
        di, dj = DIRS[d]
        return P(self.i+di, self.j+dj)

class Pathgen:
    def __init__(self, keypad):
        self.sympos = {}
        self.valid = set()
        for i, s in enumerate(keypad):
            for j, c in enumerate(s):
                if c != ' ':
                    assert c not in self.sympos
                    p = P(i, j)
                    self.sympos[c] = p
                    self.valid.add(p)

    def generate_paths(self, src, dest):
        """Generates all valid paths between the given symbols on the keypad.

        A path is represented as a string of motion symbols that need to be
        input into the keypad's controlling robot to execute the path.

        Valid paths never go off the keypad's symbol keys, and never cross the
        same key on the keypad more than once.
        """
        assert src != dest
        prefix = []
        visited = set()
        yield from self._generate_paths(self.sympos[src], self.sympos[dest], prefix, visited)

    def _generate_paths(self, u, v, prefix, visited):
        if u == v:
            yield ''.join(prefix)
            return
        for d in range(len(DIRS)):
            prefix.append(ALL_SYM[d])
            p = u.move(d)
            if p in self.valid and p not in visited:
                visited.add(p)
                yield from self._generate_paths(p, v, prefix, visited)
                visited.remove(p)
            prefix.pop()

INF = 2**63

# Dynamic programming
# For each layer of the keypad, compute the cost of outputting symbol `x` after
# outputting symbol `y` before that as `cur[(x, y)]` using `prev` which has this
# computed for the previous layer.

def path_cost(path, prev):
    # The robot at the current layer needs to traverse the path after producing
    # the previous output and then produce the next output.
    # Just before starting to traverse the path, given that the robot at the
    # current layer produced some output, all robots on the previous layers
    # (including the robot on the previous layer) must be positioned on 'A'.
    # Then the robot on the previous layer needs to output `path[0]`, and the
    # cost for doing that is stored in `prev[(path[0], 'A')]`.
    cost = prev[(path[0], 'A')]
    # Then the robot on the previous layer outputs the remaining directional
    # symbols on the path. 
    for i in range(1, len(path)):
        cost += prev[(path[i], path[i-1])]
    # Finally, the robot on the previous layer again outputs 'A' for the robot
    # on the current layer to complete its target output.
    cost += prev[('A', path[-1])]
    return cost


def bestpath(src, dest, prev, pad, path_memo):
    assert src != dest
    ret = path_memo.get((src, dest), None)
    if ret is not None:
        return ret
    best = INF
    for path in pad.generate_paths(src, dest):
        cand = path_memo.get(path, None)
        if cand is None:
            cand = path_cost(path, prev)
            path_memo[path] = cand
        if cand < best:
            best = cand
    path_memo[(src, dest)] = best
    return best

dirpad = Pathgen([' ^A', '<v>'])
numpad = Pathgen(['789', '456', '123', ' 0A'])

def solve(code, prev, path_memo):
    cost = 0
    at = 'A'
    for c in code:
        cost += bestpath(at, c, prev, numpad, path_memo)
        at = c
    return cost

# The human-operated keypad has all costs equal to 1.
prev = {(x, y): 1 for x in ALL_SYM for y in ALL_SYM}
cur = None

for _ in range(NLAYERS):
    cur = {}
    layer_paths = {}
    for x in ALL_SYM:
        for y in ALL_SYM:
            if x == y:
                # To repeat some output always costs 1 (the human just presses
                # A again and all the robots up to this layer are already on A
                # as they just output `y` on the previous step).
                cur[(x, y)] = 1
            else:
                cur[(x, y)] = bestpath(y, x, prev, dirpad, layer_paths)
    prev = cur

layer_paths = {}
# And now compute the costs of the paths
sol = 0
for i in range(5):
    code = input()
    assert code[-1] == 'A'
    sol += int(code[:-1], 10) * solve(code, prev, layer_paths)
print(sol)
