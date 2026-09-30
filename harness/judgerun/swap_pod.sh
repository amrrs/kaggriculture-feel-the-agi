#!/bin/bash
# usage: swap_pod.sh <new_pod_id> <selfdestruct_s>  -- set up a replacement pod, push baselines, then switch pod.txt once no pod job is running.
H=/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/judgerun; cd $H
for i in $(seq 1 60); do r=$(bash podip.sh $1); case "$r" in *None*) sleep 5;; *) break;; esac; done; set -- $1 $2 $r; IP=$3; PORT=$4
for i in 1 2 3 4 5 6; do ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 -i ~/.ssh/id_ed25519 -p $PORT root@$IP true 2>/dev/null && break; sleep 10; done
./setup_pod.sh $IP $PORT $2
ssh -o ConnectTimeout=20 -i ~/.ssh/id_ed25519 -p $PORT root@$IP '/opt/venv/bin/python -c "import kaggle_environments as k;print(\"engine\",k.__version__)" || /opt/venv/bin/pip install -q "kaggle-environments==1.32.7" numpy scipy; /opt/venv/bin/python -c "import kaggle_environments as k;print(\"engine\",k.__version__)"'
# wait until the old pod holds no job lock, then switch
read OIP OPORT < pod.txt
until ssh -o ConnectTimeout=20 -i ~/.ssh/id_ed25519 -p $OPORT root@$OIP 'flock -n /work/job.lock true' 2>/dev/null; do sleep 10; done
echo "$IP $PORT" > pod.txt.new
IPx=$IP; PORTx=$PORT
for t in V183:/Users/1littlecoder/kaggriculture/research/codex/2026-09-05/v179-gate-loader/build/dated_gate v183ms:$H/../../micro/build/v183ms lx1:$H/../../lateexec/build/lx1; do
  ssh -o ConnectTimeout=20 -i ~/.ssh/id_ed25519 -p $PORT root@$IP "mkdir -p /work/jr/cands/${t%%:*}"
  rsync -a -e "ssh -o ConnectTimeout=20 -i $HOME/.ssh/id_ed25519 -p $PORT" --exclude='__pycache__' --exclude='*.tar.gz' "${t#*:}/" root@$IP:/work/jr/cands/${t%%:*}/
done
mv pod.txt.new pod.txt; echo "switched to $IP $PORT at $(date -u +%H:%M:%S)"
