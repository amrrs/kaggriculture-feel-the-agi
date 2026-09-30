#!/bin/bash
# pull pod results: pull.sh <outsubdir>
cd /Users/1littlecoder/kaggriculture/research/claude/2900/agents/reactive_v1; mkdir -p out/$1
rsync -a -e "ssh -o StrictHostKeyChecking=accept-new -i $HOME/.ssh/id_ed25519 -p 40194" root@213.192.2.122:/work/kaggriculture/research/claude/2900/agents/reactive_v1/out/$1/ out/$1/
