# Method 2 (independent of Hurwitz zeta): c_m = (m-1)! + f(1)/4 + int_1^inf K(x) f''(x) dx,
# f = (log x)^{m-1}/x^2, K periodic: K(u) = -u^2 log u/2 + u^2/4 - u/4 on [0,1), mean 1/72.
import mpmath as mp
mp.mp.dps = 25
N = 1500
def run(m):
    f = lambda x: mp.log(x)**(m-1)/x**2
    f1 = lambda x: mp.diff(f, x, 1)
    f2 = lambda x: mp.diff(f, x, 2)
    # analytic f'' to avoid diff cost
    def f2a(x):
        l = mp.log(x); a = m-1
        # f = l^a x^-2 ; f' = (a l^{a-1} - 2 l^a) x^-3
        # f'' = (a(a-1) l^{a-2} - 2a l^{a-1} - 3a l^{a-1} + 6 l^a) x^-4
        t = 6*l**a - 5*a*(l**(a-1) if a>=1 else 0) + a*(a-1)*(l**(a-2) if a>=2 else 0)
        return t/x**4
    def f1a(x):
        l = mp.log(x); a=m-1
        return (a*(l**(a-1) if a>=1 else 0) - 2*l**a)/x**3
    s = mp.mpf(0)
    for j in range(1, N):
        s += mp.quad(lambda u: (-u**2*mp.log(u)/2 + u**2/4 - u/4)*f2a(j+u), [0, 1]) if True else 0
    tail = -f1a(mp.mpf(N))/72   # leading tail term
    f1v = 1 if m == 1 else 0
    return mp.factorial(m-1) + mp.mpf(f1v)/4 + s + tail, tail
for m in (1, 2, 3):
    v, t = run(m)
    print("IBP c_%d =" % m, mp.nstr(v, 18), " (tail term %s)" % mp.nstr(t, 3))
