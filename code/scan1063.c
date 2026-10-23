/* scan1063.c -- exhaustive scan for Erdos #1063 / OEIS A389360.
 * n_k = least n >= 2k such that (n-i) | C(n,k) for all but exactly one 0 <= i < k.
 *
 * Exact test (check_def): for 0<=i<k, (n-i) | C(n,k)  <=>  k! | prod_{j!=i}(n-j)
 *   <=> for every prime p <= k: v_p(n-i) <= v_p(C(n,k))   (primes p > k never obstruct).
 * v_p(C(n,k)) is computed by Legendre's formula; index i is "bad" iff p^(v_p(C)+1) | (n-i)
 * for some p <= k.  We count distinct bad indices exactly.
 *
 * Safe prefilter: for a prime p in (k/2, k], if (n mod p) >= k-p the block (n-k, n] contains
 * exactly one multiple of p, at index n mod p, and that element is bad (v_p(C) = v_p(elem)-1).
 * All such primes must therefore point at the same index; n with a conflict are rejected.
 *
 * Usage: scan1063 k lo hi   -> prints "k n" for the least valid n in [max(lo,2k), hi), or "k none <hi"
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <omp.h>

typedef unsigned long long u64;
static int primes[1000], np = 0;

static u64 vp_fact(u64 N, u64 p) { /* v_p(N!) = sum floor(N/p^e) */
    u64 s = 0; while (N) { N /= p; s += N; } return s;
}

/* returns number of distinct bad indices (0,1, or 2 meaning >=2); *i0 set if exactly 1 */
static int check_def(u64 n, int k, int *i0out) {
    long long i0 = -1;
    for (int t = 0; t < np; t++) {
        u64 p = primes[t];
        u64 c = vp_fact(n, p) - vp_fact(n - k, p) - vp_fact((u64)k, p);
        /* q = p^(c+1), stop if exceeds n */
        u64 q = 1; int over = 0;
        for (u64 e = 0; e < c + 1; e++) { if (q > n / p) { over = 1; break; } q *= p; }
        if (over || q > n) continue;              /* no multiple of q among n-k+1..n */
        u64 cnt = n / q - (n - k) / q;
        if (cnt >= 2) return 2;
        if (cnt == 1) {
            long long idx = (long long)(n % q);
            if (i0 < 0) i0 = idx; else if (i0 != idx) return 2;
        }
    }
    if (i0 < 0) return 0;
    if (i0out) *i0out = (int)i0;
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s k lo hi\n", argv[0]); return 1; }
    int k = atoi(argv[1]);
    u64 lo = strtoull(argv[2], 0, 10), hi = strtoull(argv[3], 0, 10);
    if (lo < (u64)(2 * k)) lo = 2 * k;
    for (int x = 2; x <= k; x++) { int ok = 1; for (int d = 2; d * d <= x; d++) if (x % d == 0) { ok = 0; break; } if (ok) primes[np++] = x; }
    /* large primes in (k/2, k] */
    int lp[200], nl = 0;
    for (int t = 0; t < np; t++) if (2 * primes[t] > k) lp[nl++] = primes[t];
    const u64 BLOCK = 1ULL << 26;
    for (u64 b0 = lo; b0 < hi; b0 += BLOCK) {
        u64 b1 = b0 + BLOCK < hi ? b0 + BLOCK : hi;
        u64 best = ~0ULL; int bi = -1;
        #pragma omp parallel
        {
            int nt = omp_get_num_threads(), id = omp_get_thread_num();
            u64 len = b1 - b0, s = b0 + len * id / nt, e = b0 + len * (id + 1) / nt;
            int res[200];
            for (int j = 0; j < nl; j++) res[j] = (int)(s % lp[j]);
            for (u64 n = s; n < e; n++) {
                int f = -1, bad = 0;
                for (int j = 0; j < nl; j++) {
                    int r = res[j];
                    if (r >= k - lp[j]) { if (f < 0) f = r; else if (f != r) { bad = 1; break; } }
                }
                if (!bad) {
                    int i0;
                    if (check_def(n, k, &i0) == 1) {
                        #pragma omp critical
                        { if (n < best) { best = n; bi = i0; } }
                        break;  /* first hit in this thread's range */
                    }
                }
                for (int j = 0; j < nl; j++) { if (++res[j] == lp[j]) res[j] = 0; }
            }
        }
        if (best != ~0ULL) { printf("%d %llu i0=%d\n", k, best, bi); return 0; }
    }
    printf("%d none <%llu\n", k, hi);
    return 0;
}
