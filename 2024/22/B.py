from collections import defaultdict

P = 2**24 - 1

def f(k):
    k = (k ^ (k<<6)) & P
    k = (k ^ (k>>5)) & P
    k = (k ^ (k<<11)) & P
    return k

def go(k, n):
    ret = [k%10]
    for _ in range(n):
        k = f(k)
        ret.append(k%10)
    return ret

def add_diff(diffs, d):
    if len(diffs) < 4:
        diffs.append(d)
        return
    for i in range(3):
        diffs[i] = diffs[i+1]
    diffs[3] = d

total = defaultdict(int)
while True:
    try:
        k = int(input())
    except EOFError:
        break
    prices = go(k, 2000)
    diffs = []
    done = set()
    for i, p in enumerate(prices):
        if i > 0:
            add_diff(diffs, p-prices[i-1])
            if len(diffs) < 4:
                continue
            key = tuple(diffs)
            if key in done:
                continue
            done.add(key)
            total[key] += p

print(max((v, k) for k, v in total.items())[0])
