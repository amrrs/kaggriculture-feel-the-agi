#!/bin/bash
# usage: remote.sh <name> "<command run on pod>"  -- runs the command detached on the pod (nohup, under /work/job.lock), polls for
# /work/jr/done/<name> every 10 s, tolerating ssh drops. Prints the command's last output line.
H=/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/judgerun; read IP PORT < $H/pod.txt
E="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 -o ServerAliveInterval=15 -o ServerAliveCountMax=4 -i $HOME/.ssh/id_ed25519 -p $PORT"
N=$1; C=$2
for i in 1 2 3 4 5; do $E root@$IP "mkdir -p /work/jr/done /work/jr/logs; rm -f /work/jr/done/$N; cat > /work/jr/logs/$N.sh <<'Y'
flock /work/job.lock bash -c '$C' > /work/jr/logs/$N.log 2>&1; touch /work/jr/done/$N
Y
nohup bash /work/jr/logs/$N.sh >/dev/null 2>&1 </dev/null & disown; echo launched" && break; sleep 10; done
until $E root@$IP "test -f /work/jr/done/$N" 2>/dev/null; do sleep 10; done
$E root@$IP "tail -1 /work/jr/logs/$N.log"
