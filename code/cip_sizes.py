import math, numpy as np
def primes(N):
    s=np.ones(N+1,dtype=bool); s[:2]=False
    for i in range(2,int(N**.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]
def vpf_arr(m,ps):
    out=np.zeros(len(ps),dtype=np.int64); q=ps.astype(np.int64).copy()
    while True:
        mask=q<=m
        if not mask.any(): break
        out[mask]+=m//q[mask]
        q=np.where(mask, q*ps, q)
        q=np.minimum(q, m+1)  # avoid overflow; once >m stays >m
    return out
C=1.25774688694436963
def sizes(k,e,PS):
    K=k-1; r=K-e
    lp=np.log(PS)
    A=np.floor(np.log(r)/lp+1e-12).astype(np.int64)
    d=vpf_arr(k,PS)-vpf_arr(e,PS)-vpf_arr(K-e,PS)
    vM=np.where(d>0,A+d,np.where(PS<=2*e,A+1,0))
    logM=float(np.sum(vM*lp)); logQe=float(np.sum(d*lp))
    inP=(PS>2*e)&(d==0); P=PS[inP]; a=k%P
    assert np.all(a>e)
    h=np.minimum(e,a-e); q=-(-P//h)
    logQ1=float(np.sum(np.log(q[a>2*e]))); logQ2=float(np.sum(np.log(q[a<=2*e])))
    return logM,logQe,logQ1,logQ2
print("k        L        e     logM/(k/L)  [2e logD]/(k/L)  logQ_P1/(k/L) [logD-1]  logQ_P2/(k/L)  total/(k/L)  paper:S   ")
for k in [10**4,10**5,10**6,10**7]:
    PS=primes(k)
    L=math.log(k); l=math.log(L); S=l+math.log(l)+math.log(2); D=2*L*S; e=int(k//D)
    logM,logQe,q1,q2=sizes(k,e,PS)
    u=k/L
    print(f"{k:<8d} {L:6.3f} {e:7d}   {logM/u:8.3f}   {2*e*math.log(D)/u:8.3f}        {q1/u:8.3f} [{math.log(D)-1:6.3f}]   {q2/u:8.4f}      {(logM+q1+q2)/u:8.3f}   {S:6.3f}")
# best e for this method at finite k
print("\nbest e (scan) for Cipollini's method vs density exponent C:")
for k in [10**4,10**5,10**6,10**7]:
    PS=primes(k); L=math.log(k); u=k/L
    best=None
    for f in np.geomspace(2*math.sqrt(k)/2+1, k/6, 40):
        e=int(f)
        if 2*e<=math.isqrt(k): continue
        logM,_,q1,q2=sizes(k,e,PS); tot=(logM+q1+q2)/u
        if best is None or tot<best[0]: best=(tot,e)
    print(f"k={k:<9d} min over e of log(n)/(k/log k) = {best[0]:.3f} at e={best[1]}   (density model C={C:.3f})")
