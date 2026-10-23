# Erdős Problem #1063 — the bad index, an exact density, and a growth conjecture

**Problem.** For $k\ge 2$ let $n_k\ge 2k$ be the least $n$ such that $n-i \mid \binom{n}{k}$ for all but exactly one $0\le i<k$. Estimate $n_k$. (OEIS A389360; Guy B31.)

**Relation to the two proof claims on the problem page** (Ricky Cipollini, using GPT-5.6 Sol; not visible on any page our tools could fetch, found from Paul's screenshot on 2026-10-22):
* *Upper bound* (submitted 2026-07-27): $\log n_k\le\frac{k}{\log k}\big(\log\log k+\log\log\log k+\log2+o(1)\big)$. Construction: $n=e+Mt$ with exceptional index $e\approx k/(2\log k\log\log k)$, $M$ a product of forced prime powers, and $t$ from a pigeonhole (simultaneous approximation) so that $n\bmod p<k\bmod p$ for the remaining large primes. Its Lemma 2 (stabilization) and Lemma 3 (one carry) are the same facts as our Lemma 3 and Lemma 6. It improves Cambie's $e^{(1+o(1))k}$ enormously.
* *Lower bound* (submitted 2026-08-04): $\log n_k\ge c(\log k)^2$ for all $k\ge3$, via Baker–Harman and Konyagin. Its Lemma 3 ($k\mid n-i_0$) and Lemma 5 are special cases of our Corollary 5 and Lemma 6. Its Lemma 4 gives $n_k\gg k^{3/2}$ for all $k$, which beats our $W'_k$ for prime $k$ (where $W'_k=k$).
* The site says appearing there is no guarantee of correctness. We read both papers. The upper-bound construction checks out at the level of a careful read; the lower-bound paper's analytic inputs we did not verify.
* So, if both claims hold: $c(\log k)^2\le\log n_k\le(1+o(1))\frac{k\log\log k}{\log k}$. Conjecture 9 ($\log n_k\sim Ck/\log k$) sits strictly between them and says the upper bound is off by a factor $\asymp\log\log k$.
* Why the construction loses that factor: for each large prime it confines $n$ to a residue window of width about $e$ (symmetric pigeonhole), at cost $\log(p/e)$ per prime, summing to $\frac{k}{\log k}(\log(k/e)-1)$. The density model's natural window is $[0,k\bmod p)$, at cost $\log\frac{p}{k\bmod p}$ per prime, summing to $S(k)\sim Ck/\log k$. Pigeonhole on differences can only produce symmetric windows, so closing the gap needs an equidistribution-type input. That is the same gap as between the heuristic and a proof of Conjecture 9.
* In the data, $\log n_k$ is $0.47$–$0.89$ (mean $0.68$) of the upper bound's main term for $31\le k\le100$.
* Our explicit $W'_k$ bound and $c(\log k)^2$ are not comparable without an explicit $c$. The data force $c\le0.74$ (from $k=19$: $\log n_{19}=0.740(\log19)^2$). With $c=0.740$, $\log W'_k$ exceeds $c(\log k)^2$ for 28 of the 80 composite $k\le110$, those with several small prime factors (e.g. $30,60,84,90,105$), is below it for the rest, and is trivial ($W'_k=k$) for prime $k$. Its merit is that it is explicit and attained ($k=4,6,14$), not that it is large.

**Relation to the forum thread** (as of 2026-10-21):
* An AI-assisted comment (GPT-5.5 Thinking) proves $n_k\ge\max\big(2k,\prod_{p^a\| k}p^{a+\lfloor\log_p(k/2)\rfloor}\big)$, and a reply suggests $k/2$ can be replaced by $k-1$. Corollary 5 below proves the $k-1$ version. It is exact for $k=4,6,14$.
* A reply observes that $n_p$ seems much smaller for prime $p$. Section 7 explains why.
* A comment in the thread reports that $n_k^{1/k}$ ranges over $[1.337,2.178]$ for $k\le37$ and that $\tfrac1k\log n_k$ does not converge. This is an empirical remark; its author is not shown on the pages we could fetch, so don't attribute it to Cambie without checking. Conjecture 9 predicts that it does converge, to $0$, like $C/\log k$. This is a conjecture, not a theorem.

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
* Checked: $W'_k\mid n_k-i_0$ for all 99 values $2\le k\le100$, and for all 143,383 valid $n$ in $[2k,2k+60000)$ with $k\le22$ (Fable review).

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

## 5. Size of the density (theorem)

**Theorem 8.** As $k\to\infty$,
$$\log\frac1{\delta(k)}=S(k)+O(\sqrt k),\qquad S(k):=\sum_{\sqrt k<p\le k,\ p\nmid k}\log\frac{p}{k\bmod p}=(C+o(1))\,\frac{k}{\log k},$$
where $C=\displaystyle\sum_{j\ge1}\frac1j\log\Big(1+\frac1j\Big)=\int_1^\infty\frac{-\log\{x\}}{x^2}\,dx=1.25774688694436963\ldots$ Hence $\log(1/\delta(k))=(C+o(1))\,k/\log k$.

The full proof is in `notes/theorem8_proof.md` (refereed by Claude Fable 5.1, 2026-10-22; verdict "correct with minor fixes", all applied). In outline:
* *Part 1*, $\log(1/\delta)=S(k)+O(\sqrt k)$: upper bound on $\delta$ from the closed form for $p>\sqrt k$ and the injectivity of $p\mapsto k\bmod p$ on primes $p>\sqrt k$; lower bound from the term $i_0=0$ with $p^{2L}\mid n$ for $p\le\sqrt k$.
* *Part 2*, $S(k)\sim Ck/\log k$: cover the primes by three classes according to $r=k\bmod p$ and $j=\lfloor k/p\rfloor$. Tiny remainders ($r\le4j$): at most $4$ primes per $j$, total $O(\sqrt k\log k)$. Middle remainders ($4j<r\le\varepsilon p$): dyadic ranges in $r$ and Brun–Titchmarsh, total $O(\varepsilon\log(1/\varepsilon))\,k/\log k$. Bulk ($r>\varepsilon p$): for $j>J$ bounded by $6\log(1/\varepsilon)\,k/(J\log k)$; for $j\le J$ the terms are a smooth bounded function of $p$ on $(k/(j+1),k/(j+\varepsilon))$, and partial summation with the de la Vallée Poussin error term gives $(1+o(1))\frac{k}{\log k}\int_{j+\varepsilon}^{j+1}\frac{-\log(x-j)}{x^2}dx$. The integral tends to $\frac1j\log(1+\frac1j)$ (integrate by parts with $v=\frac{u}{j(j+u)}$). Let $k\to\infty$, then $J\to\infty$, then $\varepsilon\to0$.

*Numerics.* The approach to $C$ is very slow.
* Means of $S(k)/(k/\log k)$ over windows of 21 consecutive $k$: $1.16$ ($k\approx100$; the individual values swing between $0.99$ and $1.26$, and $S(100)$ itself gives $1.10$), $1.26$ (400), $1.32$ ($10^3$), $1.37$ ($10^4$), $1.35$ ($10^5$), $1.34$ ($10^6$), $1.33$ ($10^7$). Output is in `data/S_checks.txt` (`code/S_checks.py`); Fable's reviews agree.
* From $k\approx10^4$ on, this is fitted well by $C+c_2/\log k+c_3/\log^2k$, with $c_2=\int_1^\infty\frac{-\log\{x\}\log x}{x^2}dx=1.0016551589\ldots$ and $c_3=\int_1^\infty\frac{-\log\{x\}\log^2x}{x^2}dx=1.9954535860\ldots$ (an earlier version of this note gave $c_2=1.00108$, a truncated sum; corrected 2026-10-22 after Argon's review) At $k\approx100$ the expansion is not yet accurate.
* The small-prime part $\log(1/\delta)-S(k)$ lies between $3.2$ and $17.0$ for $31\le k\le110$, peaking at $k=102$ ($15.4$ at $k=82$, $14.35$ at $k=100$), and between $0.35\sqrt k$ and $2\sqrt k$ for all $k\le256$ checked.

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
* **Second out-of-sample test, $101\le k\le110$.** Predictions were written to `PREDICTIONS_101_110.txt` at 2026-10-22T05:00:52Z (SHA-256 `ba3bad43…`) and copied to the Mac before any search started; the first value ($k=109$) was found at 05:02:46Z, and the independent minimality confirmations followed later that day.
  * 9 of 10 inside the 90% interval. The exception is $k=105$ ($x=-3.28$, floor $-2.97$).
  * Both tests together: 47 of 51 inside, against 45.9 expected.
  * For $31\le k\le110$: mean $x_k=-0.58$ (the model's $-\gamma=-0.577$), SD $1.19$, correlation $0.988$, slope $0.985$, KS $D=0.083$ (critical value $0.152$).
  * At $k=110$, $\log n_{110}=42.95$ against the model's $42.75$ and the Cipollini upper bound's main term $62.7$.
* **Correlation.** For $31\le k\le100$, $\log n_k$ and $\log(1/\delta(k))$ have correlation $0.986$ and slope $0.995$. This is the strongest single piece of evidence. The KS non-rejections on 41–70 points are weak evidence by comparison.
* **Beyond the least element** (`data/lists/`, `code/listvalid1063.c`, `code/trajectory.py`). For $k\in\{40,45,50,61,64,67\}$ the first 139–168 admissible $n$ were enumerated. The $m$-th admissible number is close to $m/\delta$ (median of $m\delta n^{(m)}$ in $[0.90,1.22]$); the count below $X$ is within 11% of $\delta X$; gaps between consecutive failing elements $n-i_0$ have CV $0.84$–$1.02$ (exponential: 1); the observed $i_0$ frequencies match the model weights $\prod_p\Pr(E_{p,i_0})$ (top-5 predicted indices: predicted 11–30% of mass, observed 9–29%). So the model describes the whole admissible set; the least element is the noisy statistic ($n_{64}$ is 20× below $1/\delta$).
* **Structure of admissible $n$.** An admissible $n$ is in the carry-free window $n\bmod p<k\bmod p$ at all but on average $0.4$–$0.7$ of the primes $\sqrt k<p\le k$, $p\nmid k$ (94–97% of them), the exceptions being almost always primes $p>k/2$ dividing $n-i_0$. Splitting $\log n$ into per-prime "costs" ($\log\frac{p}{k\bmod p}$ for a window, $\log p$ or $2\log p$ for divisibility) gives a total within about 10% of $S(k)$. Any construction matching the conjecture must hit the one-sided window at essentially every large prime.
* **Small $k$.** For $k\le30$ admissible $n$ cluster around a shared failing element (e.g. $n_{30}=37584001$ and $37584002$, both with $n-i_0=37584000$; at $k=18$, 14% of gaps equal 1). This fits the worse fit at small $k$; for $k\ge40$ clusters are rare (3 pairs among 150 at $k=50$, none at the other five $k$).
* **Checks.** Lemma 3 was checked against exact big-integer divisibility with no mismatches: on more than 128,000 pairs $(k,n)$ by an independent referee implementation, on 6,000 random pairs with $n\le10^{18}$ (Fable), and on 20,000 random pairs by ours.

## 8. New values and how they were computed

* Each new $n_k$ ($60\le k\le100$) comes from an exhaustive search using necessary conditions from Corollary 5 ($n\equiv i_0 \pmod{W_k}$) and Lemma 6 (large primes), with the exact Legendre test on every candidate.
* Each value is verified with exact big integers: exactly one $n-i$ fails, at the reported index.
* Minimality has three independent confirmations:
  * Our plain scan (`scan1063.c`, which does not use Corollary 5 or the wheel) reproduced $k=61,62,64,67,71,73$; the run log is in `results/plain_scan_log.txt`.
  * Fable's independently written wheel (`mywheel.c`, using the sharpened $W'_k$) reproduced all 41 values for $60\le k\le100$, and all 10 values for $101\le k\le110$ (six in the cloud container; $k=102,105,106,110$ on the Mac in chunks, using `mywheel_chunked.c`, which differs from Fable's file only by a lower-bound argument; diff kept).
  * Fable's plain scan reproduced $k=61,64,67,71,73$, and its $W'$-stepping search reproduced $k=60,62,63,65,66,68,69,70,72,74$.
  * Fable's outputs are in `review/fable/`.
* The same search reproduces all 58 b-file values for $k\le59$, and an independent brute force reproduces $k\le30$.
