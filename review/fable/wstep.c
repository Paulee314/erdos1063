/* wstep.c -- independent minimality check for Erdos #1063 using only Corollary 5 (proved in the
 * review) and the elementary large-prime pointer condition.  For each i0 in [0,k), every valid n with
 * bad index i0 satisfies n == i0 (mod W'), W' = prod_{p^a||k} p^(a + floor(log_p(k-1))).  We step
 * n = i0 + t*W' for t >= 1 (and n >= 2k), apply the pointer prefilter with incrementally maintained
 * residues, and run the exact Legendre test on survivors.  Reports the least valid n < hi.
 * Usage: wstep k hi */
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
typedef unsigned long long u64;
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
int main(int argc, char **argv){
    int k = atoi(argv[1]); u64 hi = strtoull(argv[2], 0, 10);
    for (int x = 2; x <= k; x++) { int ok = 1; for (int d = 2; d * d <= x; d++) if (x % d == 0) { ok = 0; break; } if (ok) P[NP++] = x; }
    u64 W = 1;
    for (int t = 0; t < NP; t++) { int p = P[t]; if (k % p) continue;
        int a = 0, kk = k; while (kk % p == 0) { kk /= p; a++; }
        int f = 0; u64 q = 1; while (q * p <= (u64)(k - 1)) { q *= p; f++; }
        for (int e = 0; e < a + f; e++) W *= p; }
    int LP[64], TH[64], NL = 0;
    for (int t = 0; t < NP; t++) if (2 * P[t] > k) { LP[NL] = P[t]; TH[NL] = k - P[t]; NL++; }
    fprintf(stderr, "k=%d W'=%llu hi=%llu candidates~%.3g\n", k, W, hi, (double)k * (double)hi / (double)W);
    u64 best = hi; int besti = -1; u64 tested = 0;
    #pragma omp parallel for schedule(dynamic,1) reduction(+:tested)
    for (int i0 = 0; i0 < k; i0++) {
        u64 n = (u64)i0 + W; while (n < (u64)(2 * k)) n += W;
        int res[64], stepr[64];
        for (int j = 0; j < NL; j++) { res[j] = (int)(n % LP[j]); stepr[j] = (int)(W % LP[j]); }
        for (;;) {
            u64 cur_best;
            #pragma omp atomic read
            cur_best = best;
            if (n >= cur_best) break;
            int ptr = -1, conflict = 0;
            for (int j = 0; j < NL; j++) { int r = res[j]; if (r >= TH[j]) { if (ptr < 0) ptr = r; else if (ptr != r) { conflict = 1; break; } } }
            if (!conflict) { int g; tested++;
                if (nbad(n, k, &g) == 1) {
                    #pragma omp critical
                    { if (n < best) { best = n; besti = g; } }
                    break; }
            }
            n += W;
            for (int j = 0; j < NL; j++) { res[j] += stepr[j]; if (res[j] >= LP[j]) res[j] -= LP[j]; }
        }
    }
    if (best < hi) printf("%d %llu i0=%d (full tests %llu)\n", k, best, besti, tested);
    else printf("%d none <%llu (full tests %llu)\n", k, hi, tested);
    return 0;
}
