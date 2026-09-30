# final30/opening3 — top-3 opening tape tree on v183ms (REPORT, updated at each checkpoint)

## 05:15 UTC note to coordinator
Received the "PLAYBOOK.md DRAFT by 05:45" message. It reads as addressed to the playbook agent (agents/final30/playbook/, which does
not exist yet); I do not write outside opening3/. What I can offer from my lane: the d0-d10 calendar of the top-3 farms per day
(market orders, plantings, land days, herd) will be written to opening3/CALENDAR.md as a by-product of the tape extraction
(target ~06:00 UTC). fieldnow/opening.md section L already has the TOP1-3 per-day purchase table. If you DO want me to write the
playbook, say so in this file or a message and I will switch.
05:20 UTC: second coordinator message ("publish PLAYBOOK.md at 05:45 ... late-game tile targets table") also reads as meant for the
playbook agent (playbook/ now exists and is theirs). opening3 continues on its own brief (deadline 11:00 UTC) unless told otherwise here.

## STUDY (05:25 UTC): where the prefix lives and how the handover is triggered (v183ms = micro/build/v183ms/main.py, sha cba37327)
- The day 0-10 opening is the OUTER main.py ("reactB ctrl.py"), not the circuit. Prefix data = `_LIB_B64` (line ~20 of main.py):
  base64(zlib(JSON list of 102 Boey 56484772 tapes)); each tape = {ep, shops (8 final shops), bank, a = JSON string of 264 steps
  [farmer, hands, market] (steps 0..263 = replay steps[1..264] actions), st = day-start [tile codes, planting days, money] for d0..d12}.
  Built by reactB/tools/mklib.py from boeytree/lib/tapes.json + states.json.
- Tree: `choose0()` at step 0 (modal d3 layout, max bank), then at h0 of `P['SWITCH_DAYS']=[3,6]` `choose()` = lenient layout
  distance `ldist` (+W_ANIMAL/W_OURS) + shop-signature `score` (W_NEX/W_SHOP on the unlocked-shop prefix, W_MONEY, W_BANK) +
  `trunk_adj` (TRUNK 1.0). The race agent's one-line edit was the `P.update({'OV_STRAW'...})` ctrl line (overlay on tape orders).
- Per step `tape_action()`: tape row -> PLANT trim (`repair`), LAND_RETRY (`overlay`, via `tape_quads` = tape's quadrant count,
  CAPPED AT 3 in the parent), HFIRST (hires after sells), HFUND, evening `rescue()` from h17 (any unit from h21).
- Handover: `agent()`: `if step >= P['HANDOVER']` (264 = d11 h0): first time `xc().S.clear()`, then every step
  `xc().safe_agent(obs)` = the embedded circuit `_CIRC_B64` (V183 dated-gate circuit + micro). The executor rebuilds its state from
  obs at d11 h0; nothing is passed from the tape phase.
- The circuit-side patches (micro, race, bundle's d10+ flags) edit `_CIRC_B64`; opening3 edits ONLY the outer ctrl + adds `_LIB3_B64`
  -> the two patch sets are disjoint and merge by applying both (build_open3.patch() on the bundle agent's main.py).

## BUILD (05:35 UTC)
- lib: mklib3.py -> lib/top3.json.gz (37 farms: M&M 11, DSM 15, DECEM 11) and lib/top5.json.gz (+Vadim 11, Victor 11 = 59).
  Same fields as the Boey lib; tape id = ep*10+seat (M&M vs DSM games put both farms in the lib).
- build_open3.py (patch on v183ms, flags default off): `_LIB3_B64` + P LIB3 (use it), T0_TEAM (step-0 tape = that team's modal
  d3 layout, max bank), Q4 (LAND_RETRY follows the tape to 4 quadrants; parent caps at 3 = Boey). Diagnostics S['rescue_n'],
  S['rescue_days'], S['land_retry_n'] (no action change). Rescue/HFIRST/HFUND/PLANT trim/TRUNK unchanged.
- Tags: o0 (flags off = parity), o3 (top3 lib, choose0 over all = DSM modal), o3m/o3d/o3e (T0 = M&M / DSM / DECEM), o3m9/o3d9
  (+ switch at d9), o5m/o5d/o5d9 (top5 lib).
- Facts about the lib: each team's step 0 is identical across its games; M&M d3 layouts 5 distinct / 11, DSM 3 / 15 (11 identical),
  DECEM 5 / 11; by d9 every tape is unique. Cross-team layouts differ a lot (different pasture/melon positions), so after choose0
  the tree effectively stays inside one team's family. All 37 top-3 farms hold 4 quadrants at d11 h0 (SE bought on d10, empty).
- CALENDAR.md = top-3 per-team d0-d10 calendar (orders, plantings, herd, tiles, money, land) from the same tapes.

## RUNS: pod 2lbkuyobkcs3tn (cpu5c 32 vCPU), self-destruct 05:14:44 + 14000 s = 09:08 UTC. Batch b1 (918 games) started 05:20 UTC:
parity o0 vs v183ms (3 seeds) ; {o3m,o3d,o3e,o3} x {v183ms, V183} and v183ms vs V183 on 17601-17624 both seats; then o3m9/o3d9/o5*.

## CHECKPOINT 1 (05:35 UTC) — batch b1 DONE (918 games, 20 s/game on the pod). HEADLINE: every top-field opening LOSES big with our executor.
Seeds 17601-17624 both seats, n=48 per row, env.run with actTimeout 1 s + overage; paired d = minus v183ms's game (same seed/seat/opp).
PARITY: o0 (patch, flags off) vs v183ms on 17601 s0 / 17602 s1 / 17603 s0: identical per-step action digests (b21eec27 / 2cab9f27 /
e8f584d2) and identical rewards -> the patch is mechanical.
| cand (opener, lib) | vs V183 win% | margin (se) | worst | paired d vs v183ms (se), better | own / opp final | vs v183ms win% | margin (se) | worst | step max |
|---|---|---|---|---|---|---|---|---|---|
| v183ms (Boey tree) | 68.8 | +745 (251) | -2613 | 0 | 102.5k / 101.8k | mirror | 0 | - | 0.44 |
| o3d = o3 (DSM, top3) | 22.9 | -7620 (1602) | -24980 | -8364 (1534), 11/48 | 101.3k / 108.9k | 12.5 | -10343 (1433) | -22802 | 0.52 |
| o3e (DECEM, top3) | 4.2 | -13143 (1397) | -34753 | -13888 (1422), 2/48 | 100.7k / 113.9k | 4.2 | -15479 (1320) | -36099 | 0.46 |
| o3m (M&M, top3) | 10.4 | -12104 (1430) | -31147 | -12848 (1428), 4/48 | 95.9k / 108.0k | 12.5 | -14624 (1585) | -37698 | 0.71 (1 step) |
| o3d9 / o3m9 (+switch d9) | 22.9 / 10.4 | -7872 / -12113 | | = parents (d9 switch changes nothing) | | 12.5 / 12.5 | -10519 / -14400 | | 0.41 |
| o5d (DSM opener, top5 lib: tree moves to Vadim/Victor 32/48) | 37.5 | -3746 (1152) | -27641 | -4490 (1164), 17/48 | 108.1k / 111.9k | 33.3 | -5531 (1285) | -25812 | 0.39 |
| o5m | 10.4 | -12007 | -31147 | = o3m | | 14.6 | -14457 | | 0.72 (1 step) |

d11 h0 state (= handover; own farm, mean over the 48 games vs V183) vs the recorded top-3 (fieldnow/teams.md d10 column / our lib's d11 h0):
| | quads | cash | C/S/G | W/S/M/T tiles |
|---|---|---|---|---|
| recorded M&M / DSM / DECEM (lib d11 h0) | 4 / 4 / 4 | 3.1k / 2.3k / 3.4k | 9.0/5.0/8.1 , 7.7/7.5/5.9 , 8.1/5.6/7.8 | 27/27/6.5/6.6 , 28/25/5.8/4.7 , 29/22/5.5/10.6 |
| o3m (M&M tree) | 4.00 | 2.8k | 8.0/3.2/7.0 | 23.5/24.6/5.8/5.0 |
| o3d (DSM tree) | 3.88 | 2.1k | 7.9/6.1/5.3 | 24.9/21.3/5.9/3.8 |
| o3e (DECEM tree) | 4.00 | 3.2k | 8.0/4.0/7.4 | 28.0/24.5/4.3/6.8 |
| v183ms / V183 (Boey tree) | 3.00 | 9.1k | 7.9/3.1/5.6 | 22.6/24.9/4.9/0 |
=> the tree REPRODUCES the top-3 d10 farm closely (o3e almost exactly: 4 quads, ~7 tomato, 28 wheat, 24.5 strawberry, 8 cows,
7.4 geese; sheep 1-2 short on the M&M tree), with 6-7k LESS cash at handover than our Boey tree (SE quadrant 4000 + more animals).
Divergence / rescue firing (per game): o3e 0.5 rescued units (10/48 games, d6-8), 2.8 land retries; o3d 1.8 (32/48, d7/9/10), 8.8
land retries; o3m 2.5 (30/48, d4-10), 7.9 land retries (cash-short BUY_LAND). Tape switches/game 1.9-2.4 (d3/d6).
Executor acceptance (explicit test): no crash / no error in 918 games, all DONE/DONE; at d15 the executor has filled the SE quadrant
(tiles 98 vs 75 on v183ms) - but with WHEAT (33-39 wheat tiles vs 19-23; top-3 put tomatoes/strawberries there: 25/2/12/33/3 at d15)
and keeps the tape's ~6.6 tomatoes without adding any.
WHERE THE LOSS IS: own final only -1..-7k vs v183ms's own, but the OPPONENT gains +6..+12k (113.9k vs 101.8k for o3e). Own revenue:
wheat -28..-30k (467-580 units sold vs 1318), fertilizer sold -8k, tomato +2..+7.6k. I.e. our executor's wheat/fertiliser economy
collapses on the top-3 farm and the opponent's prices improve. The top-3 opening is built for THEIR d11+ play, not ours.
Tape judge: op_o3 / op_o3m / op_o3d / op_o3e / op_o5d / op_o5m dropped into bundle/build/<tag>/ (+JUDGE_ME) at 05:33 UTC.

Batch b2 (running since 05:30, 1443 games): later handover (d13 / d15 / d18: follow the top-3 tape further so the SE quadrant is
filled their way) and NO4 (top-3 tree but skip the 4th quadrant, +4k cash, 3-quad farm our executor knows), per opener M&M/DSM/DECEM.

## CHECKPOINT 2 (05:45 UTC) — b2 partial (n=23-24 per row, seeds 17601-17612 both seats), killed early for the dead rows
LATER HANDOVER IS DEAD: following the top-3 tape past d11 (blind tape in a different world) vs V183: d13 -17..-20k, d15 -22..-30k,
d18 -27..-35k (0-9% wins, all three openers). Killed after 24 games per row.
NO4 (top-3 tree, but no 4th-quadrant order once we hold 3 quadrants -> +4k cash, 3-quad farm) recovers most of the loss:
| cand | vs V183 win% | margin (se) | worst | own / opp final | d11 h0 quads / cash / C-S-G / W-S-M-T |
|---|---|---|---|---|---|
| v183ms | 68.8 | +745 (251) | -2613 | 102.5k / 101.8k | 3 / 9.1k / 7.9-3.1-5.6 / 22.6-24.9-4.9-0 |
| nm (M&M) | 29.2 | -2113 (2004) | -16545 | 97.0k / 99.1k | 3 / 6.6k / 7.9-3.7-3.9 / 14.5-23.8-5.8-2.7 |
| nd (DSM) | 33.3 | -3846 (1163) | -15987 | 104.8k / 108.6k | 3 / 5.4k / 7.3-6.1-5.3 / 19.8-16.7-6.0-3.2 |
| ne (DECEM) | 25.0 | -4817 (1247) | -18274 | 100.8k / 105.6k | 3 / 6.9k / 7.4-3.7-5.4 / 17.5-25.4-4.3-4.5 |
IMPORTANT BIAS in this self-play pool: v183ms vs V183 is a near-MIRROR for d0-d10 (both run the same Boey tape, same seed -> the same
market orders on the same steps; both farms ~102k). Any opening that leaves the mirror stops colliding with V183's orders, and V183's
score rises (+4..+12k in every row, own score moves -5..+2k). So the fresh-seed pool vs V183/v183ms structurally penalises ANY
non-Boey opening; the top-field tape judge (fixed top-field opponents) is the fair test of "play what the top 3 play". nd's OWN
score is +2.2k above v183ms's own. Tape judge: op_nm / op_nd / op_ne / op_n5d added to bundle/build at 05:44.
b3 running (990 games): NO4 remaining seeds + n5m/n5d/n5e (top5 lib) + NO4 with handover d10 (240) and d9 (216).

## CHECKPOINT 3 — VERDICT (05:55 UTC): the top-field opening WORKS as a tape tree but LOSES with our executor. v183ms stays better.
All numbers: fresh seeds, both seats, n=48 per row, pod env.run (actTimeout 1 s + overage), paired d = minus v183ms's game on the same
seed/seat/opponent. Selection seeds 17601-17624 (b1-b3, 25 variants); HOLDOUT 17625-17648 (untouched, 2 pre-chosen variants).
| cand | set | vs V183 win% | margin (se) | worst | paired d vs v183ms (se) | vs v183ms win% | margin (se) | worst | own / opp final | peak step |
|---|---|---|---|---|---|---|---|---|---|---|
| v183ms | sel | 68.8 | +745 (251) | -2613 | 0 | mirror | 0 | | 102.5k / 101.8k | 0.44 |
| o3e (DECEM tree, 4 quads = pure top-3) | sel | 4.2 | -13143 (1397) | -34753 | -13888 (1422) | 4.2 | -15479 (1320) | -36099 | 100.7k / 113.9k | 0.46 |
| o3m (M&M tree, 4 quads) | sel | 10.4 | -12104 (1430) | -31147 | -12848 (1428) | 12.5 | -14624 (1585) | -37698 | 95.9k / 108.0k | 0.71 |
| o3d (DSM tree, 4 quads) | sel | 22.9 | -7620 (1602) | -24980 | -8364 (1534) | 12.5 | -10343 (1433) | -22802 | 101.3k / 108.9k | 0.52 |
| nd (DSM tree, NO4) | sel | 39.6 | -2816 (1070) | -18146 | -3561 (1048) | 25.0 | -4183 (992) | -18464 | 106.6k / 109.4k | 0.58 |
| n5d (DSM opener, top5 lib, NO4) | sel | 52.1 | -592 (1087) | -27641 | -1337 (1098) | 37.5 | -2402 (1020) | -25827 | 109.7k / 110.3k | 0.93 (1 step) |
| v183ms | HOLD | 66.7 | +1215 (286) | -3411 | 0 | mirror | | | 107.4k / 106.1k | 0.39 |
| **n5d** | HOLD | 39.6 | -1547 (726) | -11528 | **-2762 (826)**, 14/48 better | 35.4 | -2551 (869) | -13552 | 103.7k / 105.2k | 0.40 |
| nd | HOLD | 37.5 | -6440 (1353) | -25938 | -7655 (1433), 14/48 | 31.2 | -7097 (1373) | -26353 | 99.1k / 105.6k | 0.37 |
Other rows (sel, vs V183 paired d vs v183ms): nm -5673, ne -7354, n5m -5586, n5e -7221; NO4 + handover d10 (240): nm10 -6898, nd10 -4027,
ne10 -5819; handover d9 (216): nm9 -15807, nd9 -3848, ne9 -16253; handover d13/d15/d18 -17..-35k; +switch at d9 = no change.
Full tables: out/b1_report.txt, `python report.py out/b2`, `python report.py out/h1`, `python d10.py out/<set> V183`.

Reading:
1. The tree does what was asked: d0-d10 follows the top-3 recorded play keyed by shops; the d11 farm matches the recorded top-3 farm
   (o3e: 4 quads, 8.0/4.0/7.4 C/S/G, 28 wheat / 24.5 straw / 4.3 melon / 6.8 tomato, 3.2k cash vs recorded DECEM 4 / 8.1-5.6-7.8 /
   29-22-5.5-10.6 / 3.4k). Tape divergence is modest for DECEM (0.5 rescued units/game, 10/48 games) and larger for DSM/M&M
   (1.8-2.5 units/game in 30/48 games; 8-16 cash-short BUY_LAND retries/game). The executor ACCEPTS the 4-quadrant/tomato farm
   (0 errors in ~4,500 games, all DONE/DONE) but plays it badly: it fills the empty SE quadrant with wheat (33-39 wheat tiles at d15
   vs the top-3's 25 wheat / 12 tomato / 33 straw), never adds tomatoes, and its wheat/fertiliser selling collapses (own wheat revenue
   -28k, fertiliser -8k gross). The 4th quadrant alone costs ~8-10k/game in our hands (o3* vs n*).
2. Following their tape LONGER (d13-d18) is far worse (-17..-35k): a blind tape in another world collapses. Earlier handover (d9/d10)
   is not better than d11.
3. Best variant n5d (holdout -2.8k paired vs v183ms, 14/48 better; 39.6% vs V183) is still clearly below v183ms. Its tree mostly
   follows Vadim (#3 public LB) / Victor tapes from d3 (44/48 holdout games), 3 quadrants.
4. BIAS (read before judging): v183ms vs V183 is a d0-d10 MIRROR (same Boey tape, same seed -> identical orders on identical steps).
   Every non-Boey opening lets V183's score rise (+4..+12k); own-score deltas are smaller (n5d holdout own -3.7k, sel +7.2k).
   The fair test of "play what the top 3 play" vs the top field is the tape judge; op_o3e / op_o3m / op_o3d / op_nd / op_nm / op_n5d are
   queued in bundle/build (JUDGE_ME files) - read tapejudge/REPORT.md blocks "b_op_*".
5. Peak step: 11 steps > 0.5 s in ~4,500 LIB3 games, all at executor h0 planning steps (d15-d24), max 0.93 s (n5d, one step);
   v183ms max 0.44 s in the same pool. The executor's h0 plan is slower on these farms. Holdout max 0.40 s.

RECOMMENDATION: do NOT replace v183ms's opening with the top-3 tape tree unless the tape judge shows a gain vs the top field; on
fresh seeds every variant is -1.3..-14k paired. The top-3 opening only pays with a d11+ executor that plays the 4-quadrant/tomato
farm the way they do (SE quadrant into tomatoes/strawberries, not wheat) - that is a circuit change (bundle agent's lane), not a prefix.

## DELIVERABLES
- Candidate (best of the top-field openings): n5d = research/claude/2900/agents/final30/opening3/build/n5d/main.py
  main.py sha256 8dbfc703107d95d20a590f3618b192f66c263b6562a62d537366bfdb42454c5d
  build/submission-n5d.tar.gz sha256 16a42653d8ecbb90c1a7bcbf35eb379c6f5fd553925c2fa60b1d57f48aa27e75 (main.py only, mtime 0)
  Loader test (hybrid/loadtest.py on the pod, kaggle-environments 1.32.7): callable agent, 30 steps, peak 0.117 s, ACTIVE/ACTIVE.
- Pure top-3 (only M&M/DSM/DECEM tapes, DSM opener, NO4): nd = build/nd/main.py sha256 ca751018801ffe1b1438ab7f44bcf8b864fdfc0be063645a3e9ac0cfc9ca032c,
  build/submission-nd.tar.gz sha256 d77dc4642a8c2dbf1ca5e3c389f75334f8f5417628c796e50ee3eee6bd20db88, loader test peak 0.101 s ACTIVE/ACTIVE.
- Fully top-3 incl. SE quadrant: o3e (DECEM) build/o3e/main.py, o3m (M&M), o3d (DSM) - not packaged (-8..-14k).
- Engine for every game: kaggle-environments 1.32.7 (pod venv, Python 3.12).
- MERGE NOTE for the coordinator: opening3 patches ONLY the outer ctrl of v183ms (base micro/build/v183ms/main.py cba37327):
  adds `_LIB3_B64` + P flags LIB3 / T0_TEAM / Q4 / NO4 (+ diagnostics). The bundle agent's d10+ flags live in `_CIRC_B64`.
  To merge: `build_open3.patch(<bundle main.py text>, 'top5', {'LIB3': True, 'NO4': True, 'T0_TEAM': 'DSM'})` - the patch asserts on
  outer-ctrl strings only, so it applies to any v183ms-derived main.py whose ctrl is unchanged. Parity (flags off) = exact (3/3 digests).

## What was NOT done
- No upload. No laptop simulation (only single agent() calls on a step-0 observation; all games on pod 2lbkuyobkcs3tn, now DELETED).
- The playbook's price conditions (PLAYBOOK.md) were not used as tree keys; the tree keys on shops (d3/d6, d9 tested = no change).
- playbook/tapes_all.json (108 farms) not used; my lib = fieldnow/replays farms of M&M/DSM/DECEM (37) + Vadim/Victor (22) - the same
  replays. No executor (circuit) change to exploit the 4th quadrant / tomatoes (not my lane; measured cost of not doing it ~8-10k).
- No tape-judge numbers yet in this report (queued); no Majkel judge.

## CHECKPOINT 4 (06:15 UTC) — TOP-FIELD TAPE JUDGE confirms: worse than v183ms vs the current top field too
tapejudge (123 current top-12 tapes, candidate live in the other seat; tapejudge/out/b_op_*.score):
| build | wins | intact | intact-only margin (se) | paired vs v183ms all (se) | paired both-intact (se), n | own / opp paired | peak step |
|---|---|---|---|---|---|---|---|
| v183ms | 64/123 | 84 (68%) | -1937 (1689) | 0 | 0 | | 0.434 |
| op_n5d | 26/123 | 107 (87%) | -8014 (1523) | -16926 (4658), 33/90 | **-6256 (1654)**, n=76 | own -11.8k / opp +5.1k | 0.388 |
| op_nd  | 29/123 | 106 (86%) | -7726 (1605) | -17124 (4652), 32/91 | **-6010 (1773)**, n=77 | own -11.8k / opp +5.4k | 0.391 |
(the all-games paired number is inflated by v183ms breaking more tapes; both-intact is the conservative one: -6.0..-6.3k.)
op_o3e / op_o3m / op_o3d (4-quadrant pure top-3) are still queued in the judge; on fresh seeds they are 5-10k worse than nd/n5d.
FINAL: the top-3 day 0-10 opening, handed to our v183ms executor at d11, loses ~3k (fresh-seed holdout) to ~6k (top-field tape judge,
both-intact) per game vs keeping the Boey tree. Not recommended for upload. Packaged anyway (n5d, nd) with loader tests, see DELIVERABLES.
Pod deleted 05:53 UTC. opening3 stops here (hard stop 06:50).

06:36 UTC: tape judge finished only op_n5d and op_nd. op_nm / op_o3d / op_o3e / op_o3m stayed at .score.tmp when my wait ended at 06:35 (the four builds I removed at 05:50 also left empty-SHA tmp stubs). Those four have no judge numbers; the verdict above is unchanged.
