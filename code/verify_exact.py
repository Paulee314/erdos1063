#!/usr/bin/env python3
"""Exact big-integer check that n is valid for Erdos #1063: exactly one 0<=i<k with (n-i) not dividing C(n,k).
Input lines: 'k n ...'. Prints k n status bad_index."""
import sys
from math import comb
for line in sys.stdin:
    t = line.split()
    if len(t) < 2 or not t[1].isdigit(): continue
    k, n = int(t[0]), int(t[1])
    C = comb(n, k)
    bad = [i for i in range(k) if C % (n - i)]
    print(k, n, "VALID" if len(bad) == 1 else f"INVALID({len(bad)} bad)", bad[:3], flush=True)
