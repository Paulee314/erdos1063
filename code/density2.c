/* density2.c -- faster exact density for Erdos #1063 (enumerates n mod p^(L+1) only).
 * For p with L = floor(log_p k) >= 1, r = n mod p^(L+1), d = #{e<=L : r mod p^e >= k mod p^e}.
 *  d = 0                 : Bad_p empty.
 *  r < k (case A)        : element at index r has v >= L+1 (unique max). Others' valuations are
 *                          fixed by r; need v(n-r) >= M2 + d, probability p^-(max(0, M2+d-(L+1))).
 *  r >= k (case B)       : all valuations fixed by r; need unique max at i0 with M - M2 >= d.
 * density = sum_{i0} prod_p pi_p(i0).  Prints: k  log(1/density)  argmax_i0  k/log k
 * (argmax_i0 is a diagnostic only: ties/near-ties make it unstable and it differs from density1063.c; not used.)
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int isprime(int x){ if(x<2) return 0; for(int d=2;d*d<=x;d++) if(x%d==0) return 0; return 1; }
int main(int argc, char **argv) {
    int k0 = atoi(argv[1]), k1 = atoi(argv[2]), step = argc > 3 ? atoi(argv[3]) : 1;
    for (int k = k0; k <= k1; k += step) {
        double *ls = calloc(k, sizeof(double)); int *dead = calloc(k, sizeof(int));
        double *pi = malloc(k * sizeof(double));
        for (int p = 2; p <= k; p++) {
            if (!isprime(p)) continue;
            int L = 0; long long pp = 1; while (pp * p <= k) { pp *= p; L++; }
            long long pw[64]; pw[0] = 1; for (int e = 1; e <= L + 1; e++) pw[e] = pw[e-1] * p;
            long long PL1 = pw[L + 1];
            for (int i = 0; i < k; i++) pi[i] = 0;
            double all = 0;
            for (long long r = 0; r < PL1; r++) {
                int d = 0; for (int e = 1; e <= L; e++) if (r % pw[e] >= k % pw[e]) d++;
                if (d == 0) { all += 1; continue; }
                int M = -1, M2 = 0, arg = -1, ties = 0;
                for (long long i = r % p; i < k; i += p) {
                    if (i == r) continue;                    /* handled as case A element */
                    long long x = ((r - i) % PL1 + PL1) % PL1; int v = 0;
                    while (x % p == 0 && v < L + 1) { x /= p; v++; }
                    if (v > M) { if (M > M2) M2 = M; M = v; arg = (int)i; ties = 0; }
                    else if (v == M) { ties = 1; if (v > M2) M2 = v; }
                    else if (v > M2) M2 = v;
                }
                if (r < k) {                                  /* case A: index r is the unique max */
                    int others_max = (M < 0 ? 0 : M);         /* max valuation among the other elements */
                    int need = others_max + d - (L + 1);
                    pi[r] += need > 0 ? pow((double)p, -need) : 1.0;
                } else {                                      /* case B */
                    if (arg >= 0 && !ties && M - M2 >= d) pi[arg] += 1;
                }
            }
            for (int i = 0; i < k; i++) { double v = (pi[i] + all) / (double)PL1; if (v <= 0) dead[i] = 1; else ls[i] += log(v); }
        }
        double mx = -1e300; int best = -1;
        for (int i = 0; i < k; i++) if (!dead[i] && ls[i] > mx) { mx = ls[i]; best = i; }
        double s = 0; for (int i = 0; i < k; i++) if (!dead[i]) s += exp(ls[i] - mx);
        printf("%d %.6f %d %.4f\n", k, -(mx + log(s)), best, k / log((double)k));
        fflush(stdout);
        free(ls); free(dead); free(pi);
    }
    return 0;
}
