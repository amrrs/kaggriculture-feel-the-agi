#!/bin/bash
# push the reactive_v1 dir to the pod
cd /Users/1littlecoder/kaggriculture
rsync -a -e "ssh -o StrictHostKeyChecking=accept-new -i $HOME/.ssh/id_ed25519 -p 40194" --exclude='__pycache__' --exclude='out/' --relative research/claude/2900/agents/reactive_v1 root@213.192.2.122:/work/kaggriculture/
