#!/bin/bash
# Paul's request (2026-10-23 10:42 CT): let the current k=173 run finish, then start nothing else.
# Keeps the Mac awake for the k=173 process only, records its result, and ends the queue.
cd "$(dirname "$0")/.."
PID=$(pgrep -f "code/w4_1063 173 ")
[ -z "$PID" ] && { echo "no k=173 process" >> results/w4_run_batch2.log; exit 1; }
nohup /usr/bin/caffeinate -i -w $PID > /dev/null 2>&1 &
pkill -f run_w4_batch2.sh          # the queue script; the k=173 search itself keeps running
pkill -f "caffeinate -i code/run_w4_batch2.sh"
echo "=== queue stopped $(date -u +%Y-%m-%dT%H:%M:%SZ) at Paul's request; k=173 (pid $PID) left to finish, nothing after it" >> results/w4_run_batch2.log
while kill -0 $PID 2>/dev/null; do sleep 60; done
grep -v '^#' results/w4_k173.out >> results/new_121_199.txt
cat results/w4_k173.out >> results/w4_run_batch2.log
echo "=== k=173 end $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> results/w4_run_batch2.log
echo "ALL DONE (stopped after k=173) $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> results/w4_run_batch2.log
