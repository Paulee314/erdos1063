# Independent checks (Argon prompt 4). Uses only Legendre's formula and the definition.
from fractions import Fraction
def primerange(a,b):
    return [q for q in range(max(a,2),b) if all(q%d for d in range(2,int(q**0.5)+1))]

def vp(x,p):
    c=0
    while x%p==0: x//=p; c+=1
    return c
def vp_fact(m,p):
    s=0; q=p
    while q<=m: s+=m//q; q*=p
    return s
def vp_binom(n,k,p):  # Legendre, directly
    return vp_fact(n,p)-vp_fact(k,p)-vp_fact(n-k,p)
def bad_p(n,k,p):
    T=vp_binom(n,k,p)
    return {i for i in range(k) if vp(n-i,p)>T}
def L(k,p):
    l=0
    while p**(l+1)<=k: l+=1
    return l

# (1) Lemma 6, j=1 cases, all i0 including i0>=p
print("== Lemma 6 check (j=1) ==")
for (k,p) in [(10,7),(12,7),(20,11)]:
    m=p*p; base=m*10**6  # n = base + r, r over a full period mod p^2
    r_ = k%p; j=k//p; assert j==1
    allok=True; rows=[]
    for i0 in range(k):
        cnt=sum(1 for r in range(m) if bad_p(base+r,k,p)<= {i0})
        pred=Fraction(r_,p)+(Fraction(1,p) if i0%p>=r_ else 0)
        ok = Fraction(cnt,m)==pred
        allok&=ok
        if i0>=p or i0 in (0,r_-1,r_): rows.append((i0,cnt,m,str(pred),ok))
    print(f"(k,p)=({k},{p}) k mod p={r_}: all {k} values of i0 match formula: {allok}")
    for row in rows: print("   i0=%d count=%d/%d formula=%s match=%s"%row)

# (2) exact delta(13..15) by brute enumeration of n mod p^{2L} per prime
print("== exact delta ==")
res={}
for k in (13,14,15):
    ps=list(primerange(2,k+1))
    probs={}
    for p in ps:
        m=p**(2*L(k,p)); base=m*10**4
        cnt=[0]*k
        for r in range(m):
            B=bad_p(base+r,k,p)
            for i0 in range(k):
                if B<= {i0}: cnt[i0]+=1
        probs[p]=[Fraction(c,m) for c in cnt]
    d=sum( (lambda i0: __import__('math').prod(probs[p][i0] for p in ps))(i0) for i0 in range(k))
    res[k]=d
    print(f"delta({k}) = {d}  ~ {float(d):.6e}")
import json; json.dump({k:[d.numerator,d.denominator] for k,d in res.items()},open("delta13_15.json","w"))
