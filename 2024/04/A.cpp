#include <algorithm>
#include <cassert>
#include <cstdio>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <string>
#include <utility>
#include <vector>

using namespace std;

const int di[] = {-1, -1, 0, 1, 1, 1, 0, -1};
const int dj[] = {0, 1, 1, 1, 0, -1, -1, -1};
vector<string> A;

constexpr string need = "XMAS";

bool ok(int i, int j, int d) {
  for (int k = 0; k < (int)need.size(); ++k) {
    int ii = i + k * di[d];
    int jj = j + k * dj[d];
    if (ii < 0 || ii >= (int)A.size()) return false;
    if (jj < 0 || jj >= (int)A[ii].size()) return false;
    if (A[ii][jj] != need[k]) return false;
  }
  return true;
}

int main() {
  string s;
  while (cin >> s) {
    A.push_back(s);
  }
  int sol = 0;
  for (int i = 0; i < (int)A.size(); ++i) {
    for (int j = 0; j < (int)A[i].size(); ++j) {
      for (int d = 0; d < 8; ++d) {
        if (ok(i, j, d)) {
          ++sol;
        }
      }
    }
  }
  cout << sol << '\n';
}
