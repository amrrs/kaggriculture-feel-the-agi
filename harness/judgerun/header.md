# final30/judgerun — test bench for newexec candidates (REPORT; rebuilt automatically after every result)

Pod 74b2myjnkbg5zy (cpu5c 32 vCPU AMD EPYC 4564P, 16 cores x2 SMT), created 07:59 UTC, DELETED 09:24 UTC (coordinator: all builders finished). FINAL: no candidate passed; closest ms_slot (judge +54).
Engine kaggle-environments 1.32.7 (pod venv). Fresh games: bundle/game.py via jr_runq.py (one game per taskset-pinned process, env.run with
actTimeout 1 s + overage as Kaggle, loader = kaggle get_last_callable), 32 concurrent games on 32 logical CPUs (step times are under full load).
Tape judge: tapejudge/runq.py + tj_game.py on the 123 top-12 tapes (tapes.json), scored paired vs v183ms run on this same pod.
Baselines: V183 = codex dated_gate main.py sha 80d3cfc8, v183ms = micro/build/v183ms sha cba37327, lx1 = lateexec/build/lx1 sha 8408db9d.
Poller: poll.sh every 5 min until 15:30 UTC over newexec/build/*/JUDGE_ME (keyed by main.py SHA-256). Pipeline: judge_cand.sh (+ final_extra.sh for FINAL).
Seat mirroring: deterministic agents often replay the same game with seats swapped; "distinct" counts unique (seed, own, opp reward) games.
H2H vs v183ms has baseline 0 by construction; "paired d" vs V183 = candidate margin minus v183ms's margin vs V183 on the same seed/seat.

## Pipeline verification (08:03-08:15 UTC)
- v183ms vs V183, seeds 17801-17804 both seats (8 games, 8 CPUs): 6/8 wins, +436 (se 126), 5 distinct, peak step 0.222 s, no errors.
- Tape judge rebuilt on this pod: V183 +18530 all / intact 86/123 / intact-only -1663 (identical to tapejudge's numbers);
  v183ms paired vs V183 **+679 (se 85)**, better/worse 101/22, both-intact n=84 +737 (97) — reproduces the reference +686 (85) / +747 (98).
