import re
import sys

mul_re = re.compile(r'mul\((\d\d?\d?),(\d\d?\d?)\)')

sol = 0
for line in sys.stdin:
    line = line.rstrip()
    for x, y in mul_re.findall(line):
        sol += int(x) * int(y)
print(sol)
