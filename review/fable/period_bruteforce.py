#!/usr/bin/env python3
"""End-to-end check of delta(k) for small k: count n in one full period [N0, N0 + D_k) with exactly
one bad index, using ONLY math.comb and big-integer modulo (no Legendre, no lemmas).
D_k = prod_{p<=k} p^(2 floor(log_p k)).  Compare count/D_k with density_exact.py."""
import sys
from math import comb
from fractions import Fraction
sys.path.insert(0, __import__("os").path.dirname(__file__))
from density_exact import density, primes_upto

for k in map(int, sys.argv[1:]):
    D = 1
    for p in primes_upto(k):
        L = 0
        while p ** (L + 1) <= k: L += 1
        D *= p ** (2 * L)
    N0 = 2 * k
    cnt = 0
    n = N0
    C = comb(n, k)
    for n in range(N0, N0 + D):
        bad = 0
        for i in range(k):
            if C % (n - i):
                bad += 1
                if bad > 1: break
        cnt += (bad == 1)
        C = C * (n + 1) // (n + 1 - k)     # C(n+1,k)
    d_exact, _ = density(k, periodicity_check=False)
    print(f"k={k} D={D} count={cnt} count/D={Fraction(cnt, D)} formula={d_exact} match={Fraction(cnt, D) == d_exact}", flush=True)
