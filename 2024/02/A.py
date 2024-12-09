import sys

nsafe = 0
for line in sys.stdin:
    line = line.rstrip()
    a = [int(p) for p in line.split()]
    if a[0] == a[1]:
      continue
    if a[0] > a[1]:
        a.reverse()
    for i in range(1, len(a)):
        if a[i-1] >= a[i] or a[i]-a[i-1] > 3:
            break
    else:
        nsafe += 1
print(nsafe)
