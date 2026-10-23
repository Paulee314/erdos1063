# Theorem 8′: the second-order term of $S(k)$

*Written 2026-10-22 (Claude). Refereed twice on the same day, and both referees found it correct in substance. The first was an independent Claude instance with its own code, which raised eight points, all fixed. The second was Muse (Meta AI), which raised two: condition (ii) did not imply $\rho k/J>\sqrt k$, and the Step 6 tail inequality needs $J\ge4$, not $J\ge3$. Both are fixed. (Muse described itself as "Claude-family" in its review; that was a self-misidentification, since Muse is a Meta AI product.) A third referee followed the same evening: Gemini 4 Argon (Google), auditing four parts separately (2026-10-22, about \$0.08). Its verdict was "accept with minor revisions" on every part, and it independently recomputed the assembly constants. Its substantive points are applied here: explicit constants in Step 7 instead of $o(1)$; a tighter Step 6 error; a factor 2, the conditions $\log L\ge1.4$ and $A\ge1$, and $\ll_M$ in Remark 1; a rigorous divergence argument; and a note that the integrals are improper at $t=k/j$. Notation and inputs as in `theorem8_proof.md`: $p$ is prime, $\{x\}=x-\lfloor x\rfloor$, $L=\log k$, and*
$$S(k)=\sum_{\substack{\sqrt k<p\le k\\ p\nmid k}}\log\frac{p}{k\bmod p}=\sum_{\substack{\sqrt k<p\le k\\ p\nmid k}}-\log\Big\{\frac kp\Big\}.$$

Let $\varphi(x)=-\log\{x\}/x^2$ for $x\ge1$ (non-negative, integrable), and for $m\ge1$
$$c_m=\int_1^\infty\varphi(x)(\log x)^{m-1}\,dx .$$

**Theorem 8′.** For all sufficiently large $k$,
$$S(k)=C\,\frac{k}{L}+c_2\,\frac{k}{L^2}+R(k),\qquad |R(k)|\le 100\,\frac{k}{L^3},$$
with
$$C=c_1=1.25774688694436963001\ldots,\qquad c_2=\int_1^\infty\frac{-\log\{x\}\,\log x}{x^2}\,dx=1.00165515890098532865\ldots$$
Consequently (Theorem 8, part 1) $\log(1/\delta(k))=Ck/L+c_2k/L^2+O(k/L^3)$.

The threshold for "sufficiently large" is effective but astronomically large. The elementary conditions below already need $L\ge78.6$ (about $k\ge1.3\cdot10^{34}$), and Step 4 with explicit PNT constants (e.g. Trudgian 2016) needs far more. The theorem is an asymptotic statement; the numerics in Remark 2 are evidence for the expansion in Remark 1, not a test of the constant 100.

**Correction.** Earlier versions of the notes, packet and paper gave $c_2=1.0010797817$. That value was a truncated sum. The value above was computed two independent ways: piecewise quadrature over $[j,j+1]$, $j<20000$, plus an Euler–Maclaurin tail; and the closed form $c_2=\int_0^1\log u\cdot\partial_s\zeta(s,1+u)\big|_{s=2}\,du$ (Hurwitz zeta). The two agree to 20 digits. Argon flagged the discrepancy.

## Inputs

* **(PNT)** $\pi(t)=\mathrm{li}(t)+E(t)$ with $|E(t)|\le a_0\,t\,e^{-a_1\sqrt{\log t}}$ for $t\ge2$ (de la Vallée Poussin; explicit constants exist, e.g. Trudgian 2016). The letters $a_0,a_1$ are used so as not to clash with the $c_m$.
* **(BT)** For real $x\ge0$ and $y\ge2$, $\pi(x+y)-\pi(x)\le 3y/\log y$ (Montgomery–Vaughan, real-interval form as in Theorem 8).
* **(Ch)** $\vartheta(x)<x\log4$ for $x\ge1$.
* **Lemma A** (from Theorem 8): $p\mapsto k\bmod p$ is injective on primes $p\in(\sqrt k,k]$, $p\nmid k$.

## Parameters

$$J=\lfloor L^3\rfloor,\qquad \rho=\frac1{L^2\log L},\qquad R_0=\sqrt k .$$
"Sufficiently large" means that $k$ satisfies all of the following:

* (i) $\log(J+1)\le4\log L\le L/2$;
* (ii) $\sqrt k/L^3\ge2$, hence $k/(J+1)>\sqrt k$ (needed for the partition); and $\sqrt k>L^5\log L$, hence $\rho k/J=k/(L^5\log L)>\sqrt k=R_0$ (needed in Step 3). The second part does not follow from the first: at $L=20$ the first holds but $\rho k/J\approx51<\sqrt k$. It does follow from (iii), which forces $L\ge78.6$;
* (iii) $\tfrac12L-3\log L\ge L/3$;
* (iv) $$\rho\big(\log(1/\rho)+1.4\big)=\frac{2\log L+\log\log L+1.4}{L^2\log L}\le\frac3{L^2}, \tag{0}$$ which is equivalent to $\log L-\log\log L\ge1.4$;
* (v) $6L^6\log L\cdot a_0e^{-a_1\sqrt{L/2}}\le1$ (Step 4);
* (vi) $L\sqrt k\le0.1\,k/L^3$ (Step 2);
* (vii) $J\ge4$, and the tail terms of Step 6 are at most $k/L^3$.

Note that $\log(1/\rho)\le3\log L$.

## Partition of the primes

Every prime $p\in(\sqrt k,k]$ with $p\nmid k$ lies in exactly one class.

* **Z:** $p\le k/(J+1)$.

For $p>k/(J+1)$ put $j=\lfloor k/p\rfloor\in\{1,\dots,J\}$ and $r=k\bmod p=k-jp\ge1$, so that $\{k/p\}=r/p$.

* **A:** $\{k/p\}\ge\rho$.
* **N:** $\{k/p\}<\rho$ and $r<R_0$.
* **Dy:** $\{k/p\}<\rho$ and $r\ge R_0$.

Write $g(p)=-\log\{k/p\}=\log(p/r)>0$.

### Step 1 (class Z)
$g(p)\le\log p$, so $\sum_{\mathbf Z}g\le\vartheta(k/(J+1))<\log 4\cdot k/(J+1)<1.39\,k/L^3$.

### Step 2 (class N)
By Lemma A there is at most one prime for each $r<R_0$, and each has $g(p)=\log(p/r)\le L$. So $\sum_{\mathbf N}g\le L\sqrt k=o(k/L^3)$.

### Step 3 (class Dy, dyadic Brun–Titchmarsh)
Fix $j$. A Dy-prime with this $j$ has $R_0\le r<\rho p\le\rho k/j$. Let $R_i=2^iR_0$ for $0\le i\le i^*$, where $i^*$ is the largest index with $R_{i^*}<\rho k/j$; then $R_{i^*}\ge\rho k/(2j)$. A Dy-prime with $R_i\le r<2R_i$ satisfies $p=(k-r)/j\in\big((k-2R_i)/j,(k-R_i)/j\big]$, a real interval of length $y=R_i/j\ge\sqrt k/L^3\ge2$, with $\log y\ge L/2-3\log L\ge L/3$. (The index $i^*$ exists because $\rho k/j\ge\rho k/J>R_0$ by (ii). The left endpoint is positive because $k-2R_i>k-2\rho k/j\ge k(1-2\rho)>0$, as $\rho<1/2$; so (BT) applies.) By (BT) the interval contains at most $9R_i/(jL)$ primes, each with
$$g(p)=\log\frac pr\le\log\frac{k/j}{R_i}=\log\frac{k/j}{R_{i^*}}+(i^*-i)\log2\le\log\frac1\rho+(m+1)\log2,\qquad m=i^*-i .$$
Since $R_i=R_{i^*}2^{-m}<\rho k\,2^{-m}/j$, summing over $m\ge0$ (using $\sum2^{-m}=2$ and $\sum(m+1)2^{-m}=4$) gives, for this $j$,
$$\sum g\le\frac{9\rho k}{j^2L}\Big(2\log\frac1\rho+4\log2\Big)=\frac{18\rho k}{j^2L}\Big(\log\frac1\rho+2\log2\Big).$$
Summing over $j$ ($18\zeta(2)<30$) and using (0):
$$\sum_{\mathbf{Dy}}g\le30\,\rho\big(\log(1/\rho)+1.4\big)\frac kL\le90\,\frac k{L^3}.$$

### Step 4 (class A, partial summation)
For $1\le j\le J$ the A-primes with $\lfloor k/p\rfloor=j$ are exactly the primes in $U_j=\big(k/(j+1),\,k/(j+\rho)\big]$. Every prime in $U_j$ has $p\nmid k$, since $k/p\in[j+\rho,j+1)$ is not an integer, and $p>\sqrt k$, since $k/(J+1)>\sqrt k$ by (ii). On $U_j$ the function $g(t)=-\log(k/t-j)=-\log\{k/t\}$ is continuous and increasing, with limit $0$ at the open left end and value $\log(1/\rho)$ at the right end. Stieltjes integration against $\pi=\mathrm{li}+E$ gives
$$\sum_{p\in U_j}g(p)=\int_{U_j}\frac{g(t)}{\log t}\,dt+\Big[gE\Big]_{\partial U_j}-\int_{U_j}E\,dg .$$
Since $g$ is monotone with total variation $\log(1/\rho)$, the last two terms are at most $2\log(1/\rho)\max_{t\in U_j}|E(t)|\le6\log L\cdot a_0ke^{-a_1\sqrt{L/2}}$, because $t\ge k/(J+1)\ge\sqrt k$. Summed over $j\le J$, the error is at most $6L^3\log L\cdot a_0ke^{-a_1\sqrt{L/2}}\le k/L^3$ by (v).

### Step 5 (filling in the near-singular strips)
Let $V_j=\big(k/(j+\rho),\,k/j\big]$. Here and in $I$ below, the integrand $-\log\{k/t\}$ is $+\infty$ at the finitely many points $t=k/j$. These are integrable logarithmic singularities, and the integrals are understood as improper (equivalently, Lebesgue) integrals. With this convention, $U_j\cup V_j=(k/(j+1),k/j]$ and $\bigcup_{j\le J}(U_j\cup V_j)=(k/(J+1),k]$. Substituting $t=k/x$, and using $x\ge j$ and $\log(k/x)\ge L-\log(J+1)\ge L/2$,
$$\int_{V_j}\frac{-\log\{k/t\}}{\log t}dt=k\int_j^{j+\rho}\frac{-\log(x-j)}{x^2\log(k/x)}dx\le\frac{2k}{j^2L}\,\rho\big(1+\log(1/\rho)\big).$$
Summing over $j$ ($2\zeta(2)<3.3$) and using (0) gives $\sum_j\int_{V_j}\le 3.3\cdot3\,k/L^3<10\,k/L^3$. Hence
$$\sum_{\mathbf A}g=I-\theta_1\cdot10\frac k{L^3}+\theta_2\frac k{L^3},\qquad I:=\int_{k/(J+1)}^{k}\frac{-\log\{k/t\}}{\log t}\,dt,\quad \theta_1\in[0,1],\ |\theta_2|\le1 .$$

### Step 6 (the main integral)
With $t=k/x$ we get $I=k\int_1^{J+1}\varphi(x)\,\frac{dx}{L-\log x}$. For $0\le u\le\log(J+1)\le L/2$,
$$\frac1{L-u}=\frac1L+\frac u{L^2}+\frac{u^2}{L^2(L-u)},\qquad 0\le\frac{u^2}{L^2(L-u)}\le\frac{2u^2}{L^3}.$$
Hence
$$I=\frac kL\int_1^{J+1}\varphi+\frac k{L^2}\int_1^{J+1}\varphi\log x+\theta_3\,\frac{2c_3k}{L^3},\qquad\theta_3\in[0,1],\ c_3=1.99545\ldots$$
For the tails, $\int_{J+1}^\infty\varphi=\sum_{j>J}\frac1j\log(1+\frac1j)\le1/J$ (Lemma B), and $\int_{J+1}^\infty\varphi\log x\le\sum_{j>J}\log(j+1)/j^2\le\int_J^\infty\frac{\log(x+2)}{x^2}dx=\frac{\log(J+2)}J+\frac12\log\Big(1+\frac2J\Big)\le\frac{2\log J}J$. The middle step uses $\log(j+1)/j^2\le\int_{j-1}^j\log(x+2)x^{-2}dx$, and the last step holds for $J\ge4$ (it fails at $J=3$: $0.792>0.732$). These contribute at most $k/(LJ)+2k\log J/(L^2J)=o(k/L^3)$, and at most $k/L^3$ by (vii). The tails are subtracted, and the $\theta_3$ term is non-negative and at most $2c_3<3.991$. So
$$I=C\frac kL+c_2\frac k{L^2}+\theta_4\frac k{L^3},\qquad\theta_4\in[-1,4].$$

### Step 7 (assembly)
$S=\sum_{\mathbf Z}+\sum_{\mathbf N}+\sum_{\mathbf{Dy}}+\sum_{\mathbf A}$. Classes Z, N and Dy contribute between $0$ and $(1.39+0.1+90)k/L^3=91.49\,k/L^3$, using (vi) for N. Class A equals $I$ up to an error between $-11k/L^3$ and $+k/L^3$, and $I$ equals $Ck/L+c_2k/L^2$ up to an error in $[-1,4]\,k/L^3$. Therefore
$$-12\,\frac k{L^3}\ \le\ S(k)-C\frac kL-c_2\frac k{L^2}\ \le\ 97\,\frac k{L^3}$$
whenever (i)–(vii) hold. This proves Theorem 8′. $\square$

## Remarks

1. **Any order, and a closed main term.** Assume without loss of generality that $A\ge1$; the case $0<A<1$ follows from $A=1$. Run the same proof with $J=\lfloor L^A\rfloor$ and $\rho=L^{-A}$, with four changes:
   * (a) the conditions become $\sqrt k/L^A\ge2$, $L/2-A\log L\ge L/3$, $A\log L+\log2\le L/2$, $\log L\ge1.4$ and $2L^A\cdot A\log L\cdot a_0e^{-a_1\sqrt{L/2}}\le L^{-A}$;
   * (b) (0) is replaced by $\rho(\log(1/\rho)+1.4)\le(A+1)L^{-A}\log L$, so Dy and the strips are $O_A(k\log L/L^{A+1})$ and Z is at most $\log4\cdot k/L^A$;
   * (c) Step 6 is not expanded, and the integral is extended from $J+1$ to $\sqrt k$ at a cost of $k\int_{J+1}^{\sqrt k}\varphi/\log(k/x)\,dx\le(2k/L)\int_{J+1}^\infty\varphi\le2k/(LJ)=O(k/L^{A+1})$;
   * (d) for the expansion, take $A=M+1$, bound the remainder of $1/(L-\log x)$ by $2(\log x)^M/L^{M+1}$ (valid since $\log x\le L/2$ on $[1,\sqrt k]$), giving at most $2c_{M+1}k/L^{M+1}$, and note that the tails $\int_{\sqrt k}^\infty\varphi(\log x)^{m-1}\ll_M L^{m-1}/\sqrt k$ ($m\le M$) are negligible.

   The result, for every fixed $A>0$, is
$$S(k)=k\int_1^{\sqrt k}\frac{-\log\{x\}}{x^2\log(k/x)}\,dx+O_A\!\Big(\frac{k}{L^{A}}\Big),$$
and, expanding $1/(L-\log x)$ to order $M$,
$$S(k)=\frac kL\sum_{m=1}^{M}\frac{c_m}{L^{m-1}}+O_M\Big(\frac k{L^{M+1}}\Big).$$
Numerically $c_1,\dots,c_6=1.2577,\ 1.00166,\ 1.99545,\ 5.99847,\ 23.99996,\ 120.0003$, so $c_m\approx(m-1)!$ (for large $x$, $\varphi$ averages $1/x^2$ and $\int_1^\infty(\log x)^{m-1}x^{-2}dx=(m-1)!$). The series diverges and must be truncated, like the asymptotic expansion of $\mathrm{li}$. Rigorously: $-\log y\ge1-y$ on $(0,1]$ gives $c_m\ge\int_1^\infty(1-\{x\})f_m(x)\,dx$ with $f_m(x)=(\log x)^{m-1}x^{-2}$. On each $[n,n+1]$ this is at least $\tfrac12\min_{[n,n+1]}f_m$. Since $f_m$ is unimodal with maximum $((m-1)/2e)^{m-1}=o((m-1)!)$, summing gives $c_m\ge(\tfrac12-o(1))(m-1)!$. So for each fixed $L$ the terms $c_m/L^{m-1}$ are unbounded.

2. **Numerical check** (`code/S_expansion.py`, averages over 21 consecutive $k$). The column $(S/(k/L)-C-c_2/L)\,L^2$ should stay bounded and tend to $c_3+c_4/L+\dots$:

| $k$ | $S/(k/L)$ | $C+c_2/L+c_3/L^2$ | $(S/(k/L)-C-c_2/L)L^2$ (min..max) | $c_3+c_4/L+c_5/L^2+c_6/L^3$ |
|---|---|---|---|---|
| $10^4$ | 1.3674 | 1.3900 | 0.07 (−0.55..0.42) | 3.08 |
| $10^5$ | 1.3540 | 1.3598 | 1.23 (1.09..1.37) | 2.78 |
| $10^6$ | 1.3393 | 1.3407 | 1.72 (1.69..1.76) | 2.60 |
| $10^7$ | 1.3283 | 1.3276 | 2.19 (2.18..2.20) | 2.49 |
| $10^8$ | 1.3189 | 1.3180 | 2.30 (2.30..2.30) | 2.41 |

The gap between the last two columns closes (3.01, 1.54, 0.88, 0.30, 0.11). All tabulated $k$ are far below the range where the proof applies; for $k\le10^7$ even $J+1>\sqrt k$. So the table supports the expansion of Remark 1 but does not test the constant 100. An independent referee also compared $S(k)$ with Remark 1's closed main term $k\int_1^{\sqrt k}\varphi/\log(k/x)$: the difference, in units of $k/L^3$, is $-0.67,-0.62,-0.47,-0.12,-0.04$ at $k=10^4,\dots,10^8$. At $k=10^8$, with the proof's $J$ and $\rho$, the actual class sums in units of $k/L^3$ are: Z 0.04, N 1.27, Dy 3.35, strips 4.61, PNT error −0.05; the proof's bounds are 1.39, —, 90, 10, ±1. The old value $c_2=1.00108$ moves the fourth column by only $0.0006L\approx0.01$, which is why the numerics never exposed it.

3. **What this explains.** The slow approach of $S(k)/(k/L)$ to $C$ (1.37 near $10^4$, 1.32 near $10^8$) is the series $C+1.00/L+2.00/L^2+6.0/L^3+\cdots$, whose correction terms are large at computable $L$. Near $k=100$ ($L\approx4.6$) the series gives no useful approximation, and the value 1.16 observed there should not be read as evidence about the asymptotics either way.
