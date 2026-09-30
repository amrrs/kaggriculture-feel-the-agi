#!/bin/bash
# usage: run_tapes.sh <tag> [base=v183ms]   (candidate already pushed to /work/jr/cands/<tag>/main.py) -> tj/out/<tag>/, prints score.py vs base
H=/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/judgerun; read IP PORT < $H/pod.txt
E="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 -o ServerAliveInterval=15 -i $HOME/.ssh/id_ed25519 -p $PORT"
T=/work/kaggriculture/research/claude/2900/agents/final30/tapejudge; TAG=$1
$H/remote.sh "t_$TAG" "mkdir -p /work/jr/tout/$TAG; cd $T && /opt/venv/bin/python runq.py /work/jr/cands/$TAG/main.py /work/jr/tout/$TAG tapes"
mkdir -p $H/tj/out/$TAG; for i in 1 2 3 4 5; do rsync -a -e "$E" root@$IP:/work/jr/tout/$TAG/ $H/tj/out/$TAG/ && break; sleep 10; done
source /Users/1littlecoder/kaggriculture/.venv/bin/activate
python $H/tj/score.py $TAG ${2:-v183ms}
