# final30/microstructure — REPORT (FINAL 09:20 UTC 30 Sep; checkpoints below)

## VERDICT
Only **MS_SLOT** helps. It is positive in every test but small against the top field: about +50/game on the 123-tape top-12 judge, +0.45..0.8k
against our own lineage. It FAILS the +1k bar. MS_RACE and MS_DRIP lose money against the top-field tapes. MS_OVERFLOW and MS_CAPHARV have
nothing to capture on the v183ms executor. Nothing here beats v183ms by the pre-declared bar. If the coordinator wants a free, low-risk
increment on v183ms, the candidate is:
  **ms_slot** = research/claude/2900/agents/final30/newexec/build/ms_slot/main.py (= microstructure/build/mslot/main.py),
  main.py sha256 808670930fa213124feaa144f112748d3289c5349fd2859429a828e92f4da043; packaged microstructure/build/submission-mslot.tar.gz
  (main.py only, mtime 0) archive sha256 809cae1cc5218b0856dc78f2fee7ef43d88d68817aa6205bad86da391bc49e93; loader test on the pod
  (hybrid/loadtest.py, kaggle-environments 1.32.7): callable `agent`, 30 steps, peak 0.312 s, ACTIVE/ACTIVE. Parent v183ms cba37327.

## Numbers (paired d = candidate margin - v183ms margin, same seed/seat/opponent; se in brackets; env.run actTimeout 1 s + overage, 32-way load)
| build | fresh vs V183 paired (n=96, 18511-58) | H2H vs v183ms (n=96) | HOLDOUT paired vs V183 / v183ms / lx1 / lx3 / farm2945 (n=80 each, 18601-40) | tape judge paired vs v183ms (n=123) |
|---|---|---|---|---|
| **mslot** | **+479 (82)** 78/96 | **86.5% +631 (76)** | **+805 (150) / +553 (66) / +449 (74) / +655 (76) / +100 (32)** | **+43 (21)** mine, **+54 (19)** judgerun, 75/45 better/worse |
| msr (slot+race) | +751 (159) | 81.2% +941 (119) | +864 (174) / +735 (126) / +329 (176) / +498 (164) / +63 (118) | **-251 (51)** mine, -231 (49) judgerun |
| mrace | +28 (165) | 66.7% +445 (126) | - | **-304 (53)** mine, -281 (49) judgerun |
| msr5 (race only on rival lots >= 5) | +664 (124) | 80.2% +801 (113) | - | -66 (28) |
| msr10 (race on lots >= 10) | +554 (138) | 83.3% +713 (101) | - | +5 (22) |
| mslott (slot + same ordering on the d0-10 tape) | +535 (184) 69/96 | 75.0% +622 (124) | +697 (245) / +776 (186) / +451 (255) / +1001 (245) / +215 (97) | -468 (467), noisy |
| mdrip (K2/KOFF1) | **-4525 (340)** 0/42 | 0% -4257 (244) | - | -228 (70) |
| mdrip0 / mdrip4 | -4619 (314) / -3267 (201) | - / 0% -3910 (254) | - | - |
| mdrips (strawberry only) | -2297 (169) 5/96 | 8.3% -2138 (180) | - | -78 (49) |
| mdripsr (drip+slot+race) | -4037 (372) 2/42 | 4.8% -3600 (344) | - | - |
| movf / mcap | -15 (16) / -29 (16) | - | - | - |
Worst games (holdout): mslot -5667 vs V183 (v183ms -6639 on the same seeds), -894 vs v183ms, no tail < -15k anywhere. Peak step: the flags add <1 ms
(median per-game max 0.306 vs 0.311 s; mean 0.0085 vs 0.0084 s). Isolated 0.6-0.8 s spikes appear in all builds including unmodified v183ms
(0.668 s in the holdout, 0.612 s on the tape judge) = environment under 32-way load. Judgerun logged ms_race at 0.825 s (race is rejected anyway).
Parity: m0 (all flags off) per-step action digests are identical to v183ms on seeds 18501/18502 (cb92ae1f / 9274e16b). movf/mcap identical in >90% of games.

## Where the coins move per product (k/game, own | opponent, paired)
- mslot vs V183 (holdout): MELON +0.18|-0.19, TOMATO +0.09|-0.09, WOOL +0.07|-0.09, STRAW +0.02|-0.06. Realised $/unit melon 210 vs 208, tomato 121 vs 119.
  On the tapes: every product within +-0.01. It wins ties in the lockstep book when both farms sell the same product in the same step.
- MS_RACE on the tapes: STRAW -0.34|-0.15, MILK -0.10|-0.05, TOMATO -0.05|-0.02 ($143 vs $145/strawberry, $140 vs $145/tomato). The top farms sell 1-2 units
  on almost every step, so rival_sold > 0 fires every step and the race dumps the SQ-held stock into the book.
- MS_DRIP (coordinator request). Fresh vs V183: STRAW -0.72|+1.18 (units -0.8, $120 vs $123), MILK -0.31|+0.71 ($102 vs $104), WOOL -0.33|+0.51 ($130 vs $132),
  MELON -0.32|+0.34 ($201 vs $206). On the tapes: STRAW +0.35|+0.39 ($146 vs $145), MILK +0.23|+0.32, WOOL +0.20|+0.28. Our per-unit price does rise on the
  tapes, but the tape's revenue rises more. Metering leaves the high-price units to the rival, and holding hands the rival the book.
  v183ms already realises $145/strawberry against the top-12 tapes, so the playbook's $146 is not a gap in price per unit.
- Live replays (fieldnow, 64 of our games vs >= 2800 opponents, d11+): the top farms sell strawberry on ~62 steps a game, in slot 0 in 70% of their sell
  steps. When both of us sell it in the same step (32/game) we already tie in slot 0 70% of the time, go earlier 15%, go later 15% (milk 79% ties, wool 78%).
  With 1-2-unit rival lots, winning a slot is worth about one price step. That is why the slot lever is capped at ~+50 against the top field.
- Our executor's losses to the midnight shed drop are ~0-0.3 units/game and our animal cap losses 0.9-1.3 milk units/game. CAPHARV/OVERFLOW have nothing to
  capture: the circuit already makes a cap-risk harvest mandatory, plans return routes against OVERFLOW_TARGET 96 and releases held units at h23.

## Portability
build_ms.py's patch applies unchanged to every newexec/build/* circuit and to race/rd8b (anchors checked, no simulation). MS_SLOT only reorders the
final market list (SELL orders not preceded by a buy of the same item go first, ordered by rival exposure; ties keep the original order),
so it can be stacked on any v183ms-derived circuit.

## What was NOT done
- No upload, no Kaggle kernel. Laptop: 1 correctness game + 1 partial (270-step) tape-phase check of mslott. Everything else ran on pod gtva5n1v6dsgoe
  (created 08:22, self-destruct armed 08:23:04 + 14000 s, DELETED 09:18 UTC).
- ms_drip was not sent to judgerun: it is refuted on fresh seeds (0/42 better) and on my own tape-judge run with judgerun's harness (reproduced
  v183ms to +8 (10)). The builds are in microstructure/build/mdrip*, if an official run is wanted.
- No live-set replay (Majkel) judge. No RACE on the d0-10 tape. CAPHARV only covers the circuit days (the cap losses measured are all d10-19 milk).
- Shed-drop / cap diagnostics cover our own farm only, in engine games (game.py wrappers on _drop_inventories_to_shed / _daily_refresh_animals).

## Files
build_ms.py (patch + TAGS), build/<tag>/main.py, game.py (race harness + drop/cap/contest diagnostics + ms stats), runq.py, report.py, tjscore.py
(tapejudge score.py reading out/tj/), pack.py, chain*.sh, jobs_*.txt, out/par, out/b1 (fresh 18511-58), out/h1 + out/b2 (holdout 18601-40), out/tj/<tag>
(tape judge), out/b1_report.txt, out/h1_report.txt, out/tj_products.txt, out/podlogs/.


## CHECKPOINT 1 (2026-09-30 08:35 UTC): builds done, flag-off parity EXACT, batch 1 running
Pod gtva5n1v6dsgoe (cpu5c 32 vCPU, self-destruct 12:16 UTC; PODS.txt). Engine kaggle-environments 1.32.7, env.run with actTimeout 1 s.
build_ms.py patches the embedded circuit of v183ms (micro/build/v183ms/main.py cba37327); all flags default off; no delivery loops
added (micro optimiser gating untouched). Idea credit: public 'the-2945-farm' notebook layers ORDERPRI2/RACE/RACEGATE/OVERFLOW/
SHEDROOM/CAPHARV (Apache-2.0); own implementation on our circuit.
- m0 (all flags off): per-step action digests identical to v183ms on seeds 18501/18502 seat 0 vs V183 (cb92ae1f / 9274e16b), same rewards.
- Flags: MS_SLOT (sell orders ordered by rival exposure, rival stock = visible harvests - recovered sales), MS_RACE (rival_sold>0 and
  stock>0 and quote >= base -> sell our held stock now, units quoted >= base only; list full -> swap out the weakest sell),
  MS_OVERFLOW (h23 sell of what the midnight drop would destroy), MS_CAPHARV (CARE/COLLECT -> HARVEST on an animal that overflows
  tonight), MS_DRIP (coordinator: <= K premium units/product/step, K on the step after a shop tick, KOFF otherwise; free below 40% of
  base / floor / when rival_sold>0; shed <= 85 release largest stock first; free from d29 h12).
- First facts (2 parity games + diagnostics in game.py): our midnight-drop destruction = 0 units, our animal cap loss = 1 milk unit in
  2 games -> MS_OVERFLOW / MS_CAPHARV never fire (digests identical to v183ms). V183's circuit already makes the cap-risk harvest
  mandatory (cap_risk in the animal stop) and plans return-drop routes against OVERFLOW_TARGET 96, and releases held units at h23.
Batch 1 running: seeds 18511-18558 x both seats, every build vs V183 and vs v183ms (1,728 games).

## CHECKPOINT 2 (08:50 UTC): batch 1 (seeds 18511-18558, both seats) mostly done; MS_SLOT judged; MS_DRIP refuted on fresh seeds
| cand | vs V183 win% | margin (se) | paired d vs v183ms (se) better/n | vs v183ms win% | margin (se) | worst vs v183ms |
|---|---|---|---|---|---|---|
| v183ms (base) | 69.9 | +1050 (173) | 0 | - | - | - |
| mslot  | 78.5 | +1525 (164) | **+475 (84)** 75/93 | **85.9** | **+615 (79)** | -1573 |
| mrace  | 73.1 | +1089 (177) | +39 (170) 43/93 | 65.2 | +367 (125) | -3532 |
| mall (slot+race+ovf+cap) | 89.2 | +1804 (177) | +754 (164) 72/93 | 80.4 | +928 (121) | -3240 |
| movf / mcap | 69.6 | ~+1020 | -15 (16) / -29 (16) (fire ~0.3-0.5x/game) | - | - | - |
| mdrip (K2/KOFF1) | 2.4 | -3413 (270) | **-4525 (340)** 0/42 | 0.0 | -4257 (244) | -8349 |
| mdrip0 (K2/KOFF0) | 0.0 | -3507 (270) | -4619 (314) 0/42 | - | - | - |
| mdrip4 (K4/KOFF2) | 2.4 | -2154 (194) | -3267 (201) 0/42 | 0.0 | -3910 (254) | -8127 |
| mdrips (straw only) | 31.5 | -1225 (188) | -2270 (171) 5/92 | 8.8 | -2011 (178) | -7022 |
| mdripsr (drip+slot+race) | 7.1 | -2925 (311) | -4037 (372) 2/42 | 4.8 | -3600 (344) | -9724 |
(drip rows stopped at n=42 once 0/42 better; mdrips run to n=92.)
Where the coins move (vs V183, paired, k/game own|opp): mslot = MELON +0.22|-0.24, TOMATO +0.07|-0.08, STRAW +0.01|-0.08 (the slot
wins ties in the lockstep book: same-step melon/tomato/strawberry lots). mdrip = STRAW -0.72|+1.18, MILK -0.31|+0.71, WOOL -0.33|+0.51,
MELON -0.32|+0.34; our realised $/unit FALLS (straw $120 vs $123, wool $130 vs $132, melon $201 vs $206) while the rival's revenue
rises: metering hands the high-price units to the rival, who sells into the book we left (public lesson 'every sale is denial').
Diagnostics: our midnight-drop destruction ~0 units/game (0.34 carrot vs V183 only when V183 opp.), our animal cap loss 0.77 milk + 0.06
egg per game -> MS_OVERFLOW / MS_CAPHARV have nothing to capture on this executor (already handled by cap_risk mandatory harvest,
OVERFLOW_TARGET return routes and the h23 held-unit release).
Step time: flags add nothing (median per-game max 0.306 vs 0.311 s; mean 0.0085 vs 0.0084 s); 5/1300 games had a 0.51-0.68 s spike
during a queue restart (co-scheduled processes), including one v183ms-only-code step - environment, recheck on the holdout.
JUDGERUN verdict ms_slot (sha 80867093): fresh H2H vs v183ms +572 (126) 85.4%; vs V183 paired +457 (84); TAPE JUDGE paired +54 (19),
75/45 better/worse, both-intact +56 (27) -> FAIL on the +1k bar. Reading: the self-play edge is mostly ties broken against a rival with
the SAME ordering rule (V183 sorts sells by lot value); against the recorded top-12 order books the slot gain is ~+50/game.
Dropped for judging: newexec/build/ms_slot (808670930fa2...), ms_sr (slot+race, 4ab225fbaadb...), ms_race (bb232176b070...).
Running: rest of batch 1 (msr, mslot60), holdout h1 seeds 18601-18640 x 2 seats {v183ms, mslot, msr} vs {V183, v183ms, lx1, lx3,
farm2945}, then mslott (MS_SLOT + the same ordering on the d0-10 tape's market list, MS_SLOT_TAPE).

## CHECKPOINT 3 (09:02 UTC): HOLDOUT (untouched seeds 18601-18640, both seats, n=80 per row) + judgerun verdicts
| cand vs opp | V183 | v183ms | lx1 | lx3 | farm2945 (public 2945, has its own ORDERPRI2) |
|---|---|---|---|---|---|
| v183ms win% / margin (se) | 77.5 / +1544 (292) | 48.8 / -8 (28) mirror | 100 / +4700 (225) | 97.5 / +3182 (215) | 100 / +17706 (825) |
| **mslot** win% / margin | 90.0 / +2349 (274) | **88.8 / +545 (69)** | 100 / +5149 (204) | 97.5 / +3837 (203) | 100 / +17806 (828) |
| mslot paired d vs v183ms (se), better/n | **+805 (150) 72/80** | **+553 (66) 73/80** | **+449 (74) 67/80** | **+655 (76) 70/80** | **+100 (32) 56/80** |
| msr (slot+race) paired d | +864 (174) 61/80 | +735 (126) 67/80 | +329 (176) 50/80 | +498 (164) 59/80 | +63 (118) 35/80 |
| worst game: mslot / msr / v183ms | -5667 / -6332 / -6639 | -894 / -3022 / -1122 | +1553 / +205 / +366 | -1943 / -1990 / -2363 | +2962 / +2962 / +2994 |
Peak step (32-way load): mslot 0.414 s, msr 0.441 s; v183ms itself 0.668 s / 0.627 s in two games of this pool (environment spikes, not the flags).
Where the coins move with MS_SLOT (holdout, k/game own|opp): vs V183 MELON +0.18|-0.19, TOMATO +0.09|-0.09, WOOL +0.07|-0.09, STRAW +0.02|-0.06;
vs lx3 MELON +0.20|-0.17, WOOL +0.07|+0.01; vs farm2945 ~0 per product (MILK +0.05|-0.03). Realised $/unit: melon $210 vs $208, tomato $121 vs $119.
JUDGERUN (fresh 17811-17834 + 123-tape top-12 judge, paired vs v183ms):
- ms_slot 80867093: H2H +572 (126) 85.4%; vs V183 paired +457 (84); tape judge **+54 (19)**, 75/45 better/worse; peak 0.515 s -> FAIL on the +1k bar.
- ms_sr 4ab225fb: H2H +764 (188); vs V183 +444 (169); tape judge **-231 (49)**, both-intact -141; peak 0.616 s -> FAIL. MS_RACE costs ~-285/game vs the
  recorded top-12 books (they sell 1-2 units nearly every step, so rival_sold>0 fires every step and the race dumps our SQ-held stock).
Live-replay check (fieldnow, 64 of our games vs >= 2800 opponents, steps >= 264): the top farms sell strawberry on ~62 steps/game and put it in
slot 0 in 70% of those steps; when both of us sell strawberry in the same step (32/game) we are already tied in slot 0 in 70%, earlier 15%,
later 15% (milk 79% tied, wool 78%). With 1-2-unit rival lots, winning a slot is worth ~one price step -> the slot lever is capped at ~+50/game
against the top field; its +0.5-0.8k in self-play comes from rivals that dump whole lots in a later slot (our own lineage, lx1/lx3).
