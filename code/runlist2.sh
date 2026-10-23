#!/bin/bash
# usage: runlist2.sh outfile percap_seconds k1 k2 ...
out=$1; cap=$2; shift 2
for k in "$@"; do
  s=$(date +%s)
  r=$(timeout $cap ./code/wheel1063 $k 2>>${out}.log)
  e=$(date +%s)
  [ -z "$r" ] && r="$k TIMEOUT"
  echo "$r  ($((e-s))s)  $(date -u +%FT%TZ)" >> $out
done
