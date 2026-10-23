#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u64;
int main(int argc,char**argv){int k=atoi(argv[1]);u64 X=strtoull(argv[2],0,10);
 int ps[20],np=0;for(int q=2;q<=k;q++){int ok=1;for(int d=2;d*d<=q;d++)if(q%d==0)ok=0;if(ok)ps[np++]=q;}
 u64 cnt=0;
 for(u64 n=2*k;n<X;n++){int nbad=0;
  for(int i=0;i<k && nbad<2;i++){u64 m=n-i;int bad=0;
   for(int t=0;t<np&&!bad;t++){u64 p=ps[t];int v=0;u64 x=m;while(x%p==0){x/=p;v++;} if(!v)continue;
    int T=0;u64 pa=p; while(pa<=n){ if(n%pa < (u64)k%pa) T++; if(pa>n/p)break; pa*=p;}
    if(v>T)bad=1;}
   nbad+=bad;}
  if(nbad==1)cnt++;}
 printf("k=%d X=%llu count=%llu density=%.6e\n",k,X,cnt,(double)cnt/(X-2*k));}
