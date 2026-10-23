/* density1063.c -- exact density of valid n for Erdos #1063.
 * V_k = { n : exactly one 0<=i<k has (n-i) not dividing C(n,k) }.
 * For a prime p <= k with L = floor(log_p k):
 *   d_p(n) = #{1<=e<=L : n mod p^e >= k mod p^e}  (non-carries in the low L digits)
 *   Bad_p(n) = {} if d_p = 0; otherwise the set of i whose v_p(n-i) > M - d_p, M = max valuation in block.
 * n is valid iff there is i0 with Bad_p(n) subset {i0} for all p (Bad is never empty: Erdos-Selfridge).
 * The events are determined by n mod p^(2L) (Theorem 7; this program enumerates mod p^(2L+1), a multiple of
 * that period, which gives the same probabilities), independent across p (CRT), and disjoint across i0, so
 *   density(V_k) = sum_{i0<k} prod_{p<=k} pi_p(i0),  pi_p(i0) = Pr_n[Bad_p(n) subset {i0}].
 * For L = 1 (p > sqrt k), with j = floor(k/p):
 *   pi_p(i0) = (k mod p)/p + [i0 mod p >= k mod p] * (j==1 ? 1/p : 1/p^2).
 * For L >= 2 we enumerate n mod p^(2L+1).
 * Output: k, log(1/density), argmax_i0 (diagnostic only: ties/near-ties make it unstable; not used anywhere).
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

static int isprime(int x){ if(x<2) return 0; for(int d=2;d*d<=x;d++) if(x%d==0) return 0; return 1; }

int main(int argc, char **argv) {
    int k0 = atoi(argv[1]), k1 = atoi(argv[2]);
    for (int k = k0; k <= k1; k++) {
        double *logpi_sum = calloc(k, sizeof(double)); /* sum over p of log pi_p(i0) */
        int zero = 0;
        int *dead = calloc(k, sizeof(int));
        for (int p = 2; p <= k; p++) {
            if (!isprime(p)) continue;
            int L = 0; long long pp = 1; while (pp * p <= k) { pp *= p; L++; }
            double *pi = calloc(k, sizeof(double));
            if (L == 1) {
                int j = k / p, km = k % p;
                for (int i0 = 0; i0 < k; i0++)
                    pi[i0] = (double)km / p + ((i0 % p) >= km ? (j == 1 ? 1.0 / p : 1.0 / ((double)p * p)) : 0.0);
            } else {
                int B = 2 * L + 1; long long PB = 1; for (int e = 0; e < B; e++) PB *= p;
                long long pw[64]; pw[0] = 1; for (int e = 1; e <= B; e++) pw[e] = pw[e-1] * p;
                long long *cnt = calloc(k, sizeof(long long)); long long cnt_all = 0;
                for (long long r = 0; r < PB; r++) {
                    int d = 0;
                    for (int e = 1; e <= L; e++) if (r % pw[e] >= k % pw[e]) d++;
                    if (d == 0) { cnt_all++; continue; }
                    /* valuations of n - i for i in [0,k), i == r mod p */
                    int M = -1, M2 = 0, arg = -1, ties = 0;
                    for (int i = (int)(r % p); i < k; i += p) {
                        long long x = ((r - i) % PB + PB) % PB; int v;
                        if (x == 0) v = B; else { v = 0; while (x % p == 0) { x /= p; v++; } }
                        if (v > M) { if (M >= 0) { if (M > M2) M2 = M; } M = v; arg = i; ties = 0; }
                        else if (v == M) { ties = 1; if (v > M2) M2 = v; }
                        else if (v > M2) M2 = v;
                    }
                    if (arg < 0) continue;            /* cannot happen: block contains multiples of p */
                    if (ties) continue;                /* two elements share the max valuation: >= 2 bad */
                    if (M >= B || M - M2 >= d) cnt[arg]++;
                }
                for (int i0 = 0; i0 < k; i0++) pi[i0] = (double)(cnt[i0] + cnt_all) / (double)PB;
                free(cnt);
            }
            for (int i0 = 0; i0 < k; i0++) { if (pi[i0] <= 0) dead[i0] = 1; else logpi_sum[i0] += log(pi[i0]); }
            free(pi);
        }
        /* density = sum_i0 exp(logpi_sum) over live i0 (log-sum-exp) */
        double mx = -1e300; for (int i0 = 0; i0 < k; i0++) if (!dead[i0] && logpi_sum[i0] > mx) mx = logpi_sum[i0];
        double s = 0; int best = -1; for (int i0 = 0; i0 < k; i0++) if (!dead[i0]) { s += exp(logpi_sum[i0] - mx); if (logpi_sum[i0] == mx) best = i0; }
        double logdens = mx + log(s);
        printf("%d %.6f %d\n", k, -logdens, best);
        free(logpi_sum); free(dead); (void)zero;
    }
    return 0;
}
