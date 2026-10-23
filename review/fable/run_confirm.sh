#!/bin/bash
cd "$(dirname "$0")"
for k in 105 110 102 106; do
  s=$(date +%s)
  r=$(QMAX=1e13 ./mywheel $k 2>/dev/null | head -1)
  e=$(date +%s)
  echo "$r  ($((e-s))s, Mac VM, QMAX=1e13)  $(date -u +%FT%TZ)" >> mywheel_101_110_mac.out
done
