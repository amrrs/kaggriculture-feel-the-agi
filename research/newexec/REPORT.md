# final30/newexec — from-scratch day-11+ executor (FINAL REPORT, 09:15 UTC 30 Sep; stopped by the coordinator)

## PASS BAR (declared before the final batch)
paired >= +1k vs v183ms on fresh seeds with z >= 2 AND >= 60% wins vs V183 AND top-field judge paired >= +1k AND worst game > -15k
AND peak step < 0.6 s. Anything short of this is FAIL.

## VERDICT: FAIL on every clause except peak step. Nothing from newexec should be uploaded. v183ms stays.
Final fresh-seed batch 17901-17912 both seats (n=24 per row; pod env.run, actTimeout 1 s + overage; kaggle-environments 1.32.7):
| build | opening (d0-d10) | vs V183 win% | margin vs V183 (se) | paired d vs v183ms (se), better | H2H vs v183ms win% / margin (se) | worst | own / opp | peak step |
|---|---|---|---|---|---|---|---|---|
| v183ms | Boey tree + old executor | 83.3 | +1258 (389) | 0 | - | -1438 | 101.5k / 100.2k | 0.388 s |
| **nxb** (best new executor) | Boey tree (v183ms prefix) | **0.0** | -35665 (2632) | **-36924 (2787)**, 0/24 | 0.0 / -37592 (2689) | -65330 | 82.7k / 118.4k | 0.213 s |
| nxe (same executor) | top-3 DECEM tree (o3e prefix) | 0.0 | -47576 (2822) | -48834 (2910), 0/24 | 0.0 / -49525 (2672) | -74615 | 86.6k / 134.2k | 0.224 s |
- paired +1k z>=2: MISS (-36.9k, z -13). >= 60% vs V183: MISS (0%). worst > -15k: MISS (-65k). peak < 0.6 s: ok (0.22 s).
- Top-field tape judge: NOT run. At -37k on fresh seeds it cannot reach +1k; no JUDGE_ME was written so judgerun's pod stayed free
  for the microstructure candidates.
- Executor effect isolated on OUR opening: -37k/game. The top-3 opening costs a further -12k with this executor (nxe vs nxb).
- Seed/seat caveat: n=24 counts both seats; mirror games make the naive se ~20-40% too small. Irrelevant at z -13.

## Where the ~37k goes (nxb vs v183ms, both vs V183, same 24 fresh games, per game)
| line | old executor (v183ms) | new (nxb) | own delta | opponent delta |
|---|---|---|---|---|
| wheat | 1338 u / 45.7k | 1163 u / 41.0k | -4.7k | +4.2k (opp 36/u vs 34/u) |
| fertiliser | 341 u / 19.9k | 206 u / 15.1k | -4.8k | +3.0k |
| tomato | 42 u / 5.9k | 13 u / 2.4k | -3.5k | +0.2k |
| milk | 209 u / 23.1k | 183 u / 21.0k | -2.0k | +4.9k (opp 137/u vs 111/u) |
| egg | 263 u / 11.3k | 224 u / 9.7k | -1.6k | 0 |
| carrot | 112 u / 4.6k | 74 u / 3.5k | -1.1k | -1.3k |
| wool | 129 u / 14.3k | 106 u / 16.5k | +2.2k | **+8.1k** (opp 158/u vs 113/u) |
| strawberry / melon | 234 / 66 u | 255 / 66 u | +0.3k / 0 | +0.2k / 0 |
| purchases (wheat, fert, seeds, animals) | | | -1.1k | |
| **total** | | | **-16.4k** | **+19.2k** |
Mechanisms (from per-day ledgers in out/*/*.json: `sday_me`, `dstat`, `nxlog`):
1. **Supply volume vs the rival.** Every lever that raised our own revenue raised V183's more (table below): holding premium goods for a
   price (s1-s4: own +2k, opp +4..8k), keeping a feed reserve (y4: own +3.7k, opp +11k), fewer hands (r2: own +5k, opp +17k), extra
   animals eating our wheat (y2/y3: opp +6..10k). The one clearly positive change was selling everything at once (t8: +4.0k, 8/8).
   "Selling is denial, holding is a gift."
2. **Wheat volume.** The new executor sells 888-1163 wheat vs 1227-1338 and, on some seeds, buys feed at ~39 while the old one buys
   seeds at 10 (17705: new buys ~250 wheat after d11 at ~38, old ~150 seeds). V183 sells ~1300 wheat/game, so our wheat supply is the
   biggest denial lever against it.
3. **Herd.** 16.7 animals/day d11-27 vs 20.5: the old executor keeps buying animals after d11 (ours frozen per the playbook) and we
   lose 1-3 to escapes. Fewer animals = less milk/wool/egg/fertiliser supply -> opponent's wool +8.1k, milk +4.9k.
4. **Not coverage.** Per animal/plant our coverage is equal or better (fed 0.89 vs 0.85, cared 0.88 vs 0.80, watered 0.58 vs 0.58),
   with more walking: 296 unit-steps/day, 137 moves, 149 actions vs 269 / 101 / 156. 13 hands instead of 12 changed nothing (u4, z5).
5. The old executor is 3,567 lines (route 2-opt + micro-opt, MPC sell-queue/hold plans with opponent-supply forecasts, projected-margin
   allocation, herd additions, wheat churn); the gap is its market timing and volume, which a ~650-line greedy does not reproduce.

## Architecture (nx.py, ~650 lines, pure python, 0.1-0.2 s/step peak)
- Stateless per step: everything read from obs (tiles, shed, seeds, inventories, prices, market inventory, shops, hands); memory =
  per-unit target (stickiness), per-day zone map, a daily log.
- Tasks with coin values: animals FEED (needs carried wheat; 20 + product price if care still pays + care bank on production nights +
  400 if unfed yesterday), CARE (product price x CARE_K), HARVEST (yield x price, + overflow value before a production night), COLLECT
  (fertiliser value); crops WATER (must-water = plant value, in-window yield +1/+2, fert production nights), HARVEST (ready one-time
  crops, ongoing yield), FERTILIZE (exact engine gain over the 3 fertilised days), DIG/PLANT per the crop plan; shed pseudo tasks
  FETCH wheat / fertiliser / bought animal, DROP (PLACE the largest stack, never overflowing).
- Feed/care gated to production nights <= d28 (VT1: no feed/care on d29; care only if a later production night exists).
- Dispatch: 13 angular zones around the shed balanced by workload (recomputed at h0); a unit scores its zone's tasks (triage: keep the
  highest-value tasks that fit in the hours left, then nearest-first), helps other zones only when its own is empty; greedy matching,
  one unit per task.
- Crop plan (VPLAN): each free tile gets the crop with the best coins per tile-day at current prices, within caps keyed on shop
  demand (strawberry 30+6*dS <= 44 until d14, tomato 10.5+6.8*dT until d18, carrot 10+8*dC from d11, wheat filler until d27);
  seeds bought just in time with a buffer for tiles ripening today.
- Market: sells first in the order book, then hires (8 at h0 + 4 at h1), then buys; premium sold as soon as it reaches the shed
  (SELL_ALL), wheat above the remaining feed need in lots <= 10, fertiliser surplus at once, no fertiliser buying, wheat bought only
  when today's feed is short; shed-pressure courier from h15 and shed-room sells from h19 before the midnight auto-drop; d29 dump.
- Optional (off in nxb): HERD (buy -> fetch -> place on empty/new structures), PX (price-threshold holding), DRIP, TRACE.
- build.py embeds nx.py (zlib+b64) into a base outer main.py and replaces the `step >= HANDOVER` branch with nx.act (exceptions ->
  PASS for all units, counted in nx S['err']; 0 errors in ~900 games).

## All rounds (n=8 unless noted: seeds 17701-17704 or 17701-17702+17705-17706, both seats, vs V183)
| round | build | change | margin vs V183 (se) | own | opp | paired (se) |
|---|---|---|---|---|---|---|
| a | v1 / v1b | greedy dispatch, no zones (top-3 / our opening) | -68.9k / -59.7k | 70.7k / 78.4k | 139.6k / 138.1k | -69.6k / -60.4k vs v183ms |
| b | v2 | + 13 workload zones | -76.5k | 79.5k | 156.0k | -77.2k vs v183ms |
| c-h | v3-v8 | LAM/OUTPEN, fertiliser collection+buy, strict zones + idle help, ratio scoring, care needs wheat, triage | -55..-80k | 64-80k | 125-158k | |
| i-k | v9, p1-p4, q1-q4 | seed buffer, wheat-only plan (worse, -76k), sell-all, shed courier; q4 = first run on our opening | q4 -37.3k (0.8k) | 85.1k | 122.4k | q4 -38.0k vs v183ms |
| l | r0-r7 (our opening) | care x2.5 / 9 hands / nearest-first / fewer premium / fert value | r3 -38.5k (2.5k) | 91.0k | 129.5k | r2 -8.9k, r5 -12.3k, others -4.1..+1.2k vs r0 |
| m | s1-s4 | price-threshold holding of premium goods | -40.7..-43.8k | 93-94k | 134-137k | -2.1..-5.3k vs r3 |
| n | t1-t9 | no fert buy; t8 = sell-all + wheat reserve 0.5 day | t8 -34.5k (2.4k) | 94.7k | 129.2k | t8 **+4.0k (1.0k) 8/8**; t9 +1.6k; t4/t5 (no tomato / no strawberry) -5.0k / -6.0k vs r3 |
| o | u1-u8 | wheat reserve 0 (u2), lots 40, 13 hands, more tomato/carrot/strawberry | u2 -33.0k (2.3k) | 96.6k | 129.6k | -0.9..+1.5k vs t8 |
| p | w1-w6 | crop by coins/tile-day at current prices; w6 + melons | w2(=nxb) -30.3k (1.8k) | 95.2k | 125.5k | +2.7k (1.9k) vs u2; w5 (top-3 opening) -15.2k; w6 -3.2k |
| q-r | x1-x3, y1-y4 | herd purchases (x: courier bug), feed priority, 1-day feed reserve | y1 -33.4k, y4 -37.7k | 99.2k / 98.9k | 132.5k / 136.6k | y1 -3.1k, y2/y3 -13.1k/-10.8k, y4 -7.4k vs nxb |
| s | z1-z7 | wheat lots 30, wheat price x1.5 in the plan, fert on wheat, 13 hands, fewer strawberries | -31.1..-36.3k | 91-98k | 127-132k | -0.8..-6.1k vs nxb |
| final | nxb / nxe (n=24, fresh 17901-17912) | best config on our / top-3 opening | -35.7k / -47.6k | 82.7k / 86.6k | 118.4k / 134.2k | -36.9k / -48.8k vs v183ms |
Full tables: `python rep.py out/<round> <ref_tag>` (rounds a..s, final). Per-game JSONs carry sales/buys per product, per-day ledgers
(`sday_me`: product_day -> [units, revenue, hour sum]; `B..` keys = buys), engine-level day stats (`dstat`: moves, actions, h23
animals/fed/cared/plants/watered/shed/money) and the executor's own day log (`nxlog`, incl. crop fates).

## What a future from-scratch controller must do differently
1. **Maximise sold volume, never hold.** Sell every premium unit the step it reaches the shed, wheat and fertiliser surplus at once;
   no feed reserve in the shed overnight (buy feed just in time at h0 instead). Holding for price only moves revenue to the rival.
2. **Wheat is the denial product against V183** (it sells ~1300/game): keep 35-45 wheat tiles cycling on the 4-day clock with
   same-step replant (seed buffer), fertilise wheat when fertiliser is surplus, never buy feed at 1.5x base when seeds cost 10.
3. **Keep growing the herd after d11** while production nights remain (old executor ~20.5 animals vs our 16.7): buy -> pick up from
   the shed -> place, with couriers that never drop animals back (the x-round bug) and no DIG of empty structures.
4. **Feed reliability**: 11% animal-days unfed and 1-3 escapes per game come from the shed being empty at h1; fetch at spawn for the
   whole zone, and treat FEED+CARE as one visit.
5. **Routing is secondary** (13 hands = 12 hands; coverage already equal); do not spend effort on it before 1-3.
6. Judge own AND opponent revenue per product in every experiment; own-revenue gains that raise the opponent's revenue more are losses.

## Commands (bench)
```
cd research/claude/2900/agents/final30/newexec; source /Users/1littlecoder/kaggriculture/.venv/bin/activate
python build.py <tag> --base v183ms|o3e --nxp '<json flags>'   # -> build/<tag>/main.py + META.json; nxb flags: build/nxb/META.json
python mkjobs.py jobs_x.txt <seed0> <nseeds> <tag> [...]       # vs V183 both seats (paths are pod paths under /work/kaggriculture)
bash mkpod.sh newexec "cpu5c 32" "cpu3c 32"; bash setup_pod.sh <ip> <port> 14000   # self-destruct armed first; engine 1.32.7
# on the pod (call /opt/venv/bin/python explicitly; the ssh PATH has no kaggle_environments):
/opt/venv/bin/python runq.py jobs_x.txt out/x 32               # one game per pinned CPU (game.py = bundle harness + ledgers)
/opt/venv/bin/python rep.py out/x <ref_tag>                    # per tag@opponent: win%, margin, own/opp, worst, paired d, peak, errors
python pack.py <tag>; /opt/venv/bin/python loadtest_full.py build/submission-<tag>.tar.gz 15101   # archive + full-game loader test
python dlog.py out/x/<file>.json                               # per-day coverage / sells of one game
```

## Deliverables (for the record only; FAIL the bar, not for upload)
- nx.py (executor), build.py, game.py, runq.py, mkjobs.py, rep.py, dlog.py, pack.py, loadtest_full.py, setup_pod.sh, out/ (~900 game JSONs).
- build/submission-nxb.tar.gz sha256 69ee691b3c4d18ddbe52d9730f9a22bccb36e09a4d7c216c6b6b92cac4d29345; build/nxb/main.py sha256
  8cae15453d2367e7c43637a574f2225cab28e4ddcffba1724e183f270d78e064 (v183ms outer file cba37327 + nx.py; flags in build/nxb/META.json).
- build/submission-nxe.tar.gz sha256 8d9521442feabce6e8562f55073867489bb6b73746da853744893a176ff3389d; build/nxe/main.py sha256
  5e82921166305b224ac4e51b7bf8c44ed706c2fdc04175be9f488b5d7812dc2c (o3e outer file + nx.py).
- Loader test (pod, kaggle-environments 1.32.7): archive -> get_last_callable -> full 720-step games vs 'random': nxb seeds 15101/15102
  DONE/DONE, 168.1k / 102.7k, peak 0.127 / 0.131 s, executor errors 0; nxe 15101 DONE, 155.9k, peak 0.093 s, errors 0.
- Pod rb9qlasnm5mj9q (cpu3c 32 vCPU) created 08:00, self-destruct armed 08:01 (+14000 s), DELETED 09:09 UTC (REST 204 / GET 404),
  logged in PODS.txt.

## NOT done
- No top-field tape judge run (see verdict). No uploads. No laptop simulations (all games on the pod; the requested correctness games
  vs 'random' ran there as the full-game loader test). HERD was only tested after its courier-bug fix on 8 games (-10.8k / -13.1k).
- build/ms_slot, build/ms_race, build/ms_sr (+JUDGE_ME) in this directory were written by the "microstructure" agent (flag builds on
  v183ms, see their META.json); they are not newexec builds and were not touched.
