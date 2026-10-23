/* wheel1063.c -- wheel-accelerated exact search for Erdos #1063 / OEIS A389360.
 *
 * Necessary conditions used to generate candidates (each proved in notes/lemmas.md):
 *  (W) For each prime p | k, write L = floor(log_p k). The bad index i0 is the unique element of
 *      the block with maximal p-adic valuation, and v_p(n - i0) >= L + v_p(k) - 1.
 *      Hence n == i0 (mod W_k), W_k = prod_{p|k} p^(L_p + v_p(k) - 1).
 *      (Corollary 5 in notes/lemmas.md proves the sharper W'_k = prod_{p^a||k} p^(a + floor(log_p(k-1))); this
 *      program deliberately uses the weaker W_k, which only enlarges the candidate set, so the search stays exhaustive.)
 *  (P) For a prime p in (k/2, k] with p not dividing k: if n mod p >= k - p then the block holds a
 *      single multiple of p, at index n mod p, and it is bad; so n mod p must be < k-p or == i0.
 * Every candidate is then tested with the exact Legendre-based test check_def (same as scan1063).
 *
 * Usage: wheel1063 k [lo] [hi]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>
typedef unsigned long long u64;
typedef unsigned __int128 u128;
static int primes[2000], np = 0;

static u64 vp_fact(u64 N, u64 p) { u64 s = 0; while (N) { N /= p; s += N; } return s; }
static int check_def(u64 n, int k, int *i0out) {
    long long i0 = -1;
    for (int t = 0; t < np; t++) {
        u64 p = primes[t];
        u64 c = vp_fact(n, p) - vp_fact(n - k, p) - vp_fact((u64)k, p);
        u64 q = 1; int over = 0;
        for (u64 e = 0; e < c + 1; e++) { if (q > n / p) { over = 1; break; } q *= p; }
        if (over || q > n) continue;
        u64 cnt = n / q - (n - k) / q;
        if (cnt >= 2) return 2;
        if (cnt == 1) { long long idx = (long long)(n % q); if (i0 < 0) i0 = idx; else if (i0 != idx) return 2; }
    }
    if (i0 < 0) return 0;
    if (i0out) *i0out = (int)i0;
    return 1;
}
static u64 mulmod(u64 a, u64 b, u64 m) { return (u64)((u128)a * b % m); }
static long long egcd_inv(long long a, long long m) { /* inverse of a mod m */
    long long g = m, x = 0, x1 = 1, a1 = a % m; if (a1 < 0) a1 += m;
    long long b = a1; long long y = 1, y0 = 0; (void)y; (void)y0;
    /* standard extended Euclid on (b, g) */
    long long old_r = b, r = g, old_s = 1, s = 0;
    while (r) { long long qq = old_r / r, tmp;
        tmp = r; r = old_r - qq * r; old_r = tmp;
        tmp = s; s = old_s - qq * s; old_s = tmp; }
    (void)x; (void)x1;
    long long inv = old_s % m; if (inv < 0) inv += m; return inv;
}

static double QMAX = 3e10, CNTMAX = 2e7;
int main(int argc, char **argv) {
    if (getenv("QMAX")) QMAX = atof(getenv("QMAX"));
    if (getenv("CNTMAX")) CNTMAX = atof(getenv("CNTMAX"));
    if (argc < 2) { fprintf(stderr, "usage: %s k [lo] [hi]\n", argv[0]); return 1; }
    int k = atoi(argv[1]);
    u64 lo = argc > 2 ? strtoull(argv[2], 0, 10) : 0, hi = argc > 3 ? strtoull(argv[3], 0, 10) : ~0ULL;
    if (lo < (u64)(2 * k)) lo = 2 * k;
    for (int x = 2; x <= k; x++) { int ok = 1; for (int d = 2; d * d <= x; d++) if (x % d == 0) { ok = 0; break; } if (ok) primes[np++] = x; }
    /* W_k */
    u64 W = 1;
    for (int t = 0; t < np; t++) { int p = primes[t]; if (k % p) continue;
        int L = 0; u64 pp = 1; while (pp * p <= (u64)k) { pp *= p; L++; }
        int v = 0; int kk = k; while (kk % p == 0) { kk /= p; v++; }
        for (int e = 0; e < L + v - 1; e++) W *= p; }
    /* large primes not dividing k, sorted by allowed fraction (k-p+1)/p ascending */
    int lp[400], nl = 0;
    for (int t = np - 1; t >= 0; t--) if (2 * primes[t] > k && k % primes[t]) lp[nl++] = primes[t];
    /* choose wheel primes: largest first until Q = W * prod <= 2^40-ish and residue count small */
    int wp[64], nw = 0; u64 Q = W; double cnt = 1;
    for (int j = 0; j < nl; j++) {
        int p = lp[j];
        if ((double)Q * p > QMAX || cnt * (k - p + 1) > CNTMAX) break;
        wp[nw++] = p; Q *= p; cnt *= (k - p + 1);
    }
    int rest[400], nr = 0; for (int j = nw; j < nl; j++) rest[nr++] = lp[j];
    fprintf(stderr, "k=%d W=%llu Q=%llu wheel primes=%d rest=%d\n", k, W, Q, nw, nr);
    /* build candidate residues mod Q for every i0, stored with their i0 */
    size_t cap = 1 << 20, ncand = 0; u64 *cr = malloc(cap * sizeof(u64)); int *ci = malloc(cap * sizeof(int));
    for (int i0 = 0; i0 < k; i0++) {
        /* residues: start with n == i0 mod W, then combine each wheel prime */
        u64 *cur = malloc(sizeof(u64)); size_t nc = 1; cur[0] = (u64)i0 % W; u64 M = W;
        for (int j = 0; j < nw; j++) {
            int p = wp[j]; int al[400], na = 0;
            for (int r = 0; r < k - p; r++) al[na++] = r;
            if (i0 >= k - p && i0 < p) al[na++] = i0;
            u64 *nxt = malloc(nc * na * sizeof(u64)); size_t nn = 0;
            u64 invM = (u64)egcd_inv((long long)(M % p), p);
            for (size_t a = 0; a < nc; a++) for (int b = 0; b < na; b++) {
                /* x == cur[a] mod M, x == al[b] mod p  ->  x = cur + M*((al - cur)*invM mod p) */
                long long d = ((long long)al[b] - (long long)(cur[a] % p)) % p; if (d < 0) d += p;
                u64 t = (u64)d * invM % p;
                nxt[nn++] = cur[a] + M * t;
            }
            free(cur); cur = nxt; nc = nn; M *= p;
        }
        for (size_t a = 0; a < nc; a++) { if (ncand == cap) { cap *= 2; cr = realloc(cr, cap * sizeof(u64)); ci = realloc(ci, cap * sizeof(int)); } cr[ncand] = cur[a]; ci[ncand] = i0; ncand++; }
        free(cur);
    }
    fprintf(stderr, "candidates per period: %zu (density %.3g)\n", ncand, (double)ncand / (double)Q);
    /* scan periods T = lo/Q .. ; within a batch of periods, parallel; take min valid */
    u64 T0 = lo / Q;
    const u64 BATCH = 2 * (u64)omp_get_max_threads();
    for (u64 tb = T0; ; tb += BATCH) {
        if ((u128)tb * Q >= hi) break;
        u64 best = ~0ULL; int bi = -1;
        #pragma omp parallel for schedule(dynamic,1) reduction(min:best)
        for (u64 tt = tb; tt < tb + BATCH; tt++) {
            u64 base = tt * Q;
            for (size_t a = 0; a < ncand; a++) {
                u64 n = base + cr[a];
                if (n < lo || n >= hi || n >= best) continue;
                int i0 = ci[a], bad = 0;
                for (int j = 0; j < nr; j++) { int p = rest[j]; int r = (int)(n % p); if (r >= k - p && r != i0) { bad = 1; break; } }
                if (bad) continue;
                int got;
                if (check_def(n, k, &got) == 1) { if (n < best) best = n; }
            }
        }
        if (best != ~0ULL) { check_def(best, k, &bi); printf("%d %llu i0=%d\n", k, best, bi); fflush(stdout); return 0; }
    }
    printf("%d none <%llu\n", k, hi);
    return 0;
}
