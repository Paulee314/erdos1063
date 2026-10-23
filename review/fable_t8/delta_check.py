"""Part 1 check: compute delta(k) exactly via Theorem 7's product formula, with Pr(E_{p,i0})
obtained by enumerating n mod p^{2L} and testing divisibility (n-i) | C(n,k) through Lemma 1 +
Legendre (no use of Lemma 3 / Lemma 6 / the closed form for p > sqrt k).  Then test the two
inequalities of Part 1 exactly:
   lower:  log(1/delta) >= S(k) - log k - sum log(1+1/r)            (upper bound on delta)
   upper:  log(1/delta) <= S(k) + sum_{p<=sqrt k} (2L+1) log p + 2 log p_big [p_big | k]
and print log(1/delta)-S(k) against sqrt k."""
import math, sys
from fractions import Fraction
import numpy as np

def primes_upto(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, math.isqrt(n) + 1):
        if s[i]: s[i*i::i] = False
    return [int(x) for x in np.nonzero(s)[0]]

def vp_arr(a, p):
    a = a.copy(); v = np.zeros(a.shape, dtype=np.int64)
    m = (a % p == 0)
    assert not (a == 0).any()
    while m.any():
        a[m] //= p; v[m] += 1
        m = (a % p == 0)
    return v

def vp_binom(n, k, p):
    v = np.zeros_like(n); q = p
    while q <= int(n.max()):
        v += n // q - k // q - (n - k) // q
        q *= p
    return v

def Lp(k, p):
    L = 0
    while p ** (L + 1) <= k: L += 1
    return L

def probs_for_prime(k, p):
    L = Lp(k, p); mod = p ** (2 * L)
    t = max(1, -(-(2 * k) // mod))
    if t % p == 0: t += 1
    I = np.arange(k, dtype=np.int64)
    cnt_empty = 0; cnt_i0 = np.zeros(k, dtype=np.int64)
    for start in range(0, mod, 4096):
        n0 = np.arange(start, min(mod, start + 4096), dtype=np.int64)
        n = n0 + t * mod
        vb = vp_binom(n, k, p)
        V = vp_arr(n[:, None] - I[None, :], p)
        bad = V > vb[:, None]
        nb = bad.sum(axis=1)
        cnt_empty += int((nb == 0).sum())
        cnt_i0 += bad[nb == 1].sum(axis=0)
    return [Fraction(cnt_empty + int(cnt_i0[i0]), mod) for i0 in range(k)]

def delta(k):
    P = primes_upto(k)
    probs = [probs_for_prime(k, p) for p in P]
    tot = Fraction(0)
    for i0 in range(k):
        pr = Fraction(1)
        for pp in probs:
            pr *= pp[i0]
            if pr == 0: break
        tot += pr
    return tot

def S_parts(k):
    P = primes_upto(k)
    big = [p for p in P if p * p > k and k % p != 0]
    S = sum(math.log(p / (k % p)) for p in big)
    corr = sum(math.log1p(1 / (k % p)) for p in big)
    small = sum((2 * Lp(k, p) + 1) * math.log(p) for p in P if p * p <= k)
    pbig = [p for p in P if p * p > k and k % p == 0]
    extra = sum(2 * math.log(p) for p in pbig)
    return S, corr, small, extra

if __name__ == "__main__":
    for k, want in [(7, Fraction(269, 2520)), (11, Fraction(9803, 831600)), (12, Fraction(1, 1386))]:
        d = delta(k)
        print(f"delta({k}) = {d}  expected {want}  match={d == want}")
    ks = list(range(2, 61)) + [64, 72, 81, 90, 100, 110, 120, 128, 144, 150, 180, 200, 210, 240, 256]
    worst_lo = worst_hi = -1e9
    print("\n   k   log(1/delta)   S(k)   diff   diff/sqrt(k)   lower_ok  upper_ok  [slack_lo, slack_hi]")
    for k in ks:
        d = delta(k)
        L = math.log(1 / d)
        S, corr, small, extra = S_parts(k)
        lo = S - math.log(k) - corr      # proof: log(1/delta) >= this
        hi = S + small + extra           # proof: log(1/delta) <= this
        ok_lo = L >= lo - 1e-9; ok_hi = L <= hi + 1e-9
        print(f"{k:4d} {L:12.3f} {S:8.3f} {L-S:8.3f} {(L-S)/math.sqrt(k):8.3f}   {ok_lo!s:5s}   {ok_hi!s:5s}   [{L-lo:7.3f}, {hi-L:7.3f}]")
        if not (ok_lo and ok_hi): print("   *** VIOLATION ***")
