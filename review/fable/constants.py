#!/usr/bin/env python3
"""Check C = sum_{j>=1} (1/j) log(1+1/j) = int_1^inf -log{x}/x^2 dx, and c_2 = int_1^inf -log{x} log x / x^2 dx;
then S(k) = sum_{sqrt k < p <= k, p !| k} -log{k/p} for k up to 10^4 and the ratio S(k)/(k/log k)."""
import math, re
from mpmath import mp, mpf, nsum, quad, log, inf, floor
mp.dps = 30
C = nsum(lambda j: log(1 + 1/j)/j, [1, inf])
print("C (series)          =", C)
Cint = nsum(lambda j: quad(lambda x: -log(x - j)/x**2, [j, j + 1]), [1, inf])
print("C (integral)        =", Cint)
c2 = nsum(lambda j: quad(lambda x: -log(x - j)*log(x)/x**2, [j, j + 1]), [1, inf])
print("c2 = int -log{x} log x / x^2 =", c2)

def sieve(n):
    s = bytearray([1])*(n+1); s[0]=s[1]=0
    for i in range(2, int(n**.5)+1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]
P = sieve(20000)
def S(k):
    return sum(-math.log((k % p)/p) for p in P if p*p > k and p <= k and k % p)
ld = {}
for f in ["density_exact_2_30.out", "density_exact_31_100.out"]:
    for line in open(f):
        m = re.match(r"\s*(\d+) log\(1/delta\)=([-\d.]+)", line)
        if m: ld[int(m.group(1))] = float(m.group(2))
print("\n k   S(k)    log(1/delta)  diff   S/(k/logk)  log(1/d)/(k/logk)")
for k in [10,20,30,31,40,50,60,61,64,70,80,90,97,100]:
    print(f"{k:4d} {S(k):7.3f} {ld[k]:8.3f} {ld[k]-S(k):+7.3f}  {S(k)/(k/math.log(k)):6.3f}  {ld[k]/(k/math.log(k)):6.3f}")
import statistics as st
print("mean over 80..100 of log(1/delta)/(k/log k):", round(st.mean(ld[k]/(k/math.log(k)) for k in range(80,101)),3))
print("mean over 80..100 of S(k)/(k/log k):", round(st.mean(S(k)/(k/math.log(k)) for k in range(80,101)),3))
print("mean over 80..100 of log(1/delta)-S(k):", round(st.mean(ld[k]-S(k) for k in range(80,101)),3), " sqrt(100)=10")
for K in [100, 400, 2000, 10000, 20000]:
    ks = range(K-10, K+11)
    r = st.mean(S(k)/(k/math.log(k)) for k in ks)
    print(f"k~{K}: mean S(k)/(k/log k) over 21 k = {r:.3f};  C + c2/log k = {float(C)+float(c2)/math.log(K):.3f};  C={float(C):.4f}")
