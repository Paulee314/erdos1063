"""Numerical sanity checks for Theorem 8 (Part 2): S(k), constant C, class decomposition."""
import math, sys
import numpy as np
import mpmath as mp
from scipy.integrate import quad

def primes_upto(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, math.isqrt(n) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0].astype(np.int64)

# ---- constant C and Lemma B ----
mp.mp.dps = 20
C = mp.nsum(lambda j: mp.log(1 + 1/j)/j, [1, mp.inf])
Cint = mp.quad(lambda x: -mp.log(x - mp.floor(x))/x**2, [1] + list(range(2, 60)) + [mp.inf])
print("C (series)   =", C)
print("C (integral) =", Cint, " (integral truncated ~ to 60, tail <1/60 handled by quad to inf w/ floor)")
for j in [1, 2, 3, 10, 100]:
    num, _ = quad(lambda u: -math.log(u)/(j+u)**2, 0, 1)
    print(f"  c_{j}: quad={num:.10f} closed={math.log1p(1/j)/j:.10f} diff={num-math.log1p(1/j)/j:.1e}")
c2, _ = quad(lambda x: 0.0, 0, 1)
c2 = mp.quad(lambda x: -mp.log(x - mp.floor(x))*mp.log(x)/x**2, [1] + list(range(2, 200)) + [mp.inf])
print("c_2 (next-term constant) ≈", c2)

def cj_eps(j, eps):
    v, _ = quad(lambda x: -math.log(x - j)/x**2, j + eps, j + 1)
    return v

# ---- S(k) and classes ----
def analyze(k, eps, J, P_all):
    P = P_all[(P_all <= k) & (P_all.astype(np.int64)**2 > k)]
    r = k % P; m = r != 0
    P, r = P[m], r[m]; j = k // P
    terms = np.log(P / r)
    S = terms.sum()
    base = k / math.log(k)
    M = np.maximum(math.log(k)**2, 4 * j)
    T = r <= M
    B = r > eps * P
    D = (~T) & (~B)
    BJ = B & (j <= J); BgJ = B & (j > J)
    piKJ = int(((P_all <= k / J)).sum())
    print(f"\n=== k={k}  eps={eps}  J={J}   k/log k = {base:.2f}   #primes in sum = {len(P)}")
    print(f"S(k) = {S:.2f},  S/(k/log k) = {S/base:.4f}   (C = {float(C):.4f})")
    for name, mask in [("T", T), ("D", D), ("B,j>J", BgJ), ("B,j<=J", BJ)]:
        print(f"  class {name:7s}: count={int(mask.sum()):8d}  sum={terms[mask].sum():12.2f}  sum/(k/log k)={terms[mask].sum()/base:.4f}")
    print(f"  overlap T∩B count = {int((T & B).sum())}  (classes are not disjoint as written)")
    print(f"  T bound: count <= (log k)^2+4 sqrt k = {math.log(k)**2 + 4*math.sqrt(k):.1f};  T sum bound ((log k)^2+4sqrt k)log k = {(math.log(k)**2 + 4*math.sqrt(k))*math.log(k):.1f}")
    print(f"  B,j>J: count={int(BgJ.sum())} <= pi(k/J)={piKJ};  proof bound 4 log(1/eps) k/(J log k) = {4*math.log(1/eps)*base/J:.1f}")
    print(f"  D: eps log(1/eps) k/log k = {eps*math.log(1/eps)*base:.1f};  D sum / that = {terms[D].sum()/(eps*math.log(1/eps)*base):.3f}")
    # main term check
    cj = [cj_eps(jj, eps) for jj in range(1, J + 1)]
    main = base * sum(cj)
    # exact integral sum_j int_a^b g(t)/log t dt
    exact = 0.0
    for jj in range(1, J + 1):
        a, b = k / (jj + 1), k / (jj + eps)
        v, _ = quad(lambda t: -math.log(k / t - jj) / math.log(t), a, b, limit=200)
        exact += v
    print(f"  B,j<=J main term (k/log k) sum c_j(eps) = {main:.2f}  [sum c_j(eps)={sum(cj):.4f}, C-1/J-4 eps log(1/eps)={float(C)-1/J-4*eps*math.log(1/eps):.4f}]")
    print(f"  B,j<=J exact integral sum_j ∫ g/log t  = {exact:.2f};   actual = {terms[BJ].sum():.2f};  actual/main = {terms[BJ].sum()/main:.4f}, actual/exact = {terms[BJ].sum()/exact:.4f}")
    # per-j check for small j
    for jj in range(1, min(J, 4) + 1):
        mm = BJ & (j == jj)
        a, b = k / (jj + 1), k / (jj + eps)
        v, _ = quad(lambda t: -math.log(k / t - jj) / math.log(t), a, b, limit=200)
        print(f"     j={jj}: count={int(mm.sum())}, sum={terms[mm].sum():.2f}, ∫g/log t={v:.2f}, (k/log k)c_j(eps)={base*cj[jj-1]:.2f}")
    return S

if __name__ == "__main__":
    kmax = 10**7
    P_all = primes_upto(kmax)
    for k in [10**3, 10**4, 10**5, 10**6, 10**7]:
        P = P_all[(P_all <= k) & (P_all**2 > k)]
        r = k % P; m = r != 0
        S = np.log(P[m] / r[m]).sum()
        print(f"k={k:>9d}: S(k)={S:14.2f}  S/(k/log k)={S*math.log(k)/k:.4f}  minus C = {S*math.log(k)/k-float(C):+.4f}  c2/log k = {float(c2)/math.log(k):.4f}")
    for (k, eps, J) in [(10**5, 0.1, 10), (10**6, 0.1, 10), (10**6, 0.02, 30), (10**7, 0.02, 30)]:
        analyze(k, eps, J, P_all)
