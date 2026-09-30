#!/bin/bash
# run G generations of CMA-ES (tune.py) with rotating fresh seeds; usage: tune_loop.sh <run> <G> [seed_base=18501]
cd /Users/1littlecoder/kaggriculture/research/claude/2900/agents/reactive_v1
R=$1; G=$2; SB=${3:-18501}
for g in $(seq 0 $((G-1))); do
  python3 tune.py gen $R $((SB + 8*g)) 8 || break
done
