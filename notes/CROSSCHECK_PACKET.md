# Erdős Problem #1063 — cross-check packet

Prepared 2026-10-22 (revision 5; composite-count correction 86→80) for independent verification. Everything needed is in this one file: definitions, every claim with its proof, the data, and a list of what to check. Nothing has been posted anywhere yet.

**Problem (erdosproblems.com/1063; OEIS A389360; Guy B31).** For $k\ge2$ let $n_k\ge2k$ be the least $n$ such that $n-i\mid\binom nk$ for all but exactly one $0\le i<k$. Estimate $n_k$.

**Known before this work.** Erdős–Selfridge: some $n-i$ always fails. Monier (1985): $n_k\le k!$. Cambie (forum): $n_k\le k\cdot\mathrm{lcm}(2,\dots,k-1)$. A forum comment (GPT-5.5-assisted) proves $n_k\ge\max(2k,\prod_{p^a\|k}p^{a+\lfloor\log_p(k/2)\rfloor})$; a reply suggests $k/2\to k-1$. Two proof claims by Ricky Cipollini (GPT-5.6 Sol), listed in the problem page's proof-claims section (submission dates 2026-07-27 and 2026-08-04 as shown on the live page on 2026-10-22; the site states that listing is no guarantee of correctness): $\log n_k\le\frac{k}{\log k}(\log\log k+\log\log\log k+\log2+o(1))$ and $\log n_k\ge c(\log k)^2$. The OEIS b-file gives $n_k$ for $k\le59$.

**What this packet claims.**
1. (Theorem) A prime-by-prime description of the failing indices, giving a two-line proof of Erdős–Selfridge and the lower bound $n_k\ge W'_k:=\prod_{p^a\|k}p^{a+\lfloor\log_p(k-1)\rfloor}$, attained for $k=4,6,14$.
2. (Theorem) The admissible $n$ form a periodic set whose density $\delta(k)$ is an explicit finite product-sum, and $\log(1/\delta(k))=(C+o(1))\,k/\log k$ with $C=\sum_{j\ge1}\frac1j\log(1+\frac1j)=1.2577468869\ldots$
3. (Data) $n_k$ for $60\le k\le110$, each verified by exact arithmetic, minimality by two independently written exhaustive searches (all 51 values).
4. (Conjecture, not claimed as proved) $n_k\approx\mathrm{Exp}(1)/\delta(k)$, which would give $\log n_k=(C+o(1))k/\log k$. Evidence: two pre-registered out-of-sample tests, 47 of 51 values inside their 90% intervals (46 expected); correlation 0.988 between $\log n_k$ and $\log(1/\delta(k))$ for $31\le k\le110$.

---

## Part A. Definitions and the local theory (with proofs)

Notation. Fix $k$ and $n\ge 2k$. The *block* is $B=\{n-k+1,\dots,n\}$; index $i\in[0,k)$ refers to the element $n-i$, and $i$ is *bad* if $(n-i)\nmid\binom nk$. For a prime $p$:
$$L=L_p(k)=\lfloor \log_p k\rfloor\quad(p^L\le k<p^{L+1}),\qquad M_p(n)=\max_{0\le i<k} v_p(n-i).$$


## 1. The bad set prime by prime

**Lemma 1.** For $0\le i<k$: $(n-i)\mid\binom nk$ iff $v_p(n-i)\le v_p\binom nk$ for every prime $p\le k$.

*Proof.* With $P=\prod_{j<k}(n-j)=k!\binom nk$, $(n-i)\mid\binom nk\iff k!\mid P/(n-i)$. For $p>k$ there is no condition. For $p\le k$ the condition $v_p(P)-v_p(n-i)\ge v_p(k!)$ reads $v_p(n-i)\le v_p\binom nk$. $\square$

**Lemma 2.** For $q=p^e$, the block contains $\lfloor k/q\rfloor+\delta_e$ multiples of $q$, with $\delta_e=[\,n\bmod q<k\bmod q\,]$. Hence $v_p\binom nk=\sum_{e\ge1}\delta_e$.

*Proof.* With $n=aq+r$, $k=bq+s$ ($0\le r,s<q$), the count $\lfloor n/q\rfloor-\lfloor(n-k)/q\rfloor$ is $b$ if $r\ge s$ and $b+1$ if $r<s$. Summing over $e$ and using Legendre's formula gives the second claim. $\square$

Define the *deficiency* $d_p(n)=\#\{1\le e\le L:\ \delta_e(n)=0\}=\#\{1\le e\le L:\ n\bmod p^e\ \ge\ k\bmod p^e\}$.

**Lemma 3.** $v_p\binom nk=M_p(n)-d_p(n)$. Hence $\mathrm{Bad}_p(n):=\{i: v_p(n-i)>v_p\binom nk\}=\{i: v_p(n-i)>M_p-d_p\}$, and:
1. $\mathrm{Bad}_p(n)=\varnothing$ iff $d_p(n)=0$.
2. If $d_p\ge1$, every index of maximal valuation is bad. $|\mathrm{Bad}_p|=1$ iff the maximum is attained at a single index $i^*$ and every other index has valuation $\le M_p-d_p$.

*Proof.* The block has $k\ge p^L$ elements, so $M_p\ge L$. For $e>L$, $p^e>k$ and $\delta_e=[M_p\ge e]$. So $\sum_e\delta_e=(L-d_p)+(M_p-L)$. $\square$

**Corollary 4 (Erdős–Selfridge).** If $p\mid k$ then $d_p(n)\ge v_p(k)\ge1$ for every $n$, because $k\bmod p^e=0$ for $e\le v_p(k)$. So $\mathrm{Bad}_p(n)\ne\varnothing$, and for every $n\ge k$ some $n-i$ fails to divide $\binom nk$. $\square$

## 2. The bad index is forced; a lower bound

**Corollary 5.** Let $n$ be valid with unique bad index $i_0$, and let $p\mid k$. Then $n-i_0$ is the unique element of the block with maximal $p$-adic valuation, and
$$v_p(n-i_0)\ \ge\ v_p(k)+\lfloor\log_p(k-1)\rfloor\ =\ v_p(k)+L_p-[\,k=p^{L_p}\,].$$
Hence $W'_k:=\prod_{p^a\|k}p^{\,a+\lfloor\log_p(k-1)\rfloor}$ divides $n-i_0$, and $n_k\ge \max(2k,\,W'_k)$.

*Proof.* By Corollary 4, $\mathrm{Bad}_p=\{i_0\}$, so $i_0$ is the unique argmax (Lemma 3.2), and every other index has valuation $\le M_p-d_p$. Let $e_1$ be the largest $e\le L$ such that the block holds at least two multiples of $p^e$; one of them is not $n-i_0$, so the second-largest valuation is $\ge e_1$. Every $e\in(e_1,L]$ has exactly one multiple of $p^e$ in the block. Since $\lfloor k/p^e\rfloor\ge1$, this forces $\lfloor k/p^e\rfloor=1$ and $\delta_e=0$. If $k$ is not a power of $p$, the block holds exactly $k/p^{v_p(k)}\ge2$ multiples of $p^{v_p(k)}$, so $e_1\ge v_p(k)$. The levels $e\le v_p(k)$ (where $k\bmod p^e=0$) and $e\in(e_1,L]$ are then disjoint non-carries, giving $d_p\ge v_p(k)+L-e_1$. So $M_p\ge e_1+d_p\ge L+v_p(k)$. If $k=p^L$, then $d_p=L$ and the second-largest valuation is $\ge L-1$ (there are $p\ge2$ multiples of $p^{L-1}$), so $M_p\ge 2L-1$; and since then $a=L$ and $\lfloor\log_p(k-1)\rfloor=L-1$, this is exactly the claimed exponent $a+\lfloor\log_p(k-1)\rfloor$. $\square$

*Remarks.*
* Compared with the forum bound: $\lfloor\log_p(k-1)\rfloor\ge\lfloor\log_p(k/2)\rfloor$, with strict inequality when $p^{L_p}>k/2$ and $k\ne p^{L_p}$. For example, for $k=6,14,18,54$ we get $W'_k=72,784,2592,46656$, against $36,392,1296,23328$.
* The bound is attained: $n_4-1=8=W'_4$, $n_6-3=72=W'_6$, $n_{14}-9=784=W'_{14}$. These are the only $k\le110$ with equality.
* $W'_k>k^{\omega(k)}\cdot k/\mathrm{rad}(k)$ when $k$ is not a prime power. Along primorials this gives $n_k\ge\exp\big((1+o(1))(\log k)^2/\log\log k\big)$.
* Checked: $W'_k\mid n_k-i_0$ for all 109 values $2\le k\le110$, and for all 143,383 valid $n$ in $[2k,2k+60000)$ with $k\le22$ (independent review).

## 3. Primes $p>\sqrt k$

**Lemma 6.** Let $p$ be a prime with $\sqrt k<p\le k$ (so $L=1$ and $p^2>k$) and $j=\lfloor k/p\rfloor$.
* If $n\bmod p<k\bmod p$, then $\mathrm{Bad}_p=\varnothing$.
* Otherwise, if $j=1$, the block holds exactly one multiple of $p$, at index $n\bmod p$, and $\mathrm{Bad}_p=\{n\bmod p\}$.
* Otherwise ($j\ge2$), the block holds exactly $j$ multiples of $p$, and at most one is divisible by $p^2$. $|\mathrm{Bad}_p|=1$ iff one of them is divisible by $p^2$, and that one is the bad index. If none is, all $j$ are bad.

Consequently, for $0\le i_0<k$, the proportion of $n$ (mod $p^2$) with $\mathrm{Bad}_p(n)\subseteq\{i_0\}$ is
$$\Pr(E_{p,i_0})=\frac{k\bmod p}{p}+\big[\,i_0\bmod p\ge k\bmod p\,\big]\cdot\begin{cases}1/p&(j=1)\\1/p^2&(j\ge2).\end{cases}$$

*Proof.* With $L=1$, $d_p=[\,n\bmod p\ge k\bmod p\,]$. If $n\bmod p<k\bmod p$ then $d_p=0$ and $\mathrm{Bad}_p=\varnothing$ by Lemma 3.1. Otherwise $d_p=1$, so $\mathrm{Bad}_p=\{i:v_p(n-i)\ge M_p\}$ is the set of indices of maximal valuation, and by Lemma 2 the block holds exactly $\lfloor k/p\rfloor+\delta_1=j$ multiples of $p$. If $j=1$, the one multiple of $p$ has index $i\equiv n\pmod p$ with $0\le i<p\le k$, i.e. $i=n\bmod p$; its valuation is $M_p\ge1$ and all other valuations are $0$. If $j\ge2$, two multiples of $p^2$ in the block would differ by at least $p^2>k$, so at most one index has valuation $\ge2$; if there is one it is the unique maximum, and if not, all $j$ multiples of $p$ tie at valuation $1=M_p$.

For the proportion: the events $d_p=0$ and $d_p=1$ are disjoint, and $\Pr(d_p=0)=(k\bmod p)/p$. Given $d_p=1$: for $j=1$, $\mathrm{Bad}_p=\{i_0\}$ iff $n\bmod p=i_0$, which needs $i_0<p$ and $i_0\ge k\bmod p$ and has probability $1/p$ (if $i_0\ge p$ then $i_0\bmod p=i_0-p<k-p=k\bmod p$, so the indicator is $0$, as it should be); for $j\ge2$, $\mathrm{Bad}_p=\{i_0\}$ iff $p^2\mid n-i_0$, probability $1/p^2$, and then $n\bmod p=i_0\bmod p$, so $d_p=1$ is exactly the condition $i_0\bmod p\ge k\bmod p$. $\square$

## 4. Periodicity and the exact density

**Theorem 7.** Let $E_{p,i_0}=\{n:\mathrm{Bad}_p(n)\subseteq\{i_0\}\}$.
1. For each prime $p\le k$, the set $\mathrm{Bad}_p(n)$ depends only on $n\bmod p^{2L_p}$; so each $E_{p,i_0}$ is a union of residue classes mod $p^{2L_p}$.
2. $n$ is valid iff $n\in\bigcap_{p\le k}E_{p,i_0}$ for some $i_0$, and these $k$ sets are pairwise disjoint.
3. Hence the valid $n$ form a union of residue classes mod $D_k=\prod_{p\le k}p^{2L_p}$, of natural density
$$\delta(k)=\sum_{i_0=0}^{k-1}\ \prod_{p\le k}\Pr\nolimits(E_{p,i_0}),$$
where $\Pr(E_{p,i_0})$ is the proportion of residue classes mod $p^{2L_p}$ lying in $E_{p,i_0}$.

*Proof.* (1) Write $L=L_p$ and let $n'\equiv n\pmod{p^{2L}}$. The deficiency $d_p$ depends only on $n\bmod p^L$, so $d_p(n')=d_p(n)$. For each index $i$, $n'-i\equiv n-i\pmod{p^{2L}}$, so $v_p(n'-i)=v_p(n-i)$ whenever $v_p(n-i)<2L$, and $v_p(n'-i)\ge2L$ iff $v_p(n-i)\ge2L$. Two indices with valuation $\ge L+1$ would differ by a multiple of $p^{L+1}>k$, so at most one index has valuation $\ge L+1$.
   * If no index has valuation $\ge2L$, all valuations agree between $n$ and $n'$, so $M_p$, $d_p$ and $\mathrm{Bad}_p$ agree.
   * If one index $i^*$ has $v_p(n-i^*)\ge2L$, then it is the unique maximum for both $n$ and $n'$, and every other valuation is $\le L$ and agrees. By Lemma 3, $i^*$ is bad iff $d_p\ge1$, the same for $n$ and $n'$. Another index $i$ is bad iff $v_p(n-i)>M_p-d_p$; but $v_p(n-i)\le L$ and $M_p-d_p\ge2L-L=L$, so this never happens, for $n$ or $n'$.
   So $\mathrm{Bad}_p(n')=\mathrm{Bad}_p(n)$. (The modulus $p^{2L-1}$ does not suffice in general. For $(k,p)=(6,3)$, $L=1$: the block of $n=12$ is $\{7,\dots,12\}$ with $v_3(9)=2$ at $i=3$ and $v_3(12)=1$ at $i=0$, so $M_3=2$, $d_3=[\,12\bmod3\ge6\bmod3\,]=1$, and $\mathrm{Bad}_3=\{i:v_3(12-i)>1\}=\{3\}$; the block of $n=15\equiv12\pmod 3$ is $\{10,\dots,15\}$ with $v_3(12)=v_3(15)=1$, so $M_3=1$, $d_3=1$, and $\mathrm{Bad}_3=\{0,3\}$.)

(2) By Lemma 1, the bad set of $n$ is $\bigcup_{p\le k}\mathrm{Bad}_p(n)$, and it is nonempty by Corollary 4, since $k\ge2$ has a prime factor. So it has exactly one element iff there is an $i_0$ with $\mathrm{Bad}_p(n)\subseteq\{i_0\}$ for every $p\le k$. If this held for two indices $i_0\ne i_1$, every $\mathrm{Bad}_p(n)$ would be contained in $\{i_0\}\cap\{i_1\}=\varnothing$, contradicting Corollary 4.

(3) By (1) and the Chinese remainder theorem, $\bigcap_{p\le k}E_{p,i_0}$ is a union of residue classes mod $D_k$, and the proportion of classes it contains is the product of the proportions $\Pr(E_{p,i_0})$, because the map $n\bmod D_k\mapsto(n\bmod p^{2L_p})_{p\le k}$ is a bijection. The natural density of a periodic set is its proportion of classes per period, and by (2) the valid $n$ are the disjoint union over $i_0$. (The restriction $n\ge2k$ does not affect density.) $\square$

For $p>\sqrt k$, Lemma 6 gives the closed form
$$\Pr(E_{p,i_0})=\frac{k\bmod p}{p}+[\,i_0\bmod p\ge k\bmod p\,]\cdot\begin{cases}1/p&(j=1)\\1/p^2&(j\ge2).\end{cases}$$
For $p\le\sqrt k$ the probability is computed by enumerating $n\bmod p^{L+1}$, treating the valuation of the (at most one) multiple of $p^{L+1}$ as a geometric tail. Two independent implementations agree exactly. Brute force over full periods confirms $\delta(k)$ for $k\le12$, e.g. $\delta(7)=269/2520$, $\delta(11)=9803/831600$, $\delta(12)=1/1386$. Monte Carlo agrees at $k=13,16,20,24,31$.


---

## Part B. The density asymptotic (full proof)

# Theorem 8: the size of the density $\delta(k)$

Throughout, $p$ denotes a prime, $\log$ is natural, and $\{x\}=x-\lfloor x\rfloor$. For a prime $p\in(\sqrt k,k]$ with $p\nmid k$ write
$$j=j(p)=\lfloor k/p\rfloor,\qquad r=r(p)=k-jp=k\bmod p\in[1,p-1],$$
so that $\{k/p\}=r/p$ and $1\le j<\sqrt k$. Define
$$S(k)=\sum_{\substack{\sqrt k<p\le k\\ p\nmid k}}\log\frac{p}{k\bmod p}=\sum_{\substack{\sqrt k<p\le k\\ p\nmid k}}-\log\Big\{\frac kp\Big\}.$$
Every term is positive. (The at most one prime $p>\sqrt k$ dividing $k$ is excluded because $k\bmod p=0$; Part 1 shows it contributes $O(\log k)$ to $\log(1/\delta(k))$.)

**Theorem 8.** As $k\to\infty$,
$$\log\frac1{\delta(k)}=S(k)+O(\sqrt k)\qquad\text{and}\qquad S(k)=(C+o(1))\,\frac{k}{\log k},$$
where
$$C=\int_1^\infty\frac{-\log\{x\}}{x^2}\,dx=\sum_{j\ge1}\frac1j\log\Big(1+\frac1j\Big)=\sum_{m\ge1}\frac{(-1)^{m+1}\zeta(m+1)}{m}=1.25774688694436963001\ldots$$
Consequently $\log(1/\delta(k))=(C+o(1))\,k/\log k$.

## Two inputs from prime number theory

**(PNT)** $\pi(x)=\mathrm{li}(x)+E(x)$ with $E(x)\ll x\exp(-c\sqrt{\log x})$ for an absolute $c>0$ (de la Vallée Poussin).

**(BT)** For real $x\ge0$ and $y\ge2$, $\pi(x+y)-\pi(x)\le 3y/\log y$. (Montgomery–Vaughan give $2y/\log y$ for integer lengths; a real interval of length $y$ lies in an integer interval of length at most $y+1$, and $2(y+1)/\log(y+1)\le3y/\log y$ for $y\ge2$.) We also use Chebyshev's bounds $\pi(x)\ll x/\log x$ and $\vartheta(x)=\sum_{p\le x}\log p\ll x$.

## Lemma A (injectivity)
The map $p\mapsto k\bmod p$ is injective on primes $p\in(\sqrt k,k]$ with $p\nmid k$.

*Proof.* If $p\ne q$ are two such primes with $k\bmod p=k\bmod q=r$, then $pq\mid k-r$. But $k-r=jp\ge p>0$ and $k-r\le k<pq$, a contradiction. $\square$

## Lemma B (the constant)
For $j\ge1$, $\displaystyle c_j:=\int_j^{j+1}\frac{-\log(x-j)}{x^2}\,dx=\frac1j\log\Big(1+\frac1j\Big)$, and $\sum_{j\ge1}c_j=C$ with $\sum_{j>J}c_j\le 1/J$.

*Proof.* Substituting $u=x-j$, $c_j=\int_0^1\frac{-\log u}{(j+u)^2}\,du$. Integrate by parts with $v(u)=\frac{u}{j(j+u)}$, which satisfies $v'(u)=\frac{1}{(j+u)^2}$ and $v(0)=0$:
$$c_j=\Big[-\log u\cdot\frac{u}{j(j+u)}\Big]_0^1+\int_0^1\frac1u\cdot\frac{u}{j(j+u)}\,du=0+\frac1j\int_0^1\frac{du}{j+u}=\frac1j\log\frac{j+1}{j}.$$
The boundary term vanishes because $\log1=0$ and $u\log u\to0$. Since $\log(1+1/j)\le1/j$, $c_j\le1/j^2$ and $\sum_{j>J}c_j\le\sum_{j>J}1/j^2\le1/J$. Summing $c_j$ over $j$ gives $\int_1^\infty-\log\{x\}\,x^{-2}dx$ by splitting $[1,\infty)$ at the integers. $\square$

## Part 1: $\log(1/\delta(k))=S(k)+O(\sqrt k)$

Recall from Theorem 7 that
$$\delta(k)=\sum_{i_0=0}^{k-1}\prod_{p\le k}\Pr(E_{p,i_0}),\qquad \Pr(E_{p,i_0})=\frac{k\bmod p}{p}+\big[\,i_0\bmod p\ge k\bmod p\,\big]\cdot\begin{cases}1/p&(\lfloor k/p\rfloor=1)\\1/p^2&(\lfloor k/p\rfloor\ge2)\end{cases}\quad(p>\sqrt k).$$

*Upper bound for $\delta$.* Bound each of the $k$ summands by the product over $p>\sqrt k$, $p\nmid k$ only (the other factors are $\le1$), and each such factor by $\{k/p\}+1/p$:
$$\delta(k)\le k\prod_{\substack{\sqrt k<p\le k\\p\nmid k}}\Big(\Big\{\frac kp\Big\}+\frac1p\Big)
=k\prod\Big\{\frac kp\Big\}\prod\Big(1+\frac{1}{k\bmod p}\Big).$$
By Lemma A the values $k\bmod p$ are distinct positive integers $\le k$, so $\sum\log(1+\frac1{k\bmod p})\le\sum_{r\le k}\frac1r\le\log k+1$. Hence $\log(1/\delta(k))\ge S(k)-2\log k-1$.

*Lower bound for $\delta$.* Keep only the term $i_0=0$.
* For $p\le\sqrt k$: if $p^{2L}\mid n$ (with $L=\lfloor\log_pk\rfloor\ge1$), then $v_p(n)\ge2L$ while $v_p(n-i)=v_p(i)\le L<2L$ for $1\le i<k$ (as $i<k<p^{L+1}$). So $M_p=v_p(n)$ is attained only at $i=0$, and every other index has valuation $\le L\le M_p-d_p$ because $d_p\le L$. By Lemma 3, $\mathrm{Bad}_p(n)\subseteq\{0\}$. Thus $\Pr(E_{p,0})\ge p^{-2L}\ge k^{-2}$, and $\sum_{p\le\sqrt k}2\log k\ll\sqrt k$ by Chebyshev.
* For $\sqrt k<p\le k$, $p\nmid k$: $\Pr(E_{p,0})\ge(k\bmod p)/p=\{k/p\}$.
* For the at most one prime $p>\sqrt k$ with $p\mid k$: $k\bmod p=0$, so $\Pr(E_{p,0})\ge1/p^2\ge1/k^2$.

Hence $\log(1/\delta(k))\le S(k)+O(\sqrt k)$. Together: $\log(1/\delta(k))=S(k)+O(\sqrt k)$. $\square$

## Part 2: $S(k)=(C+o(1))\,k/\log k$

Fix $\varepsilon\in(0,1/e)$ and an integer $J\ge2$; they stay fixed while $k\to\infty$ (assume $k>(J+1)^2$), and are sent to $0$ and $\infty$ at the end. Cover the primes $p\in(\sqrt k,k]$, $p\nmid k$, by three classes according to $r=k\bmod p$ and $j=\lfloor k/p\rfloor$:
$$\mathcal T:\ r\le4j,\qquad \mathcal D:\ 4j<r\le\varepsilon p,\qquad \mathcal B:\ r>\varepsilon p.$$
($\mathcal T$ and $\mathcal B$ can overlap for $p<2\sqrt{k/\varepsilon}$. That is harmless: the upper bound on $S(k)$ only needs a cover, and the lower bound uses only the part of $\mathcal B$ with $j\le J$, which is a subset of the terms.)

### Class $\mathcal T$ (tiny remainders): $O(\sqrt k\log k)$
For primes with $r\le4j$ we have $jp\le k-1$ (as $r\ge1$) and $k\le jp+4j$, so $p\in[k/j-4,\,k/j)$, a half-open interval of length $4$ containing at most $4$ integers. So there are at most $4$ such primes for each of the fewer than $\sqrt k$ values of $j$. Every term is at most $\log p\le\log k$. So the class contributes $\le4\sqrt k\log k=o(k/\log k)$.

### Class $\mathcal D$ (dyadic middle): $\ll\varepsilon\log(1/\varepsilon)\,k/\log k+o(k/\log k)$
Group the primes by $j$ and by dyadic ranges $r\in(R,2R]$ with $R$ a power of $2$. A prime in the group satisfies $k-2R\le jp<k-R$, so $p$ lies in an interval of length $R/j$; and $r>4j$ forces $R>2j$, so $R/j>2$ and (BT) applies: the group has at most $\frac{3R/j}{\log(R/j)}$ primes. Each term is $\log(p/r)\le\log\frac{k}{jR}$, since $p\le k/j$ and $r>R$. Also $R<r\le\varepsilon p\le\varepsilon k/j$.

Put $V=\varepsilon k/j^2$ and, for a group with range $(R,2R]$, $u=R/j$; then $2<u$ and, since $R<\varepsilon k/j$, $u<V$. Also $\log\frac{k}{jR}=\log\frac Vu+\log\frac1\varepsilon$. So the contribution of fixed $j$ is at most
$$\sum_{u}\frac{3u}{\log u}\Big(\log\frac Vu+\log\frac1\varepsilon\Big),$$
where $u$ runs over the values $R/j$ with $R$ a power of two, $2<u<V$. The admissible $R$ are the powers of two below $\varepsilon k/j$; the largest, $R_{\max}$, satisfies $R_{\max}\ge\varepsilon k/(2j)$, so the $u$ are $V'/2^m$ ($m\ge0$) with $V/2\le V'<V$, and $V/2^{m+1}\le u\le V/2^m$.
* For $m\le\frac12\log_2V-1$: here $\log u\ge\log(V/2^{m+1})\ge\frac12\log V$ and $\log(V/u)\le(m+1)\log2$, so these terms sum to at most $\frac{6V}{\log V}\sum_{m\ge0}\frac{(m+1)\log2+\log(1/\varepsilon)}{2^m}\le\frac{24V}{\log V}\Big(\log2+\log\frac1\varepsilon\Big)$.
* For $m>\frac12\log_2V-1$: here $u\le V/2^m<2\sqrt V$, while $u>2$ gives $\log u\ge\log2$ and $\log(V/u)\le\log V$. Each such group therefore contributes at most $\frac{6\sqrt V}{\log2}\big(\log V+\log\frac1\varepsilon\big)$, and there are at most $\log_2V$ such groups (as $u>2$ forces $2^m<V/2$). So these terms sum to $\ll\sqrt V\,(\log k)^2$ (as $V\le k$ and $\varepsilon$ is fixed).

Now sum over $j$ (only $j$ with $V>2$, i.e. $j<\sqrt{\varepsilon k/2}$, contribute).
* The $\sqrt V$ terms give $\ll\sqrt{\varepsilon k}\,(\log k)^2\sum_{j<\sqrt k}\frac1j\ll\sqrt k(\log k)^3=o(k/\log k)$.
* For $j\le k^{1/4}$: $\log V\ge\log(\varepsilon\sqrt k)\ge\frac14\log k$ for large $k$, so $\sum_{j\le k^{1/4}}\frac{24V}{\log V}(\log2+\log\tfrac1\varepsilon)\le\frac{96\,\varepsilon k}{\log k}(\log2+\log\tfrac1\varepsilon)\sum_j\frac1{j^2}\ll\varepsilon\log(1/\varepsilon)\frac{k}{\log k}$.
* For $k^{1/4}<j<\sqrt{\varepsilon k/2}$: $\log V\ge\log2$, so these give $\ll\varepsilon k\log(1/\varepsilon)\sum_{j>k^{1/4}}j^{-2}\ll\varepsilon\log(1/\varepsilon)\,k^{3/4}=o(k/\log k)$.

So class $\mathcal D$ contributes at most $A\,\varepsilon\log(1/\varepsilon)\,k/\log k+o(k/\log k)$ for an absolute constant $A$.

### Class $\mathcal B$ (bulk), $j>J$: $\le 6\log(1/\varepsilon)\,k/(J\log k)$
Each term is $\log(p/r)<\log(1/\varepsilon)$. The primes with $j>J$ satisfy $p<k/J$, so there are at most $\pi(k/J)\le\frac{3k}{J\log(k/J)}\le\frac{6k}{J\log k}$ of them for $k\ge J^2$ (BT with $x=0$).

### Class $\mathcal B$, $j\le J$: the main term
Fix $j\le J$. The primes of class $\mathcal B$ with $\lfloor k/p\rfloor=j$ are the primes $p\nmid k$ in the interval
$$I_j(\varepsilon)=\Big(\frac{k}{j+1},\ \frac{k}{j+\varepsilon}\Big),$$
because $r>\varepsilon p\iff k>(j+\varepsilon)p$. On this interval put $g(t)=\log\frac{t}{k-jt}=-\log\big(\frac kt-j\big)$; then $0<g(t)<\log(1/\varepsilon)$ and $g'(t)=\frac1t+\frac{j}{k-jt}\le\frac{1+j/\varepsilon}{t}\le\frac{(J+1)(1+J/\varepsilon)}{k}$. (A prime $p\mid k$ with $\lfloor k/p\rfloor=j$ equals $k/j$, which is not in $I_j(\varepsilon)$, so the condition $p\nmid k$ excludes nothing here. Since $k>(J+1)^2$, $I_j(\varepsilon)\subset(\sqrt k,k]$.)

By partial summation with $\pi(t)=\mathrm{li}(t)+E(t)$, writing $a,b$ for the endpoints of $I_j(\varepsilon)$,
$$\sum_{p\in I_j(\varepsilon)}g(p)=\int_a^b\frac{g(t)}{\log t}\,dt+\Big[g(t)E(t)\Big]_a^b-\int_a^bg'(t)E(t)\,dt+O\big(\log\tfrac1\varepsilon\big),$$
where the $O(\cdot)$ covers the endpoints. The two error terms are at most $2\log(1/\varepsilon)\max_{[a,b]}|E|+(b-a)\max_{[a,b]}|g'|\max_{[a,b]}|E|\ll_{\varepsilon,J}k\exp(-c'\sqrt{\log k})=o(k/\log k)$ by (PNT), since $[a,b]\subset[k/(J+1),k]$.

For the main integral, $\log t=\log k+O(\log(J+1))=(1+o(1))\log k$ on $[a,b]$, so
$$\int_a^b\frac{g(t)}{\log t}\,dt=\frac{1+o(1)}{\log k}\int_{k/(j+1)}^{k/(j+\varepsilon)}-\log\Big(\frac kt-j\Big)\,dt=\frac{(1+o(1))\,k}{\log k}\int_{j+\varepsilon}^{j+1}\frac{-\log(x-j)}{x^2}\,dx,$$
by the substitution $x=k/t$, $dt=-k\,x^{-2}dx$. Write $c_j(\varepsilon)$ for the last integral. Then $0\le c_j-c_j(\varepsilon)=\int_j^{j+\varepsilon}\frac{-\log(x-j)}{x^2}dx\le\frac1{j^2}\int_0^\varepsilon-\log u\,du=\frac{\varepsilon(1+\log(1/\varepsilon))}{j^2}$.

Summing over $j\le J$:
$$\sum_{\substack{p\in\mathcal B\\ j(p)\le J}}\log\frac pr=\frac{(1+o(1))\,k}{\log k}\sum_{j\le J}c_j(\varepsilon),\qquad C-\frac1J-4\varepsilon\log\frac1\varepsilon\ \le\ \sum_{j\le J}c_j(\varepsilon)\ \le\ C,$$
using Lemma B, $\sum_jj^{-2}<2$, and $\varepsilon(1+\log(1/\varepsilon))\le2\varepsilon\log(1/\varepsilon)$ for $\varepsilon<1/e$.

### Conclusion
All terms of $S(k)$ are positive, so the $j\le J$ part of class $\mathcal B$ alone gives the lower bound, and the four pieces together give the upper bound:
$$\Big(C-\frac1J-4\varepsilon\log\frac1\varepsilon-o(1)\Big)\frac{k}{\log k}\ \le\ S(k)\ \le\ \Big(C+A\varepsilon\log\frac1\varepsilon+\frac{6\log(1/\varepsilon)}{J}+o(1)\Big)\frac{k}{\log k},$$
where $o(1)\to0$ as $k\to\infty$ with $\varepsilon,J$ fixed. Letting $k\to\infty$, then $J\to\infty$, then $\varepsilon\to0$ gives $S(k)=(C+o(1))\,k/\log k$. With Part 1, $\log(1/\delta(k))=(C+o(1))\,k/\log k$. $\blacksquare$

## Remarks
* The proof gives nothing about the rate. Numerically $S(k)/(k/\log k)$ averages $1.16$ over $k\in[90,110]$, and is $1.37$ at $k\approx10^4$ and $1.34$ at $10^6$ (computed independently twice); the next term should be $c_2k/\log^2k$ with $c_2=\int_1^\infty-\log\{x\}\log x\,x^{-2}dx=1.0016551589\ldots$, obtainable by keeping the $\log t$ variation in the main integral.
* Numerical check of the class bounds (direct sums over primes, no model): the class $\mathcal D$ sum divided by $\varepsilon\log(1/\varepsilon)\,k/\log k$ is $2.29$, $2.08$, $2.10$, $1.97$ at $(k,\varepsilon)=(10^6,0.1)$, $(10^6,0.02)$, $(10^7,0.02)$, $(10^7,0.005)$, so the implied constant $A$ is about $2$ in practice and the $\varepsilon\log(1/\varepsilon)$ scaling is visible; the class $\mathcal T$ sum is $0.011$ and $0.004$ times $k/\log k$ at $k=10^6,10^7$.
* The density is an exact rational, so Theorem 8 is a statement about $\delta(k)$ only. It says nothing rigorous about $n_k$; that is Conjecture 9.
* A second review (Gemini 4 Argon, 2026-10-22, of the cross-check packet) found no mathematical issues and one presentational one, applied here: the displayed bound for class $\mathcal D$ is now stated before the substitution $\log u\ge\log(V/2^{m+1})$, which is only valid in the first bullet.
* Refereed by Claude Fable 5.1 on 2026-10-22 (verdict: correct with minor fixes, all applied here: the constant $4\varepsilon\log(1/\varepsilon)$ in the lower bound, the treatment of the dyadic grid via $V'$, the $p\le k$ in Lemma A, the cover wording, the half-open interval in class $\mathcal T$, BT for real intervals, and the vacuous remark about $p\mid k$). The referee also checked Part 1's two inequalities exactly, with $\delta(k)$ computed as an exact rational without Lemma 3 or the closed form, for all $k\le60$ and fifteen larger $k$ up to $256$, and checked the class decomposition numerically at $k=10^6,10^7$ (class $\mathcal D$ is about $2\,\varepsilon\log(1/\varepsilon)\,k/\log k$, so $A\approx2$ in practice).


---

## Part C. Conjecture and evidence

## 6. Growth conjecture

**Conjecture 9.** The valid set behaves like a random set of density $\delta(k)$ (Theorem 8 makes $\delta(k)$ itself rigorous; the conjecture is only about the least element): $n_k\delta(k)$ is approximately $\mathrm{Exp}(1)$, so $\log n_k=\log(1/\delta(k))+O(1)$ typically. Under this heuristic, and only under it,
$$\log n_k=(C+o(1))\frac{k}{\log k}.$$
In particular $\frac1k\log n_k\to0$ and $n_k^{1/k}\to1$, but slowly. This is far below Cambie's upper bound $e^{(1+o(1))k}$ and far above the lower bound of Corollary 5.

## 7. Evidence

* **Prime $k$.** If $p\mid k$, Corollary 5 forces $W'_k\mid n-i_0$ and removes the factor $\{k/p\}\approx0$ for $p>\sqrt k$ dividing $k$. So $\delta(k)$ is much larger, and $n_k$ much smaller, when $k$ is prime: for example $n_{30}\approx3.8\cdot10^7$ but $n_{31}=8100$. The model tracks these swings.
* **Fit, $2\le k\le59$** (58 values from the b-file). $x_k=\log n_k-\log(1/\delta(k))$ has mean $-0.06$ (s.e. $0.16$) and SD $1.19$. (All SDs in this note are sample SDs, with $n-1$.) Under an exact $\mathrm{Exp}(1)$ law, $\log(\mathrm{Exp}(1))$ has mean $-0.577$ and SD $1.28$. The fit is poor for small $k$ (mean $+0.19$ for $k\le30$; a KS test rejects on all 58) and good for $31\le k\le59$ (mean $-0.31$). Small $k$ are distorted by the constraint $n\ge2k$ and the coarse structure of the valid set.
* **Out of sample.** Predicted 90% intervals for every $60\le k\le100$ were written to `PREDICTIONS_60_100.txt` (timestamped 2026-10-21T23:05:07Z) before the searches for these $k$ were launched (the first, $k=61$, finished 27 seconds later). The timing is a convenience, not the argument: the model has no fitted parameters, so no ordering of events could have influenced the predictions.
  * 38 of the 41 values fall inside their interval; about 37 would be expected.
  * The three outside are $k=64$ ($x=-3.01$), $91$ ($+1.15$) and $95$ ($-3.16$).
  * For $60\le k\le100$, $x_k$ has mean $-0.67$ (s.e. $0.17$) and SD $1.09$, KS $D=0.168$ (5% critical value $0.212$).
  * For $31\le k\le100$ (70 values): mean $-0.52$ (s.e. $0.14$), SD $1.20$, KS $D=0.076$ (critical value $0.162$). This is a close match to $\log\mathrm{Exp}(1)$.
  * For $k\le30$: mean $+0.19$, KS $D=0.348$ (critical value $0.252$, rejected). Using $n_k-2k+1$ in place of $n_k$ lowers $D$ to $0.229$.
  * All 99 values ($2\le k\le100$) together: KS $D=0.109$ (critical value $0.136$).
* **Second out-of-sample test, $101\le k\le110$.** Predictions were written to `PREDICTIONS_101_110.txt` at 2026-10-22T05:00:52Z (SHA-256 `ba3bad43…`) and copied to a second machine before any search started; the first value ($k=109$) was found at 05:02:46Z, and the independent minimality confirmations followed later that day.
  * 9 of 10 inside the 90% interval. The exception is $k=105$ ($x=-3.28$, floor $-2.97$).
  * Both tests together: 47 of 51 inside, against 45.9 expected.
  * For $31\le k\le110$: mean $x_k=-0.58$ (the model's $-\gamma=-0.577$), SD $1.19$, correlation $0.988$, slope $0.985$, KS $D=0.083$ (critical value $0.152$).
  * At $k=110$, $\log n_{110}=42.95$ against the model's $42.75$ and the Cipollini upper bound's main term $62.7$.
* **Correlation.** For $31\le k\le100$, $\log n_k$ and $\log(1/\delta(k))$ have correlation $0.986$ and slope $0.995$. This is the strongest single piece of evidence. The KS non-rejections on 41–70 points are weak evidence by comparison.
* **Not quite Poisson.** Gaps between consecutive valid $n$ are somewhat more regular than Poisson (coefficient of variation $0.80$–$0.96$). For some small $k$ valid $n$ cluster, e.g. $k=18$, where 14% of gaps equal 1. This affects $n_k$ by a bounded factor and fits the worse behaviour at small $k$.
* **Checks.** Lemma 3 was checked against exact big-integer divisibility with no mismatches: on more than 128,000 pairs $(k,n)$ by an independent referee implementation, on 6,000 random pairs with $n\le10^{18}$ (Fable), and on 20,000 random pairs by ours.


### Pre-registration records
* `PREDICTIONS_60_100.txt`: generated 2026-10-21T23:05:07Z, before the searches for $k\ge60$ were launched (the first value, $k=61$, finished 23:05:34Z). The timing is a convenience, not the argument: the model has no fitted parameters, so no ordering of events could have influenced the predictions. SHA-256 of the file as shipped: `e63062e928b778ed9e45ffb7c0dca9f893ca38dfbb20c29b06b793ff538ff81d`.
* `PREDICTIONS_101_110.txt`: generated 2026-10-22T05:00:52Z, copied to a second machine before any search started; the first value ($k=109$) was found at 05:02:46Z, and the independent minimality confirmations followed later that day. SHA-256: `ba3bad43d0ae30aa92e5f5c6795e6c2c207cc12d4f0c4e4ca3883e19d388a8ed`.
* Model: $n_k\sim\mathrm{Exp}(1)/\delta(k)$ with no fitted parameters; central 90% interval $[0.0513/\delta,\,2.996/\delta]$.
* Results: $60\le k\le100$: 38/41 inside (outside: $k=64,91,95$). $101\le k\le110$: 9/10 inside (outside: $k=105$). Combined 47/51; 45.9 expected.
* Statistics, $31\le k\le110$ (80 values; sample SDs throughout): $x_k=\log n_k-\log(1/\delta(k))$ has mean $-0.58$ (model: $-\gamma=-0.577$), SD $1.19$ (model: $1.283$), KS $D=0.083$ (5% critical value $0.152$); correlation$(\log n_k,\log(1/\delta))=0.988$, slope $0.985$. For $k\le30$ the KS test rejects ($D=0.348$).

### Relation to Cipollini's bounds
If both proof claims hold, $c(\log k)^2\le\log n_k\le(1+o(1))\,k\log\log k/\log k$. The conjecture sits strictly between and predicts the upper bound is off by a factor $\asymp\log\log k$. Explanation: the construction pins $n$ into a residue window of width $\approx e=k/(2\log k\log\log k)$ for each large prime (symmetric pigeonhole), at cost $\log(p/e)$ per prime; the density model's natural window is $[0,k\bmod p)$, at cost $\log\frac{p}{k\bmod p}$, summing to $S(k)$. Data: for $31\le k\le100$, $\log n_k$ is $0.47$–$0.89$ (mean $0.68$) of $\frac{k}{\log k}(\log\log k+\log\log\log k+\log2)$. Our $W'_k$ bound and $c(\log k)^2$ are not comparable without an explicit $c$; the data force $c\le0.74$ (from $k=19$), and with that $c$ the explicit bound is larger for 28 of the 80 composite $k\le110$ (those with several small prime factors), smaller for the rest, and trivial ($W'_k=k$) for prime $k$.

---

## Part D. Data

Columns: $k$, $n_k$, the bad index $i_0$ (so $n_k-i_0$ is the element that fails), and $\log(1/\delta(k))$ from the exact density. Values for $k\le59$ coincide with the OEIS b-file of A389360.

| k | n_k | i0 | log(1/delta(k)) |
|---|---|---|---|
| 2 | 4 | 0 | 0.000000 |
| 3 | 6 | 0 | 0.405465 |
| 4 | 9 | 1 | 1.386294 |
| 5 | 12 | 2 | 1.321756 |
| 6 | 75 | 3 | 3.583519 |
| 7 | 30 | 2 | 2.237303 |
| 8 | 70 | 6 | 3.555348 |
| 9 | 56 | 2 | 4.047825 |
| 10 | 2403 | 3 | 6.532731 |
| 11 | 280 | 5 | 4.440663 |
| 12 | 3465 | 9 | 7.234177 |
| 13 | 210 | 2 | 4.665831 |
| 14 | 793 | 9 | 8.322295 |
| 15 | 4732 | 7 | 8.740303 |
| 16 | 3213 | 13 | 7.773566 |
| 17 | 1456 | 11 | 6.227707 |
| 18 | 31110 | 6 | 10.116033 |
| 19 | 612 | 4 | 7.326764 |
| 20 | 67203 | 3 | 10.789537 |
| 21 | 145540 | 10 | 11.831021 |
| 22 | 464646 | 6 | 12.722603 |
| 23 | 2640 | 18 | 8.705590 |
| 24 | 476938 | 10 | 12.570580 |
| 25 | 21000 | 0 | 10.403105 |
| 26 | 86550 | 22 | 14.017919 |
| 27 | 234026 | 17 | 12.181970 |
| 28 | 1053702 | 6 | 14.996741 |
| 29 | 34776 | 5 | 11.396121 |
| 30 | 37584001 | 1 | 17.457716 |
| 31 | 8100 | 9 | 11.432639 |
| 32 | 2301456 | 16 | 13.906315 |
| 33 | 77780756 | 20 | 16.881940 |
| 34 | 61924632 | 24 | 18.183518 |
| 35 | 26515138 | 13 | 18.176345 |
| 36 | 105846930 | 18 | 18.607188 |
| 37 | 665280 | 20 | 13.924330 |
| 38 | 622999377 | 17 | 18.865021 |
| 39 | 233999782 | 16 | 19.565791 |
| 40 | 510752034 | 34 | 19.975724 |
| 41 | 1154440 | 3 | 14.873636 |
| 42 | 5567268681 | 9 | 21.720993 |
| 43 | 24458112 | 13 | 15.333983 |
| 44 | 191137416 | 8 | 19.830992 |
| 45 | 2115072003 | 3 | 21.520828 |
| 46 | 236924325 | 37 | 21.666393 |
| 47 | 3076480 | 1 | 16.254262 |
| 48 | 2641061412 | 36 | 21.598384 |
| 49 | 4255968 | 24 | 18.233549 |
| 50 | 4060800030 | 30 | 22.799423 |
| 51 | 2069262000 | 36 | 23.870679 |
| 52 | 40638048276 | 20 | 23.991200 |
| 53 | 35865700 | 17 | 18.974324 |
| 54 | 115993207876 | 4 | 24.972022 |
| 55 | 221981623878 | 3 | 24.989959 |
| 56 | 247307719725 | 45 | 25.477317 |
| 57 | 218175259280 | 41 | 25.510268 |
| 58 | 34156387476 | 20 | 26.661216 |
| 59 | 4967281530 | 22 | 20.632155 |
| 60 | 2117441088029 | 29 | 28.881757 |
| 61 | 569181900 | 50 | 20.834288 |
| 62 | 155275274056 | 8 | 27.109569 |
| 63 | 216949362182 | 35 | 26.703760 |
| 64 | 2600001558 | 22 | 24.687522 |
| 65 | 1936512990784 | 34 | 27.686693 |
| 66 | 1618958347825 | 49 | 30.466056 |
| 67 | 1178168706 | 37 | 23.139515 |
| 68 | 260686545186 | 34 | 28.093846 |
| 69 | 709479687556 | 28 | 29.517160 |
| 70 | 66383308992066 | 66 | 32.654593 |
| 71 | 13760436550 | 35 | 23.990009 |
| 72 | 890473430071 | 55 | 29.159105 |
| 73 | 40861892736 | 21 | 23.767872 |
| 74 | 3146202243081 | 9 | 30.028068 |
| 75 | 32639932074432 | 57 | 30.922732 |
| 76 | 16233110681625 | 25 | 31.061796 |
| 77 | 18874715290176 | 53 | 31.494209 |
| 78 | 780422752841501 | 29 | 34.755251 |
| 79 | 420957410952 | 14 | 26.351812 |
| 80 | 60137833600000 | 0 | 31.460504 |
| 81 | 2418072694480 | 46 | 29.088586 |
| 82 | 94878375215625 | 9 | 33.155977 |
| 83 | 885437574400 | 11 | 27.608328 |
| 84 | 3765171612545280 | 0 | 36.749028 |
| 85 | 1718626725667152 | 27 | 34.095595 |
| 86 | 129713628198225 | 81 | 35.311827 |
| 87 | 2221164774687826 | 82 | 34.933813 |
| 88 | 754618137360426 | 42 | 34.761782 |
| 89 | 3208190120080 | 80 | 29.354863 |
| 90 | 57753167368032004 | 4 | 37.889759 |
| 91 | 10789171853293890 | 56 | 35.771712 |
| 92 | 2643061175354691 | 67 | 36.169197 |
| 93 | 7201679510714780 | 29 | 36.121856 |
| 94 | 2544131371430937 | 25 | 37.010892 |
| 95 | 213706678047814 | 64 | 36.157630 |
| 96 | 11795043698546775 | 87 | 36.897883 |
| 97 | 10432185034560 | 35 | 30.275738 |
| 98 | 23154863741528961 | 1 | 37.088152 |
| 99 | 7525993870612546 | 43 | 36.643264 |
| 100 | 24275936775680073 | 73 | 38.288427 |
| 101 | 83339504740900 | 4 | 32.383743 |
| 102 | 455022751908409400 | 56 | 41.350416 |
| 103 | 80855126198850 | 57 | 33.142659 |
| 104 | 28292410857118753 | 33 | 38.986403 |
| 105 | 114184320231814976 | 101 | 42.559013 |
| 106 | 505139783269972305 | 81 | 40.791244 |
| 107 | 314604394073026 | 96 | 33.547281 |
| 108 | 42039517780512072 | 72 | 40.051081 |
| 109 | 92095914818376 | 95 | 33.686976 |
| 110 | 4499581121078560101 | 101 | 42.754493 |

Spot values of the exact density: $\delta(7)=269/2520$, $\delta(9)=11/630$, $\delta(10)=11/7560$, $\delta(11)=9803/831600$, $\delta(12)=1/1386$ (all confirmed by brute force over a full period).

---

## Part E. Review history

| Reviewer | Scope | Outcome |
|---|---|---|
| Claude (fresh referee instance, own code, >128,000 tests) | Lemmas 1–3, Cor 4–5, Lemma 6, Thm 7, statistics | Correct; sharpened the lower bound from $a+L-1$ to $a+\lfloor\log_p(k-1)\rfloor$ (now Cor 5); several overstatements fixed |
| Gemini 4 Argon | Same, in five parts | No errors found; two of its objections (the "iff" in Lemma 1, periodicity mod $p^{2L}$) were themselves wrong |
| Claude Fable 5.1 (own code; exact rational $\delta(k)$ computed without Lemma 3; own wheel search) | Everything incl. all 41 values $60\le k\le100$ (validity and minimality) | Correct; presentational fixes applied |
| Muse (Meta AI) | Bundle audit | Agreed with all numbers; found a weak-vs-sharp bound mislabel in a test script (fixed) and one wrong range (fixed) |
| Claude Fable 5.1 (second instance) | Full proof of Theorem 8 | "Correct with minor fixes" — nine items, all applied (see end of Part B) |
| Fable's independent search | $101\le k\le110$ minimality | All 10 confirmed (four of them in chunks, with a three-line lower-bound patch to Fable's program; diff kept) |
| Gemini 4 Argon (second pass, on this packet) | Everything in Parts A–F; recomputed $W'_k$, residuals and interval membership for $101\le k\le110$ | No mathematical issues; one presentational fix in class $\mathcal D$ (applied) and one LaTeX typo (fixed) |
| Grok (on revision 2/3 of this packet) | Everything; flagged class $\mathcal D$ and the Theorem 7 modulus for a second look, the $k=p^L$ case of Cor 5, and the conjecture's wording | Found no error; asked for a numeric check of class $\mathcal D$ (now in Part B remarks), explicit valuations for $(6,3)$ (added), a uniformity line in Cor 5 (added), more digits for $C$ and $c_2$ (added), and a reproducibility script for $\delta(k)$ (Appendix) |
| Muse (second pass, on this packet) | Traced Theorem 8 step by step; recomputed $\delta(k)$ from the printed formula and by brute force for $k\le8$; all values, statistics and the Cipollini reading | No substantive error. Six cosmetic points, all applied in revision 3: Lemma 6 and Theorem 7 now have written proofs; the $W'_k$ vs $c(\log k)^2$ comparison was overstated and is corrected; SD convention fixed (sample SD throughout); $S(k)$ window-mean wording; pre-registration wording; $\delta(2)$ row |

---

## Part F. What to cross-check (in priority order)

1. **Theorem 8, Part 2 (Part B above).** This is the newest and least-reviewed piece: one referee pass. Check especially the class-$\mathcal D$ dyadic bound (the $V'$ vs $V$ handling, the split at $m=\frac12\log_2V-1$, the $j$-sums), the partial summation in class $\mathcal B$ with the PNT error term, and the order of limits. Is there any step that silently needs more than de la Vallée Poussin's PNT, Montgomery–Vaughan's Brun–Titchmarsh, and Chebyshev?
2. **Theorem 8, Part 1.** The two inequalities for $\delta(k)$. Independently: compute $\delta(k)$ exactly for some $k$ (enumerate $n\bmod p^{2L}$ and test $(n-i)\mid\binom nk$ directly), compute $S(k)$, and confirm $S(k)-2\log k-1\le\log(1/\delta)\le S(k)+\sum_{p\le\sqrt k}2\log k+2\log k$.
3. **Corollary 5** (the $k-1$ lower bound), including the case $k=p^L$ and the claim that $k=4,6,14$ are the only $k\le110$ with $n_k-i_0=W'_k$.
4. **Theorem 7**: periodicity mod $p^{2L}$ (not $p^{2L-1}$; counterexample $(k,p)=(6,3)$), disjointness across $i_0$, and the closed form for $p>\sqrt k$.
5. **Values.** Pick any of the new $n_k$ and verify with big integers that exactly one index fails and it is the listed $i_0$. Minimality for $k=61,64,67$ is feasible by a direct scan in minutes with a fast valuation test.
6. **Statistics.** Recompute the 47/51 count and the $31\le k\le110$ summary from the table above and the $\log(1/\delta)$ column (interval in $x$: $[\log0.0513,\log2.996]=[-2.970,1.097]$).
7. **Reading of Cipollini's papers.** Is the explanation of the $\log\log k$ loss (symmetric windows of width $\approx e$) a fair description of his construction? Is anything in the packet inconsistent with his lemmas?
8. **Overstatement check.** Is anything above stated more strongly than the evidence supports? The intended status: items 1–3 proved; item 4 conjectural.

---

## Appendix. Reproducibility script for $\delta(k)$

The script below (written by the Fable reviewer, independent of the authors' code) computes $\delta(k)$ as an exact rational by enumerating $n\bmod p^{2L_p}$ for each prime and deciding each bad set directly from Legendre's formula on actual integers, with no use of Lemma 3 or the closed form. It also asserts the mod-$p^{2L}$ periodicity of Theorem 7 on two representatives of every residue class. Run `python3 density_exact.py 2 30`; $k\le30$ takes under a minute, $k\le110$ a few minutes. Expected: $\delta(7)=269/2520$, $\delta(11)=9803/831600$, $\delta(12)=1/1386$, and $\log(1/\delta)$ matching Part D to six decimals.

```python
#!/usr/bin/env python3
"""Independent exact-rational computation of delta(k) for Erdos #1063.

Method (deliberately NOT via Lemma 3 / the M_p - d_p formula):
  For each prime p <= k, L = floor(log_p k), m = p^(2L).  For every residue r mod m pick two
  representatives n = r + m*T (T = T1, T2, both with n >= 2k), compute
      Bad_p(n) = { 0<=i<k : v_p(n-i) > v_p(C(n,k)) }
  with v_p(C(n,k)) from Legendre's formula on actual integers, and assert the two agree
  (a direct test of the mod p^(2L) periodicity claim of Theorem 7).  Then
      Pr(E_{p,i0}) = #{ r : Bad_p subset {i0} } / m        (exact Fraction)
      delta(k)     = sum_{i0<k} prod_{p<=k} Pr(E_{p,i0})    (exact Fraction)
Prints k, log(1/delta), argmax i0, and the exact fraction for small k.
Usage: density_exact.py kmin kmax [--check-vs file1,file2]
"""
import sys, math
from fractions import Fraction

def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]

def legendre(N, p):
    s = 0
    while N:
        N //= p; s += N
    return s

def vp(x, p):
    v = 0
    while x % p == 0:
        x //= p; v += 1
    return v

def bad_set_p(n, k, p):
    c = legendre(n, p) - legendre(n - k, p) - legendre(k, p)
    r = n % p
    bad = set()
    for i in range(r, k, p):          # only n-i with i == n (mod p) are divisible by p
        if vp(n - i, p) > c:
            bad.add(i)
    return bad

def density(k, periodicity_check=True):
    ps = primes_upto(k)
    per_prime = {}
    for p in ps:
        L = 0
        while p ** (L + 1) <= k: L += 1
        m = p ** (2 * L)
        T1 = (2 * k) // m + 1
        T2 = T1 + 7919
        cnt_all = 0                      # residues with empty bad set
        cnt = [0] * k                    # residues with bad set == {i0}
        for r in range(m):
            b1 = bad_set_p(r + m * T1, k, p)
            if periodicity_check:
                b2 = bad_set_p(r + m * T2, k, p)
                assert b1 == b2, (k, p, r, b1, b2)
            if not b1:
                cnt_all += 1
            elif len(b1) == 1:
                cnt[next(iter(b1))] += 1
        per_prime[p] = [Fraction(cnt_all + cnt[i], m) for i in range(k)]
    total = Fraction(0)
    best, bestv = -1, Fraction(0)
    for i0 in range(k):
        pr = Fraction(1)
        for p in ps:
            pr *= per_prime[p][i0]
            if pr == 0: break
        total += pr
        if pr > bestv: best, bestv = i0, pr
    return total, best

if __name__ == "__main__":
    k0, k1 = int(sys.argv[1]), int(sys.argv[2])
    ref = {}
    if len(sys.argv) > 3 and sys.argv[3] == "--check-vs":
        for f in sys.argv[4].split(','):
            for line in open(f):
                t = line.split()
                if len(t) >= 3 and t[0].isdigit():
                    ref[int(t[0])] = (float(t[1]), int(t[2]))
    worst = 0.0
    for k in range(k0, k1 + 1):
        d, i0 = density(k)
        ld = math.log(d.denominator) - math.log(d.numerator)
        s = f"{k:3d} log(1/delta)={ld:.6f} argmax={i0:3d}"
        if d.denominator < 10 ** 12:
            s += f"  delta={d}"
        if k in ref:
            diff = ld - ref[k][0]
            worst = max(worst, abs(diff))
            s += f"  | model {ref[k][0]:.6f} argmax {ref[k][1]:3d}  diff={diff:+.2e} {'ARGMAX-MISMATCH' if ref[k][1] != i0 else ''}"
        print(s, flush=True)
    if ref:
        print("max |diff| in log(1/delta) vs model files:", worst)
```
