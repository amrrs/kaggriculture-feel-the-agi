# final30/bundle — top-3 late programme as a flag bundle on v183ms (REPORT, updated at each checkpoint)

## PRE-DECLARED PASS RULE (written 05:17 UTC, before any game result)
Original rule (coordinator brief): bundle beats v183ms paired >= +1.0k (z >= 2) AND wins >= 60% vs V183 AND no game worse than
-15k AND top-field tape judge paired >= +1.0k. Coordinator cut the clock to 06:50 UTC and dropped the 48-game batch, so the only
evidence available will be a 16-game smoke vs V183 (seeds 17501-17508, both seats). Rule applied to the smoke (necessary, not
sufficient): paired margin vs v183ms's own games on the same seed/seat > 0, win rate vs V183 >= v183ms's on the same games, worst
game > -15k, peak step < 0.6 s. A smoke pass is NOT the full pass rule; the tarball is shipped as "smoke-only evidence".

## Build
build_bundle.py patches ANY v183ms-derived main.py (circuit text edits + ctrl day-10 hook), flags default off:
  python build_bundle.py <tag> --base <path/to/main.py> --flags '{"B_LAND4": true, "B_TOM": true, "B_FEED": true}'
Tags: bz (all off = parity), bl (LAND4), blt (LAND4+TOM+FEED), bltf (+FERT0), ball (+HAND+1 +CAR), bt (TOM+FEED, no land).
Pod wiffoax5h3653a (cpu5c 32 vCPU), self-destruct ~09:03 UTC (PODS.txt).

## CHECKPOINT 1 (05:35 UTC) — the bundle as specified LOSES BADLY; one implementation defect found (tomato hold), fix in smoke
Parity: bz (all flags off) = v183ms action-for-action on 17501/17502/17503 seat 0 (identical per-step digests 676c74c2 / 6b28204e /
e75bf758, identical rewards) on a lightly loaded pod. (Under 32-way load v183ms itself is not reproducible on 17501: its micro
optimiser has a 0.2 s wall-clock budget; bz vs v183ms under load differed on 17501 only.)
Smoke vs V183, seeds 17501-17508 both seats (n=16 per row; paired d = minus v183ms's own game on the same seed/seat; the null
control bn re-draws the world (one idle tile -> different weed RNG -> different shops) with ~no strategy change: +0.27k (se 0.71),
75% win, so world re-draws do NOT explain the losses below):
| build | flags | win% vs V183 | margin (se) | worst | paired d vs v183ms (se) | better |
|---|---|---|---|---|---|---|
| v183ms | base | 75.0 | +961 (393) | -896 | 0 | - |
| bn | null control | 75.0 | +1228 (453) | -2274 | +267 (709) | 10/16 |
| bl | LAND4 | 0.0 | -9919 (831) | -15047 | -10880 (744) | 0/16 |
| bt | TOM+FEED | 0.0 | -10557 (1142) | -17194 | -11518 (974) | 0/16 |
| blt | LAND4+TOM+FEED | 0.0 | -23498 (1901) | -31637 | -24459 (2017) | 0/16 |
| bltf | +FERT0 | 0.0 | -19462 (1918) | -33360 | -20423 (1969) | 0/16 |
| ball | +HAND+1 +CAR | 0.0 | -23645 (1173) | -30446 | -24606 (1273) | 0/16 |
| bt0 | TOM alone | 12.5 | -6931 (1573) | -18527 | -7892 (1562) | 0/16 |
| bt2 | TOM + FEED tile floor only | 12.5 | -3901 (787) | -8071 | -4862 (758) | 2/16 |
| blt2 | LAND4+TOM+FEED tile floor | 0.0 | -14144 (1604) | -23427 | -15105 (1733) | 0/16 |
| blc | LAND4+CAR | 0.0 | -9992 (746) | -13379 | -10953 (645) | 0/16 |
| bf | FEEDGUARD (tile floor + 1.5-day shed reserve) | 12.5 | -3572 (613) | -7048 | -4533 (534) | 0/16 |
| bf2 | FEEDGUARD tile floor only | 100 | +1566 (297) | +138 | +605 (184) | 8/16 |
| bh | HAND+1 | 25.0 | -363 (402) | -2458 | -1324 (169) | 0/16 |
| bx | FERT0 | 37.5 | -1307 (637) | -5461 | -2268 (614) | 4/16 |
| bc | carrot floor | 87.5 | +1179 (239) | -524 | +218 (246) | 12/16 |
| bd | DRIP sell (strawberry/milk/wool 1-2 per post-tick hour) | 0.0 | -3355 (334) | -5150 | - | - (peak step 1.54 s, 317 steps > 0.6 s: FAIL) |
Peak step of every other build <= 0.41 s under 32-way load.
bf2 (the only smoke positive) on FRESH seeds 17509-17548 both seats (n=80): vs V183 56.2% win, paired d vs v183ms -814 (341); head-to-head
vs v183ms on 17501-17548 (n=96): 40.6% win, -908 (283), worst -15.9k. The smoke +0.6k was selection noise -> bf2 REJECTED. bf2c (+carrot
floor) n=80 vs V183: 67.5%, paired -560 (385) -> rejected.
Tape judge (tapejudge agent, 123 top-12 tapes, noise floor bz -6 +-3, reported by the coordinator): bl -4.1k, bt -9.4k, blt -14.9k,
bltf -15.5k, ball -16.6k paired vs v183ms.
Per-product (smoke, own/opp revenue vs v183ms, k): LAND4: our wheat +3.3 / opp wheat -4.3 but opp straw +4.2, fert +1.5, milk +1.4,
egg +1.1, wool +1.0; we pay 4k land + ~26 more hires. TOM (bt): our tomato +4.5, but our wheat -3.9, carrot -2.0, milk -2.0, egg -1.2;
opp straw +3.9, wheat +3.4, wool +1.8.
DIAGNOSIS (diag.py per-day ledger, bt/bt0/bt2 vs v183ms on 17501/17503 seat 0, out/diag): tomatoes ARE executed correctly (planted on
schedule, watered - 0-1 tomato tiles lost to weeds per game -, fertilised on production days, 8 units/day harvested from 4 tiles at
d19-22) BUT V183's tomato hold (TOM_HOLD with TOM_FLOOR 9999 + TOM_END_RULE, held units EXEMPT from the shed-room check) keeps every
tomato in the shed until day 29 (0 sold on d11-28, 48-65 sold on d29 at $56-73). The shed then has 50-60 fewer free slots: the
planner pays return-drop routes / MPC shed-room squeezes and milk collapses (17501: milk 93 units / 4.8k vs 135 / 12.0k in v183ms;
wool -1.6k, wheat -1.7k). bt's extra 1.5-day wheat reserve in the shed makes it worse (-13.6k on 17501) - the same shed-room
mechanism is why FEEDGUARD's shed reserve (bf) alone costs -4.5k. Top-3 sell tomatoes every evening (h22-h0, no hold).
FIX in smoke now: B_TOM_NOHOLD (tomatoes sell daily like the top 3): bt3 = TOM+NOHOLD+FEED tile floor, bt3n = TOM+NOHOLD, blt3 =
LAND4+TOM+NOHOLD+FEED tile floor (build/<tag>/JUDGE_ME written for the tape judge).

## CHECKPOINT 2 / FINAL VERDICT (05:45 UTC) — FAIL. Nothing to ship. The bundle loses on every judge; stop.
Pre-declared rule (top of this file): FAILS on every clause for every bundle build. No tarball was packaged (per the coordinator's
"ship nothing rather than a broken build"); v183ms stays.

Fix result (B_TOM_NOHOLD = tomatoes sold daily instead of V183's hold-to-day-29): the defect was real - it halves the smoke loss
(bt2 -4.9k -> bt3 -2.3k; blt2 -15.1k -> blt3 -7.5k) - but on FRESH seeds 17509-17548 both seats (n=80 per row, vs V183, paired d =
minus v183ms's game on the same seed/seat):
| build | flags | win% vs V183 | margin (se) | worst | paired d vs v183ms (se) | better | peak step |
|---|---|---|---|---|---|---|---|
| v183ms | base | 71.2 | +808 (213) | -4393 | 0 | - | 0.40 |
| bt3 | TOM + TOM_NOHOLD + FEED tile floor | 16.2 | -5313 (988) | -35916 | -6122 (924) | 7/80 | 0.39 |
| blt3 | LAND4 + TOM + TOM_NOHOLD + FEED tile floor | 6.2 | -5262 (498) | -14590 | -6071 (542) | 3/80 | 0.40 |
| bf2 | FEED tile floor only | 56.2 | -6 (379) | -16337 | -814 (341) | 15/80 | 0.39 |
| bf2c | FEED tile floor + carrot floor | 67.5 | +248 (416) | -16830 | -560 (385) | 41/80 | 0.39 |
| mo3d | MERGED: opening3 DSM top-3 prefix (o3d) + LAND4+TOM+NOHOLD+FEED | 10.0 | -13139 (1347) | -46411 | -13947 (1329) | 8/80 | 0.44 |
| mo3d0 | opening3 DSM prefix alone (control for mo3d) | 12.5 | -12469 (1469) | -55630 | -13277 (1463) | 10/80 | 0.40 |
bf2 head-to-head vs v183ms (17501-17548 both seats, n=96): 40.6% win, -908 (283).
(Smoke on 17501-17508: bt3 -2296 (526) 2/16; blt3 -7490 (836) 0/16; bt3n = TOM+NOHOLD without the tile floor -2798 (619) 0/16;
mo3e = opening3 DECEM prefix + flags -9918 (1434) vs its control mo3e0 -22021 (2451); mo3d -3973 (2030) - the smoke's mo3d/mo3e
gain over their controls did not replicate on fresh seeds: mo3d - mo3d0 = -0.7k.)
Tape judge (tapejudge/REPORT.md, 123 top-12 tapes, paired vs v183ms, noise bz -6 (3)): bl -4100 (463), bt -9401 (547), blt -14940,
bltf -15468, ball -16642, bt0 (TOM alone) -5768 (431), bt2 -4944 (468), blt2 -6342 (606), bf (FEEDGUARD with shed reserve) -6756 (373),
bf2 -1197 (236), bf2c -1111 (244), bh (HAND+1) -1451 (110), bx (FERT0) -3005 (189), bc (carrots) -72 (64), blc -3788 (470),
bn (null control) -556 (99). bt3 / blt3 / mo3d / mo3e were dropped with JUDGE_ME and will be appended by the poller.

WHICH COMPONENT KILLED IT (every judge agrees; none carried it):
- LAND4 alone: -10.9k smoke (0/16), -4.1k tape. Mechanically correct (4 quadrants at d11 in 16/16 games, bought d10 after the tape's
  own orders are funded). The executor fills the SE quadrant with wheat (40 wheat tiles at d15 vs 24): own wheat +3.3k / opp wheat -4.3k,
  but +26 hires/game and the opponent's premium lines rise (straw +4.2k, fert +1.5k, milk +1.4k, egg +1.1k, wool +1.0k) - our
  premium pressure on the shared markets drops (the tape judge shows the same with FIXED opponents: opp +1.65k).
- TOM: executed correctly (diag.py per-day ledger, out/diag: planted on schedule, 0-1 tomato tiles lost to weeds per game, fertilised
  on production days, 2 units/tile/production harvested). With V183's tomato hold it lost -7.9k (bt0); with daily selling -2.8..-6.1k.
  It displaces wheat/carrot tiles on a 3-quadrant farm (own wheat -1.8k, carrot -2.1k; opp wheat +2.3k because we sell less wheat)
  and the opponent's premium revenue rises (+3..4k). With LAND4 the displacement goes away but LAND4's own cost remains.
- FEEDGUARD shed reserve (1.5 days of feed held in the shed): -4.5k smoke / -6.8k tape: shed room is the binding constraint of this
  executor (return-drop routes, MPC room). The tile-floor part alone (bf2) is ~-0.8..-1.2k. The -25k starvation tail did not appear;
  the worst bt3 game (-35.9k, 17515) is a milk/tomato-price world, not an escape (herd 16 all game).
- HAND+1 -1.3k smoke / -1.45k tape (13th hand costs fib 233/day, adds little); FERT0 -2.3k / -3.0k; carrot floor ~0 (+0.2k / -0.07k).
- DRIP selling (playbook item 2, bd): -3.4k, 0/16 and 317 steps > 0.6 s (peak 1.54 s) - the held stock slows the MPC sell DP. Killed.
- The top-3's own opening on our executor (opening3, and my merged mo3d/mo3e) loses 12-22k: the whole top-3 programme only works
  with THEIR executor; transplanting its parts into V183's circuit loses, singly and bundled.

Methodology caveat for every agent's "both seats" numbers: in 50-70% of seeds the seat-0 and seat-1 games are exact mirrors (identical
margin; farms are symmetric and the agents deterministic), so n = 2 x seeds overstates independent games ~1.5x and the naive se is
~20-40% too small. None of the verdicts above is close enough for this to matter.

PARITY (final build_bundle.py): bz (all flags off) = v183ms on 17501/17502/17503 seat 0, identical per-step action digests
(676c74c2f589 / 6b28204ed8d4 / e75bf7580b61) and rewards, on a lightly loaded pod (under 32-way load v183ms itself is not
reproducible because of the micro optimiser's 0.2 s wall-clock budget).

Files: build_bundle.py (patch; command: python build_bundle.py <tag> --base <any v183ms-derived main.py> --flags '<json>'; flags
B_LAND4, B_TOM, B_TOM_NOHOLD, B_FEED (+B_FEED_DAYS), B_FERT0, B_HAND, B_CAR, B_DRIP, B_NULL), merge_open3.py (bundle flags then
opening3's build_open3.patch on top), game.py (race harness + farm snapshots), diag.py / diag_rep.py (per-day tomato/herd ledger),
snap.py, report.py, runq.py, jobs_*.txt, out/{s1..s7,h1,h2,h3,par*,diag}.
SHA-256 of main.py: bz 72fd4924c944..., bt3 c9019e891263..., blt3 30560e432c14..., mo3d 8deb5fbe54d0..., bf2 8c55f6fb4362...
NOT done: no upload; no laptop simulation (all ~1,100 games on pod wiffoax5h3653a); no lx1 pair (dropped by the coordinator);
no tarball/loader test (nothing passed); HAND via OPT_HIRE not tried (simple +1 floor only).
