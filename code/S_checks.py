#!/usr/bin/env python3
"""Numerics for Proposition 8. S(k) = sum over primes sqrt(k) < p <= k, p not dividing k, of log(p/(k mod p)).
Prints window means of S(k)/(k/log k) and the range of log(1/delta(k)) - S(k) for k <= 100."""
import math, bisect, sys
N = 1000100
sv = bytearray([1]) * (N + 1); sv[0] = sv[1] = 0
for i in range(2, int(N**.5) + 1):
    if sv[i]: sv[i*i::i] = bytearray(len(sv[i*i::i]))
P = [i for i in range(N + 1) if sv[i]]
def S(k):
    lo = bisect.bisect_right(P, math.isqrt(k)); hi = bisect.bisect_right(P, k)
    return sum(math.log(p / (k % p)) for p in P[lo:hi] if k % p)
C = sum(math.log1p(1/j)/j for j in range(1, 10**6)) + 1e-6
print(f"C = sum_j (1/j) log(1+1/j) ~ {C:.7f}")
for c, w in [(100, 10), (400, 10), (1000, 10), (10000, 10), (100000, 5), (1000000, 3)]:
    rs = [S(k) / (k / math.log(k)) for k in range(c - w, c + w + 1)]
    print(f"k~{c:>7}: mean S(k)/(k/log k) = {sum(rs)/len(rs):.3f} over {len(rs)} k (min {min(rs):.3f}, max {max(rs):.3f})")
dens = {}
for f in ['data/density2_2_59.txt', 'data/density2_60_100.txt']:
    for l in open(f): t = l.split(); dens[int(t[0])] = float(t[1])
diff = {k: dens[k] - S(k) for k in range(2, 101)}
for lo, hi in [(2, 100), (31, 100), (60, 100)]:
    sub = {k: diff[k] for k in range(lo, hi + 1)}
    kmax = max(sub, key=sub.get)
    print(f"log(1/delta)-S(k) for k={lo}..{hi}: min {min(sub.values()):.2f}, max {max(sub.values()):.2f} (at k={kmax})")
