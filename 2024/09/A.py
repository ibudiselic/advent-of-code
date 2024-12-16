from dataclasses import dataclass

@dataclass
class File:
    fileid: int
    start: int
    sz: int

nxt = 0
A = []
pos = 0
for i, sz in enumerate(input()):
    sz = int(sz)
    if (i&1) == 0:
        if sz > 0:
            A.append(File(nxt, pos, sz))
        nxt += 1
    pos += sz

sol = 0
pos = 0
at = 0
while True:
    assert pos == A[at].start
    for _ in range(A[at].sz):
        sol += A[at].fileid * pos
        pos += 1
    at += 1
    if at == len(A):
        break
    assert A[at].sz > 0
    while at < len(A) and pos < A[at].start:
        sol += A[-1].fileid * pos
        pos += 1
        if A[-1].sz == 1:
            A.pop()
        else:
            A[-1].sz -= 1
print(sol)
