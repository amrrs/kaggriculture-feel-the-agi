#!/bin/bash
# usage: run_jobs.sh <jobs.txt> <outname> [workers] [cpu_list]  -- push jobs, run detached on the pod under the global flock, pull out/<outname>/
H=/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/judgerun; read IP PORT < $H/pod.txt
E="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 -o ServerAliveInterval=15 -i $HOME/.ssh/id_ed25519 -p $PORT"
J=$1; O=$2; W=${3:-32}; CL=${4:-0-31}; BJ=$(basename $J)
for i in 1 2 3 4 5; do $E root@$IP "mkdir -p /work/jr/jobs /work/jr/out/$O" && rsync -a -e "$E" $H/jr_runq.py root@$IP:/work/jr/ && rsync -a -e "$E" $J root@$IP:/work/jr/jobs/$BJ && break; sleep 10; done
$H/remote.sh "j_${BJ%.txt}_$O" "cd /work/jr && /opt/venv/bin/python jr_runq.py jobs/$BJ out/$O $W $CL"
mkdir -p $H/out/$O; for i in 1 2 3 4 5; do rsync -a -e "$E" root@$IP:/work/jr/out/$O/ $H/out/$O/ && break; sleep 10; done
