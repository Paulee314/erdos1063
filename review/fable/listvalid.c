/* listvalid.c -- print all valid n in [2k, hi) for given k (exact Legendre test + elementary prefilter). */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u64;
static int P[256], NP = 0;
static u64 leg(u64 N, u64 p){ u64 s = 0; while (N) { N /= p; s += N; } return s; }
static int nbad(u64 n, int k){
    long long i0 = -1; int nb = 0;
    for (int t = 0; t < NP; t++) { u64 p = P[t];
        u64 c = leg(n, p) - leg(n - k, p) - leg((u64)k, p);
        u64 q = 1; int over = 0; for (u64 e = 0; e < c + 1; e++) { if (q > n / p) { over = 1; break; } q *= p; }
        if (over) continue; u64 m = n / q - (n - k) / q;
        if (m >= 2) return 2;
        if (m == 1) { long long idx = (long long)(n % q); if (i0 < 0) { i0 = idx; nb = 1; } else if (i0 != idx) return 2; } }
    return nb;
}
int main(int argc, char **argv){
    int k = atoi(argv[1]); u64 hi = strtoull(argv[2], 0, 10);
    for (int x = 2; x <= k; x++) { int ok = 1; for (int d = 2; d * d <= x; d++) if (x % d == 0) { ok = 0; break; } if (ok) P[NP++] = x; }
    int LP[64], TH[64], NL = 0; for (int t = 0; t < NP; t++) if (2 * P[t] > k) { LP[NL] = P[t]; TH[NL] = k - P[t]; NL++; }
    int res[64]; u64 s = 2 * k; for (int j = 0; j < NL; j++) res[j] = (int)(s % LP[j]);
    for (u64 n = s; n < hi; n++) {
        int ptr = -1, conflict = 0;
        for (int j = 0; j < NL; j++) { int r = res[j]; if (r >= TH[j]) { if (ptr < 0) ptr = r; else if (ptr != r) { conflict = 1; break; } } }
        if (!conflict && nbad(n, k) == 1) printf("%llu\n", n);
        for (int j = 0; j < NL; j++) { if (++res[j] == LP[j]) res[j] = 0; }
    }
    return 0;
}
