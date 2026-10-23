#!/usr/bin/env python3
"""Analyse the lists of admissible n (data/lists/valid_k.txt) against the density model."""
import math, statistics as st, sys
from collections import Counter
def primes(n): return [p for p in range(2,n+1) if all(p%q for q in range(2,int(p**.5)+1))]
def vp(x,p):
    v=0
    while x%p==0: x//=p; v+=1
    return v
dens={}
for f in ['data/density2_2_59.txt','data/density2_60_100.txt']:
    for l in open(f): t=l.split(); dens[int(t[0])]=float(t[1])
def model_i0_weights(k):
    """prod_p Pr(E_{p,i0}) using the closed form for p>sqrt k and enumeration mod p^(2L) for p<=sqrt k (Lemma 3)."""
    P=primes(k); w=[1.0]*k
    for p in P:
        L=0
        while p**(L+1)<=k: L+=1
        if p*p>k:
            j=k//p; km=k%p
            for i0 in range(k):
                w[i0]*= km/p + ((1/p if j==1 else 1/p**2) if (i0%p)>=km else 0)
        else:
            m=p**(2*L); cnt=[0]*k; cnt_all=0
            for r in range(m):
                n=r+m*(2*k//m+1)
                d=sum(1 for e in range(1,L+1) if n%(p**e)>=k%(p**e))
                if d==0: cnt_all+=1; continue
                vals=[vp(n-i,p) for i in range(k)]; M=max(vals)
                bad=[i for i in range(k) if vals[i]>M-d]
                if len(bad)==1: cnt[bad[0]]+=1
            for i0 in range(k): w[i0]*=(cnt[i0]+cnt_all)/m
    return w
for k in [40,45,50,61,64,67]:
    rows=[tuple(map(int,l.split())) for l in open(f'data/lists/valid_{k}.txt')]
    ns=[r[1] for r in rows]; i0s=[r[2] for r in rows]
    delta=math.exp(-dens[k]); N=len(ns)
    # 1. m-th admissible vs m/delta
    ratios=[ns[m-1]*delta/m for m in range(1,N+1)]
    # distinct failing elements (clusters): m = n - i0
    elems=sorted(set(n-i for _,n,i in rows))
    gaps=[b-a for a,b in zip(elems,elems[1:])]
    mean_gap=st.mean(gaps); cv=st.pstdev(gaps)/mean_gap
    # cluster sizes
    cl=Counter(n-i for _,n,i in rows); sizes=Counter(cl.values())
    # i0 distribution vs model
    w=model_i0_weights(k); tot=sum(w); pred=[x/tot for x in w]
    obs=Counter(i0s)
    # top predicted indices and their observed share
    top=sorted(range(k),key=lambda i:-pred[i])[:5]
    # cost allocation at large primes: for each admissible n, each prime p in (sqrt k, k], p not | k:
    # (A) n mod p < k mod p  (carry-free window)   (B) otherwise (must be p^2 | n-i0, or p | n-i0 with j=1)
    P=[p for p in primes(k) if p*p>k and k%p]
    A=B=0
    for _,n,i in rows:
        for p in P:
            if n%p < k%p: A+=1
            else: B+=1
    print(f"k={k}: {N} admissible n below {ns[-1]:.2e}; 1/delta={1/delta:.3e}")
    print(f"   m-th admissible * delta / m : first={ratios[0]:.2f}, median={st.median(ratios):.2f}, last={ratios[-1]:.2f}  (model: ~1)")
    print(f"   distinct failing elements: {len(elems)}; count below X vs delta*X at X={ns[-1]:.1e}: {len(elems)/(delta*ns[-1]):.2f}")
    print(f"   gaps between failing elements: CV={cv:.2f} (Poisson: 1.00); cluster sizes {dict(sorted(sizes.items()))}")
    print(f"   top-5 model-predicted i0 {top} carry {sum(pred[i] for i in top):.0%} of predicted mass; observed share of those i0: {sum(obs[i] for i in top)/N:.0%}")
    print(f"   large primes satisfied by carry-free window: {A/(A+B):.1%}  (by divisibility of the failing element: {B/(A+B):.1%})")
