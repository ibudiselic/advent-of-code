import re
import sys

mul_re = re.compile(r'(do\(\)|don\'t\(\))|mul\((\d\d?\d?),(\d\d?\d?)\)')

do = True
sol = 0
for line in sys.stdin:
    line = line.rstrip()
    for m in mul_re.findall(line):
        if m[0] == 'do()':
            do = True
        elif m[0] == 'don\'t()':
            do = False
        elif do:
            _, x, y = m
            sol += int(x) * int(y)
print(sol)
