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

## Summary (updated 09:24 UTC)
Pass bar: H2H vs v183ms >= +1k (z >= 2), >= 60% vs V183, judge paired >= +1k, worst > -15k, peak step < 0.6 s. Fresh seeds 17811-17834 both seats (48 games per pair); d = distinct games.

| candidate | seen UTC | H2H vs v183ms margin (se) | vs V183 win% / paired d vs v183ms (se) | judge paired vs v183ms (se) / both-intact | judge wins /123 | worst | peak step s | verdict |
|---|---|---|---|---|---|---|---|---|
| BASE v183ms (vs V183) 17811-34 | 08:17 | 0 by def. | 72.9% / +875 (249) margin, d39 | 0 (+679 vs V183) | 64 | -2915 | 0.383 | ref |
| BASE v183ms (vs V183) 17841-64 | 08:17 | 0 by def. | 93.8% / +1416 (340) margin, d33 | | | -8883 | 0.408 | ref |
| BASE lx1 17811-34 | 08:17 | -3182 (310) d36 | 6.2% / -3587 (433) | -5783 (311) / bi -5074 (249) | 53 | -8165 | 0.520 (tapes) | FAIL |
| BASE lx1 17841-64 | 08:17 | -4768 (264) d30 | 6.2% / -5273 (477) | | | -9083 | 0.317 | FAIL |
| farm2945_4f3ca95d | 08:19 | -18215 (1152) d30 | 0.0% / -18136 (1129) | -7347 (4604) / bi -7293 | 54 | -34032 | 0.327 | **FAIL** |
| ms_slot_80867093 | 08:40 | +572 (126) d34 | 79.2% / +457 (84) | +54 (19) / bi +56 | 64 | -2153 | 0.515 | **FAIL** |
| ms_sr_4ab225fb | 08:48 | +764 (188) d34 | 77.1% / +444 (169) | -231 (49) / bi -141 | 64 | -3188 | 0.616 | **FAIL** |
| ms_race_bb232176 | 08:52 | +108 (166) d33 | 64.6% / -194 (151) | -281 (49) / bi -205 | 64 | -2733 | 0.825 | **FAIL** |

## Log (append-only, newest last)

### Baselines — 08:20 UTC (all on pod 74b2myjnkbg5zy, 32-way load)
- v183ms vs V183, 17811-17834: n=48 (distinct 39), 72.9% win, +875 (se 249), worst -2915, peak 0.383 s. 17841-17864: n=48 (distinct 33), 93.8%, +1416 (se 340), worst -8883, peak 0.408 s.
- lx1 vs V183, 17811-17834: 6.2% win, -2712 (299); paired vs v183ms -3587 (433). 17841-17864: 6.2%, -3857 (288); paired -5273 (477).
- lx1 vs v183ms H2H: 17811-17834 -3182 (310), 2/48 wins, worst -8165; 17841-17864 -4768 (264), 0/48, worst -9083. Peak step <= 0.35 s.
- Tape judge: V183 +18530 all, intact-only -1663 (86/123); v183ms paired vs V183 +679 (85), both-intact +737 (97); lx1 paired vs v183ms **-5783 (311)**, 0/123 better, both-intact -5074 (249), wins 64 -> 53, peak 0.520 s.

### farm2945_4f3ca95d — 08:22 UTC (seen 08:19 UTC)
- path /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/outside/farm2945/main.py, sha256 4f3ca95dd12d9a94b03339999d8803c155f450a8d3956636f050643301fcc5dd
- crash check (4 games vs V183, 17801-17802): OK, margins -13324 avg, peak 0.080 s
- H2H vs v183ms (seeds 17811-17834 both seats): n=48 (distinct 30), W/D/L 0/0/48 = **0.0%**, margin **-18215** (se 1152, z -15.8; se over seed-means 1646), worst -33930 at seed/seat [17818, 0], peak step 0.207 s, max p99 0.008 s, steps>0.6 s 0, errors 0, non-DONE 0
  - revenue own/opp per game: carrot 6.2/7.0k, egg 4.4/15.9k, fertilizer 14.2/20.2k, melon 15.9/12.3k, milk 13.0/12.6k, strawberry 26.0/28.1k, tomato 1.8/3.1k, wheat 28.1/44.7k, wool 19.4/21.1k
- vs V183 (seeds 17811-17834 both seats): n=48 (distinct 24), W/D/L 0/0/48 = **0.0%**, margin **-17262** (se 1137, z -15.2; se over seed-means 1625), worst -34032 at seed/seat [17818, 0], peak step 0.225 s, max p99 0.009 s, steps>0.6 s 0, errors 0, non-DONE 0
  - paired d vs v183ms's own games vs V183 (same seed/seat): **-18136** (se 1129, z -16.1), better/worse 0/48; v183ms there: 72.9% / +875
  - revenue own/opp per game: carrot 6.2/7.2k, egg 4.4/15.8k, fertilizer 14.1/20.2k, melon 15.9/12.3k, milk 12.8/12.6k, strawberry 25.2/26.8k, tomato 2.5/3.7k, wheat 28.2/44.2k, wool 20.3/21.7k
  - revenue delta vs v183ms own/opp: carrot -695/+529, egg -7945/+3537, fertilizer -5002/+1212, melon +1884/-1623, milk -1658/-1775, strawberry -1279/+658, tomato -852/+280, wheat -14167/+2236, wool -2234/-949
- tape judge (n=123): paired vs v183ms **-7347** (se 4604), better/worse 41/82, wins 64->54; both-intact n=68 **-7293** (se 2594); intact 82/123 (v183ms 84), intact-only margin -10831 (se 2052) wins 16; peak step 0.327 s, steps>0.6 0, non-DONE 0
- **VERDICT: FAIL** — MISS h2h vs v183ms -18215 (z -15.8) >= +1k & z>=2; MISS vs V183 0.0% >= 60%; MISS judge paired -7347 >= +1k; MISS worst -34032 > -15k; ok peak 0.327 s < 0.6
- farm2945 notes (08:25 UTC): loader verified = Kaggle's get_last_callable (file ends `agent = globals().pop('agent')`, so the picked callable is the final
  `def agent` at line 5629); 0 stderr lines, 0 non-DONE in 4+96+123 games, ~3 ms mean step (p99 <= 0.009 s), so the losses are not a load/timeout artefact.
  v183ms vs farm2945 direct H2H = the H2H row above with the sign flipped: v183ms +18215/game, 48/48 wins. The deficit is mostly wheat (-14.2k own revenue
  vs v183ms's games) and eggs (-7.9k); it sells MORE melon. Its 2944.7 rating is from the 19 Sep field; against V183/v183ms it is not competitive offline.
  Its file header reads "v9/3" (the coordinator's note says v9/4) - sha256 4f3ca95d... is what was judged.

### ms_slot_80867093 — 08:43 UTC (seen 08:40 UTC)
- path /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/newexec/build/ms_slot/main.py, sha256 808670930fa213124feaa144f112748d3289c5349fd2859429a828e92f4da043
- crash check (4 games vs V183, 17801-17802): OK, margins +448 avg, peak 0.257 s
- H2H vs v183ms (seeds 17811-17834 both seats): n=48 (distinct 34), W/D/L 41/0/7 = **85.4%**, margin **+572** (se 126, z 4.5; se over seed-means 143), worst -1780 at seed/seat [17832, 1], peak step 0.393 s, max p99 0.265 s, steps>0.6 s 0, errors 0, non-DONE 0
  - revenue own/opp per game: carrot 6.0/6.0k, egg 12.4/12.4k, fertilizer 19.0/19.1k, melon 14.1/13.7k, milk 15.8/15.8k, strawberry 26.5/26.4k, tomato 3.8/3.6k, wheat 42.7/42.7k, wool 22.3/22.3k
- vs V183 (seeds 17811-17834 both seats): n=48 (distinct 39), W/D/L 38/0/10 = **79.2%**, margin **+1332** (se 246, z 5.4; se over seed-means 334), worst -2153 at seed/seat [17815, 0], peak step 0.515 s, max p99 0.237 s, steps>0.6 s 0, errors 0, non-DONE 0
  - paired d vs v183ms's own games vs V183 (same seed/seat): **+457** (se 84, z 5.4), better/worse 42/6; v183ms there: 72.9% / +875
  - revenue own/opp per game: carrot 6.9/6.7k, egg 12.4/12.2k, fertilizer 19.1/19.0k, melon 14.1/13.7k, milk 14.4/14.4k, strawberry 26.5/26.0k, tomato 3.4/3.5k, wheat 42.3/42.0k, wool 22.5/22.6k
  - revenue delta vs v183ms own/opp: carrot +8/-10, egg +7/-7, fertilizer -30/+29, melon +175/-199, milk -9/+4, strawberry +6/-109, tomato +11/-9, wheat -5/+3, wool -37/-1
- tape judge (n=123): paired vs v183ms **+54** (se 19), better/worse 75/45, wins 64->64; both-intact n=84 **+56** (se 27); intact 84/123 (v183ms 84), intact-only margin -1891 (se 1692) wins 28; peak step 0.426 s, steps>0.6 0, non-DONE 0
- **VERDICT: FAIL** — MISS h2h vs v183ms +572 (z 4.5) >= +1k & z>=2; ok vs V183 79.2% >= 60%; MISS judge paired +54 >= +1k; ok worst -2153 > -15k; ok peak 0.515 s < 0.6

### ms_sr_4ab225fb — 08:52 UTC (seen 08:48 UTC)
- path /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/newexec/build/ms_sr/main.py, sha256 4ab225fbaadbb5afe3278c776696807d8f3b7c2c2d474579ff20fd71458f8b8c
- crash check (4 games vs V183, 17801-17802): OK, margins +610 avg, peak 0.187 s
- H2H vs v183ms (seeds 17811-17834 both seats): n=48 (distinct 34), W/D/L 42/0/6 = **87.5%**, margin **+764** (se 188, z 4.1; se over seed-means 256), worst -3188 at seed/seat [17831, 0], peak step 0.393 s, max p99 0.268 s, steps>0.6 s 0, errors 0, non-DONE 0
  - revenue own/opp per game: carrot 6.0/6.0k, egg 12.4/12.4k, fertilizer 19.0/19.1k, melon 14.1/13.7k, milk 15.8/15.9k, strawberry 26.7/26.2k, tomato 3.7/3.6k, wheat 42.7/42.8k, wool 22.3/22.3k
- vs V183 (seeds 17811-17834 both seats): n=48 (distinct 35), W/D/L 37/0/11 = **77.1%**, margin **+1319** (se 246, z 5.4; se over seed-means 347), worst -2116 at seed/seat [17820, 0], peak step 0.382 s, max p99 0.207 s, steps>0.6 s 0, errors 0, non-DONE 0
  - paired d vs v183ms's own games vs V183 (same seed/seat): **+444** (se 169, z 2.6), better/worse 36/12; v183ms there: 72.9% / +875
  - revenue own/opp per game: carrot 6.9/6.7k, egg 12.4/12.2k, fertilizer 19.1/19.0k, melon 14.1/13.7k, milk 14.4/14.3k, strawberry 26.5/26.0k, tomato 3.3/3.4k, wheat 42.3/42.0k, wool 22.4/22.6k
  - revenue delta vs v183ms own/opp: carrot +28/+13, egg +28/-12, fertilizer -60/+28, melon +172/-199, milk -62/-94, strawberry -7/-106, tomato -69/-99, wheat -5/-22, wool -82/-14
- tape judge (n=123): paired vs v183ms **-231** (se 49), better/worse 39/84, wins 64->64; both-intact n=84 **-141** (se 45); intact 84/123 (v183ms 84), intact-only margin -2089 (se 1678) wins 28; peak step 0.616 s, steps>0.6 1, non-DONE 0
- **VERDICT: FAIL** — MISS h2h vs v183ms +764 (z 4.1) >= +1k & z>=2; ok vs V183 77.1% >= 60%; MISS judge paired -231 >= +1k; ok worst -3188 > -15k; MISS peak 0.616 s < 0.6

### ms_race_bb232176 — 08:55 UTC (seen 08:52 UTC)
- path /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/newexec/build/ms_race/main.py, sha256 bb232176b070f32eef1639f979b975355827f748aecbb28548388acb3b3b733a
- crash check (4 games vs V183, 17801-17802): OK, margins -222 avg, peak 0.189 s
- H2H vs v183ms (seeds 17811-17834 both seats): n=48 (distinct 33), W/D/L 32/0/16 = **66.7%**, margin **+108** (se 166, z 0.7; se over seed-means 211), worst -2733 at seed/seat [17831, 0], peak step 0.825 s, max p99 0.261 s, steps>0.6 s 1, errors 0, non-DONE 0
  - revenue own/opp per game: carrot 6.0/6.0k, egg 12.4/12.4k, fertilizer 19.0/19.1k, melon 13.9/14.0k, milk 15.8/15.9k, strawberry 26.7/26.3k, tomato 3.7/3.6k, wheat 42.7/42.8k, wool 22.3/22.3k
- vs V183 (seeds 17811-17834 both seats): n=48 (distinct 35), W/D/L 31/0/17 = **64.6%**, margin **+681** (se 244, z 2.8; se over seed-means 345), worst -2674 at seed/seat [17812, 0], peak step 0.384 s, max p99 0.240 s, steps>0.6 s 0, errors 0, non-DONE 0
  - paired d vs v183ms's own games vs V183 (same seed/seat): **-194** (se 151, z -1.3), better/worse 22/26; v183ms there: 72.9% / +875
  - revenue own/opp per game: carrot 6.9/6.7k, egg 12.4/12.2k, fertilizer 19.1/19.0k, melon 13.9/13.9k, milk 14.4/14.3k, strawberry 26.4/26.1k, tomato 3.3/3.4k, wheat 42.3/42.0k, wool 22.5/22.6k
  - revenue delta vs v183ms own/opp: carrot +9/+29, egg +24/-6, fertilizer -40/+8, melon -51/+40, milk -53/-85, strawberry -74/-36, tomato -74/-93, wheat -5/-9, wool -72/-10
- tape judge (n=123): paired vs v183ms **-281** (se 49), better/worse 21/94, wins 64->64; both-intact n=84 **-205** (se 43); intact 84/123 (v183ms 84), intact-only margin -2152 (se 1680) wins 28; peak step 0.432 s, steps>0.6 0, non-DONE 0
- **VERDICT: FAIL** — MISS h2h vs v183ms +108 (z 0.7) >= +1k & z>=2; ok vs V183 64.6% >= 60%; MISS judge paired -281 >= +1k; ok worst -2733 > -15k; MISS peak 0.825 s < 0.6

### FINAL — 09:25 UTC (stopped early on the coordinator's instruction: all builders finished, no further candidates)
- Judged 4 candidates (farm2945 from outside/, ms_slot, ms_sr, ms_race from newexec/build); each reported within 4-6 min of its JUDGE_ME appearing.
- **None passes the bar.** Closest is ms_slot: H2H vs v183ms +572 (se 126, 41/48 wins), 79.2% vs V183, paired vs v183ms +457 (se 84), but judge only
  +54 (se 19), which is about 1/20 of the required +1k. ms_sr and ms_race lose on the judge (-231 / -281) and break the step cap (peak 0.616 / 0.825 s under 32-way load).
- newexec never dropped a JUDGE_ME (coordinator: newexec stopped at -37k). No FINAL candidate, so the FINAL extras (lx1 H2H, 2nd seed block) were not run on any candidate;
  lx1 and v183ms baselines on both seed blocks are in the table above.
- Pod 74b2myjnkbg5zy deleted 09:24 UTC (REST DELETE 204, GET 404); no replacement pod created. Poller stopped 09:24 UTC.
- NOT done: no uploads; no laptop simulations; step times were measured under 32 concurrent games on 16 physical cores (conservative vs Kaggle's ~1.6 vCPU per agent, but not identical).
