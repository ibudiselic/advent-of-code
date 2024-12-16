def get(x, level):
    if level == 25:
        return 1
    if x == 0:
        return get(1, level+1)
    s = str(x)
    n = len(s)
    if n & 1:
        return get(x*2024, level+1)
    return get(int(s[:n//2]), level+1) + get(int(s[n//2:]), level+1)

sol = 0
for x in [int(x) for x in input().split(' ')]:
    sol += get(x, 0)
print(sol)
