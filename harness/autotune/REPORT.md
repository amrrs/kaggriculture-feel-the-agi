# final30/autotune — automated optimiser over the v183ms executor/opening parameters (REPORT; updated at each checkpoint)

## FINAL (15:15 UTC 30 Sep) — numbers first
**Result: g012m** (uploaded by the coordinator as 56707760) is the harness's best vector and the only one that met the full pre-declared bar.
Pooled over the 10 untouched seed blocks that played no part in choosing it (c1 19201-19248, b0-b8 19301-19732; seat = seed % 2; 480 games per opponent;
paired vs v183ms on the same pod/seed/seat):
| g012m vs | paired margin (se), z | win rate (v183ms's win rate on the same games) |
|---|---|---|
| v183ms (H2H) | **+938 (102), z 9.2** | **0.713** (0.5 by symmetry) |
| V183 | **+969 (131)** | **0.850** (0.733) |
| lx3 | **+780 (134)** | **0.946** (0.919) |
Worst game in those 1440 games: -8697 (none < -15k). Per-block H2H: +588, +632, +1024, +734, +1287, +345, +805, +1556, +1454, +955.
The selection block (19001-19048, v2) gave +1632 and its re-run in the final batch fA +1735 (347): expect ~+0.9k, not +1.7k.
Top-field tape judge (123 tapes = top-12 farms; final batch fA, paired vs v183ms on the same tapes): all +662 (139), 68 vs 64 wins, both-intact +596;
**33 held-out tapes +758 (252), 20 vs 19 wins**; the 90 search tapes +627 (166). Band >= 2850 (60 tapes of M&M&P&Q, DSM, DECEM, Victor, Mother-Goose):
+607 (205) paired but **26 vs 25 wins**; held-out 16 band tapes: 8 vs 8 wins in every one of the 9 band rounds.
Peak step: low-load check (pod p13, 8 concurrent games, 12 games each vs V183): g012m 0.430 s max (median game max 0.373, 0 steps > 0.6 s) vs
v183ms 0.512 s (0.390); under 26-32-way load spikes to 0.5-0.8 s hit v183ms equally (0.764 s in fA, 0.996 s in v1). Loader test: callable `agent`, ACTIVE/ACTIVE.
Package: **build/submission-at12m.tar.gz sha256 2b2fe6e972e08559a6f3b59c66a23621a22e26b556f8f5623e760a68285aec0f**, main.py
**sha256 abef1c1726f3905b22a4e5e0b6860a3f1974189c923da00a8351a193587c0660** (build/at12m/main.py; parent ms_slot 80867093 = v183ms cba37327 + MS_SLOT;
the change is an appended override block only). Engine kaggle-environments 1.32.7.

### Final batch fA (14:56-15:02 UTC; holdout 19001-19048 seat = seed % 2 + both seats on 19001-19012, n = 60 per opponent; all 123 tapes)
| cand | H2H vs v183ms (se), win | vs V183 paired (se), win (v183ms 0.683) | vs lx3 paired (se), win (0.950) | tapes all 123 paired (se), wins (64) | held-out 33 tapes paired (se), wins (19) | worst | peak max / p95 |
|---|---|---|---|---|---|---|---|
| **g012m** | +1735 (347), 0.750 | +1566 (362), 0.900 | +1236 (349), 0.967 | +662 (139), 68 | +758 (252), 20 | -4609 | 0.430 / 0.399 |
| g010c04 | +2454 (381), 0.817 | +2340 (452), 0.867 | +1704 (421), 0.983 | +483 (154), 65 | +453 (308), 19 | -5888 | 0.531 / 0.402 |
| g107m (band mean) | +1161 (389), 0.667 | +1437 (452), 0.850 | +1325 (388), 0.967 | +686 (165), 67 | +835 (383), 19 | -6111 | 0.589 / 0.378 |
| g103m (band mean) | +1004 (337), 0.717 | +1714 (448), 0.817 | +983 (430), 0.983 | +754 (151), 69 | +622 (268), 19 | -4261 | 0.590 / 0.403 |
| ms_slot (reference) | +629 (131), 0.800 | +421 (104), 0.783 | +592 (114), 0.983 | +31 (22), 64 | +51 (45), 19 | -2651 | 0.484 / 0.403 |
fA reuses the selection seeds (19001-19048), so it ranks, it does not estimate. Batch fB (untouched 19801-19896) was cut off when the coordinator deleted
the pods at 15:06 (no games synced) - the untouched-block evidence for the alternatives is the c1 row (g010c04 H2H +1529 (362), vs V183 +1703 (446)).
**Alternative if a second slot is wanted: g010c04** (build/submission-at10c4.tar.gz sha256 811d15cf32353d9dc5b6112620ea62e8efe1f432f12b614f85d9c064884dce57,
main.py c4507819c652b7d8a254d77b928a985d3881778626c0c70560380c12e5dc87ed, loader test OK): stronger reactive numbers (H2H / V183 / lx3 on both blocks it
was tested on) but weaker on the top-field tapes (+483, held-out +453, 65 wins). Only 2 blocks of evidence, not 10.

### What the harness found (landscape; details in the checkpoints below)
- The hand-tuned base is a sharp optimum: at sigma 0.6 (0.3 of the range, the briefed value) 12/12 random joint moves lost 0.4-3.2k/game on the tapes.
  At sigma 0.25 CMA-ES found a direction that gains +0.4..0.8k on the tapes and ~+0.9k H2H within 5-10 generations.
- The joint move (g012m vs v183ms): SQ_W 2.0 -> 1.52, MPC_H 30 -> 21, AH_V 0.3 -> 0.12, ALLOC_MARGIN 150 -> 105, LATE_START 22 -> 20, FERT_WHEAT_MAXP 120 -> 149,
  WHEAT_BUFFER 3 -> 2, SELL0_MAX 3 -> 2, STRAW_AB x0.94, HAND_W 0.75 -> 0.98, TOM_OPP_MARGIN 0.5 -> 0.78, SQ_SPLIT 0.5 -> 0.66, SQ_DECAY 0.3 -> 0.43, MPC_W 1.0 -> 1.21,
  CARE_W 0.9 -> 0.81, OVERFLOW_TARGET 96 -> 97, ALLOC_MAX TOMATO 24 -> 22, SQ_START_DAY 13 -> 14 (HIRE_DOWN_W 1.21, LATE_HARVEST_W 0.098 ~ unchanged).
  Coins (per game vs v183ms's own games): tomato +1.3k own, wool +0.7k own (and +0.8k for the rival), melon +0.2k, carrot +0.2k own / -0.6k rival,
  milk -0.4k, strawberry -0.8k own / +0.7k rival.
- Ridge fit over ~160 vectors (effect of a knob moving from base to the + end of its range): tapes: AH_V -412 (111), LATE_HARVEST_W -360 (111), SQ_W -297 (106),
  ALLOC_MARGIN -201 (113); H2H: STRAW_AB -1294 (236), WHEAT_BUFFER +726 (264), MPC_H -673 (266), HANDS_MAX +640 (299), SQ_W +513 (238); vs V183:
  STRAW_AB -1188 (258), WHEAT_BUFFER +989 (290), MPC_H -777 (292), SQ_SPLIT +730 (278). No single knob reproduces the gain (48 one-at-a-time probes:
  only PLANT_LAST_DAY 25 -904, HAND_SLACK 2 -971, SQ_W 3.0 -626 exceed 2 se, all negative).
- 46 of 77 screened knobs never changed an action on the executor days (tomato hold, herd sizing, allocation caps/last days, carrot hold, cash reserve,
  FERT_BUY_MAXP, MPC_TV/DEC/ROOM ...): out/screen_summary.json.
- Overfitting is real: tape-weighted objectives produce tape specialists that lose H2H to v183ms (g015c09: held-out tapes +1133 but H2H -138;
  band means g108-g117: band-tape margins up, H2H -390..+232). The band objective (0.7 x band wins) did not produce a single held-out band win in 9 rounds.
- Band wins do not move because v183ms loses 29 of its 35 band-tape losses by > 5k (20 by > 10k); a +0.6-0.9k executor gain converts ~1 of 60 games.
  The band needs a different plan (supply volume / premium prices), not these parameters.

### Rerun on a fresh pod (harness = run_gen.sh + space.py + build_cand.py + at_game.py + pod_run.py + cma.py + eval_cand.py + driver.py / driver_band.py + validate.py)
```
cd research/claude/2900/agents/final30/autotune
bash mkpod.sh autotuneN "cpu5c 32" "cpu3c 32" || bash mkgpod.sh autotuneN 32 SECURE "NVIDIA L40S"   # log id/ip in ../PODS.txt
./run_gen.sh pod-setup <ip> <port>                    # self-destruct 14000 s armed first; engine 1.32.7; code + tapes + baselines rsynced
echo "p1 <ip> <port> 30" >> pods.txt                  # name ip port workers (one line per pod; the driver re-reads it every generation)
./run_gen.sh screen                                   # optional: det-mode knob screen (out/screen*/, screen_report.py)
./run_gen.sh init && ./run_gen.sh run 18:00           # CMA-ES (obj v1); sigma: set driver.SIGMA0 (0.25 worked; 0.6 is too wide)
./run_gen.sh band-init && ./run_gen.sh band 18:00     # band objective (starts at g012m); holdout rounds every 2 generations
./run_gen.sh report 105 106 ; ./run_gen.sh landscape 5
VAL_SEEDS=19901-19996 VAL_TAPES=0 ./run_gen.sh validate x1 g012m g010c04   # holdout check on an untouched block (never reuse 19001-19732, 19801-19896 = used/queued)
./run_gen.sh pack <tag> <cid>                         # then hybrid/loadtest.py on a pod
```
Every evaluated vector is in evals.jsonl (579 rows: 309 obj v1, 270 obj band; z vector, values, all components), generation specs in gens/, games in out/
(~91k JSONs, 734 MB), CMA states in state/, the driver logs in state/driver*.out.

### NOT done
- Batch fB (untouched 19801-19896 for all five finalists) was lost when the pods were deleted at 15:06; g010c04 / g107m / g103m have 1-2 untouched blocks each vs g012m's 10.
- No live-set (Majkel) replay judge, no Kaggle kernel, no upload by this agent. Laptop: no games (JSON parsing only).
- The briefed sigma 0.6 and "both seats" fresh games were changed (sigma 0.25; seat = seed % 2 from gen 5, because both seats replay the same game) - see checkpoints.
- The held-out band set is 16 tapes (a quarter, not a third): only those were never searched on.

## CHECKPOINT 1 (09:50 UTC) — harness built, knob screen done, CMA-ES generation 0 running
No result on strength yet. Nothing uploaded. No local simulations (all games on the pods below).

### Pods (all logged in ../PODS.txt; CPU flavors were SUPPLY_CONSTRAINT at 09:30, so GPU pods are used for their CPUs)
| name | id | hardware | workers | self-destruct |
|---|---|---|---|---|
| p1 | lqmmv5yj9ecje0 | RTX PRO 4500 pod, 32 vCPU (quota 27.2), EPYC 9554 | 26 | 09:32:36 + 14000 s = 13:25:56 UTC |
| p2 | o1oqc3o65t7452 | L40S pod, 36 vCPU, EPYC 7713P | 32 | 09:32:36 + 14000 s = 13:25:56 UTC |
| p3 | ro6lm0o59u1rmh | L40S pod, 32 vCPU (quota 27.2), EPYC 7702 | 26 | 09:34:03 + 14000 s = 13:27:23 UTC |
Replacement pods are needed ~13:10 UTC for generations after 13:25 and for the holdout validation.

### Knob screen (phase A; det mode = wall-clock planning caps lifted, ops-bounded, reproducible)
77 knobs x (z=-1, z=+1) vs V183, seat 0, seeds 20001-20006 (base = ms_slot). Base digests identical on all 3 pods for 20001/20002;
seed 20004 is not reproducible across processes (string-hash order), so it is excluded from the liveness count.
LIVE (digest changes on >= 2 usable seeds): 40. DEAD on every usable seed: TOM_HOLD, TOM_HOLD_MAX, TOM_HOLD_OPP_W, all herd
knobs (HERD_SHEEP scale, HERD_SHEEP_Y1, HERD_LEAD, HERD_DAY_MAX), every ALLOC_LAST_DAY, ALLOC_MAX STRAW/SHEEP/COW/GOOSE/CARROT,
CARROT_HOLD/_PRICE/_OPP_TRIG, CASH_RESERVE, FERT_BUY_MAXP, MPC_ROOM/TV/DEC/SHED_MAX(1 seed), MELON_LABOUR, END_MIN, HIRE_DOWN_MIN,
WHEAT_KEEP_ROOM, LAND_RESERVE. (i.e. the tomato hold, herd sizing and allocation caps do not bind on the executor days in these games.)
Single-knob margin deltas vs V183 (2 seeds, det; indicative only, n=2): STRAW_AB x1.6 -25.5k/-8.1k, HANDOVER 288 -16.3k/-22.8k,
LAND_MAX_EXTRA 3 -16.9k/-6.9k, RESCUE_HOUR 21 -8.2k, LATE_START 26 -7.1k; SELL0_MAX 1 +4.5k/+2.0k, OVERFLOW_TARGET 88 +0.9k/+1.4k,
TOM_FIRST_DAY 19 +6.1k (1 seed). Full table: out/screen_summary.json (+ out/screen_chg.json).

### Search space (25 knobs, space_final.json; z in [-1,1], 0 = ms_slot value)
hiring HANDS_MAX 10-14, HAND_SLACK 0-2, HIRE_DOWN_W 0.6-2.4, HAND_W 0.375-1.5 | sales SQ_W 1-4, SQ_DECAY 0.1-1, SQ_SPLIT 0-1,
SQ_START_DAY 11-17, MPC_W 0.5-2, MPC_H 12-60, MS_SLOT on/off, SELL0_MAX 1-8 | economics CARE_W 0.45-1.8, FERT_WHEAT_MAXP 60-240,
WHEAT_BUFFER 0-8, OVERFLOW_TARGET 88-100, LATE_HARVEST_W 0-0.6, AH_V 0-1, ALLOC_MARGIN 75-300, STRAW_AB scale 0.6-1.25 |
timing LATE_START 19-26, PLANT_LAST_DAY 24-28, TOM_FIRST_DAY 12-19, TOM_OPP_MARGIN 0-1.5, ALLOC_MAX TOMATO 8-32.

### Objective (eval_cand.py; paired, common random numbers, within pod)
Each pod plays a fixed slice of the 90 SEARCH tapes (33 tapes held out, tape_split.json, stratified by team) and a slice of the
generation's 12 fresh seeds (30001 + 12 g ..., both seats, vs V183 and vs v183ms) for every candidate, + v183ms vs V183 on the
same seeds. score = 0.5 x T/300 + 0.3 x ((WV + WH)/2)/0.10 + 0.2 x TW/4 - penalties (0.25 per game < -15k, 1.0 if p95 peak step
> 0.55 s and > base + 0.03). CMA-ES (cma.py) lambda 12, mu 6, sigma0 0.6 (= 0.3 of the range) + the CMA mean each generation.

## CHECKPOINT 2 (10:00 UTC) — generation 0 (sigma 0.6 as briefed): every sampled vector loses; restarted at sigma 0.25
Gen 0 = 12 CMA samples + the mean (= ms_slot unchanged) + v183ms as a control; 90 search tapes + 24 games vs V183 + 24 vs v183ms each.
| cand | score | T tapes paired vs v183ms (se) | TW | FV paired vs V183 (se) | WV | WH (vs v183ms - 0.5) | MH H2H margin |
|---|---|---|---|---|---|---|---|
| v183ms (control, noise floor) | +0.01 | +5 (12) | 0 | 0 | 0 | 0 | -1 |
| g000m = ms_slot | **+1.02** | **+50 (19)** | 0 | +51 (277) | +0.17 | +0.46 | +772 |
| best sample g000c11 | -0.90 | -60 (146) | -1 | -2026 (979) | -0.33 | -0.17 | -1690 |
| other 11 samples | -2.4 .. -8.1 | -434 .. -3202 | -5..0 | -7601 .. +38 | | | |
At sigma 0.6 (0.3 of the range, ~20 knobs moved at once) 12/12 samples lose 0.4-3.2k/game against the top-field tapes and 11/12 lose to
V183. The optimum is sharp around the hand-tuned base; the (mu/mu_w) recombination of 12 losers would only drag the mean away from it.
Decision (10:00): CMA-ES restarted at mean = base, sigma 0.25 (0.125 of the range), from generation 1 (fresh seeds rotate; gen-0 rows
kept in evals.jsonl for the landscape). The ms_slot/v183ms rows reproduce judgerun/microstructure (+54 / 0), so the harness is sound.

## CHECKPOINT 3 (10:40 UTC) — 5 generations (73 vectors), best-so-far = the base itself; nothing beats ms_slot yet
~9.5 min per generation of 17 (12 CMA samples + mean + 4 one-at-a-time probes), ~2.3k games/gen on 3 pods.
Best by score (single-generation estimates; scores near the base are inflated by WH because MS_SLOT alone beats v183ms 23/24):
| cand | score | T tapes paired vs v183ms (se) | TW | FV vs V183 paired (se) | WV | WH | MH vs v183ms (se) | note |
|---|---|---|---|---|---|---|---|---|
| g000m = ms_slot | +1.02 | +50 (19) | 0 | +51 (277) | +0.17 | +0.46 | +772 (154) | base |
| g004o0 PLANT_LAST_DAY 28 | +1.01 | +42 (21) | 0 | +661 (138) | +0.17 | +0.46 | +614 (78) | = base within noise |
| g004c09 (19 knobs moved) | +0.89 | **+392 (122)** | +1 | +66 (615) | -0.04 | +0.17 | +388 (346) | best tape delta so far |
| g004m (CMA mean) | +0.41 | +331 (130) | +1 | -934 (652) | -0.21 | +0.08 | +197 (321) | |
| g002m (CMA mean) | +0.76 | +239 (106) | +1 | +919 (494) | +0.04 | +0.17 | +675 (323) | |
One-at-a-time probes (z = +-0.6, paired, tapes n=90): PLANT_LAST_DAY 25 **-904 (98)**, OVERFLOW_TARGET 91 -289 (99), HANDS_MAX 13 -358 (95),
SELL0_MAX 6 -258 (111), SELL0_MAX 2 +170 (99), LATE_START 24 +75 (54) but H2H -1585 (761); everything else within +-100 of the base.
Landscape so far (ridge fit over gens 1-4, effect of z 0 -> +1 on T): HIRE_DOWN_W +334 (206), SQ_W -314 (181), AH_V -340 (216), MPC_H -255 (201),
SQ_DECAY +256 (217) - nothing at 2 se yet. Fresh-seed components (12 distinct games per gen) are very noisy: from gen 6 every gen uses
24 distinct seeds with seat = seed % 2 (both seats of one seed replayed the same game in >90% of cases).

## CHECKPOINT 4 (11:18 UTC) — first real signal: the CMA mean region beats ms_slot on the search tapes by ~+400; holdout validation v1 running
Pods: +3 cpu3c 32 vCPU pods p4-p6 from 10:44 (self-destruct 14:39 UTC); 6 pods, ~8 min/gen of 18 candidates (12 CMA + mean + base
control g{g}b = ms_slot unchanged + 4 one-at-a-time probes); fresh seeds per gen: 24 distinct (gens 5-6), 36 distinct (gen 7+), seat = seed % 2.
CMA mean trajectory (T = search-tape paired vs v183ms, n=90; MH = H2H vs v183ms; the same-generation ms_slot control in brackets):
| gen | mean T (se) | TB | TW | FV vs V183 paired (se) | MH (se) | control ms_slot T / MH |
|---|---|---|---|---|---|---|
| 5 | +406 (171) | +406 | +1 | +2115 (445) | +1268 (407) | (no control) |
| 6 | +284 (169) | +343 | -1 | +2114 (1051) | +2285 (672) | +47 / +341 |
| 7 | +473 (163) | +496 | +2 | +304 (316) | +160 (323) | +32 / +550 |
| 8 | +439 (151) | +563 | +3 | +1710 (465) | +1080 (305) | +30 / +524 |
| 9 | +455 (154) | +513 | +2 | +1132 (538) | +1493 (414) | (control ran) |
Best single samples: g009c07 T +615 (181) TB +710 TW +3 MH +1332 (455); g006c10 T +506 (154) TW +3 MH +1853 (464); g009c02 T +610 (144).
Caveat: every generation uses the same 90 search tapes, so the tape number is optimistically biased by selection; the 33 held-out tapes decide.

g005m full parameter vector (everything not listed = ms_slot/v183ms value; MS_SLOT on):
HIRE_DOWN_W 1.2195 (base 1.2), HAND_W 0.7806 (0.75), SQ_W 1.4689 (2.0), SQ_DECAY 0.3108 (0.3), SQ_SPLIT 0.5538 (0.5), MPC_W 0.9797 (1.0),
MPC_H 24 (30), CARE_W 0.8379 (0.9), FERT_WHEAT_MAXP 152.73 (120), WHEAT_BUFFER 2 (3), OVERFLOW_TARGET 97 (96), LATE_HARVEST_W 0.1145 (0.1),
AH_V 0.2401 (0.3), ALLOC_MARGIN 118.68 (150), STRAW_AB scale 0.9465 (1.0 -> STRAW_AB (12.30, 8.05)), LATE_START 21 (22), TOM_OPP_MARGIN 0.7868 (0.5).
The later means move the same way (g009m: SQ_W 1.55, MPC_H 23, SELL0_MAX 2, FERT_WHEAT_MAXP 170, ALLOC_MARGIN 125, STRAW_AB x0.91, TOM_FIRST_DAY 15, AMAX_TOM 20).
Validation v1 (coordinator request, 11:20): g005m, g005c11, g008m, g009m, g009c07 on holdout seeds 19001-19048 (seat = seed % 2, + both seats on
19001-19012 -> 60 games per opponent) vs V183, v183ms, lx3, and all 123 tapes (33 held out reported separately), paired vs v183ms on the same
pod. It runs on all 6 pods (~6 min) with the search paused (faster than one pod for 30 min); the search resumes right after.

## CHECKPOINT 5 (11:27 UTC) — HOLDOUT VALIDATION v1: g009m PASSES the paired / H2H / worst-game clauses; tape judge +480 (bar +500) — CANDIDATE packaged
Holdout seeds 19001-19048 seat = seed % 2 + both seats on 19001-19012 (n = 60 per opponent, 48 distinct), all 123 tapes (33 never used in the
search), paired vs v183ms on the same pod/seed/seat/tape; 6 pods under full load (env.run actTimeout 1 s + overage, kaggle-environments 1.32.7).
| cand | H2H vs v183ms margin (se) z, win | vs V183 paired (se) z, win (v183ms win) | vs lx3 paired (se), win | tapes ALL paired (se), wins (v183ms 64) | HELD-OUT tapes n=33 paired (se), wins (19) | worst game | peak step max / p95 / n>0.6 |
|---|---|---|---|---|---|---|---|
| v183ms (ref) | 0 | 0; win 0.667 | 0; win 0.983 | 0; 64 | 0; 19 | -3026 | 0.996 / 0.491 / 10 |
| g005m | +678 (283) z 2.4, 0.583 | +706 (363) z 1.9, 0.783 | +1029 (292), 1.000 | +421 (158), 65 | +401 (367), 19 | -5178 | 1.060 / 0.412 / 4 |
| g005c11 | +395 (278) z 1.4, 0.500 | +838 (428) z 2.0, 0.733 | +422 (333), 0.917 | +521 (137), 65 | +560 (308), 19 | -3699 | 0.714 / 0.399 / 1 |
| g008m | +1161 (342) z 3.4, 0.733 | +1765 (435) z 4.1, 0.867 | +763 (386), 0.967 | +444 (143), 67 | +566 (296), 19 | -7453 | 0.574 / 0.381 / 0 |
| **g009m** | **+1651 (252) z 6.5, 0.800** | **+2255 (421) z 5.4, 0.933** | **+1024 (384), 0.933** | **+480 (142), 66** | **+411 (329), 19** | **-2528** | 0.745 / 0.415 / 2 |
| g009c07 | +941 (345) z 2.7, 0.633 | +1575 (395) z 4.0, 0.850 | +1505 (386), 0.967 | +670 (164), 68 | +663 (363), 20 | -6014 | 0.724 / 0.392 / 3 |
Pass bar (paired >= +1k vs v183ms with z >= 2 AND top-field judge paired >= +500 with more wins AND no game < -15k AND peak step < 0.6 s):
- g005m (coordinator's pick): FAILS the +1k H2H clause (+678). Not packaged.
- **g009m: H2H +1651 z 6.5 PASS; judge +480 (se 142) with 66 vs 64 wins - 20 coins short of +500 (held-out tapes +411, se 329); worst -2528 PASS;
  peak step 0.745 s max under 32-way load, but v183ms in the same run peaks at 0.996 s (10 steps > 0.6) - the spikes are the loaded pods, p95 0.415
  vs 0.491. Not a clean pass on the judge clause (within 0.15 se of it) - a low-load timing check is queued for the final validation.**
- g009c07: best judge (+670, holdout tapes +663, 68 wins) but H2H +941 < +1k.
Per-product coins vs v183ms's own games (per game, vs V183 + lx3, own | opponent), g009m: TOMATO +1437 | -682, WOOL +995 | +986, WHEAT +443 | -209,
MELON +188 | -184, CARROT -20 | -367, MILK -35 | -107, STRAWBERRY -916 | +955, EGG -65 | -24, FERTILIZER -28 | +67. The gain is tomatoes (earlier
TOM_FIRST_DAY 15, ALLOC_MARGIN 125 -> more tomato additions sold daily) and wheat; the price is ~0.9k of strawberry revenue handed to the rival
(STRAW_AB scale 0.91 plants fewer strawberries); wool rises on both sides (SQ_W 1.55 vs 2.0 -> wool sold earlier in the day).
**CANDIDATE (interim): g009m** = build/at9m/main.py, main.py sha256 e8d8e05fb8fc62fcb29cb6ed437b748c475a8e244b18e86bcecb2d23a7198976
(= the file validated on the pods, cands/g009m/main.py), archive build/submission-at9m.tar.gz sha256 1cdb90b7445fa824defd395fb26242263f7091be3c44279a5f94b0a9d13f6bcc
(main.py only, mtime 0). Loader test on pod p5 (hybrid/loadtest.py, kaggle-environments 1.32.7): callable `agent`, 30 steps, peak 0.114 s, ACTIVE/ACTIVE.
Parent: ms_slot 80867093 (v183ms cba37327 + MS_SLOT); the change is an appended override block only (AUTOTUNE dict + P['XC_P'] update), no code edits.
Vector (everything else = v183ms/ms_slot): HIRE_DOWN_W 1.3232, HAND_W 0.8724, SQ_W 1.5487, SQ_DECAY 0.2911, SQ_SPLIT 0.6013, SQ_START_DAY 14, MPC_W 1.1862,
MPC_H 23, SELL0_MAX 2, CARE_W 0.8341, FERT_WHEAT_MAXP 170.04, OVERFLOW_TARGET 97, LATE_HARVEST_W 0.1401, AH_V 0.1784, ALLOC_MARGIN 125.19,
STRAW_AB scale 0.9111, LATE_START 21, TOM_FIRST_DAY 15, TOM_OPP_MARGIN 0.5859, ALLOC_MAX TOMATO 20.
Search resumed 11:24 (gen 10+) around this region; final validation of the best 3 at ~14:50-15:30 on fresh holdout-only rules.

## CHECKPOINT 6 (12:05 UTC) — 14 generations, 212 vectors evaluated; the CMA mean keeps improving on the search tapes
| gen | CMA mean T (se) | TB | TW | FV vs V183 (se) | MH vs v183ms (se) | ms_slot control T / MH |
|---|---|---|---|---|---|---|
| 10 | +468 (163) | +609 | 0 | +1219 (444) | +1859 (449) | +36 / +527 |
| 11 | +388 (170) | +591 | +1 | +557 (550) | +1321 (424) | +5 / +550 |
| 12 | **+638 (166)** | +697 | +3 | +1007 (541) | +1202 (451) | +34 / +707 |
| 13 | **+661 (128)** | +665 | +3 | +191 (541) | +717 (365) | +31 / +322 |
Landscape (ridge fit over gens 5-13, n~140 vectors; effect of moving a knob from its base value to the +end of its range, se):
- tapes T: AH_V -412 (111), LATE_HARVEST_W -360 (111), SQ_W -297 (106), ALLOC_MARGIN -201 (113), HAND_SLACK -155 (104), HIRE_DOWN_W +192 (131).
- H2H vs v183ms: STRAW_AB scale -1294 (236) (fewer strawberries = better H2H), WHEAT_BUFFER +726 (264), MPC_H -673 (266), HANDS_MAX +640 (299), SQ_W +513 (238).
- vs V183 (FV): STRAW_AB scale -1188 (258), WHEAT_BUFFER +989 (290), MPC_H -777 (292), SQ_SPLIT +730 (278), ALLOC_MARGIN -716 (280).
- < 1 se on T, H2H and FV alike: CARE_W, HAND_W, SELL0_MAX, SQ_DECAY (within the explored region; MS_SLOT never flipped at this sigma).
One-at-a-time probes (48, z = +-0.6, n = 90 tapes each): the only single knobs outside +-2 se on the tapes are PLANT_LAST_DAY 25 (-904), HAND_SLACK 2 (-971),
SQ_W 3.03 (-626), SQ_W 1.32 (+262, se 65; but H2H -422), HANDS_MAX 13 (-358). No single knob reproduces the mean's +600: the gain is the joint move.
Pods: p7/p8 (RTX PRO 4500 pods, 32 vCPU, self-destruct 15:52 UTC) added at 12:02 for the p1-p3 expiry at 13:26.

## CHECKPOINT 7 (12:22 UTC) — HOLDOUT VALIDATION v2 (coordinator request 12:13): **CANDIDATE = g012m**
Same protocol as v1: holdout seeds 19001-19048 seat = seed % 2 + both seats on 19001-19012 (n = 60 per opponent, 48 distinct), vs V183, v183ms, lx3;
all 123 tapes (33 held out, never used in the search); paired vs v183ms on the same pod/seed/seat/tape; 6 pods (p2, p4-p8) under full load while the
search continued on p1/p3. g009m re-run as the reference (reproduces v1: H2H +1680 vs +1651, tapes +500 vs +480).
| cand | H2H vs v183ms (se) z, win | vs V183 paired (se), win (v183ms 0.633) | vs lx3 paired (se), win (0.983) | tapes ALL paired (se), wins (64), both-intact | **HELD-OUT 33 tapes** paired (se), wins (19) | worst game (fresh) / worst tape paired | peak step max / p95 / n>0.6 |
|---|---|---|---|---|---|---|---|
| v183ms (ref) | 0 | 0 | 0 | 0, 64 | 0, 19 | -3084 | 0.751 / 0.421 / 1 |
| g009m (v1 CANDIDATE) | +1680 (262) z 6.4, 0.833 | +2317 (412), 0.917 | +1082 (393), 0.933 | +500 (144), 66, +499 | +420 (333), 19 | -2528 / -3764 | 0.795 / 0.385 / 4 |
| g015c09 | **-138 (297)**, 0.467 | +540 (411), 0.700 | +241 (421), 0.883 | **+992 (162)**, 68, +946 | **+1133 (294)**, 20 | -6345 / -4922 | 0.466 / 0.380 / 0 |
| g015m | +680 (262) z 2.6, 0.650 | +1166 (363), 0.817 | +947 (372), 0.967 | +582 (138), 65, +500 | +426 (345), 19 | -4524 / -6507 | 0.490 / 0.393 / 0 |
| g013m | +1010 (322) z 3.1, 0.633 | +1850 (367), 0.900 | +992 (372), 0.933 | +671 (110), 67, +661 | +621 (231), 19 | -4329 / -2667 | 0.474 / 0.387 / 0 |
| **g012m** | **+1632 (329) z 5.0, 0.767** | **+1531 (419), 0.900** | **+1156 (331), 0.950** | **+675 (138), 68, +638** | **+782 (264) z 3.0, 20** | -5888 / -5623 | 0.822 / **0.393** / 3 |
| g010c04 | +2272 (378) z 6.0, 0.800 | +2475 (469), 0.883 | +1415 (405), 0.983 | +492 (154), 66, +512 | +417 (314), 19 | -5543 / -4844 | 0.553 / 0.377 / 0 |
Selection rule (coordinator): holdout H2H and held-out tapes together, step p95 < 0.5 s, no game < -15k.
- **g012m** is the only vector that clears every clause of the pre-declared bar: H2H +1632 z 5.0 (>= +1k, z >= 2), judge +675 with 68 vs 64 wins
  (>= +500, more wins), held-out tapes +782 (se 264, z 3.0, 20 vs 19 wins), worst game -5888 (> -15k), p95 step 0.393 s. Its peak 0.822 s
  (3 steps > 0.6 s in 303 games) is load-induced: v183ms peaks at 0.751 / 0.996 s in the same v2 / v1 batches; circuit caps are unchanged
  (OPT_STEP_CAP 0.35, PLAN_WALL 0.4).
- g010c04 has the best H2H (+2272) but the judge is +492 (+417 held out) - just under the tape clause. g009m: judge +500 exactly, held out +420.
- g015c09 is a tape specialist (+1133 held out) that LOSES H2H to v183ms (-138): rejected; this is the overfitting risk of the 0.5 tape weight.
Per-product coins vs v183ms's own games (per game, fresh holdout vs V183 + lx3, own | opponent), g012m: TOMATO +1319 | -207, WOOL +687 | +780,
MELON +196 | -194, CARROT +169 | -621, WHEAT +79 | -106, EGG +19 | -91, FERTILIZER -41 | +9, MILK -421 | -538, STRAWBERRY -809 | +726.
(Mechanism: earlier/more tomato additions sold daily, lower SQ_W sells wool/milk earlier; fewer strawberries (STRAW_AB x0.94) hand some strawberry
revenue to the rival.)
**CANDIDATE: g012m** = build/at12m/main.py, main.py sha256 **abef1c1726f3905b22a4e5e0b6860a3f1974189c923da00a8351a193587c0660** (identical to the
validated pod file cands/g012m/main.py); archive **build/submission-at12m.tar.gz sha256 2b2fe6e972e08559a6f3b59c66a23621a22e26b556f8f5623e760a68285aec0f**
(main.py only, mtime 0, uid/gid 0). Loader test on pod p4 (hybrid/loadtest.py, kaggle-environments 1.32.7): callable `agent`, 30 steps, peak 0.115 s,
ACTIVE/ACTIVE. Parent ms_slot 80867093 (v183ms cba37327 + MS_SLOT); change = appended override block only (AUTOTUNE dict + P['XC_P'] update).
g012m vector (everything else = ms_slot/v183ms): HIRE_DOWN_W 1.209 (1.2), HAND_W 0.9772 (0.75), SQ_W 1.5153 (2.0), SQ_DECAY 0.4317 (0.3),
SQ_SPLIT 0.6575 (0.5), SQ_START_DAY 14 (13), MPC_W 1.2062 (1.0), MPC_H 21 (30), SELL0_MAX 2 (3), CARE_W 0.8112 (0.9), FERT_WHEAT_MAXP 149.09 (120),
WHEAT_BUFFER 2 (3), OVERFLOW_TARGET 97 (96), LATE_HARVEST_W 0.098 (0.1), AH_V 0.1209 (0.3), ALLOC_MARGIN 105.03 (150), STRAW_AB scale 0.9372
(-> (12.18, 7.97)), LATE_START 20 (22), TOM_OPP_MARGIN 0.7817 (0.5), ALLOC_MAX TOMATO 22 (24).
Caveats: (1) g012m was chosen out of 6 on this holdout (and g009m out of 5 in v1), so its holdout numbers carry some selection optimism; a
confirmation on an untouched block (seeds 19201-19248) is queued for the final validation. (2) The tape judge cannot react; H2H vs v183ms and the
V183/lx3 pairings are the reactive evidence. (3) Held-out tape se is 260-350 (n = 33).
The previous interim CANDIDATE g009m (build/submission-at9m.tar.gz) is superseded by g012m.

### CONFIRMATION c1 (12:27 UTC) on an UNTOUCHED seed block 19201-19248 (seat = seed % 2, 48 distinct games per opponent; never used by search or v1/v2)
| cand | H2H vs v183ms (se) z, win | vs V183 paired (se) z, win (v183ms 0.667) | vs lx3 paired (se), win (0.875) | worst | peak max / p95 |
|---|---|---|---|---|---|
| g012m (CANDIDATE) | +588 (287) z 2.0, 0.729 | +1075 (368) z 2.9, 0.792 | +692 (435), 0.958 | -4429 | 0.570 / 0.380 |
| g010c04 | **+1529 (362) z 4.2, 0.812** | **+1703 (446) z 3.8, 0.833** | **+1312 (501)**, 0.958 | -3918 | 0.602 / 0.402 |
| g009m | +1068 (340) z 3.1, 0.667 | +1102 (401) z 2.8, 0.771 | +603 (429), 0.938 | -3876 | 0.436 / 0.404 |
| g013m | +447 (351) z 1.3, 0.604 | +454 (408) z 1.1, 0.792 | +144 (463), 0.938 | -5444 | 0.511 / 0.386 |
g012m's H2H shrinks from +1632 (the block it was selected on) to +588 here: the expected selection optimism. Pooled over both holdout blocks
(n = 108 games per opponent): **g012m H2H ~+1.17k, vs V183 ~+1.33k; g010c04 H2H ~+1.94k, vs V183 ~+2.13k; g009m H2H ~+1.41k, vs V183 ~+1.78k.**
Top-field tapes (v2, all 123 / held-out 33 / wins vs 64): g012m +675 / +782 / 68; g010c04 +492 / +417 / 66; g009m +500 / +420 / 66.
**Reading for the upload decision:** every one of the three beats v183ms on every axis with no tail (worst > -6k anywhere). g012m is the
better top-field (tape) vector (+4 tape wins, held-out +782), g010c04 the better reactive vector (H2H / V183 / lx3 on both holdout blocks,
H2H z 6.0 and 4.2). g012m stays CANDIDATE by the coordinator's pre-declared rule (only full pass); **g010c04 is packaged as the alternative**
(below). If only one slot: the tape evidence is the only top-field evidence, so g012m; if the pair is being chosen, g012m + g010c04 are
different enough (tomato-heavy vs strawberry-light moves of the same region) to be a sensible pair only if the other slot is not needed for V183-line safety.
**ALTERNATIVE: g010c04** = build/at10c4/main.py, main.py sha256 **c4507819c652b7d8a254d77b928a985d3881778626c0c70560380c12e5dc87ed** (= pod file
cands/g010c04/main.py); archive **build/submission-at10c4.tar.gz sha256 811d15cf32353d9dc5b6112620ea62e8efe1f432f12b614f85d9c064884dce57**;
loader test on pod p5: callable `agent`, 30 steps, peak 0.116 s, ACTIVE/ACTIVE.
g010c04 vector: HIRE_DOWN_W 1.318, HAND_W 0.9274, SQ_W 1.5284, SQ_DECAY 0.3651, SQ_SPLIT 0.5836, SQ_START_DAY 14, MPC_W 1.3305, MPC_H 20, SELL0_MAX 2,
CARE_W 0.7273, FERT_WHEAT_MAXP 161.35, WHEAT_BUFFER 2, OVERFLOW_TARGET 98, LATE_HARVEST_W 0.1315, AH_V 0.0857, ALLOC_MARGIN 108.41, STRAW_AB scale 0.8908,
LATE_START 20, TOM_FIRST_DAY 15, TOM_OPP_MARGIN 0.6721, ALLOC_MAX TOMATO 22.

## CHECKPOINT 8 (12:40 UTC) — objective switched to the >= 2850 BAND (coordinator 12:35); search restarted at g012m, sigma 0.2
Old objective (obj v1) stopped after generation 18 (274 vectors). Last two generations: g017m T +806 (201) TW +4, g018c08 T +1025 (182) TW +4,
g018m T +750 (136) MH +993 (337) - the tape delta kept growing, but on the SAME 90 search tapes (optimism; the held-out tapes decide).
New objective (driver_band.py, rows in evals.jsonl carry obj='band', generations numbered from 100):
- band tapes = M & M & P & Q, DSM, DECEM, Victor @ Tufa Labs, Unknown Mother-Goose (Boey and CDE have no tapes in tapes.json): 60 tapes.
  Held out = the 16 band tapes that no search ever used (the pre-existing holdout; a quarter, not a third: the other 44 were already
  searched on, so they cannot be called untouched). Search on the 44 (band_split.json).
- score = 0.7 x BW/2 + 0.3 x BM/500 - tail/step penalties (BW = band-tape wins - v183ms wins, BM = band paired margin);
  REJECTED (score -1000) if FV (paired vs V183 on the generation's 36 fresh seeds) < -300 or H2H vs v183ms < -300.
- CMA mean = g012m's vector, sigma 0.2, lambda 12; each generation also runs the CMA mean, the ms_slot control (g{g}b) and g012m itself (g{g}r).
- Every 2 generations: validation on untouched seeds 19301+48k .. +47 (seat = seed % 2) vs V183 / v183ms / lx3 + the 16 held-out band tapes,
  for the current mean, the best sample of the 2 generations and g012m (reference). BAND-CANDIDATE rule: >= +2 held-out band-tape wins over
  g012m, H2H vs v183ms >= 0, no game < -15k.
Baseline on the band (v2 batch, held-out 16 band tapes): computed in the first validation round (b0) for g012m and v183ms on the same pods.

### BAND round b0 (12:51 UTC): seeds 19301-19348 (seat = seed % 2, untouched), 48 games per opponent, + the 16 held-out band tapes
| cand | H2H vs v183ms (se), win | vs V183 paired (se), win (v183ms 0.812) | vs lx3 paired (se), win (0.917) | held-out band tapes paired (se), wins (v183ms 8/16) | worst | peak max / p95 |
|---|---|---|---|---|---|---|
| g012m (CANDIDATE, reference) | +632 (376), 0.667 | +570 (419), 0.812 | +980 (421), 0.958 | +342 (406), 8 | -8697 | 0.449 / 0.382 |
| g101m (band CMA mean) | +1139 (363), 0.688 | +869 (370), 0.896 | +517 (399), 0.917 | +204 (574), 7 | -4819 | 0.415 / 0.373 |
| g101c07 (best band sample g100-101) | +26 (348), 0.542 | +292 (397), 0.854 | +583 (478), 0.938 | +345 (438), 7 | -6576 | 0.466 / 0.387 |
No BAND-CANDIDATE (needs >= +2 held-out band wins over g012m). The 16 held-out band tapes cannot separate these vectors: margins +200..+350 with
se 400-570, wins 7-8 of 16 for everyone including v183ms. On the 44 band SEARCH tapes (gens 100-101): g012m +1 win / +680..695 paired, CMA mean +1..+3 wins.
g012m's H2H on this third untouched block: +632 (376) - with c1 (+588) the honest estimate of g012m vs v183ms is ~+0.6k/game, ~67-73% wins
(the +1632 of v2 was the selection block).

### Why band wins do not move (13:05 UTC) — structural, from the v1/v2 tape runs (60 band tapes = 44 search + 16 held out)
- Band-tape wins, all 60: v183ms 25; g012m 26, g013m 26, g009m 26, g009c07 26, g015c09 27, g010c04 25, g005m 25. Held-out 16: v183ms 8, all others 7-8.
  Paired margins on the 60 band tapes are clearly positive (g012m +607 (205), g013m +615 (150), g015c09 +1014 (256)) but they do not convert.
- v183ms loses 35 of the 60 band tapes; **29 of those 35 by more than 5k (20 by more than 10k)**, only 3 within 2k. g012m flips 1 of them.
  Of v183ms's 25 band "wins", only 11 are on intact tapes (the rest are broken-tape artefacts).
- So the >= 2850 band beats our lineage by 5-10k+ in most games; an executor re-tune worth +0.5-1k/game cannot change the band W/L count.
  Band win rate needs a different game plan (the wild/ledger decomposition: supply volume / premium prices), not parameters of this executor.
  The band objective will keep running to 15:00 as instructed, but a BAND-CANDIDATE (>= +2 held-out band wins over g012m) is unlikely by construction.

### BAND round b1 (13:06 UTC): seeds 19349-19396 (untouched), 48 games per opponent, + 16 held-out band tapes
| cand | H2H vs v183ms (se), win | vs V183 paired (se), win (v183ms 0.833) | vs lx3 paired (se), win (0.917) | held-out band tapes paired (se), wins (8/16) | worst | peak max / p95 |
|---|---|---|---|---|---|---|
| g012m (reference) | +1024 (302), 0.688 | +1419 (374), 0.896 | +997 (425), 0.979 | +374 (397), 8 | -3285 | 0.425 / 0.387 |
| g103m (band CMA mean) | +1160 (349), 0.708 | +1350 (400), 0.875 | +990 (393), 0.938 | +666 (443), 8 | -4796 | 0.493 / 0.381 |
| g103c00 | +1323 (361), 0.771 | +1190 (363), 0.896 | +1074 (413), 0.896 | +550 (441), 7 | -5014 | 0.549 / 0.384 |
No BAND-CANDIDATE (0 extra held-out band wins). g012m on the three untouched blocks (c1, b0, b1; 144 games): H2H +748/game (~+185 se), ~69% wins;
vs V183 +1021/game. Search tapes, band gens 100-103: g012m +1 band win and ~+700 paired every generation (stable); mean g103m +2 wins, +954.

### BAND round b2 (13:20 UTC): seeds 19397-19444 (untouched), 48 games per opponent, + 16 held-out band tapes
| cand | H2H vs v183ms (se), win | vs V183 paired (se), win | vs lx3 paired (se), win | held-out band tapes paired (se), wins /16 | worst | peak max / p95 |
|---|---|---|---|---|---|---|
| v183ms | 0 | win 0.688 | win 0.833 | +0 (0), 8 | -4084 | 0.413 / 0.397 |
| g105m | +763 (341), 0.708 | +978 (376), 0.833 | +790 (410), 0.917 | +594 (437), 8 | -4575 | 0.438 / 0.378 |
| g104c02 | +332 (364), 0.479 | +937 (376), 0.771 | +926 (368), 0.896 | +456 (633), 7 | -3974 | 0.476 / 0.378 |
| g012m | +734 (304), 0.646 | +1110 (400), 0.854 | +1329 (397), 0.875 | +366 (401), 8 | -4054 | 0.412 / 0.387 |
No BAND-CANDIDATE. g012m pooled over the 4 untouched blocks (c1, b0, b1, b2; 192 games): H2H ~+745/game, vs V183 ~+1040/game, vs lx3 ~+1000/game.
Band search tapes (44): the CMA mean climbs (g104m +2 wins / +947, g105m +2 / +1156) while g012m stays at +1 / ~+760; on the held-out 16 it is 8 wins for everyone.

### BAND round b3 (13:34 UTC): seeds 19445-19492 (untouched), 48 games per opponent, + 16 held-out band tapes
| cand | H2H vs v183ms (se), win | vs V183 paired (se), win | vs lx3 paired (se), win | held-out band tapes paired (se), wins /16 | worst | peak max / p95 |
|---|---|---|---|---|---|---|
| v183ms | 0 | win 0.688 | win 0.896 | +0 (0), 8 | -2165 | 0.509 / 0.426 |
| g107m | +1516 (307), 0.812 | +1472 (347), 0.875 | +1181 (466), 0.917 | +593 (667), 7 | -3313 | 0.637 / 0.426 |
| g106c02 | +1377 (269), 0.708 | +852 (450), 0.771 | +834 (385), 0.938 | -91 (564), 7 | -4092 | 1.261 / 0.405 |
| g012m | +1287 (300), 0.833 | +1651 (416), 0.917 | +920 (426), 0.938 | +367 (397), 8 | -6153 | 0.531 / 0.414 |
No BAND-CANDIDATE. g106c02 hit one 1.261 s step here (0.398 s max in its search generation: a load spike, but noted). g012m over 5 untouched blocks (240 games): H2H ~+853/game (range +588..+1287 per block).

### BAND round b4 (13:48 UTC): seeds 19493-19540 (untouched), 48 games per opponent, + 16 held-out band tapes
| cand | H2H vs v183ms (se), win | vs V183 paired (se), win | vs lx3 paired (se), win | held-out band tapes paired (se), wins /16 | worst | peak max / p95 |
|---|---|---|---|---|---|---|
| v183ms | 0 | win 0.708 | win 0.958 | +0 (0), 8 | -2713 | 0.911 / 0.433 |
| g109m | -390 (350), 0.458 | +82 (485), 0.688 | +268 (446), 0.896 | +566 (476), 7 | -5735 | 0.960 / 0.461 |
| g108c08 | -387 (306), 0.375 | -75 (494), 0.667 | -107 (376), 0.854 | +716 (559), 7 | -5914 | 0.571 / 0.421 |
| g012m | +345 (333), 0.625 | +803 (426), 0.812 | +369 (404), 0.896 | +373 (398), 8 | -7618 | 0.503 / 0.394 |
**Warning:** the band search is now drifting into tape specialists: g109m and g108c08 LOSE H2H to v183ms on untouched seeds (-390, -387) and are flat vs V183,
while gaining on band tapes (+566 / +716 paired, still 7 wins of 16). g109m was also rejected by the -300 FV constraint in its own generation.
(Same failure as g015c09 under the old objective.) The mean moved MPC_H to 13 (range floor 12), SQ_W 1.3, STRAW_AB x0.87-0.89, AH_V ~0.05.
g012m over 6 untouched blocks (288 games): H2H ~+768/game (+345..+1287 per block).

### BAND round b5 (14:02 UTC): seeds 19541-19588 (untouched), 48 games per opponent, + 16 held-out band tapes
| cand | H2H vs v183ms (se), win | vs V183 paired (se), win | vs lx3 paired (se), win | held-out band tapes paired (se), wins /16 | worst | peak max / p95 |
|---|---|---|---|---|---|---|
| v183ms | 0 | win 0.667 | win 0.979 | +0 (0), 8 | -5415 | 0.479 / 0.420 |
| g111m | +1173 (474), 0.688 | +603 (622), 0.792 | -173 (520), 0.875 | +394 (663), 7 | -7071 | 0.549 / 0.397 |
| g111c09 | +509 (507), 0.604 | +411 (698), 0.625 | +148 (545), 0.917 | +422 (613), 7 | -4615 | 0.653 / 0.430 |
| g012m | +805 (321), 0.667 | +1321 (487), 0.854 | +512 (451), 0.917 | +358 (400), 8 | -4524 | 0.506 / 0.391 |
No BAND-CANDIDATE (held-out band wins 7 vs g012m's 8). g012m over 7 untouched blocks (336 games): H2H ~+773/game.

### BAND round b6 (14:17 UTC): seeds 19589-19636 (untouched), 48 games per opponent, + 16 held-out band tapes
| cand | H2H vs v183ms (se), win | vs V183 paired (se), win | vs lx3 paired (se), win | held-out band tapes paired (se), wins /16 | worst | peak max / p95 |
|---|---|---|---|---|---|---|
| v183ms | 0 | win 0.833 | win 0.917 | +0 (0), 8 | -1946 | 0.453 / 0.425 |
| g113m | +822 (316), 0.604 | -74 (405), 0.708 | +361 (388), 0.875 | -154 (618), 7 | -3682 | 0.500 / 0.420 |
| g112c06 | +275 (373), 0.521 | -148 (523), 0.708 | -717 (449), 0.750 | -201 (833), 6 | -5388 | 0.688 / 0.417 |
| g012m | +1556 (286), 0.792 | +403 (365), 0.896 | +820 (385), 1.000 | +358 (397), 8 | -4780 | 0.533 / 0.419 |
No BAND-CANDIDATE; the band search's current vectors are weaker than g012m on every reactive axis. g012m over 8 untouched blocks (384 games): H2H ~+871/game.

### BAND round b7 (14:36 UTC): seeds 19637-19684 (untouched), 48 games per opponent, + 16 held-out band tapes
| cand | H2H vs v183ms (se), win | vs V183 paired (se), win | vs lx3 paired (se), win | held-out band tapes paired (se), wins /16 | worst | peak max / p95 |
|---|---|---|---|---|---|---|
| v183ms | 0 | win 0.708 | win 0.958 | +0 (0), 8 | -2627 | 0.561 / 0.451 |
| g115m | +232 (344), 0.500 | +555 (413), 0.750 | -255 (378), 0.854 | +395 (667), 7 | -4339 | 0.584 / 0.425 |
| g114c02 | +617 (340), 0.688 | +374 (452), 0.792 | +90 (364), 0.917 | +678 (621), 7 | -5192 | 0.548 / 0.427 |
| g012m | +1454 (356), 0.771 | +1574 (407), 0.875 | +705 (339), 0.958 | +364 (395), 8 | -8262 | 0.619 / 0.437 |
No BAND-CANDIDATE. g012m over 9 untouched blocks (432 games): H2H ~+936/game; it has out-validated every band-search mean since b1.

### BAND round b8 (14:54 UTC): seeds 19685-19732 (untouched), 48 games per opponent, + 16 held-out band tapes
| cand | H2H vs v183ms (se), win | vs V183 paired (se), win | vs lx3 paired (se), win | held-out band tapes paired (se), wins /16 | worst | peak max / p95 |
|---|---|---|---|---|---|---|
| v183ms | 0 | win 0.729 | win 0.938 | +0 (0), 8 | -4891 | 0.579 / 0.481 |
| g117m | -148 (434), 0.521 | -213 (450), 0.750 | +117 (521), 0.958 | +829 (588), 7 | -7199 | 0.831 / 0.442 |
| g116c07 | +24 (316), 0.500 | -963 (534), 0.604 | -322 (496), 0.938 | +150 (818), 7 | -5868 | 0.736 / 0.508 |
| g012m | +955 (338), 0.708 | -231 (434), 0.792 | +477 (534), 0.979 | +372 (400), 8 | -5968 | 0.621 / 0.486 |
Band search stopped at 14:55 (generations 100-117 = 18 generations, 270 vectors; final validation next).
