import mpmath as mp, math
mp.mp.dps = 20
z2 = mp.zeta(2)
print("18 zeta2 =", 18*z2, " 2 zeta2 =", 2*z2, " log4 =", mp.log(4), " 2log2 =", 2*mp.log(2))
# tail: sum_{j>J} log(j+1)/j^2 <= 2 log J / J ?
for J in (1,2,3,4,5,10,100,1000,10**4):
    t = mp.nsum(lambda j: mp.log(j+1)/j**2, [J+1, mp.inf])
    print(J, mp.nstr(t, 8), mp.nstr(2*mp.log(J)/J, 8), t <= 2*mp.log(J)/J)
# exact tail integral vs bound
for J in (10, 1000):
    exact = mp.quad(lambda x: -mp.log(x-mp.floor(x))*mp.log(x)/x**2, [J+1+i for i in range(0, 400)]) 
# thresholds in L
def first(cond, lo=2.0):
    L = lo
    while not cond(L): L += 0.01
    return L
print("log(L^3+1) <= 4logL <= L/2 from L =", first(lambda L: math.log(math.floor(L**3)+1) <= 4*math.log(L) <= L/2))
print("sqrt(k)/L^3 >= 2 from L =", first(lambda L: math.exp(L/2)/L**3 >= 2))
print("L/2-3logL >= L/3 from L =", first(lambda L: L/2-3*math.log(L) >= L/3))
print("(0) from L =", first(lambda L: (2*math.log(L)+math.log(math.log(L))+1.4)/(L*L*math.log(L)) <= 3/L**2, 3.0))
# old c2 as truncated sum? find J with c2 - tail(J) = 1.0010797817
c2 = mp.mpf('1.00165515890098532865')
for J in (10000, 18000, 19000, 20000):
    tail = mp.quad(lambda u: -mp.log(u)*mp.zeta(2, J+1+u, 1)*(-1), [0, 1])  # sum_{j>J} int_0^1 -log u log(j+u)/(j+u)^2
    print("truncate at j<=", J, ": c2 - tail =", mp.nstr(c2 - tail, 12))
