#!/usr/bin/env python3
"""Recompute the out-of-sample statistics with my own exact log(1/delta) values.
x_k = log n_k - log(1/delta_k).  Under the model n_k*delta_k ~ Exp(1), x ~ log Exp(1) (Gumbel-min),
CDF F(x) = 1 - exp(-e^x), mean -gamma = -0.5772, SD pi/sqrt(6) = 1.2825."""
import math, re, sys
import numpy as np
from scipy import stats

vals = {}
for line in open("../erdos/data/A389360_extended_2_100.txt"):
    t = line.split()
    if len(t) >= 2: vals[int(t[0])] = int(t[1])
ld = {}
for f in ["density_exact_2_30.out", "density_exact_31_100.out"]:
    for line in open(f):
        m = re.match(r"\s*(\d+) log\(1/delta\)=([-\d.]+)", line)
        if m: ld[int(m.group(1))] = float(m.group(2))

x = {k: math.log(vals[k]) - ld[k] for k in vals}
F = lambda t: 1 - np.exp(-np.exp(t))
lo, hi = math.log(0.0513), math.log(2.996)
print(f"90% interval in x: [{lo:.4f}, {hi:.4f}]; exact central 90% of Exp(1): [{-math.log(1-0.05):.5f}, {-math.log(0.05):.5f}] -> x in [{math.log(-math.log(0.95)):.4f}, {math.log(-math.log(0.05)):.4f}]")

def report(name, ks):
    xs = np.array([x[k] for k in ks])
    n = len(xs)
    D, p = stats.kstest(xs, F)
    crit = 1.36 / math.sqrt(n)
    print(f"{name:22s} n={n:3d} mean={xs.mean():+.3f} s.e.={xs.std(ddof=1)/math.sqrt(n):.3f} SD(pop)={xs.std():.3f} SD(samp)={xs.std(ddof=1):.3f} KS D={D:.3f} (p={p:.3f}, asymptotic 5% crit={crit:.3f})")
    return xs

report("2<=k<=59 (b-file)", range(2, 60))
report("2<=k<=30", range(2, 31))
report("31<=k<=59", range(31, 60))
xs = report("60<=k<=100 (new)", range(60, 101))
report("31<=k<=100", range(31, 101))
report("2<=k<=100", range(2, 101))
inside = [(k, x[k]) for k in range(60, 101) if lo <= x[k] <= hi]
outside = [(k, round(x[k], 3)) for k in range(60, 101) if not (lo <= x[k] <= hi)]
print(f"inside 90% interval: {len(inside)}/41  (expected 36.9); outside: {outside}")
# binomial check
print("P(>=38 of 41 inside | p=0.9) =", 1 - stats.binom.cdf(37, 41, 0.9))
# prime vs composite split for k>=31
pr = [k for k in range(31, 101) if all(k % q for q in range(2, int(k**.5)+1))]
co = [k for k in range(31, 101) if k not in pr]
report("31..100 prime k", pr); report("31..100 composite k", co)
# shifted variant for small k
xs2 = np.array([math.log(vals[k] - 2*k + 1) - ld[k] for k in range(2, 31)])
D2, p2 = stats.kstest(xs2, F); print(f"2<=k<=30 using n_k-2k+1: KS D={D2:.3f} p={p2:.3f}")
# Anderson-Darling style check via transformed uniforms for 31..100
u = np.array([1 - math.exp(-math.exp(x[k])) for k in range(31, 101)])
print("31..100: mean of U=F(x):", u.mean().round(3), " (0.5 expected); Cramer-von Mises:", stats.cramervonmises(u, 'uniform'))
# list the x_k for the new range
print("\nk   n_k                 log n_k   log(1/delta)   x_k")
for k in range(60, 101):
    print(f"{k:3d} {vals[k]:<20d} {math.log(vals[k]):8.3f} {ld[k]:10.3f} {x[k]:+7.3f}")
