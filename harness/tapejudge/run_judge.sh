#!/bin/bash
# usage: run_judge.sh <candidate main.py> <tag> [set=tapes|check|all]
# Copies the candidate to the tape-judge pod, runs every tape game (one pinned process per game; runs on the pod are serialised by
# flock so two candidates never share CPUs), pulls results to out/<tag>/, prints the score vs the baseline (BASE, default v183ms).
set -e
CAND=$(cd "$(dirname "$1")" && pwd)/$(basename "$1"); TAG=$2; SET=${3:-tapes}
H=/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/tapejudge; read IP PORT < $H/pod.txt
E="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 -o ServerAliveInterval=30 -i $HOME/.ssh/id_ed25519 -p $PORT"
R=/work/kaggriculture/research/claude/2900/agents/final30/tapejudge
mkdir -p $H/out/$TAG; shasum -a 256 "$CAND" | tee $H/out/$TAG/SHA256; echo "$CAND" > $H/out/$TAG/CAND
$E root@$IP "mkdir -p $R/cands/$TAG $R/out/$TAG"
rsync -a -e "$E" "$(dirname "$CAND")/" root@$IP:$R/cands/$TAG/ --exclude='__pycache__' --exclude='*.tar.gz'
rsync -a -e "$E" $H/tj_game.py $H/runq.py $H/tape_agent.py $H/tapes.json $H/check.json root@$IP:$R/
$E root@$IP "cd $R && flock /work/tj.lock /opt/venv/bin/python runq.py $R/cands/$TAG/$(basename "$CAND") $R/out/$TAG $SET > $R/out/$TAG.log 2>&1; tail -2 $R/out/$TAG.log"
rsync -a -e "$E" root@$IP:$R/out/$TAG/ $H/out/$TAG/
source /Users/1littlecoder/kaggriculture/.venv/bin/activate
python $H/score.py $TAG ${BASE:-v183ms}
