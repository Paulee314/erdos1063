/* mywheel.c -- independent wheel search for Erdos #1063 (review implementation).
 * Necessary conditions used (all proved/verified in the review):
 *   (C5)  n == i0 (mod W'),  W' = prod_{p^a||k} p^(a+floor(log_p(k-1)))         [Corollary 5]
 *   (L6a) prime p in (k/2,k], p !| k:  n mod p < k-p, or n mod p == i0 (needs k-p <= i0 < p)   [Lemma 6, j=1]
 *   (L6b) prime p in (sqrt k, k/2], p !| k:  n mod p < k mod p, or n == i0 (mod p^2) with i0 mod p >= k mod p
 * Wheel: W' and the j=1 primes with the smallest allowed fraction, up to QMAX; the other large primes are
 * checked per candidate; survivors get the exact Legendre test (nbad).  For each i0 all candidates below the
 * running minimum are examined, so the output is the least valid n (n>=2k).
 * Usage: mywheel k [hi] [lo]   (env QMAX, default 4e11)
 * CHUNKED VARIANT: identical to Fable's mywheel.c except for an optional third argument lo; the scan for each i0
 * starts at the period containing lo and skips n < lo. Chunks [lo,hi) therefore partition the search. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
typedef unsigned long long u64; typedef unsigned __int128 u128;
static int P[256], NP = 0;
static u64 leg(u64 N, u64 p){ u64 s = 0; while (N) { N /= p; s += N; } return s; }
static int nbad(u64 n, int k, int *i0out){
    long long i0 = -1; int nb = 0;
    for (int t = 0; t < NP; t++) {
        u64 p = P[t];
        u64 c = leg(n, p) - leg(n - k, p) - leg((u64)k, p);
        u64 q = 1; int over = 0;
        for (u64 e = 0; e < c + 1; e++) { if (q > n / p) { over = 1; break; } q *= p; }
        if (over) continue;
        u64 m = n / q - (n - k) / q;
        if (m >= 2) return 2;
        if (m == 1) { long long idx = (long long)(n % q); if (i0 < 0) { i0 = idx; nb = 1; } else if (i0 != idx) return 2; }
    }
    if (nb == 1 && i0out) *i0out = (int)i0;
    return nb;
}
static u64 inv_mod(u64 a, u64 m){ /* a^{-1} mod m, gcd=1, extended Euclid */
    long long r0 = (long long)m, r1 = (long long)(a % m), s0 = 0, s1 = 1;
    while (r1) { long long q = r0 / r1, t = r0 - q * r1; r0 = r1; r1 = t; t = s0 - q * s1; s0 = s1; s1 = t; }
    if (s0 < 0) s0 += (long long)m; return (u64)s0;
}
int main(int argc, char **argv){
    int k = atoi(argv[1]); u64 HI = argc > 2 ? strtoull(argv[2], 0, 10) : ~0ULL; u64 LO = argc > 3 ? strtoull(argv[3], 0, 10) : 0;
    double QMAX = getenv("QMAX") ? atof(getenv("QMAX")) : 4e11;
    for (int x = 2; x <= k; x++) { int ok = 1; for (int d = 2; d * d <= x; d++) if (x % d == 0) { ok = 0; break; } if (ok) P[NP++] = x; }
    u64 W = 1;
    for (int t = 0; t < NP; t++) { int p = P[t]; if (k % p) continue;
        int a = 0, kk = k; while (kk % p == 0) { kk /= p; a++; }
        int f = 0; u64 q = 1; while (q * p <= (u64)(k - 1)) { q *= p; f++; }
        for (int e = 0; e < a + f; e++) W *= p; }
    /* large primes p > sqrt(k), p !| k, sorted by allowed fraction ascending (j=1 first, largest p first) */
    int big[128], nb = 0;
    for (int t = NP - 1; t >= 0; t--) { int p = P[t]; if ((u64)p * p > (u64)k && k % p) big[nb++] = p; }
    /* choose wheel primes among j==1 ones (2p>k), in order of decreasing p (smallest fraction (k-p)/p) */
    int wh[64], nw = 0, rest[128], nr = 0; u64 Q = W; double cands = 1;
    for (int t = 0; t < nb; t++) { int p = big[t];
        if (2 * p > k && (double)Q * p <= QMAX && cands * (k - p + 1) <= 1e7) { wh[nw++] = p; Q *= p; cands *= (k - p + 1); }
        else rest[nr++] = p; }
    fprintf(stderr, "k=%d W'=%llu wheel=%d primes Q=%llu rest=%d cands/i0<=%.3g\n", k, W, nw, Q, nr, cands);
    u64 best = HI; int besti = -1; u64 ntests = 0;
    #pragma omp parallel for schedule(dynamic,1) reduction(+:ntests)
    for (int i0 = 0; i0 < k; i0++) {
        /* build candidate residues mod Q for this i0 */
        size_t cap = 1 << 16, nc = 1; u64 *cur = malloc(cap * sizeof(u64)); cur[0] = (u64)i0 % W; u64 M = W;
        for (int j = 0; j < nw; j++) { int p = wh[j];
            int al[128], na = 0; for (int r = 0; r < k - p; r++) al[na++] = r;
            if (i0 >= k - p && i0 < p) al[na++] = i0;
            u64 inv = inv_mod(M % p, p);
            u64 *nxt = malloc(nc * na * sizeof(u64)); size_t nn = 0;
            for (size_t a = 0; a < nc; a++) { u64 c = cur[a], cp = c % p;
                for (int b = 0; b < na; b++) { u64 d = ((u64)al[b] + p - cp) % p; nxt[nn++] = c + M * ((d * inv) % p); } }
            free(cur); cur = nxt; nc = nn; M *= p; }
        /* scan periods */
        for (u64 t = LO / Q; ; t++) {
            u64 base = t * Q; u64 cb;
            #pragma omp atomic read
            cb = best;
            if (base >= cb) break;
            for (size_t a = 0; a < nc; a++) { u64 n = base + cur[a];
                if (n < LO || n < (u64)(2 * k) || n >= cb) continue;
                int ok = 1;
                for (int j = 0; j < nr && ok; j++) { int p = rest[j]; int r = (int)(n % p);
                    if (2 * p > k) { if (r >= k - p && r != i0) ok = 0; }
                    else { if (r >= k % p) { if (!(i0 % p >= k % p && n % ((u64)p * p) == (u64)i0)) ok = 0; } } }
                if (!ok) continue;
                int g; ntests++;
                if (nbad(n, k, &g) == 1) {
                    #pragma omp critical
                    { if (n < best) { best = n; besti = g; } }
                    #pragma omp atomic read
                    cb = best;
                } }
        }
        free(cur);
    }
    if (best < HI) printf("%d %llu i0=%d (full tests %llu)\n", k, best, besti, ntests);
    else printf("%d none <%llu (full tests %llu)\n", k, HI, ntests);
    return 0;
}
