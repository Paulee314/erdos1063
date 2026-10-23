import numpy as np, math
C=1.2577468869443696300; c2=1.0016551589009853286; c3=1.9954535859778266
N=10**8+50
s=np.ones(N+1,dtype=bool); s[:2]=False
for i in range(2,int(N**.5)+1):
    if s[i]: s[i*i::i]=False
P=np.nonzero(s)[0].astype(np.int64); del s
def S(k):
    q=P[(P*P>k)&(P<=k)]; r=k%q; m=r>0
    return float(np.sum(np.log(q[m]/r[m])))
print(" k        L      S/(k/L)   C+c2/L   C+c2/L+c3/L^2   (S/(k/L)-C-c2/L)*L^2  [mean over 21 k; min..max]")
for k0 in [10**4,10**5,10**6,10**7,10**8]:
    vals=[]
    for k in range(k0-10,k0+11):
        L=math.log(k); vals.append(((S(k)/(k/L)), (S(k)/(k/L)-C-c2/L)*L*L))
    L=math.log(k0); a=np.array(vals)
    print(f"{k0:<9d} {L:6.2f}  {a[:,0].mean():8.4f}  {C+c2/L:8.4f}  {C+c2/L+c3/L**2:8.4f}        {a[:,1].mean():7.3f}  [{a[:,1].min():.2f}..{a[:,1].max():.2f}]")
