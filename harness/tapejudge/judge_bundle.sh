#!/bin/bash
# judge_bundle.sh: score every agents/final30/bundle/build/<b>/main.py not yet judged (or changed since: keyed by SHA-256) vs v183ms;
# appends each result block to REPORT.md. Safe to re-run (poll loop calls it).
H=/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/tapejudge; cd $H
for m in ../bundle/build/*/main.py; do
  b=$(basename $(dirname $m)); sha=$(shasum -a 256 $m | cut -c1-12); tag=b_${b}_$sha
  [ -f out/$tag.score ] && continue
  echo "== $(date -u +%H:%M) judging $m ($tag)"
  BASE=v183ms ./run_judge.sh $m $tag tapes > out/$tag.score.tmp 2>&1 && mv out/$tag.score.tmp out/$tag.score || { echo "FAILED $tag"; continue; }
  { echo; echo "### $tag  ($(date -u +%H:%M) UTC) bundle/build/$b/main.py sha256 $(shasum -a 256 $m | cut -d' ' -f1)"; echo '```'; grep -v '^  99 ' out/$tag.score; echo '```'; } >> REPORT.md
done
