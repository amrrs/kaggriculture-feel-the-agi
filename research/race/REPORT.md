# final30/race — premium-market race hypothesis (REPORT, updated at each checkpoint)

## CHECKPOINT 1 (premise, 2026-09-29 ~23:00 UTC) — hypothesis mostly KILLED; one fragment (same-day sale) kept for one cheap test

Data: the 69 beta engine-replayed ledgers of Codex V183 56641767 live games (beta/led/*.json: exact executed units and unit prices
from the engine's _commit_unit, per-day plant/fertilize/accrue/harvest per farm; rewards reproduced 69/69) + the 50 raw replays in
beta/replays (market inventory per step, per-farm inventories -> harvest steps). Losses vs >= 2600 opponents: n=37 (ledger), 33 with a
raw replay (counterfactuals). v183ms has 0 public games vs >= 2600 yet (pairselect/games.json); it runs the same day 0-10 tape and the
same planting/fertilizer/sell logic as V183 (micro only re-routes), so V183's numbers stand for it. fieldnow/replays is empty.
Scripts: premise.py (tables), hours.py (sales by day x 3h block), lag.py (FIFO harvest->sale lag), cf_sameday.py / cf_prefix.py
(market counterfactuals: lockstep re-pricing with the engine's market_price and the recorded town consumption; recorded-stream
re-pricing error <= ~$0.2k/game/product, symmetric).

### Numbers (per game, losses vs >= 2600, n=37, mean margin -9.9k)
| measure | us (V183) | opponent |
|---|---|---|
| first strawberry planting day | 3.35 (d3 24/37, d4 13/37) | 2.11 (d2 34/37) |
| strawberry tiles on d4 / d5 / d6 / d8 (main wave planted d6 by both) | 2.2 / 3.6 / 3.9 / 18.7 | 5.8 / 7.7 / 8.2 / 20.5 |
| FERTILIZE on strawberry (whole game) | 58.6 | 56.9 |
|   ... on the main-wave production days d15 / d19 | 14.4 / 13.5 | 12.4 / 10.1 |
| strawberry units produced on d15 / d17 / d19 / d21 (2 per fertilized tile) | 32 / 35 / 34 / 40 | 30 / 31 / 27 / 27 |
| strawberry produced / sold / avg price / revenue | 237 / 237 / $114 / 26.96k | 216 / 214 / $140 / 29.93k |
| strawberry sold by end of d18 (the $160-210 window) | 52 | 80 |
| harvest->sale lag, strawberry: same day / next day / 2+ days | 23 / 214 / 0.5 | 56 / 136 / 22 |
|   milk | 66 / 125 / 0 | 87 / 81 / 14 |
|   wool | 60 / 85 / 0 | 80 / 48 / 12 |
|   melon | 35 / 30 / 1 | 58 / 15 / 3 |
| revenue gap us - opp: strawberry / milk / wool / melon / tomato | -3.0k / -1.2k / -2.6k / -1.2k / -7.5k | |

Engine facts checked (kaggriculture.py): strawberry produces at the end of days p+9, p+11, p+13, p+15 (harvestable next morning);
FERTILIZE on day d covers d..d+2, so FERT at ages 9 and 13 doubles all four productions; harvested units sit in the unit's
inventory until the unit DROPs/PLACEs at the shed or the end-of-day auto-drop, and SELL only takes shed units -> without a
mid-day drop a wave harvested on day d sells at d+1 h0.

### Verdict per part of the hypothesis
(a) Fertilizer on the first waves: ALREADY DONE. V183 fertilizes strawberries at least as much as the >= 2600 opponents and on the
    right days (d15/d19 = ages 9/13 of the d6 wave); its main-wave productions are 2 units/tile and exceed the opponents' (+5..13
    units per wave). Also melon: fertilizer only brings the harvest forward ~1 day (window crop, 6-unit cap). Nothing to build.
    (Same finding as exec-circuit-3 section 2: 'v8 already fertilizes every production-day strawberry'.)
(c) Planting day: the opponents' first strawberry tile is on d2, ours d3-4, but it is 2-4 tiles; the main wave (11-15 tiles) is
    planted on d6 by both farms, so there is no one-day head start on the 30 tiles. Cost of our current planting day measured
    (cf_prefix.py: our first 12 / 24 early-tile units sold 24 steps earlier): -62 / +188 margin per game. The scarce side is sqrt
    and flat (every early unit sells at ~$190-210 either way). The opponents' early edge is VOLUME (7.7 vs 3.6 tiles by d5, +15
    units in d11-14) from their tape, not timing; our day 0-10 part is a recorded tape tree (calendar openings are CLOSED).
    Not built, as the brief allows.
(b) Same-day sale of the waves (the only part with money in it): opponents sell 33 more strawberries, 21 milk, 20 wool, 23 melon
    per game on the harvest day; we carry everything to the overnight auto-drop and sell at h0 next morning (17-19 units per wave at
    d17/d19 h0). Counterfactual (cf_sameday.py, n=33, oracle, labour FREE, opponent's sales fixed):
      sell each next-day unit at harvest step + 2 : margin +2.38k/game (straw +1.66k, milk +0.35k, wool +0.33k, melon +0.05k)
      harvest step + 4                          : +1.85k (straw +1.22k, milk +0.31k, wool +0.29k, melon +0.04k)
      at h18 of the harvest day                 : +2.38k;  at h22 of the harvest day: +1.73k
    Split: our own revenue only +0.2..0.3k; ~85 % of the margin is the opponent's lot re-quoted after ours (first-mover on the
    linear strawberry glut). Upper bound ~1.7-2.4k, i.e. at/below the 2k kill line BEFORE labour.
    History: every same-day delivery implementation on earlier executors lost more labour than this bound: exec-circuit-3 prem15 /
    prem_hi -1.3..-7k, premret -12.6k (8-game screens); lateexec MIDDROP -1.2k (30 games); Fable DAWN_LOOP -1.9k, PREM_LOOP -6..-14k.
    New fact found here: in the v183ms circuit, ANY loop (PREM_LOOP / DAWN_LOOP) switches the micro optimiser OFF for that day
    (`if P['OPT_ROUTE'] and day < LAST_DAY and not loops:`, same for OPT_HIRE / FILL / XFILL) -> a flag-only test on v183ms would
    turn off the one lever that works exactly on the strawberry days. So the only untested form is 'dawn loop + micro routing'.

Decision: (a) and (c) killed; the headline '+4k head start / +3k fertilizer' is not supported (measured +0.2k / 0). I keep (b) for
ONE cheap test only because the loop-disables-micro gating is new and the patch is small: flag LOOP_MICRO lets OPT_ROUTE run with
the loop unit's reduced budget; variants = DAWN_LOOP (price-gated) and a prem_hi-style PREM_LOOP (price >= threshold, <= 2 loops,
dist <= 4), both + LOOP_MICRO. Expectation stated in advance: <= +0.5k vs v183ms, likely negative.

### Coordinator addendum (fieldnow facts) answered
- Fertiliser: agreed, not a gap (my numbers above: we fertilise strawberries as much as the opponents; melons: nobody). 2(a) dropped.
- Is the d0-10 play a calendar or a tape? A RECORDED TAPE TREE: the ctrl in v183ms/V183 main.py (reactB) follows one of 102 recorded
  Boey games (lib = _LIB_B64, actions steps 0..287), switching at h0 of d3/d6 only to a recording with the identical day-start layout
  (tile codes + planting days). Library tally per game: d2 = BUY GOOSE orders 3.6 / BUILD_COOP 2.06 / PLACE GOOSE 2.06 / melon 3.3 /
  strawberry 0.01; d3 = strawberry PLANT 2.45; d4 1.73; d6 13.4.
- The day-2 swap IS mechanical: the ctrl already has Fable's OV_STRAW overlay (tape BUY_ANIMAL of OV_KINDS on OV_DAYS -> BUY_SEED
  STRAWBERRY, tape BUILD_PASTURE/COOP -> PLANT STRAWBERRY while seeds are held; RESCUE waters until the handover). Re-aimed with one
  ctrl line: sw2 = {OV_STRAW 2, OV_DAYS [2], OV_KINDS [GOOSE]}, sw3 = OV_STRAW 3. Probe (pod, seed 17301 seat 0 vs v183ms): sw2 plants
  2 strawberries on d2 (+3 on d3), sw3 2 on d2 (+5 on d3), baseline 0 on d2 / 4 on d3. CAVEAT seen in the probe: the changed layout
  makes the d3/d6 tape switch pick different recordings (baseline 11 sheep / 2 geese at d9; sw2 3 sheep / 6 geese) - the swap
  re-routes the whole opening, as Fable found ('prefix can only be replaced, not edited'). Batch decides (running).

## CHECKPOINT 2 (build + first batch, 2026-09-29 ~23:05 UTC)
Pod 1k48x80k6yq6ml (cpu5c 32 vCPU, AMD EPYC 4564P; self-destruct armed 22:23:09 UTC + 14000 s; PODS.txt). Harness = game.py
(microbudget's env.run harness: actTimeout 1 s + overage exactly as Kaggle, per-step time, action digest) + per-product SELL revenue
per farm (engine _commit_unit wrapper). runq.py: one pinned process per game, 32 concurrent (both SMT siblings busy = the load case).
SEEDS: 17301-17348 both seats (NOT 17101-148: microbudget's jobs_p1.txt already uses 17101-17115; 17301+ is used by nobody).
Builds (build_race.py, patch on the embedded circuit of v183ms cba37327, flags default off):
  r0 = patch, flags off: PARITY EXACT vs v183ms on 17301/17302/17303 (identical per-step action digests 72128e5c / 7a55b425 / d02236d8,
  identical rewards); lx3m port l0: digests identical to lx3m on the same 3 seeds (e39e8e66 / d76eedc8 / 31892beb). Patch is mechanical.
Batch 1 (n=96 per row = 48 seeds x 2 seats; paired d = same seed/seat minus v183ms's game; worlds diverge after any layout change
because shop draws share the weed RNG, so pairing only removes seat/seed luck):
| cand | vs V183: win% | margin (se) | worst | paired d vs v183ms (se) | vs v183ms: win% | margin (se) | worst | step max |
|---|---|---|---|---|---|---|---|---|
| v183ms (base) | 75.0 | +987 (158) | -2871 | 0 | 48.4 (mirror) | -10 (43) | -2082 | 0.50 |
| rd  (DAWN K4, loop<=18, straw>=100, LOOP_MICRO) | 62.5 | +333 (197) | -4648 | -655 (259) | 39.6 | -717 (173) | -6622 | 0.51 |
| **rd8** (DAWN K8, loop<=24, straw>=100, LOOP_MICRO) | **84.4** | **+1865 (188)** | -2365 | **+877 (216)** 62/96 | **59.4** | +103 (195) | -5277 | 0.38 |
| rdn (DAWN K4 without LOOP_MICRO = parent gating) | 30.2 | -1216 (179) | -5457 | -2203 (232) | 12.5 | -1880 (168) | -5484 | 0.37 |
| rp  (prem_hi PREM_LOOP k2 d4 p100, LOOP_MICRO) | 63.5 | +565 (158) | -2516 | -423 (175) | 29.2 | -946 (186) | -6762 | 0.40 |
- rdn confirms the gating fact: a loop day without micro costs ~2k/game (that is what refuted DAWN_LOOP before, -1.9k on f3).
- rd8's own strawberry revenue vs V183 +1.57k/game (opp +0.29k); vs v183ms +0.48k own, -0.54k opp.
- Day-2 swap (partial, n=40 each): sw2 paired -1.8k (se 0.6) vs V183 / -2.2k (0.7) vs v183ms, win 57.5% / 32.5%; sw3 -4.4k / -4.2k, tail
  -32k. The swap re-routes the tape tree (different recordings from d3) and loses eggs/milk; KILLED (final numbers below).
Round 2 running: rd8 neighbourhood (rd12, rd16, rd8a price>=0, rd8b price>=150, rd8c loop<=30) + lx3m port ld8 vs lx3m, same seeds;
then a HOLDOUT on untouched seeds 17401-17448 for the chosen variant vs v183ms, V183 and the 2900-bar anchors (lx1, lx3, hybrid, r9).

### Round 2 (same seeds 17301-17348, n=96 per row) — rd8 is an isolated peak, neighbours are not better than v183ms
| cand | vs V183 win% | paired d vs v183ms (se) | vs v183ms win% | paired d (se) | worst vs v183ms |
|---|---|---|---|---|---|
| rd8  (K8, loop<=24, >=100) | 84.4 | +877 (216) | 59.4 | +113 (192) | -5277 |
| rd8b (K8, loop<=24, >=150) | 76.0 | +530 (259) | 53.1 | -107 (184) | -5277 |
| rd8a (K8, loop<=24, >=0)   | 68.8 | +198 (225) | 33.3 | -636 (169) | -5380 |
| rd8c (K8, loop<=30, >=100) | 57.3 | -335 (252) | 47.9 | -318 (198) | -4732 |
| rd12 (K12, loop<=30)       | 64.6 | -333 (203) | 47.9 | -102 (180) | -5788 |
| rd16 (K16, loop<=30)       | 69.8 | -219 (198) | 49.0 | -92 (185) | -5788 |
| sw2 (day-2 swap, final)    | 45.8 | -2711 (536) | 24.0 | -2706 (504) | -24506 |
| sw3                        | 32.3 | -4367 (756) | 20.8 | -4629 (707) | -32347 |
| lx3m port: ld8 vs lx3m     | 38.5 (lx3m 30.2) | +175 (235) vs lx3m | 17.7 (lx3m 10.4) | +350 (247) vs lx3m | -7361 |
Reading: the price gate matters (>=0 loses 0.6k vs v183ms: loops on crashed-price days waste the farmer); loop length > 24 or K > 8 is
flat-to-negative. rd8's advantage over its neighbours (~+0.3..1.2k vs V183) is larger than their se would suggest for a smooth knob ->
treat rd8's first-batch numbers as partly selection luck. The lx3m port is mechanical and neutral-to-slightly-positive vs lx3m, but
lx3m itself is far below v183ms on these seeds (10% vs v183ms), so no lx3m variant is a candidate.
PRE-DECLARED (before the holdout): rd8 replaces v183ms as our candidate only if on the untouched holdout seeds 17401-17448 (n=96 per
pair) its paired margin vs v183ms is > 0 by >= 2 se AND its win rate vs v183ms is > 55% AND it is not worse than v183ms vs any anchor
(V183, lx3, lx1, hybrid, r9) by more than 1 se, with no new tail < -15k and peak step < 0.6 s. Otherwise: v183ms stays.
Holdout running: {rd8, rd8b, v183ms} x {v183ms, V183, lx3, lx1, hybrid, r9} x 48 seeds x 2 seats = 1728 games.

## CHECKPOINT 3 — FINAL VERDICT (2026-09-29 23:10 UTC): nothing clearly beats v183ms; keep v183ms. Pod deleted.
HOLDOUT (untouched seeds 17401-17448, both seats, n=96 per row; paired d = minus v183ms's game on the same seed/seat/opponent):
| opponent | v183ms win% / margin (se) | rd8 win% / margin | rd8 paired d (se) | rd8b win% / margin | rd8b paired d (se) | 2900-bar win% |
|---|---|---|---|---|---|---|
| v183ms | 50.0 / 0 (59) | 55.2 / +276 | +276 (153), 54/96 better | 66.7 / +379 | +379 (145), 65/96 | - |
| V183   | 74.0 / +1126 (171) | 74.0 / +1165 | +39 (214) | 74.0 / +1180 | +53 (212) | 75 |
| lx3    | 90.6 / +3147 (239) | 94.8 / +3196 | +49 (289) | 90.6 / +3276 | +130 (264) | 74 |
| lx1    | 95.8 / +5189 (324) | 95.8 / +4639 | -550 (258) | 94.8 / +4698 | -491 (291) | 67 |
| hybrid | 87.5 / +2383 (234) | 85.4 / +2313 | -70 (241) | 83.3 / +2291 | -92 (234) | 72 |
| r9     | 100 / +7796 (319) | 100 / +7805 | +9 (250) | 100 / +7961 | +164 (266) | 68 |
worst game (all holdout rows): v183ms -3649, rd8 -2939, rd8b -3046 (no tail < -15k). Peak step under 32-way load: rd8 0.547 s,
rd8b 0.386 s, v183ms 0.404 s (none > 0.6 s; p99 <= 0.25 s). All 4,416 games DONE/DONE.
- Pre-declared rule for rd8: paired vs v183ms +276 = 1.8 se (needs >= 2 se) -> FAIL; win 55.2% (> 55% barely); vs lx1 -550 = 2.1 se
  worse -> FAIL. rd8's first-batch +877 vs V183 did not replicate (+39): it was selection luck among 7 neighbours.
- rd8b (price gate >= 150; NOT the pre-declared candidate): holdout +379 (2.6 se), 66.7% vs v183ms, but -491 (1.7 se) vs lx1 -> also fails
  the anchor clause; on the selection seeds it was -107 (184) vs v183ms. Pooled 192 games: rd8b vs v183ms +136 (118), 59.9% win;
  vs V183 +292 (168), 75.0%. rd8 pooled (includes its selection batch, biased up): vs v183ms +194 (123) 57.3%; vs V183 +458 (155) 79.2%.
- Against the 2900 bar (final29/DECISION_RULE.md: V183 >= 75%, lx3 >= 74%, lx1 >= 67%, hybrid >= 72%, r9 >= 68%): v183ms, rd8 and rd8b all
  pass lx3/lx1/hybrid/r9 easily on this pool and all sit at 74% vs V183 on the holdout (bar 75%). None clears the bar more clearly than
  v183ms does; the variants are v183ms-equivalent within noise with a small (+0.1..0.4k, 1-2.6 se) edge in the direct head-to-head only.
- Mechanism check (per-product, holdout vs v183ms): rd8's dawn loop moves the OPPONENT's strawberry revenue -1.16k/game (rd8b -1.05k)
  while ours is flat (-0.1k) - exactly the first-mover effect the counterfactual predicted (~85 % of the value is the opponent's price)
  - but the farmer's lost work elsewhere eats most of it, leaving +0.3..0.4k.
Candidate package (only if the coordinator wants the small head-to-head edge; NOT recommended by the pre-declared rule):
  rd8b  = research/claude/2900/agents/final30/race/build/rd8b/main.py  sha256 391c084d20f4b6ef2cc3d2f270aabfc541e7a6501d5aef59a3f713e5b9cd1d21
  rd8   = build/rd8/main.py sha256 c8b00b0983e956dbc7854147fa7d4d256510ecb336b25f41350567de0478c042;
          packaged build/submission-rd8.tar.gz sha256 aac7448a9cad6ff935ace01fd30fad59eaf2ad3e00db68119287cc3d9efba0b9 (main.py only, mtime 0,
          like submission-v183ms.tar.gz); loader test (hybrid/loadtest.py on the pod, kaggle-environments 1.32.7): callable agent, 30 steps,
          peak 0.299 s, status ACTIVE/ACTIVE. rd8b can be packaged the same way: python pack.py rd8b (loader test not run for rd8b).
  Engine for every game: kaggle-environments 1.32.7 (pod venv, Python 3.12), env.run with actTimeout 1 s + overage.

## What was NOT done
- No upload, no laptop simulation (all 4,416 games + probes on pod 1k48x80k6yq6ml; laptop work = JSON parsing of existing ledgers/replays).
- No tape-judge (final29/judge) or Majkel-judge run for rd8/rd8b; no live-set replay check. Only fresh-seed self-play pool.
- The fieldnow 'bundle' (SE quadrant d10 + early tomatoes) and any rewrite of the tape tree: not attempted (closed classes / not a last-day item).
- lx3m port (ld8) built and batched only on the selection seeds (+175 / +350 vs lx3m, n.s.); lx3m itself is far below v183ms here.
- Fertilizer logic (hypothesis part a) not built: measured as already done.

## Files
premise.py / hours.py / lag.py / cf_sameday.py / cf_prefix.py (step 1), build_race.py (patch + variants, incl. sw2/sw3 ctrl overlay),
game.py / runq.py / probe.py / report.py / pack.py / loadtest.py, jobs_*.txt, out/b1 (2,688 games, selection seeds 17301-348),
out/h1 (1,728 games, holdout 17401-448), out/ps (parity/smoke), out/b1_report_*.txt, out/h1_report.txt, build/<tag>/main.py.
