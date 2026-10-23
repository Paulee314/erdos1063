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

(The $\zeta$-series follows by expanding $\log(1+1/j)=\sum_{m\ge1}(-1)^{m+1}/(mj^m)$ and interchanging sums. The $j=1$ term needs care because its series converges only conditionally. Write the $\zeta$-series as $\sum_m(-1)^{m+1}/m+\sum_m(-1)^{m+1}(\zeta(m+1)-1)/m$. The first sum is $\log2$, the $j=1$ term. The second converges absolutely, since $\zeta(m+1)-1\le2^{-m-1}+\int_2^\infty x^{-m-1}dx=2^{-m-1}(1+2/m)\le3\cdot2^{-m-1}$, and by Fubini it equals $\sum_{j\ge2}\frac1j\log(1+\frac1j)$.)

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
* The proof gives nothing about the rate. Numerically $S(k)/(k/\log k)$ averages $1.16$ over $k\in[90,110]$, and is $1.37$ at $k\approx10^4$ and $1.34$ at $10^6$ (`data/S_checks.txt`); the next term should be $c_2k/\log^2k$ with $c_2=\int_1^\infty-\log\{x\}\log x\,x^{-2}dx=1.0016551589\ldots$, obtainable by keeping the $\log t$ variation in the main integral.
* Numerical check of the class bounds (direct sums over primes, no model): the class $\mathcal D$ sum divided by $\varepsilon\log(1/\varepsilon)\,k/\log k$ is $2.29$, $2.08$, $2.10$, $1.97$ at $(k,\varepsilon)=(10^6,0.1)$, $(10^6,0.02)$, $(10^7,0.02)$, $(10^7,0.005)$, so the implied constant $A$ is about $2$ in practice and the $\varepsilon\log(1/\varepsilon)$ scaling is visible; the class $\mathcal T$ sum is $0.011$ and $0.004$ times $k/\log k$ at $k=10^6,10^7$.
* The density is an exact rational, so Theorem 8 is a statement about $\delta(k)$ only. It says nothing rigorous about $n_k$; that is Conjecture 9.
* A second review (Gemini 4 Argon, 2026-10-22, of the cross-check packet) found no mathematical issues and one presentational one, applied here: the displayed bound for class $\mathcal D$ is now stated before the substitution $\log u\ge\log(V/2^{m+1})$, which is only valid in the first bullet.
* Refereed by Claude Fable 5.1 on 2026-10-22 (verdict: correct with minor fixes, all applied here: the constant $4\varepsilon\log(1/\varepsilon)$ in the lower bound, the treatment of the dyadic grid via $V'$, the $p\le k$ in Lemma A, the cover wording, the half-open interval in class $\mathcal T$, BT for real intervals, and the vacuous remark about $p\mid k$). The referee also checked Part 1's two inequalities exactly, with $\delta(k)$ computed as an exact rational without Lemma 3 or the closed form, for all $k\le60$ and fifteen larger $k$ up to $256$, and checked the class decomposition numerically at $k=10^6,10^7$ (class $\mathcal D$ is about $2\,\varepsilon\log(1/\varepsilon)\,k/\log k$, so $A\approx2$ in practice).
