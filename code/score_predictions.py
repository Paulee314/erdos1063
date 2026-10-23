#!/usr/bin/env python3
"""Score computed n_k against a pre-registered predictions file.
Usage: score_predictions.py PREDICTIONS.txt values.txt
Predictions lines: k  log(1/delta)  median  [lo90, hi90].  Values lines: k n ...
Under the model n_k ~ Exp(1)/delta, the PIT value u = 1 - exp(-n*delta) is uniform on (0,1)."""
import sys, math
pred = {}
for line in open(sys.argv[1]):
    if line.startswith('#') or not line.strip(): continue
    t = line.replace('[', ' ').replace(']', ' ').replace(',', ' ').split()
    pred[int(t[0])] = (float(t[1]), float(t[2]), float(t[3]), float(t[4]))
vals = {}
for line in open(sys.argv[2]):
    t = line.split()
    if len(t) >= 2 and t[1].isdigit(): vals[int(t[0])] = int(t[1])
rows, inside, us = [], 0, []
for k in sorted(pred):
    if k not in vals: print(f"{k:4d}  (no value yet)"); continue
    L, med, lo, hi = pred[k]; n = vals[k]
    x = n * math.exp(-L)                      # n * delta
    u = 1 - math.exp(-x)                      # PIT under Exp(1)
    ins = lo <= n <= hi; inside += ins; us.append(u)
    print(f"{k:4d}  n={n:<24d} pred median={med:.3e}  90%=[{lo:.2e},{hi:.2e}]  {'inside ' if ins else 'OUTSIDE'}  "
          f"ln(n*delta)={math.log(x):+.2f}  PIT={u:.3f}")
m = len(us)
if m:
    us.sort()
    D = max(max((i + 1) / m - u, u - i / m) for i, u in enumerate(us))
    # Kolmogorov asymptotic p-value (adequate as a rough guide for m >= 10)
    lam = (math.sqrt(m) + 0.12 + 0.11 / math.sqrt(m)) * D
    p = 2 * sum((-1) ** (j - 1) * math.exp(-2 * j * j * lam * lam) for j in range(1, 101))
    mean_log = sum(math.log(-math.log(1 - u)) for u in us) / m
    print(f"\n{m} values scored: {inside}/{m} inside the 90% intervals (expected {0.9*m:.1f});"
          f" mean ln(n*delta) = {mean_log:+.3f} (Exp(1) model: -0.577); KS D={D:.3f}, p~{min(1,max(0,p)):.2f}")
