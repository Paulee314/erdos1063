import numpy as np, math
N = 10**7
j = np.arange(1, N+1, dtype=np.float64)
t = np.log(j+1)/j**2
cs = np.cumsum(t[::-1])[::-1]          # cs[i] = sum_{j>=i+1} up to N
tailN = (math.log(N)+1)/N               # approx remainder beyond N
bad = []
for J in [1,2,3,4,5,6,8,10,30,100,1000,10**4,10**5,10**6]:
    T = cs[J] + tailN                    # sum_{j>J}
    print(J, round(T,8), round(2*math.log(J)/J,8), T <= 2*math.log(J)/J)
