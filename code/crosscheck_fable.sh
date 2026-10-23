#!/bin/bash
# Independent minimality check of a w4_1063 result with Fable's mywheel_chunked.c (review/fable/).
# Usage: crosscheck_fable.sh k V [chunks]   -- searches [0, V+1) in disjoint chunks, 28 processes at a time.
# Prints the least admissible n found below V+1; it must equal V.
cd "$(dirname "$0")/.."
k=$1; V=$2; C=${3:-112}
out=results/fable_xcheck_k$k.txt; : > $out
python3 - "$V" "$C" <<'PY' > results/.chunks_k$k
import sys
V=int(sys.argv[1])+1; C=int(sys.argv[2])
b=[V*i//C for i in range(C+1)]
for i in range(C): print(b[i], b[i+1])
PY
while read lo hi; do echo "$lo $hi"; done < results/.chunks_k$k | \
  xargs -P ${XP:-14} -L 1 sh -c 'r=$(./review/fable/mywheel_chunked '"$k"' $1 $0 2>/dev/null); echo "[$0,$1) $r"' >> $out
echo "k=$k chunks=$C hits:"; grep -v none $out | sort -t' ' -k3,3n
