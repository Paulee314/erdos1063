#!/bin/bash
# validate w4_1063 against the known values in data/A389360_extended_2_110.txt for k in [$1,$2]
cd "$(dirname "$0")/.."
for k in $(seq $1 $2); do
  exp=$(awk -v k=$k '$1==k{print $2}' data/A389360_extended_2_110.txt)
  s=$(date +%s)
  out=$(LOGSEC=1e9 ./code/w4_1063 $k 0 100000000000000000000 | grep -v '^#')
  t=$(( $(date +%s) - s ))
  got=$(echo "$out" | awk '{print $2}')
  if [ "$got" == "$exp" ]; then st=OK; else st=MISMATCH; fi
  echo "$k $got $exp $st ${t}s"
done
