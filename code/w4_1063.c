/* w4_1063.c -- exhaustive multi-threaded search for Erdos #1063 (OEIS A389360), 128-bit arithmetic.
 *
 * Finds the least n in [lo, hi) with exactly one 0 <= i < k such that (n - i) does not divide C(n,k).
 *
 * Necessary conditions used to generate candidates; each surviving candidate gets the exact test check_def.
 *  (D) If every n - i with i != e divides C(n,k) (and n >= 2k), then
 *        D(k,e) = prod_{p^a || k} p^(a + v_p(C(k-1,e)) + floor(log_p max(e, k-1-e)))  divides n - e,
 *      and k | D(k,e), so e = n mod k.  Formally verified in Lean 4: Erdos1063Lower.D_dvd, index_eq_mod
 *      (lean/Erdos1063Lower.lean). So for each possible failing index e we scan n == e (mod D(k,e)).
 *  (L) Let p be a prime with p^2 > k and p not dividing k; write k = j p + s, 0 < s < p, r = n mod p.
 *      If r >= s, the block n-k+1..n holds exactly j multiples of p (at indices r, r+p, ..., r+(j-1)p) and
 *      v_p C(n,k) = max_i v_p(n-i) - 1, so the multiples of maximal valuation are all bad. Hence:
 *        j = 1:  r < s, or r = e;
 *        j >= 2: r < s, or (r = e mod p and p^2 | n - e)   [j < p, so at most one of the j multiples is
 *                                                           divisible by p^2, and it must be the only bad one].
 *      (Paper, Lemma 4.1; this is the same Kummer computation.)
 * check_def is the exact Legendre-formula test, independent of (D) and (L).
 *
 * Work is split into blocks of n; each (block, e) pair is one unit. Threads take units in increasing order;
 * the answer is reported only when every unit below and in the first block with a hit has finished.
 *
 * Usage:  w4_1063 k lo hi
 * Env:    THREADS (default: all online CPUs), QMAX (1e14), CNTMAX (4e6), BLOCK (auto), LOGSEC (60)
 * Output: progress lines "# ..." and a final line "k n i0=e" or "k none [lo,hi)".
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>
typedef unsigned long long u64;
typedef unsigned int u32;
typedef unsigned __int128 u128;

static int K, primes[512], np = 0;

static u128 parse_u128(const char *s) { u128 x = 0; for (; *s >= '0' && *s <= '9'; s++) x = x * 10 + (u128)(*s - '0'); return x; }
static char *fmt_u128(u128 x, char *buf) { char t[64]; int i = 0; if (!x) { strcpy(buf, "0"); return buf; } while (x) { t[i++] = '0' + (int)(x % 10); x /= 10; } for (int j = 0; j < i; j++) buf[j] = t[i - 1 - j]; buf[i] = 0; return buf; }
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static u128 vpf(u128 N, u128 p) { u128 s = 0; while (N) { N /= p; s += N; } return s; }   /* v_p(N!) */
static int vpi(u64 x, u64 p) { int c = 0; if (!x) return 0; while (x % p == 0) { x /= p; c++; } return c; }

/* exact test: 1 iff exactly one index fails (index in *i0out); 0 if none; 2 if at least two */
static int check_def(u128 n, int k, int *i0out) {
    long long i0 = -1;
    for (int t = 0; t < np; t++) {
        u128 p = (u128)primes[t];
        u128 c = vpf(n, p) - vpf(n - k, p) - vpf((u128)k, p);        /* v_p C(n,k) */
        u128 q = 1; int over = 0;
        for (u128 z = 0; z < c + 1; z++) { if (q > n / p) { over = 1; break; } q *= p; }   /* q = p^(c+1) */
        if (over || q > n) continue;
        u128 cnt = n / q - (n - k) / q;                                /* block elements divisible by p^(c+1) */
        if (cnt >= 2) return 2;
        if (cnt == 1) { long long idx = (long long)(n % q); if (i0 < 0) i0 = idx; else if (i0 != idx) return 2; }
    }
    if (i0 < 0) return 0;
    if (i0out) *i0out = (int)i0;
    return 1;
}
static long long inv_mod(long long a, long long m) {
    long long old_r = ((a % m) + m) % m, r = m, old_s = 1, s = 0;
    while (r) { long long q = old_r / r, t; t = r; r = old_r - q * r; old_r = t; t = s; s = old_s - q * s; old_s = t; }
    long long v = old_s % m; return v < 0 ? v + m : v;
}
static int cmp_u64(const void *a, const void *b) { u64 x = *(const u64 *)a, y = *(const u64 *)b; return x < y ? -1 : x > y; }

/* filter primes (L) */
typedef struct { int p, s, j; } FP;
static FP F[512]; static int nf = 0;

/* per-e wheel */
typedef struct {
    int e; u64 D, Q; size_t nc; u64 *cur;
    int nr; u32 rp[512], rs[512], rQ[512]; int rx[512];    /* rest primes: p, s, Q mod p, extra residue or -1 */
    int nsq; u32 sqp[512], sqs[512];                        /* primes needing the p^2 test when r >= s */
    double dens;
} EW;
static EW *W;

static double QMAX = 1e14, CNTMAX = 4e6;

static void build(int e) {
    EW *w = &W[e]; w->e = e;
    u128 D = 1; int K1 = K - 1, mx = e > K1 - e ? e : K1 - e;
    for (int t = 0; t < np; t++) { int p = primes[t]; if (K % p) continue;
        int a = vpi(K, p), b = (int)(vpf(K1, p) - vpf(e, p) - vpf(K1 - e, p)), u = 0; long long pp = p;
        while (pp <= mx) { pp *= p; u++; }
        for (int z = 0; z < a + b + u; z++) D *= p; }
    if (D >= ((u128)1 << 62)) { fprintf(stderr, "D too large for e=%d\n", e); exit(3); }
    w->D = (u64)D;
    int cnt[512], ext[512], order[512];
    for (int i = 0; i < nf; i++) { int p = F[i].p, r0 = e % p;
        ext[i] = (r0 >= F[i].s && (F[i].j >= 2 || e < p)) ? r0 : -1;
        cnt[i] = F[i].s + (ext[i] >= 0); order[i] = i; }
    for (int i = 0; i < nf; i++) for (int j = i + 1; j < nf; j++) {      /* most selective first */
        int A = order[i], B = order[j];
        if ((double)cnt[B] / F[B].p < (double)cnt[A] / F[A].p) { order[i] = B; order[j] = A; } }
    int inw[512] = {0}, wl[128], nw = 0; double Q = (double)D, nc = 1;
    for (int i = 0; i < nf; i++) { int f = order[i];
        if (Q * F[f].p > QMAX || nc * cnt[f] > CNTMAX || nw >= 128) continue;
        wl[nw++] = f; inw[f] = 1; Q *= F[f].p; nc *= cnt[f]; }
    size_t n = 1; u64 *cur = malloc(sizeof(u64)); cur[0] = (u64)e; u64 M = w->D;
    for (int t = 0; t < nw; t++) { int f = wl[t], p = F[f].p;
        int al[512], na = 0; for (int r = 0; r < F[f].s; r++) al[na++] = r; if (ext[f] >= 0) al[na++] = ext[f];
        u64 *nx = malloc(n * na * sizeof(u64)); size_t m = 0; u64 inv = (u64)inv_mod((long long)(M % p), p);
        for (size_t a = 0; a < n; a++) { long long cm = (long long)(cur[a] % p);
            for (int b = 0; b < na; b++) { long long d = ((long long)al[b] - cm) % p; if (d < 0) d += p;
                nx[m++] = cur[a] + M * ((u64)d * inv % p); } }
        free(cur); cur = nx; n = m; M *= p; }
    qsort(cur, n, sizeof(u64), cmp_u64);
    w->Q = M; w->nc = n; w->cur = cur; w->dens = (double)n / (double)M;
    w->nr = 0; w->nsq = 0;
    for (int i = 0; i < nf; i++) { int f = order[i];
        if (!inw[f]) { int z = w->nr++; w->rp[z] = F[f].p; w->rs[z] = F[f].s; w->rQ[z] = (u32)(M % F[f].p); w->rx[z] = ext[f]; }
        if (F[f].j >= 2 && ext[f] >= 0) { int z = w->nsq++; w->sqp[z] = F[f].p; w->sqs[z] = F[f].s; } }
}

/* scheduling state */
#define RING 65536
typedef struct { int remaining; u128 best; int best_e; } Slot;
static Slot ring[RING];
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static u128 LO, HI, BLK; static u64 nblocks, next_unit = 0, frontier = 0, found_block = ~0ULL;
static volatile int done = 0; static u128 answer = 0; static int answer_e = -1, answer_found = 0;
static double t_start, t_lastlog; static double LOGSEC = 60; static u64 n_cand = 0, n_def = 0;

/* scan n == e (mod D) in [n0, n1) for wheel w; 1 and the least admissible n in *hit, else 0 */
static int scan(const EW *w, u128 n0, u128 n1, u128 *hit, int *hit_e, u64 *cands, u64 *defs) {
    const u64 Q = w->Q; const u64 *cur = w->cur; const size_t nc = w->nc; const int nr = w->nr;
    u128 t = n0 / Q, base = t * Q;
    u64 off = (u64)(n0 - base);
    size_t lo_i = 0, hi_i = nc; while (lo_i < hi_i) { size_t mid = (lo_i + hi_i) / 2; if (cur[mid] < off) lo_i = mid + 1; else hi_i = mid; }
    size_t a0 = lo_i;
    u32 bm[512]; for (int i = 0; i < nr; i++) bm[i] = (u32)(base % w->rp[i]);
    u64 lastchk = 0;
    while (base < n1) {
        int last = (base + Q > n1);
        u64 lim = last ? (u64)(n1 - base) : ~0ULL;
        for (size_t a = a0; a < nc; a++) {
            u64 c = cur[a];
            if (c >= lim) return 0;
            int ok = 1;
            for (int i = 0; i < nr; i++) {
                u32 p = w->rp[i], r = bm[i] + (u32)(c % p); if (r >= p) r -= p;
                if (r < w->rs[i]) continue;
                if ((int)r != w->rx[i]) { ok = 0; break; }
            }
            if (!ok) continue;
            u128 n = base + c;
            (*cands)++;
            for (int i = 0; i < w->nsq && ok; i++) { u32 p = w->sqp[i]; u32 r = (u32)(n % p);
                if (r >= w->sqs[i] && (n - (u128)w->e) % ((u128)p * p) != 0) ok = 0; }
            if (!ok) continue;
            (*defs)++;
            int got = -1;
            if (check_def(n, K, &got) == 1) {
                if (got != w->e) { char b[64]; fprintf(stderr, "WARNING: n=%s has exception %d, expected %d\n", fmt_u128(n, b), got, w->e); }
                *hit = n; *hit_e = got; return 1;
            }
        }
        a0 = 0; base += Q;
        for (int i = 0; i < nr; i++) { u32 v = bm[i] + w->rQ[i]; if (v >= w->rp[i]) v -= w->rp[i]; bm[i] = v; }
        if (done && ++lastchk) return 0;
    }
    return 0;
}

static void *worker(void *arg) {
    (void)arg;
    for (;;) {
        pthread_mutex_lock(&mu);
        if (done || next_unit >= nblocks * (u64)K || next_unit / K > found_block) { pthread_mutex_unlock(&mu); return NULL; }
        u64 u = next_unit, b = u / K; int e = (int)(u % K);
        if (b >= frontier + RING) { pthread_mutex_unlock(&mu); usleep(1000); continue; }
        next_unit++;
        pthread_mutex_unlock(&mu);
        u128 n0 = LO + (u128)b * BLK, n1 = n0 + BLK; if (n1 > HI) n1 = HI;
        u128 hit = 0; int he = -1; u64 c = 0, d = 0;
        int got = scan(&W[e], n0, n1, &hit, &he, &c, &d);
        pthread_mutex_lock(&mu);
        n_cand += c; n_def += d;
        Slot *s = &ring[b % RING];
        if (got && hit < s->best) { s->best = hit; s->best_e = he; if (b < found_block) found_block = b; }
        s->remaining--;
        while (frontier < nblocks && ring[frontier % RING].remaining == 0) {
            Slot *f = &ring[frontier % RING];
            if (f->best_e >= 0) { answer = f->best; answer_e = f->best_e; answer_found = 1; done = 1; break; }
            f->remaining = K; f->best = ~(u128)0; f->best_e = -1;
            frontier++;
            double tn = now();
            if (tn - t_lastlog >= LOGSEC) { char bb[64];
                printf("# k=%d searched [lo, %s) elapsed=%.0fs candidates=%llu exact_tests=%llu\n", K, fmt_u128(LO + (u128)frontier * BLK, bb), tn - t_start, n_cand, n_def);
                fflush(stdout); t_lastlog = tn; }
        }
        if (frontier >= nblocks) done = 1;
        pthread_mutex_unlock(&mu);
    }
}

static int next_e = 0;
static void *builder(void *arg) { (void)arg; for (;;) { pthread_mutex_lock(&mu); int e = next_e++; pthread_mutex_unlock(&mu); if (e >= K) return NULL; build(e); } }

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s k lo hi\n", argv[0]); return 1; }
    if (getenv("QMAX")) QMAX = atof(getenv("QMAX"));
    if (getenv("CNTMAX")) CNTMAX = atof(getenv("CNTMAX"));
    if (getenv("LOGSEC")) LOGSEC = atof(getenv("LOGSEC"));
    int T = getenv("THREADS") ? atoi(getenv("THREADS")) : (int)sysconf(_SC_NPROCESSORS_ONLN);
    if (T < 1) T = 1;
    K = atoi(argv[1]); LO = parse_u128(argv[2]); HI = parse_u128(argv[3]);
    if (K < 2 || K > 500) { fprintf(stderr, "k out of range\n"); return 1; }
    if (LO < (u128)(2 * K)) LO = 2 * K;
    if (HI <= LO) { printf("%d none (empty range)\n", K); return 0; }
    for (int x = 2; x <= K; x++) { int ok = 1; for (int d = 2; d * d <= x; d++) if (x % d == 0) { ok = 0; break; } if (ok) primes[np++] = x; }
    for (int t = 0; t < np; t++) { int p = primes[t]; if (p * p > K && K % p) { F[nf].p = p; F[nf].s = K % p; F[nf].j = K / p; nf++; } }
    t_start = t_lastlog = now();
    W = calloc(K, sizeof(EW));
    pthread_t th[1024]; if (T > 1024) T = 1024;
    for (int i = 0; i < T; i++) pthread_create(&th[i], NULL, builder, NULL);
    for (int i = 0; i < T; i++) pthread_join(th[i], NULL);
    double dens = 0; size_t totc = 0; u64 maxQ = 0;
    for (int e = 0; e < K; e++) { dens += W[e].dens; totc += W[e].nc; if (W[e].Q > maxQ) maxQ = W[e].Q; }
    if (getenv("BLOCK")) BLK = parse_u128(getenv("BLOCK"));
    else { double b = (double)T * 1e9 / dens; if (b < 1e6) b = 1e6; if (b > 1e30) b = 1e30; BLK = (u128)b; }
    u128 span = HI - LO; u128 nb = (span + BLK - 1) / BLK;
    if (nb > ((u128)1 << 62)) { fprintf(stderr, "too many blocks; raise BLOCK\n"); return 1; }
    nblocks = (u64)nb;
    for (int i = 0; i < RING; i++) { ring[i].remaining = K; ring[i].best = ~(u128)0; ring[i].best_e = -1; }
    { char b1[64], b2[64], b3[64];
      printf("# k=%d lo=%s hi=%s threads=%d wheels built in %.1fs: residues=%zu maxQ=%.3e density=%.3e block=%s blocks=%llu\n",
             K, fmt_u128(LO, b1), fmt_u128(HI, b2), T, now() - t_start, totc, (double)maxQ, dens, fmt_u128(BLK, b3), nblocks);
      fflush(stdout); }
    for (int i = 0; i < T; i++) pthread_create(&th[i], NULL, worker, NULL);
    for (int i = 0; i < T; i++) pthread_join(th[i], NULL);
    char b1[64], b2[64], b3[64];
    if (answer_found) printf("%d %s i0=%d\n", K, fmt_u128(answer, b1), answer_e);
    else printf("%d none [%s,%s)\n", K, fmt_u128(LO, b2), fmt_u128(HI, b3));
    printf("# k=%d finished elapsed=%.1fs candidates=%llu exact_tests=%llu\n", K, now() - t_start, n_cand, n_def);
    return 0;
}
