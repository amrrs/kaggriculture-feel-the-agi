# reactive_v1 — FINAL REPORT (15:10 UTC 30 Sep; stopped by the coordinator's spend cut)
(Saved by the coordinator from the agent's final message; the agent's own Write was refused. Earlier checkpoint kept as REPORT_checkpoint2.md.)

A fully reactive controller (no tape at any step) is built and works end to end, and so does a low-noise bench for it. It is still well behind v183ms: about -29k per game against V183 and 0 wins head-to-head. Nothing was uploaded.

## 1. Numbers
Fresh seeds 18401-18412, both seats, n=24 per row. Shop sequence pinned (section 5). Engine 1.32.7, actTimeout 1 s.

| build | vs V183: win / margin (se) / own / opp | H2H vs v183ms | vs at12m | self-play own | tape judge, paired vs v183ms (all / both-intact) |
|---|---|---|---|---|---|
| rv1a (sha b5067ab3)* | 0% / -47.8k (2.3k) / 69.0k / 116.8k | 0%, -49.7k | -50.1k | 74.2k | -56.5k / -49.8k |
| rv1b (sha 67efc715) | 0% / -31.6k (1.6k) / 84.4k / 116.0k | 0%, -33.0k | -34.4k | 97.5k | -44.0k / -34.8k |
| rv1d (sha 0fa19793, final) | 0% / -28.8k (1.4k) / 88.9k / 117.7k | 0%, -31.2k (1.7k) | -32.0k | 97.9k | -40.0k (4.5k) / -31.3k (1.9k); 27/123 tape wins vs v183ms's 64 |
| v183ms vs V183, same seeds | 75% / +0.9k / 107.0k / 106.1k | | | | 0 |
* rv1a ran on the engine's own shop draws, before pinning existed.
- 0 controller errors in ~3,000 games; 3-5 ms per step unloaded (0.45 s peaks = 40 processes on 32 vCPU). rv1c (017734fd) within +-0.3k of rv1d.

## 2. Milestones (rv1d)
(a) 720 steps error-free, >= 90k self-play: MET (0 errors, 97.9k). (b) own revenue >= v183ms's own: NOT MET (88.9k vs 107.0k). (c) >= 50% vs v183ms: NOT MET (0/24). (d) >= v183ms on the 123 tapes: NOT MET (-40.0k paired).

## 3. What improved rv1a -> rv1d (paired on the pinned bench, seeds 18301-18308 both seats vs V183, n=16; base -51.7k -> final ~-24.1k)
- Dispatch: score every admitted task as reachable + do unassigned tasks on a unit's shortest path (on-the-way); turning on-the-way off costs -28.0k.
- Four changes worth +16.2k together: no low-value "keep" waterings +7.2k; no urgency bonus +6.4k; smaller plan (~50 crop tiles) +6.7k (largest plan -13.6k); feed/care coverage 0.73/0.68 -> 0.85/0.83.
- Better task values +3.9k: must-water worth plant value minus remaining labour; care worth nothing when next production is capped; fertiliser on ongoing crops only when the window covers >= 2 production nights.
- Selling and herd mix +6.5k: earlier deliveries to the shed, fewer geese, stricter admission, fewer tomatoes.
- Seeds before animals + early wheat harvest to free tiles for strawberries (removing costs -2.8k; reproduces the top-3's 17 strawberry tiles by d6).
- Stop buying animals whose product is forecast below 40% of base: +1.9k.
- Smaller: busy-neighbour reward +2.2k; stop at 3 quadrants +1.6k; cash guard on fertiliser use (prevents a -132k starvation spiral).
- Rejected: zones (-2..-8.6k), dedicated animal keepers (-6..-16k), finish-the-tile bonuses (-10k), more/fewer hires, more crops, 2 quadrants (-9.2k), 4 quadrants, wheat floors, more cows/sheep, holding goods for price (0), sell-order variants (0), timed deliveries (0), cheaper fertiliser use.
- CMA-ES (24 knobs, 16 games/candidate, 11 generations): flat within +-2k (noise = effect size).

## 4. Remaining gap (rv1d vs v183ms, both vs V183, same seeds): -29.8k = own -18.1k + V183 earning +11.7k more against us (less denial)
Own money net of same-product purchases per game: wheat -9.1k (we sell 13.7k and buy 11.4k; v183ms nets +11.4k), eggs -3.1k, strawberries -2.6k, melons -1.7k, fertiliser -1.6k, carrots -1.6k, wool -1.1k, milk +0.9k, tomatoes +4.8k, animals/seeds/hires/land -3.2k.
Causes: (1) labour productivity binds: 13 units do 124 actions + 125-145 moves/day (1.15 moves/action) vs top-3 ~160 actions at ~0.8 moves/action with 22-23 animals and 75 crop tiles; every "more assets" variant loses at our efficiency, so the plan stays at ~50 tiles / 17 animals -> 475 wheat vs V183's 800, feed bought mid-game, 3.5 geese vs 7. (2) Denial: lower wheat/fertiliser/egg supply keeps V183's prices higher (+11.7k). (3) Late game: d20-28 we earn 3.4k/day vs 4.8k. Money d10/d15/d20/d28: 6.7k/24.3k/50.6k/77.4k vs V183 8.9k/29.6k/60.8k/98.9k.

## 5. Harness (agents/reactive_v1/)
rx.py = controller (pure Python, params in dict P, last callable `agent`); builds build/<tag>/main.py via mkvar.py (rx.py + P.update). game.py records per-product/per-day ledgers + daily controller log; PIN_SHOPS=1 pins the shop sequence (our layout changes weed draws which change shops; pinning cut paired own-money se from ~4k to ~0.5k at n=16); PIN_SHOPS=0 = engine draws. runq.py/mkjobs.py jobs; report.py, dlog.py; tj.sh/tjscore.py tape judge vs final30 tapejudge's v183ms baseline; round.sh pinned screening round; bench.sh full milestone bench + tape judge; tune.py/space.py/cma.py/tune_loop.sh tuning. out/ = all games; tune/r1/evals.jsonl.

## 6. Next three changes
1. Route-level dispatch: each unit a 4-6 stop route (cheapest insertion), re-planned every step, on-the-way as fallback; target <= 0.9 moves/action; then retry a larger plan (plan-size 0.8-0.9, more geese). Evidence: crude path insertion was worth +28k; asset-heavier variants lose only because coverage falls.
2. Wheat economy (-9.1k line): fertilise wheat at age 2 from collected fertiliser when two extra wheat beat the fertiliser's value (V183 does; our gate almost never fires); count a harvester's wheat as feed only for animals on its path; buy the day's shortfall once at h0-h1 instead of piecemeal (~11.4k/game at ~39).
3. Retune properly: pinned bench, 32 games/candidate, <= 10 knobs (LAM, VCAP, ADMIT_K, EFF, CL_B, DROP_K, HERD_PMIN, HG0, CARE_K, FEED_V); run v183ms vs V183 on the same seeds every generation.

## 7. Resume on a fresh pod
cd research/claude/2900/agents/reactive_v1; source ../../../../.venv/bin/activate
bash mkpod.sh reactive_v1 "cpu3c 32" "cpu5c 32"   # CPU often exhausted; fallback: bash mkgpod.sh reactive_v1 32 SECURE "NVIDIA GeForce RTX 3090"
bash podip.sh <id>   # until not None; log the pod in ../final30/PODS.txt
bash setup_pod.sh <ip> <port> 14000   # arms self-destruct first; if engine missing: bash pod.sh '/opt/venv/bin/pip install -q "kaggle-environments==1.32.7"'
# point pod.sh, push.sh, pull.sh at the new ip/port
bash round.sh z '{"base": {}, "z1": {"EFF": 0.75}}' base     # pinned screening round
bash bench.sh rv1e 18401 12                                   # milestone bench + tape judge
python3 tune.py init r2 0.3 10; bash tune_loop.sh r2 10 18601 # tuning (edit space.py first)
(Scripts no longer pass CPU lists: on one pod the CPU ids were not 0-31.)

## 8. Pods: 8o16ji6wk0j1a9 (RTX 3090 GPU pod, 32 vCPU, 13:03, self-destruct armed 13:05 +14000 s, deleted 15:04); ijpf8ak1c8frp0 (cpu3c 32 vCPU, 14:35, armed 14:37, deleted 15:04). No laptop games; one local step-0 loader check of rv1d.

## 9. Not done: rv1d never validated on unpinned shop draws; none of the three next changes started; tape-judge baseline for v183ms from another pod's run; holding goods / rival-exposure sell ordering measured no effect; zones, keepers, urgency and finish bonuses remain in code, switched off.
Controller: build/rv1d/main.py. Also DESIGN.md, PLAN.md, out/bench_rv1d.txt, out/tj_rv1d.txt.
