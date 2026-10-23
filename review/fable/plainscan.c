/* plainscan.c -- fresh plain scan for Erdos #1063: least n in [max(lo,2k), hi) with exactly one
 * 0<=i<k such that (n-i) does not divide C(n,k).  Written for this review; shares no code with
 * the erdos/code directory.
 *
 * Exact test: i is bad iff for some prime p<=k, v_p(n-i) > c_p := v_p(C(n,k)) (Legendre). The bad
 * indices at p are the multiples of p^(c_p+1) in the block (n-k, n]; counted via floor division.
 *
 * Elementary prefilter (no lemma from the note needed): for a prime p with k/2 < p <= k, if
 * (n mod p) >= k-p then the block contains exactly ONE multiple of p, namely n-(n mod p); since
 * v_p(k!) = 1, v_p(C(n,k)) = v_p(that element) - 1, so index (n mod p) is bad.  (For p = k, prime k,
 * this always applies.)  Hence all such "pointers" must agree, else >= 2 bad indices.
 *
 * Usage: plainscan k lo hi   -> "k n i0=.." or "k none <hi".  Uses OpenMP (2 threads here).
 */
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
typedef unsigned long long u64;
static int P[256], NP = 0;
static u64 leg(u64 N, u64 p){ u64 s = 0; while (N) { N /= p; s += N; } return s; }

/* returns number of distinct bad indices capped at 2; sets *i0 when exactly one */
static int nbad(u64 n, int k, int *i0out){
    long long i0 = -1; int nb = 0;
    for (int t = 0; t < NP; t++) {
        u64 p = P[t];
        u64 c = leg(n, p) - leg(n - k, p) - leg((u64)k, p);
        u64 q = 1; int over = 0;
        for (u64 e = 0; e < c + 1; e++) { if (q > n / p) { over = 1; break; } q *= p; }
        if (over) continue;                        /* p^(c+1) > n: no multiple in block */
        u64 m = n / q - (n - k) / q;
        if (m >= 2) return 2;
        if (m == 1) { long long idx = (long long)(n % q); if (i0 < 0) { i0 = idx; nb = 1; } else if (i0 != idx) return 2; }
    }
    if (nb == 1 && i0out) *i0out = (int)i0;
    return nb;
}

int main(int argc, char **argv){
    if (argc < 4) { fprintf(stderr, "usage: plainscan k lo hi\n"); return 1; }
    int k = atoi(argv[1]);
    u64 lo = strtoull(argv[2], 0, 10), hi = strtoull(argv[3], 0, 10);
    if (lo < (u64)(2 * k)) lo = 2 * k;
    for (int x = 2; x <= k; x++) { int ok = 1; for (int d = 2; d * d <= x; d++) if (x % d == 0) { ok = 0; break; } if (ok) P[NP++] = x; }
    int LP[64], NL = 0, TH[64];
    for (int t = 0; t < NP; t++) if (2 * P[t] > k) { LP[NL] = P[t]; TH[NL] = k - P[t]; NL++; }   /* includes p=k if prime */
    fprintf(stderr, "k=%d primes=%d prefilter primes=%d lo=%llu hi=%llu threads=%d\n", k, NP, NL, lo, hi, omp_get_max_threads());
    const u64 BLOCK = 1ULL << 28;
    u64 tested = 0;
    for (u64 b0 = lo; b0 < hi; b0 += BLOCK) {
        u64 b1 = (b0 + BLOCK < hi) ? b0 + BLOCK : hi;
        u64 best = ~0ULL; int besti = -1; u64 tloc = 0;
        #pragma omp parallel reduction(+:tloc)
        {
            int nt = omp_get_num_threads(), id = omp_get_thread_num();
            u64 len = b1 - b0, s = b0 + (len * id) / nt, e = b0 + (len * (id + 1)) / nt;
            int res[64];
            for (int j = 0; j < NL; j++) res[j] = (int)(s % LP[j]);
            u64 found = ~0ULL; int fi = -1;
            for (u64 n = s; n < e; n++) {
                int ptr = -1, conflict = 0;
                for (int j = 0; j < NL; j++) {
                    int r = res[j];
                    if (r >= TH[j]) { if (ptr < 0) ptr = r; else if (ptr != r) { conflict = 1; break; } }
                }
                if (!conflict) {
                    int i0; tloc++;
                    if (nbad(n, k, &i0) == 1) { found = n; fi = i0; break; }
                }
                for (int j = 0; j < NL; j++) { if (++res[j] == LP[j]) res[j] = 0; }
            }
            #pragma omp critical
            { if (found < best) { best = found; besti = fi; } }
        }
        tested += tloc;
        if (best != ~0ULL) { printf("%d %llu i0=%d  (full tests: %llu)\n", k, best, besti, tested); fflush(stdout); return 0; }
    }
    printf("%d none <%llu  (full tests: %llu)\n", k, hi, tested);
    return 0;
}
