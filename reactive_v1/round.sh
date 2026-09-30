#!/bin/bash
# quick pinned-shop screening round: round.sh <name> '<json {tag: {P overrides}}>' [base_tag=b] [seed0=18301] [nseeds=8]
# builds from rx.py, runs every tag vs V183 both seats on the pod, prints paired margins vs the base tag (out/a holds b).
set -e
N=$1; J=$2; B=${3:-b}; S0=${4:-18301}; NS=${5:-8}
cd /Users/1littlecoder/kaggriculture/research/claude/2900/agents/reactive_v1
TAGS=$(python3 mkvar.py rx.py "$J" | awk '{print $1}' | tr '\n' ' ')
python3 mkjobs.py jobs_$N.txt $S0 $NS V183 $TAGS >/dev/null
bash push.sh
bash pod.sh "cd /work/kaggriculture/research/claude/2900/agents/reactive_v1 && /opt/venv/bin/python runq.py jobs_$N.txt out/$N 30 > out_$N.log 2>&1"
bash pull.sh $N
python3 report.py out/$N out/a out/d --base $B | grep "n=" | grep -E "^($(echo $TAGS | tr ' ' '|')|$B)@" | cut -c1-230
