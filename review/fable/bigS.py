import math, statistics as st
import numpy as np
from mpmath import mp, quad, nsum, log, inf
mp.dps = 20
C = float(nsum(lambda j: log(1 + 1/j)/j, [1, inf]))
c2 = float(nsum(lambda j: quad(lambda x: -log(x - j)*log(x)/x**2, [j, j + 1]), [1, inf]))
c3 = float(nsum(lambda j: quad(lambda x: -log(x - j)*log(x)**2/x**2, [j, j + 1]), [1, inf]))
print(f"C={C:.6f} c2={c2:.6f} c3={c3:.6f}")
N = 2_000_000
s = np.ones(N+1, dtype=bool); s[:2] = False
for i in range(2, int(N**.5)+1):
    if s[i]: s[i*i::i] = False
P = np.nonzero(s)[0]
def S(k):
    ps = P[(P*P > k) & (P <= k)]
    r = k % ps
    ps = ps[r != 0]; r = r[r != 0]
    return float(np.sum(np.log(ps / r)))
for K in [1000, 10000, 100000, 1000000]:
    ks = range(K-10, K+11)
    ratio = st.mean(S(k)/(k/math.log(k)) for k in ks)
    lk = math.log(K)
    print(f"k~{K:8d}: mean S/(k/log k) = {ratio:.4f};  C + c2/L = {C + c2/lk:.4f};  C + c2/L + c3/L^2 = {C + c2/lk + c3/lk**2:.4f}")
