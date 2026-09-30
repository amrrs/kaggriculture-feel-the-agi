#!/bin/bash
# usage: push_cand.sh <tag> <dir containing main.py>  -> pod /work/jr/cands/<tag>/
H=/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/judgerun; read IP PORT < $H/pod.txt
E="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 -i $HOME/.ssh/id_ed25519 -p $PORT"
$E root@$IP "mkdir -p /work/jr/cands/$1" && rsync -a -e "$E" --exclude='__pycache__' --exclude='*.tar.gz' "$2/" root@$IP:/work/jr/cands/$1/
