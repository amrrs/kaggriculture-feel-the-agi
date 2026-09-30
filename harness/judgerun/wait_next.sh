#!/bin/bash
# wait up to 540 s for a new results/*.done or a new poll.log line; print status
cd /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/judgerun
n0=$(wc -l < poll.log); end=$(( $(date +%s) + 540 ))
until [ $(wc -l < poll.log) -gt $n0 ] || [ $(date +%s) -ge $end ]; do sleep 10; done
date -u; tail -2 poll.log; tail -1 poll.heartbeat; grep "VERDICT\|CRASH" log.md | tail -1 | cut -c1-300
