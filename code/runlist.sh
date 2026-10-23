#!/bin/bash
# usage: runlist.sh outfile k1 k2 ...   (runs wheel1063 sequentially, logs timing)
out=$1; shift
for k in "$@"; do
  s=$(date +%s)
  r=$(./code/wheel1063 $k 2>>${out}.log)
  e=$(date +%s)
  echo "$r  ($((e-s))s)  $(date -u +%FT%TZ)" >> $out
done
