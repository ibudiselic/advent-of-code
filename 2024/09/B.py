from dataclasses import dataclass
import heapq

@dataclass
class File:
    fileid: int
    start: int
    sz: int

nxt = 0
A = []
pos = 0
slots = [[] for _ in range(10)]
for i, sz in enumerate(input()):
    sz = int(sz)
    if (i&1) == 0:
        # There are no 0-size files (true in the input).
        # Otherwise, the problem would be a bit more difficult as slots could
        # be much larger.
        assert sz > 0
        A.append(File(nxt, pos, sz))
        nxt += 1
    else:
        slots[sz].append(pos)
    pos += sz

for s in slots:
    heapq.heapify(s)

for f in reversed(A):
    bestsz = None
    for slotsz in range(f.sz, 10):
        if slots[slotsz] and (bestsz == None or slots[bestsz][0] > slots[slotsz][0]):
            bestsz = slotsz
    if bestsz is None or slots[bestsz][0] > f.start:
        continue
    newsz = bestsz - f.sz
    slotpos = heapq.heappop(slots[bestsz])
    f.start = slotpos
    if newsz > 0:
        heapq.heappush(slots[newsz], slotpos+f.sz)

sol = 0
for f in A:
    sol += f.fileid * (f.sz*f.start + f.sz*(f.sz-1)//2)
print(sol)
