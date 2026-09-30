#!/bin/bash
# LOCAL driver of the full bench for one build (pod must be live; pod.sh/push.sh/pull.sh point at it).
# usage: bench.sh <tag> [seed0=18401] [nseeds=12]
#   fresh games (pinned shops, both seats): <tag> vs V183, v183ms, at12m, self  -> out/bench_<tag>/
#   baseline v183ms vs V183 on the same seeds (skipped if present)            -> out/bench_<tag>/
#   tape judge on the 123 top-field tapes (tapejudge/tj_game.py)              -> out/tj_<tag>/
set -e
T=$1; S0=${2:-18401}; N=${3:-12}; cd /Users/1littlecoder/kaggriculture/research/claude/2900/agents/reactive_v1
python3 mkjobs.py jobs_bench_$T.txt $S0 $N V183,v183ms,at12m,self $T
python3 mkjobs.py jobs_bench_base.txt $S0 $N V183 v183ms:/work/kaggriculture/research/claude/2900/agents/micro/build/v183ms/main.py
cat jobs_bench_base.txt >> jobs_bench_$T.txt
bash push.sh
R=/work/kaggriculture/research/claude/2900/agents/reactive_v1
bash pod.sh "cd $R && (bash tj.sh $T 10 &) ; /opt/venv/bin/python runq.py jobs_bench_$T.txt out/bench_$T 20 > out/bench_$T.log 2>&1; until grep -q '^done' out/tj_$T.log 2>/dev/null; do sleep 5; done; ls out/bench_$T | wc -l; ls out/tj_$T | wc -l"
bash pull.sh bench_$T; bash pull.sh tj_$T
python3 report.py out/bench_$T --base v183ms > out/bench_$T.txt; python3 tjscore.py tj_$T v183ms > out/tj_$T.txt
cat out/bench_$T.txt; head -4 out/tj_$T.txt
