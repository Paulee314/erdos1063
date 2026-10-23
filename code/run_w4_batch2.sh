#!/bin/bash
# Second batch, queued behind run_w4.sh. Predictions pre-registered in data/PREDICTIONS_121_199.txt
# (SHA256 b8183d19...2f54, committed 2e78cf0 before any of these runs).
# Larger wheel tables: QMAX=4e18, CNTMAX=2e7. Step 1 re-checks these settings on known values.
# Each run logs "searched [lo, X)" every 5 minutes, so a run that is stopped still proves n_k >= X.
cd "$(dirname "$0")/.."
while ! grep -q "ALL DONE" results/w4_run_111_139.log 2>/dev/null; do sleep 30; done
export QMAX=4e18 CNTMAX=2e7 LOGSEC=300
LOG=results/w4_run_batch2.log
echo "=== batch2 start $(date -u +%Y-%m-%dT%H:%M:%SZ) QMAX=$QMAX CNTMAX=$CNTMAX" >> $LOG
# 1. settings check on known values (must reproduce exactly)
for k in 100 101 102 103 104 105 106 107 108 109 110 113 127 131; do
  exp=$( (cat data/A389360_extended_2_110.txt; grep -v '^#' results/new_111_139.txt) | awk -v k=$k '$1==k{print $2; exit}')
  got=$(./code/w4_1063 $k 0 1000000000000000000000000 | grep -v '^#' | awk '{print $2}')
  if [ "$got" == "$exp" ]; then st=OK; else st=MISMATCH; fi
  echo "settings-check k=$k got=$got expected=$exp $st" >> $LOG
  if [ "$st" != OK ]; then echo "STOPPING: settings check failed" >> $LOG; exit 1; fi
done
# 2. new values
for k in 121 122 123 124 125 126 128 129 130 132 133 134 135 136 138 140 149 151 157 163 167 173 179 181 191 193 197 199; do
  echo "=== k=$k start $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $LOG
  ./code/w4_1063 $k 0 100000000000000000000000000 > results/w4_k$k.out 2>&1
  grep -v '^#' results/w4_k$k.out >> results/new_121_199.txt
  cat results/w4_k$k.out >> $LOG
  echo "=== k=$k end $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $LOG
done
echo "ALL DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $LOG
