#!/usr/bin/env python3
"""Independent exact-rational computation of delta(k) for Erdos #1063.

Method (deliberately NOT via Lemma 3 / the M_p - d_p formula):
  For each prime p <= k, L = floor(log_p k), m = p^(2L).  For every residue r mod m pick two
  representatives n = r + m*T (T = T1, T2, both with n >= 2k), compute
      Bad_p(n) = { 0<=i<k : v_p(n-i) > v_p(C(n,k)) }
  with v_p(C(n,k)) from Legendre's formula on actual integers, and assert the two agree
  (a direct test of the mod p^(2L) periodicity claim of Theorem 7).  Then
      Pr(E_{p,i0}) = #{ r : Bad_p subset {i0} } / m        (exact Fraction)
      delta(k)     = sum_{i0<k} prod_{p<=k} Pr(E_{p,i0})    (exact Fraction)
Prints k, log(1/delta), argmax i0, and the exact fraction for small k.
Usage: density_exact.py kmin kmax [--check-vs file1,file2]
"""
import sys, math
from fractions import Fraction

def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]

def legendre(N, p):
    s = 0
    while N:
        N //= p; s += N
    return s

def vp(x, p):
    v = 0
    while x % p == 0:
        x //= p; v += 1
    return v

def bad_set_p(n, k, p):
    c = legendre(n, p) - legendre(n - k, p) - legendre(k, p)
    r = n % p
    bad = set()
    for i in range(r, k, p):          # only n-i with i == n (mod p) are divisible by p
        if vp(n - i, p) > c:
            bad.add(i)
    return bad

def density(k, periodicity_check=True):
    ps = primes_upto(k)
    per_prime = {}
    for p in ps:
        L = 0
        while p ** (L + 1) <= k: L += 1
        m = p ** (2 * L)
        T1 = (2 * k) // m + 1
        T2 = T1 + 7919
        cnt_all = 0                      # residues with empty bad set
        cnt = [0] * k                    # residues with bad set == {i0}
        for r in range(m):
            b1 = bad_set_p(r + m * T1, k, p)
            if periodicity_check:
                b2 = bad_set_p(r + m * T2, k, p)
                assert b1 == b2, (k, p, r, b1, b2)
            if not b1:
                cnt_all += 1
            elif len(b1) == 1:
                cnt[next(iter(b1))] += 1
        per_prime[p] = [Fraction(cnt_all + cnt[i], m) for i in range(k)]
    total = Fraction(0)
    best, bestv = -1, Fraction(0)
    for i0 in range(k):
        pr = Fraction(1)
        for p in ps:
            pr *= per_prime[p][i0]
            if pr == 0: break
        total += pr
        if pr > bestv: best, bestv = i0, pr
    return total, best

if __name__ == "__main__":
    k0, k1 = int(sys.argv[1]), int(sys.argv[2])
    ref = {}
    if len(sys.argv) > 3 and sys.argv[3] == "--check-vs":
        for f in sys.argv[4].split(','):
            for line in open(f):
                t = line.split()
                if len(t) >= 3 and t[0].isdigit():
                    ref[int(t[0])] = (float(t[1]), int(t[2]))
    worst = 0.0
    for k in range(k0, k1 + 1):
        d, i0 = density(k)
        ld = math.log(d.denominator) - math.log(d.numerator)
        s = f"{k:3d} log(1/delta)={ld:.6f} argmax={i0:3d}"
        if d.denominator < 10 ** 12:
            s += f"  delta={d}"
        if k in ref:
            diff = ld - ref[k][0]
            worst = max(worst, abs(diff))
            s += f"  | model {ref[k][0]:.6f} argmax {ref[k][1]:3d}  diff={diff:+.2e} {'ARGMAX-MISMATCH' if ref[k][1] != i0 else ''}"
        print(s, flush=True)
    if ref:
        print("max |diff| in log(1/delta) vs model files:", worst)
