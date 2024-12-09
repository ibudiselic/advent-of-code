import sys

def ok(a):
    assert len(a) >= 2
    if a[0] == a[1]:
      return False
    if a[0] > a[1]:
        a.reverse()
    for i in range(1, len(a)):
        if a[i-1] >= a[i] or a[i]-a[i-1] > 3:
            return False
    return True

nsafe = 0
for line in sys.stdin:
    line = line.rstrip()
    a = [int(p) for p in line.split()]
    if ok(a):
        nsafe += 1
        continue
    for i in range(len(a)):
        b = a[:i] + a[i+1:]
        if ok(b):
            nsafe += 1
            break
print(nsafe)
