#!/usr/bin/env python3
"""Randomized test of Lemma 3 / Lemma 6 / Corollary 5 against exact big-integer divisibility."""
import random, sys
from math import comb
def primes(n): return [p for p in range(2,n+1) if all(p%q for q in range(2,int(p**.5)+1))]
def vp(x,p):
    v=0
    while x%p==0: x//=p; v+=1
    return v
def bad_exact(n,k):
    C=comb(n,k); return {i for i in range(k) if C%(n-i)}
def bad_lemma(n,k):
    B=set()
    for p in primes(k):
        L=0
        while p**(L+1)<=k: L+=1
        d=sum(1 for e in range(1,L+1) if n%(p**e) >= k%(p**e))
        if d==0: continue
        vals=[vp(n-i,p) for i in range(k)]
        M=max(vals)
        B |= {i for i in range(k) if vals[i] > M-d}
    return B
random.seed(1)
bad=0; tests=0
for _ in range(20000):
    k=random.randint(2,40); n=random.randint(2*k, 10**random.randint(2,9))
    tests+=1
    if bad_exact(n,k)!=bad_lemma(n,k): bad+=1; print("MISMATCH",k,n); 
print(f"Lemma 3 vs exact divisibility: {tests} random (k,n), {bad} mismatches")
# Corollary 5 on all computed values.
# W_weak  = prod_{p|k} p^(L_p + v_p(k) - 1)               (the condition the wheel search uses; necessary, weaker)
# W_sharp = prod_{p^a||k} p^(a + floor(log_p(k-1)))       (Corollary 5 as stated in notes/lemmas.md)
def W_weak(k):
    w=1
    for p in primes(k):
        if k%p: continue
        L=0
        while p**(L+1)<=k: L+=1
        w*=p**(L+vp(k,p)-1)
    return w
def W_sharp(k):
    w=1
    for p in primes(k):
        if k%p: continue
        L=0
        while p**(L+1)<=k-1: L+=1      # floor(log_p(k-1))
        w*=p**(vp(k,p)+L)
    return w
okw=oks=tot=0; eq=[]
for f in sys.argv[1:]:
    for line in open(f):
        t=line.split()
        if len(t)<3 or not t[1].isdigit(): continue
        k,n,i0=int(t[0]),int(t[1]),int(t[2].split('=')[1])
        tot+=1; okw+=((n-i0)%W_weak(k)==0); oks+=((n-i0)%W_sharp(k)==0)
        if n-i0==W_sharp(k): eq.append(k)
print(f"Corollary 5 (sharp W'_k): divides n_k - i0 for {oks} of {tot} values; equality n_k - i0 = W'_k at k = {eq}")
print(f"(weak W_k used by the wheel search: divides n_k - i0 for {okw} of {tot})")
