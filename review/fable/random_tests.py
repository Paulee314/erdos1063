#!/usr/bin/env python3
"""Randomized tests, fresh code:
 (1) Lemma 1+3: bad set from {i : v_p(n-i) > M_p - d_p for some p<=k} equals the exact set {i : (n-i) !| C(n,k)}.
 (2) Theorem 7: Bad_p(n) is unchanged when n is shifted by a multiple of p^(2L).
 (3) Corollary 5 on ALL valid n (not just the least) for small k: W' | n - i0, and n-i0 is the unique
     element of max p-adic valuation for every p | k.
 (4) Lemma 6 for p > sqrt(k)."""
import random
from math import comb, gcd

def primes_upto(n): return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** .5) + 1))]
def vp(x, p):
    v = 0
    while x % p == 0: x //= p; v += 1
    return v
def Lp(k, p):
    L = 0
    while p ** (L + 1) <= k: L += 1
    return L
def bad_exact(n, k):
    C = comb(n, k); return {i for i in range(k) if C % (n - i)}
def bad_p_lemma(n, k, p):
    L = Lp(k, p)
    d = sum(1 for e in range(1, L + 1) if n % p ** e >= k % p ** e)
    if d == 0: return set()
    vals = [vp(n - i, p) for i in range(k)]
    M = max(vals)
    return {i for i in range(k) if vals[i] > M - d}
def bad_lemma(n, k):
    B = set()
    for p in primes_upto(k): B |= bad_p_lemma(n, k, p)
    return B
def Wprime(k):
    w = 1
    for p in primes_upto(k):
        if k % p == 0:
            f = 0
            while p ** (f + 1) <= k - 1: f += 1
            w *= p ** (vp(k, p) + f)
    return w

random.seed(20261021)
# (1)
mism = 0; N = 0
for _ in range(6000):
    k = random.randint(2, 100); n = random.randint(2 * k, 10 ** random.randint(3, 18))
    N += 1
    if bad_exact(n, k) != bad_lemma(n, k): mism += 1; print("MISMATCH(1)", k, n)
print(f"(1) Lemma 1+3 vs exact: {N} random pairs, {mism} mismatches")
# (2)
mism = 0; N = 0
for _ in range(3000):
    k = random.randint(2, 100); p = random.choice(primes_upto(k)); L = Lp(k, p)
    n = random.randint(2 * k, 10 ** random.randint(3, 15)); t = random.randint(1, 10 ** 6)
    N += 1
    if bad_p_lemma(n, k, p) != bad_p_lemma(n + t * p ** (2 * L), k, p): mism += 1; print("MISMATCH(2)", k, p, n, t)
    # also show p^(2L-1) is not enough in general: count failures
print(f"(2) periodicity of Bad_p mod p^(2L): {N} tests, {mism} failures")
fail = 0; N = 0
for _ in range(3000):
    k = random.randint(2, 100); p = random.choice(primes_upto(k)); L = Lp(k, p)
    n = random.randint(2 * k, 10 ** 9); t = random.randint(1, 10 ** 6)
    N += 1
    if bad_p_lemma(n, k, p) != bad_p_lemma(n + t * p ** (2 * L - 1), k, p): fail += 1
print(f"    (for contrast, shifting by multiples of p^(2L-1) changes Bad_p in {fail} of {N} tests)")
# (3)
tot = 0; bad = 0
for k in range(2, 23):
    W = Wprime(k); ps = [p for p in primes_upto(k) if k % p == 0]
    for n in range(2 * k, 2 * k + 60000):
        B = bad_lemma(n, k)
        if len(B) != 1: continue
        i0 = next(iter(B)); tot += 1
        ok = (n - i0) % W == 0
        for p in ps:
            vals = [vp(n - i, p) for i in range(k)]; M = max(vals)
            ok &= vals[i0] == M and vals.count(M) == 1
        if not ok: bad += 1; print("COR5 FAIL", k, n, i0)
print(f"(3) Corollary 5 on all valid n in [2k, 2k+60000) for 2<=k<=22: {tot} valid n, {bad} failures")
# (4)
mism = 0; N = 0
for _ in range(4000):
    k = random.randint(2, 100); big = [p for p in primes_upto(k) if p * p > k]
    if not big: continue
    p = random.choice(big); n = random.randint(2 * k, 10 ** 12); j = k // p; N += 1
    B = bad_p_lemma(n, k, p)
    if n % p < k % p: pred = set()
    elif j == 1: pred = {n % p}
    else:
        mult = [i for i in range(n % p, k, p)]
        sq = [i for i in mult if (n - i) % (p * p) == 0]
        pred = set(sq) if sq else set(mult)
    if B != pred: mism += 1; print("LEMMA6 MISMATCH", k, p, n)
print(f"(4) Lemma 6: {N} tests, {mism} mismatches")
