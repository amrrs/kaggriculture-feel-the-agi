#!/bin/bash
# usage: judge_cand.sh <build_dir with main.py> [FINAL]  -> tag = <dirname>_<sha8>; runs crash check, fresh 17811-17834 vs V183 + v183ms,
# tape judge (123), and for FINAL also 17841-17864; writes results/<tag>.json and appends to log.md; rebuilds REPORT.md.
H=/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/judgerun; cd $H
D=$(cd "$1" && pwd); B=$(basename $D); SHA=$(shasum -a 256 $D/main.py | cut -d' ' -f1); TAG=${B}_${SHA:0:8}; FIN=$2
source /Users/1littlecoder/kaggriculture/.venv/bin/activate
mkdir -p results
if [ -f results/$TAG.done ]; then [ "$FIN" = FINAL ] && [ ! -f results/$TAG.final.done ] && exec ./final_extra.sh $TAG; exit 0; fi
echo "$(date -u +%H:%M:%S) start $TAG $D $FIN" >> poll.log
echo "{\"tag\":\"$TAG\",\"dir\":\"$D\",\"sha\":\"$SHA\",\"seen\":\"$(date -u +%H:%M)\",\"final\":\"$FIN\"}" > results/$TAG.meta.json
./push_cand.sh $TAG $D || { echo "push failed $TAG" >> poll.log; exit 1; }
# (1) crash / timeout check: 4 games vs V183 (17801-17802 both seats)
python3 mkjobs.py $TAG V183 17801 17802 > jobs/$TAG.crash.txt
./run_jobs.sh jobs/$TAG.crash.txt $TAG 4 0,2,4,6 >> poll.log 2>&1
python fresh_score.py $TAG V183 17801 17802 --base v183ms --json > results/$TAG.crash.json
if ! python report.py crashok $TAG; then python report.py crashfail $TAG; touch results/$TAG.done; exit 0; fi
# (2) fresh seeds
python3 mkjobs.py $TAG V183 17811 17834 $TAG v183ms 17811 17834 > jobs/$TAG.fresh.txt
./run_jobs.sh jobs/$TAG.fresh.txt $TAG 32 >> poll.log 2>&1
python fresh_score.py $TAG V183 17811 17834 --base v183ms --json > results/$TAG.fV.json
python fresh_score.py $TAG v183ms 17811 17834 --json > results/$TAG.fM.json
# (3) tape judge
./run_tapes.sh $TAG v183ms > results/$TAG.tapes.txt 2>&1
python report.py tapes $TAG > results/$TAG.tj.json
python report.py full $TAG
touch results/$TAG.done; echo "$(date -u +%H:%M:%S) done $TAG" >> poll.log
[ "$FIN" = FINAL ] && exec ./final_extra.sh $TAG
