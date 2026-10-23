/* period_bf.c -- count n in a full period [N0, N0+D) with exactly one bad index, k given.
 * Bad index test: Lemma 1 + Legendre only (i bad iff v_p(n-i) > v_p(C(n,k)) for some prime p<=k),
 * implemented by counting multiples of p^(c+1) in the block, c = v_p(C(n,k)).
 * Prints k D count. */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u64;
static u64 leg(u64 N, u64 p){ u64 s=0; while(N){ N/=p; s+=N; } return s; }
int main(int argc, char **argv){
    int k = atoi(argv[1]);
    int ps[64], np=0;
    for(int x=2;x<=k;x++){ int ok=1; for(int d=2;d*d<=x;d++) if(x%d==0){ok=0;break;} if(ok) ps[np++]=x; }
    u64 D=1;
    for(int t=0;t<np;t++){ u64 p=ps[t]; int L=0; u64 q=1; while(q*p<=(u64)k){q*=p;L++;} for(int e=0;e<2*L;e++) D*=p; }
    u64 N0 = 2*k, cnt=0;
    for(u64 n=N0; n<N0+D; n++){
        long long i0=-1; int nb=0;
        for(int t=0;t<np && nb<2;t++){
            u64 p=ps[t];
            u64 c = leg(n,p)-leg(n-k,p)-leg(k,p);
            u64 q=1; int over=0;
            for(u64 e=0;e<c+1;e++){ if(q>n/p){over=1;break;} q*=p; }
            if(over) continue;
            u64 m = n/q - (n-k)/q;           /* multiples of p^(c+1) in (n-k, n] */
            if(m>=2){ nb=2; break; }
            if(m==1){ long long idx=(long long)(n%q); if(i0<0){i0=idx; nb=1;} else if(i0!=idx){nb=2;} }
        }
        if(nb==1) cnt++;
    }
    printf("k=%d D=%llu count=%llu\n", k, D, cnt);
    return 0;
}
