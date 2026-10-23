#!/bin/bash
# Independent minimality check (Fable's mywheel_chunked) of the pre-registered k=111..119 and 127 values,
# cheapest first, run at low priority alongside the main searches.
cd "$(dirname "$0")/.."
while ! grep -q "^119 " results/new_111_139.txt 2>/dev/null; do sleep 30; done
for k in 111 112 113 114 119 115 117 116 127 118; do
  V=$(awk -v k=$k '$1==k{print $2; exit}' results/new_111_139.txt)
  echo "=== xcheck k=$k V=$V start $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> results/fable_xcheck.log
  ./code/crosscheck_fable.sh $k $V 112 >> results/fable_xcheck.log 2>&1
  echo "=== xcheck k=$k end $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> results/fable_xcheck.log
done
echo "XCHECK ALL DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> results/fable_xcheck.log
