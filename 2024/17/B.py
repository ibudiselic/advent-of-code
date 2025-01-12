# Specialized to the input (though the initial B and C values also don't matter):
# 
#   Register A: ???
#   Register B: 0
#   Register C: 0
#   
#   Program: 2,4,1,3,7,5,1,5,0,3,4,3,5,5,3,0
#
# This program that outputs the last value can be simplified to:
#
#   out (!a_47 !a_46 a_45) ^ [(a_47 a_46 a_45) >> (a_47 !a_46 !a_45)]  // this must equal P[15] == 0 (mod 8)
#   A >>= 3
#   jnz 0
#
# Manually solving this, it turns out that (a_47 a_46 a_45) = (1 0 1).
#
# On the iteration yielding the ith output (going from i == 15 downward), we have:
#
#   out (!a_{3i+2} !a_{3i+1} a_{3i}) ^ [(a_47 a_46 ... a_{3i+3} a_{3i+2} a_{3i+1} a_{3i}) >> (a_{3i+2} !a_{3i+1} !a_{3i})]  // must equal P[i] (mod 8)
#   A >>= 3
#   jnz 0
#
# This program just tries all 8 values for each sequence of 3 bits of A.

from functools import cache
import sys

def get_reg_input():
    parts = input().split(': ')
    assert len(parts) == 2
    assert parts[0].startswith('Register')
    return int(parts[1])

def get_program_input():
    parts = input().split(': ')
    assert len(parts) == 2
    assert parts[0].startswith('Program')
    return [int(x) for x in parts[1].split(',')]

[get_reg_input() for _ in range(3)]
input()
P = get_program_input()
# This script only works for this program.
assert P == [2,4,1,3,7,5,1,5,0,3,4,3,5,5,3,0]

@cache
def go(A, at):
    if at == -1:
        return A
    out = P[at]
    for v in range(8):
        a = (A<<3)|v
        b = v ^ 6
        c = a >> (v ^ 3)
        if (b^c)&7 == out:
            cand = go(a, at-1)
            if cand is not None:
                return cand
    return None

print(go(0, len(P)-1))
