#!/usr/bin/env python3
"""Fresh exact check of the claimed n_k (2<=k<=100): exactly one 0<=i<k with (n-i) not dividing C(n,k).
Also checks n >= 2k, reports the bad index, and checks the sharpened Corollary 5 divisibility
W'_k | n - i0 with W'_k = prod_{p^a || k} p^(a + floor(log_p(k-1))).
Uses only math.comb and big-integer modulo: no number-theoretic shortcuts."""
import sys
from math import comb

def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]

def vp(x, p):
    v = 0
    while x % p == 0:
        x //= p; v += 1
    return v

def Wprime(k):
    w = 1
    for p in primes_upto(k):
        if k % p: continue
        a = vp(k, p)
        f = 0
        while p ** (f + 1) <= k - 1: f += 1
        w *= p ** (a + f)
    return w

def Wforum(k):  # the GPT-5.5 forum bound: prod p^(a + floor(log_p(k/2)))
    w = 1
    for p in primes_upto(k):
        if k % p: continue
        a = vp(k, p)
        f = 0
        while p ** (f + 1) <= k / 2: f += 1
        w *= p ** (a + f)
    return w

vals = {}
for line in open(sys.argv[1]):
    t = line.split()
    if len(t) >= 2 and t[0].isdigit() and t[1].isdigit():
        vals[int(t[0])] = int(t[1])

allok = True
for k in sorted(vals):
    n = vals[k]
    C = comb(n, k)
    bad = [i for i in range(k) if C % (n - i)]
    ok = (len(bad) == 1) and n >= 2 * k
    i0 = bad[0] if len(bad) == 1 else None
    w = Wprime(k)
    divis = (i0 is not None) and ((n - i0) % w == 0)
    attained = (i0 is not None) and (n - i0 == w)
    print(f"k={k:3d} n={n:<20d} nbad={len(bad)} bad={bad[:4]} n>=2k={n>=2*k} W'={w:<10d} W'|n-i0={divis} W'==n-i0={attained} Wforum={Wforum(k)}")
    allok &= ok and divis
print("ALL VALID AND W' DIVIDES n-i0:", allok)
