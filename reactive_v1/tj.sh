#!/bin/bash
# on the pod: tape judge of build/<tag>/main.py on the 123 top-field tapes -> out/tj_<tag>/   (usage: tj.sh <tag> <workers> [cpus])
T=/work/kaggriculture/research/claude/2900/agents/final30/tapejudge
R=/work/kaggriculture/research/claude/2900/agents/reactive_v1
cd $T && /opt/venv/bin/python runq.py $R/build/$1/main.py $R/out/tj_$1 tapes $2 $3 > $R/out/tj_$1.log 2>&1
