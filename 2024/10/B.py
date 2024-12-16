from collections import defaultdict
import sys

di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

G = [line.rstrip() for line in sys.stdin]
n = len(G)
m = len(G[0])

P = defaultdict(list)

for i in range(n):
    for j in range(m):
        P[ord(G[i][j])-ord('0')].append((i, j))
dp = [[0]*m for _ in range(n)]
for i, j in P[9]:
    dp[i][j] = 1

sol = 0
for val in range(8, -1, -1):
    for i, j in P[val]:
        for d in range(4):
            ii = i + di[d]
            jj = j + dj[d]
            if not (0 <= ii < n) or not (0 <= jj < m) or ord(G[ii][jj]) != ord(G[i][j])+1:
                continue
            dp[i][j] += dp[ii][jj]
        if val == 0:
            sol += dp[i][j]
print(sol)
