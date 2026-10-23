#!/usr/bin/env python3
"""Reference brute force for Erdos #1063 / OEIS A389360.
n_k = least n >= 2k such that (n-i) | C(n,k) for all but exactly one 0<=i<k.
Uses exact integer binomials only (no number-theoretic shortcuts)."""
import sys
from math import comb

def count_bad(n, k, C):
    bad = 0
    for i in range(k):
        if C % (n - i):
            bad += 1
            if bad > 1:
                return bad
    return bad

def n_k(k, limit=None):
    n = 2 * k
    C = comb(n, k)
    while True:
        if count_bad(n, k, C) == 1:
            return n
        # C(n+1,k) = C(n,k)*(n+1)/(n+1-k)
        C = C * (n + 1) // (n + 1 - k)
        n += 1
        if limit and n > limit:
            return None

if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for k in range(lo, hi + 1):
        print(k, n_k(k), flush=True)
