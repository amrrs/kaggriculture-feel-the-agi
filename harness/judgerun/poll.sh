#!/bin/bash
# poll.sh: every 5 min until 15:30 UTC, judge every newexec/build/<tag>/ that has JUDGE_ME (keyed by main.py SHA-256; FINAL if the
# JUDGE_ME text contains FINAL or a FINAL file exists). Candidates run one at a time, oldest JUDGE_ME first.
H=/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/judgerun; cd $H
N=/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/newexec/build
while [ $(date -u +%H%M) -lt 1530 ]; do
  for j in $(ls -tr $N/*/JUDGE_ME 2>/dev/null); do
    d=$(dirname $j); [ -f $d/main.py ] || continue
    F=; { grep -qi final $j || [ -f $d/FINAL ]; } && F=FINAL
    ./judge_cand.sh $d $F
  done
  echo "$(date -u +%H:%M:%S) poll" >> poll.heartbeat
  sleep 300
done
