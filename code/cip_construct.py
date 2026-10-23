# Implement Cipollini's construction (Sections 2-3) for explicit (k,e) and verify admissibility exactly.
import math, sys
def primes(N):
    s=bytearray([1])*(N+1); s[0:2]=b'\0\0'
    for i in range(2,int(N**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(N+1) if s[i]]
def vpf(m,p):
    s=0;q=p
    while q<=m: s+=m//q; q*=p
    return s
def vp(x,p):
    c=0
    while x%p==0: x//=p;c+=1
    return c
def bad_set(n,k,PS):
    out=set()
    for p in PS:
        T=vpf(n,p)-vpf(k,p)-vpf(n-k,p)
        for i in range(k):
            if vp(n-i,p)>T: out.add(i)
    return out
def construct(k,e,tmax=10**7):
    K=k-1; PS=primes(k); r=max(e,K-e)
    A={p:int(math.floor(math.log(r)/math.log(p)+1e-12)) for p in PS}
    for p in PS:
        while p**(A[p]+1)<=r: A[p]+=1
        while p**A[p]>r: A[p]-=1
    d={p: vpf(k,p)-vpf(e,p)-vpf(K-e,p) for p in PS}   # v_p(Q_e), Q_e = k!/(e!(K-e)!)
    M=1
    for p in PS:
        if d[p]>0: M*=p**(A[p]+d[p])
        elif p<=2*e: M*=p**(A[p]+1)
    P=[p for p in PS if p>2*e and d[p]==0]
    a={p:k%p for p in P}
    assert all(a[p]>e for p in P), "Lucas step failed"
    h={p:min(e,a[p]-e) for p in P}
    Q=math.prod(-(-p//h[p]) for p in P)
    t=1
    while t<=min(Q,tmax):
        if all(min((M*t)%p, p-(M*t)%p)<h[p] for p in P): break
        t+=1
    else: return None
    return M,t,Q,e+M*t
fails=0;tested=0;skipped=0
for k in range(6,61):
    K=k-1
    for e in range(1,K):
        if not (2*e>math.isqrt(k) and 2*e*2*e>k and e<K/2): continue
        res=construct(k,e)
        if res is None: skipped+=1; continue
        M,t,Q,n=res
        PS=primes(k)
        B=bad_set(n,k,PS); tested+=1
        ok = (B=={e}) and n>=2*k and t<=Q
        if not ok: fails+=1; print("FAIL",k,e,n,B)
print(f"tested {tested} (k,e) pairs for 6<=k<=60, failures {fails}, skipped (t>1e7) {skipped}")
