#!/bin/bash
# usage: setup_pod.sh <ip> <port> <selfdestruct_seconds>   (self-destruct armed FIRST; <= 4 h)
set -e
IP=$1; PORT=$2; SD=${3:-14000}; cd /Users/1littlecoder/kaggriculture
E="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 -i $HOME/.ssh/id_ed25519 -p $PORT"
$E root@$IP 'mkdir -p /work; cat > /work/sd.sh <<"X"
sleep ${1:-14000}; export $(tr "\0" "\n" < /proc/1/environ | grep -E "^RUNPOD_(API_KEY|POD_ID)="); runpodctl remove pod "$RUNPOD_POD_ID" || curl -s -X DELETE "https://rest.runpod.io/v1/pods/$RUNPOD_POD_ID" -H "Authorization: Bearer $RUNPOD_API_KEY"
X
nohup bash /work/sd.sh '$SD' >/work/sd.log 2>&1 </dev/null & disown; echo armed; date -u; ps aux | grep -c "[s]d.sh"; tr "\0" "\n" < /proc/1/environ | grep -c "^RUNPOD_API_KEY="; command -v runpodctl'
$E root@$IP 'command -v rsync >/dev/null || (apt-get update -qq && apt-get install -y -qq rsync >/dev/null); python3 -m venv /opt/venv && /opt/venv/bin/pip install -q "kaggle-environments==1.32.7" numpy scipy 2>&1 | tail -1; ln -sf /opt/venv/bin/python /usr/local/bin/python; mkdir -p /work/kaggriculture; python -c "import kaggle_environments as k;print(\"engine\",k.__version__)"; nproc; lscpu | grep -E "Model name|Thread|Core|Socket"'
rsync -a -e "$E" --exclude='__pycache__' --exclude='out/' --relative research/claude/2900/agents/final30/tapejudge research/claude/2900/agents/micro/build/v183ms/main.py research/codex/2026-09-05/v179-gate-loader/build/dated_gate/main.py root@$IP:/work/kaggriculture/
$E root@$IP 'du -sh /work/kaggriculture'
