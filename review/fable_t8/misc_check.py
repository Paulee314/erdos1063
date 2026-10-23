import math
from scipy.integrate import quad
# c_2 = int_1^inf -log{x} log x / x^2 dx = sum_j int_0^1 -log u log(j+u)/(j+u)^2 du
tot = 0.0
for j in range(1, 200000):
    v, _ = quad(lambda u: -math.log(u)*math.log(j+u)/(j+u)**2, 0, 1)
    tot += v
# tail: ~ sum_{j>N} log j / j^2 ~ (log N + 1)/N
N = 199999
print("c_2 ≈", tot, "+ tail ≈", (math.log(N)+1)/N)

# Non-monotonicity of f(u) = 2u/log u * (log(V/u) + log(1/eps)) on (2, V]: the 'replace V' by V' step
eps = 0.1
for V in [1e2, 1e4, 1e6]:
    f = lambda u: 2*u/math.log(u)*(math.log(V/u) + math.log(1/eps))
    # compare sum over u=V'/2^m (V'=V/2^theta) with sum over u=V/2^m, for theta in (0,1]
    def tot(Vp):
        s = 0.0; m = 0
        while Vp/2**m > 2:
            s += f(Vp/2**m); m += 1
        return s
    worst = max((tot(V/2**th) - tot(V), th) for th in [i/1000 for i in range(1, 1001)])
    print(f"V={V:g}: f(2.1)={f(2.1):.2f} f(4.2)={f(4.2):.2f} (f decreasing near u=2);  max over theta of [sum with V' - sum with V] = {worst[0]:.3f} at theta={worst[1]:.3f};  sum with V = {tot(V):.1f}")
# constant in the lower bound: eps(1+log(1/eps)) * sum 1/j^2 vs 2 eps log(1/eps)
for eps in [0.3, 0.1, 0.01, 1e-4]:
    lhs = eps*(1+math.log(1/eps))*math.pi**2/6
    print(f"eps={eps}: eps(1+log(1/eps))*pi^2/6 = {lhs:.5f};  2 eps log(1/eps) = {2*eps*math.log(1/eps):.5f};  4 eps log(1/eps) = {4*eps*math.log(1/eps):.5f}")
