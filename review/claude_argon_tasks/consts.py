# Method 1: Hurwitz zeta closed form  c_m = int_0^1 (-log u) * (-1)^{m-1} d^{m-1}/ds^{m-1} zeta(s,1+u) |_{s=2} du
import mpmath as mp
mp.mp.dps = 30
def cm_hurwitz(m):
    f = lambda u: -mp.log(u) * (-1)**(m-1) * mp.zeta(2, 1+u, m-1)
    return mp.quad(f, [0, 0.25, 0.5, 1])
for m in range(1, 7):
    print("hurwitz c_%d =" % m, mp.nstr(cm_hurwitz(m), 25))
# C other forms
print("C sum (1/j)log(1+1/j) =", mp.nstr(mp.nsum(lambda j: mp.log(1+1/j)/j, [1, mp.inf]), 25))
print("C alt zeta sum        =", mp.nstr(mp.nsum(lambda m: (-1)**(m+1)*mp.zeta(m+1)/m, [1, mp.inf]), 25))
