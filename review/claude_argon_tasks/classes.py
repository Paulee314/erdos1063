import numpy as np, math
from scipy.special import roots_genlaguerre
from scipy.integrate import quad
NMAX = int(1e8) + 100
s = np.ones(NMAX+1, dtype=bool); s[:2] = False
for i in range(2, int(NMAX**0.5)+1):
    if s[i]: s[i*i::i] = False
P = np.nonzero(s)[0].astype(np.int64); del s
xs, ws = roots_genlaguerre(60, 1.0)
def Iint(k, X):   # k * int_1^X phi(x)/(L-log x) dx, X integer
    L = math.log(k)
    jj = np.arange(1, X, dtype=np.float64)[:, None]
    x = jj + np.exp(-xs)[None, :]
    return k*float(np.sum((1.0/(x*x*(L-np.log(x)))) @ ws))
def strips(k, J, rho):
    L = math.log(k); tot = 0.0
    # int_0^rho -log u w(j+u) du ; substitute u = rho*v: rho*int_0^1 (-log rho - log v) w(j+rho v) dv
    # gauss-legendre for the smooth part, gen-laguerre for -log v part
    gl_x, gl_w = np.polynomial.legendre.leggauss(30); gl_x = (gl_x+1)/2; gl_w = gl_w/2
    j = np.arange(1, J+1, dtype=np.float64)[:, None]
    w1 = lambda x: 1.0/(x*x*(L-np.log(x)))
    part1 = (-math.log(rho)) * (w1(j + rho*gl_x[None,:]) @ gl_w)
    part2 = w1(j + rho*np.exp(-xs)[None,:]) @ ws
    return k*rho*float(np.sum(part1 + part2))
for k in (10**7, 10**8):
    L = math.log(k); J = math.floor(L**3); rho = 1/(L*L*math.log(L)); R0 = math.sqrt(k)
    u = k/L**3
    lo = np.searchsorted(P, math.isqrt(k), side='right'); hi = np.searchsorted(P, k, side='right')
    p = P[lo:hi]; p = p[p*p > k]; r = k % p; p = p[r > 0]; r = r[r > 0]
    g = np.log(p.astype(float)) - np.log(r.astype(float))
    Z = p*(J+1) <= k
    f = r/p
    A = (~Z) & (f >= rho); N = (~Z) & (f < rho) & (r < R0); Dy = (~Z) & (f < rho) & (r >= R0)
    assert (Z.astype(int)+A+N+Dy == 1).all()
    I = Iint(k, J+1); V = strips(k, J, rho)
    SA = g[A].sum()
    print(f"k={k}: L={L:.3f} J={J} rho={rho:.3e} sqrt(k)/L^3={R0/L**3:.2f}  unit k/L^3={u:.1f}")
    print(f"  Z  = {g[Z].sum()/u:8.4f}  (bound 1.39)   count {Z.sum()}")
    print(f"  N  = {g[N].sum()/u:8.4f}  (bound L*sqrt(k)/unit = {L*R0/u:.2f})  count {N.sum()}")
    print(f"  Dy = {g[Dy].sum()/u:8.4f}  (bound 90)  count {Dy.sum()}")
    print(f"  strips sum_j int_Vj = {V/u:8.4f} (bound 10)")
    print(f"  A - (I - strips) = {(SA-(I-V))/u:8.4f}  (PNT/partial-summation error, bound 1)")
    print(f"  I - Ck/L - c2k/L^2 = {(I - 1.25774688694437*k/L - 1.00165515890099*k/L**2)/u:8.4f} (bound +-5; 2c3=3.99)")
    print(f"  total R = {(g.sum() - 1.25774688694437*k/L - 1.00165515890099*k/L**2)/u:8.4f}")
