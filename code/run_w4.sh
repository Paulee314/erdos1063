#!/bin/bash
# Pre-registered run (predictions: data/PREDICTIONS_111_139.txt, SHA256 c7a6cbab...d025).
# Exhaustive search from 2k upward for each k, all CPU threads. Results: results/new_111_139.txt
cd "$(dirname "$0")/.."
for k in 113 127 111 112 114 115 116 117 118 119 131 137 139 120; do
  echo "=== k=$k start $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> results/w4_run_111_139.log
  LOGSEC=300 ./code/w4_1063 $k 0 1000000000000000000000000 > results/w4_k$k.out 2>&1
  grep -v '^#' results/w4_k$k.out >> results/new_111_139.txt
  cat results/w4_k$k.out >> results/w4_run_111_139.log
  echo "=== k=$k end $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> results/w4_run_111_139.log
done
echo "ALL DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> results/w4_run_111_139.log
