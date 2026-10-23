#!/usr/bin/env python3
"""Compare computed n_k with the density model. Usage: compare.py values.txt density.txt [predictions.txt]"""
import sys, math, statistics as st
vals = {}
for f in [sys.argv[1]]:
    for line in open(f):
        t = line.split()
        if len(t) >= 2 and t[1].isdigit(): vals[int(t[0])] = int(t[1])
dens = {}
for f in sys.argv[2].split(','):
    for line in open(f):
        t = line.split()
        if len(t) >= 2: dens[int(t[0])] = float(t[1])
def isp(x): return x > 1 and all(x % q for q in range(2, int(x**.5) + 1))
xs_old, xs_new, inside, total = [], [], 0, 0
rows = []
for k in sorted(vals):
    if k not in dens: continue
    x = math.log(vals[k]) - dens[k]
    (xs_old if k < 60 else xs_new).append(x)
    if k >= 60:
        lo, hi = math.log(0.0513), math.log(2.996)
        total += 1; inside += (lo <= x <= hi)
    rows.append((k, vals[k], dens[k], x))
for k, n, d, x in rows:
    if k >= 60: print(f"{k:3d} {n:>20d}  log n={math.log(n):6.2f}  model={d:6.2f}  diff={x:+5.2f} {'P' if isp(k) else ''}")
print(f"k<60 : n={len(xs_old)} mean diff {st.mean(xs_old):+.3f} sd {st.pstdev(xs_old):.3f}")
if xs_new:
    print(f"k>=60: n={len(xs_new)} mean diff {st.mean(xs_new):+.3f} sd {st.pstdev(xs_new):.3f}; inside pre-registered 90% interval: {inside}/{total}")
allx = xs_old + xs_new
print(f"all  : n={len(allx)} mean {st.mean(allx):+.3f} sd {st.pstdev(allx):.3f}   (Exp(1) model: mean -0.577, sd 1.283)")
