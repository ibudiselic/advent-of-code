P = 2**24 - 1

def f(k):
    k = (k ^ (k<<6)) & P
    k = (k ^ (k>>5)) & P
    k = (k ^ (k<<11)) & P
    return k

def go(k, n):
    for _ in range(n):
        k = f(k)
    return k

sol = 0
while True:
    try:
        k = int(input())
    except EOFError:
        break
    sol += go(k, 2000)
print(sol)
