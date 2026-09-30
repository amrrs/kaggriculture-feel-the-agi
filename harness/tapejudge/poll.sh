#!/bin/bash
# poll.sh: every 5 min until 08:55 UTC, judge any new/changed bundle build (judge_bundle.sh skips SHAs already scored).
cd /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/tapejudge
while pgrep -f "judge_bundle.sh" | grep -qv $$; do sleep 20; done
while [ $(date -u +%H%M) -lt 0855 ]; do ./judge_bundle.sh; sleep 300; done
