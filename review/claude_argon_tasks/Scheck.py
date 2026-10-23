import numpy as np, math, sys
from scipy.special import roots_genlaguerre
NMAX = int(1e8) + 100
s = np.ones(NMAX+1, dtype=bool); s[:2] = False
for i in range(2, int(NMAX**0.5)+1):
    if s[i]: s[i*i::i] = False
P = np.nonzero(s)[0].astype(np.int64)
del s
print("pi(1e8+100) =", len(P), flush=True)
C  = 1.2577468869443696300
c  = [None, C, 1.0016551589009853286, 1.9954535859778266003, 5.9984653513544852403, 23.999963566264235609, 120.00031781193806058]
c2old = 1.0010797817

def S(k):
    lo = np.searchsorted(P, math.isqrt(k), side='right')   # p > sqrt(k)  (p = isqrt(k) only if k square of prime; p^2=k means p=sqrt k, excluded)
    hi = np.searchsorted(P, k, side='right')
    p = P[lo:hi]
    p = p[p*p > k]
    r = k % p
    m = r > 0
    return float(np.sum(np.log(p[m].astype(np.float64)) - np.log(r[m].astype(np.float64))))

# main integral M(k) = k * int_1^{sqrt k} phi(x)/(L - log x) dx, with phi = -log{x}/x^2
# per unit interval: int_0^1 -log u * w(j+u) du = int_0^inf s e^{-s} w(j+e^{-s}) ds  (gen. Laguerre alpha=1)
xs, ws = roots_genlaguerre(60, 1.0)
def Mint(k):
    L = math.log(k); X = math.sqrt(k)
    J = int(math.floor(X))
    jj = np.arange(1, J, dtype=np.float64)[:, None]
    x = jj + np.exp(-xs)[None, :]
    w = 1.0/(x*x*(L - np.log(x)))
    tot = float(np.sum(w @ ws))
    # last partial interval [J, X]: int_0^{X-J} -log u w(J+u) du, do with fine composite rule
    a = X - J
    if a > 0:
        from scipy.integrate import quad
        tot += quad(lambda u: -math.log(u)/((J+u)**2*(L-math.log(J+u))), 0, a, limit=200)[0]
    return k*tot

for k0 in (10**4, 10**5, 10**6, 10**7, 10**8):
    L = math.log(k0)
    rows = []
    for k in range(k0-10, k0+11):
        Lk = math.log(k)
        sk = S(k)
        rows.append((k, sk, sk/(k/Lk), (sk/(k/Lk) - C - c[2]/Lk)*Lk*Lk, (sk - Mint(k))/(k/Lk**3) if k in (k0-10, k0, k0+10) else None))
    a = np.array([r[2] for r in rows]); b = np.array([r[3] for r in rows])
    ser = c[3] + c[4]/L + c[5]/L**2 + c[6]/L**3
    print(f"k0={k0:>10}  avg S/(k/L)={a.mean():.4f}  C+c2/L+c3/L^2={C+c[2]/L+c[3]/L**2:.4f}  col4 avg={b.mean():.3f} (min {b.min():.3f} max {b.max():.3f})  c3+..+c6/L^3={ser:.3f}  col4 with old c2: {np.mean((a-C-c2old/L)*L*L):.3f}")
    for r in rows:
        if r[4] is not None:
            print(f"    k={r[0]}  S={r[1]:.3f}  S/(k/L)={r[2]:.6f}  (S - mainIntegral)/(k/L^3) = {r[4]:.4f}   (S - Ck/L - c2k/L^2)/(k/L^3) = {r[3]:.4f}", flush=True)
