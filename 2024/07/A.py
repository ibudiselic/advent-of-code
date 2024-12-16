def generate_inputs():
    while True:
        try:
            line = input()
        except EOFError:
            return
        parts = line.split(' ')
        yield int(parts[0][:-1]), [int(x) for x in parts[1:]]

def can(target, cur, at, vs):
    if cur > target:
        return False
    if at == len(vs):
        return target == cur
    return can(target, cur+vs[at], at+1, vs) or can(target, cur*vs[at], at+1, vs)

sol = 0
for x, vs, in generate_inputs():
    if can(x, vs[0], 1, vs):
        sol += x
print(sol)
