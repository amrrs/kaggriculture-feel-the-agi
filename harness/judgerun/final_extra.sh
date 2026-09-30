#!/bin/bash
# usage: final_extra.sh <tag>  -- FINAL candidate extras: 2nd seed block 17841-17864 vs V183 + v183ms, and H2H vs lx1 on 17811-17834
H=/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/judgerun; cd $H; TAG=$1
source /Users/1littlecoder/kaggriculture/.venv/bin/activate
python report.py crashok $TAG || exit 0
echo "$(date -u +%H:%M:%S) final extras $TAG" >> poll.log
python3 - <<P
import json; p='results/$TAG.meta.json'; m=json.load(open(p)); m['final']='FINAL'; json.dump(m,open(p,'w'))
P
python3 mkjobs.py $TAG V183 17841 17864 $TAG v183ms 17841 17864 $TAG lx1 17811 17834 > jobs/$TAG.final.txt
./run_jobs.sh jobs/$TAG.final.txt $TAG 32 >> poll.log 2>&1
python fresh_score.py $TAG V183 17841 17864 --base v183ms --json > results/$TAG.fV2.json
python fresh_score.py $TAG v183ms 17841 17864 --json > results/$TAG.fM2.json
python fresh_score.py $TAG lx1 17811 17834 --json > results/$TAG.fL.json
python fresh_score.py $TAG V183 17811 17864 --base v183ms --json > results/$TAG.fVall.json
python fresh_score.py $TAG v183ms 17811 17864 --json > results/$TAG.fMall.json
python report.py final $TAG
touch results/$TAG.final.done; echo "$(date -u +%H:%M:%S) final done $TAG" >> poll.log
