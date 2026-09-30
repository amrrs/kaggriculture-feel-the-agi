# PART 2 (coordinator job 20:40): lx3ms + g012m knob transplant (T1/T2/T3)

Status 21:01 UTC: COMPLETE. Pre-declared run (seeds 20101-20116, n=16 per pair): NO variant passed (table below).
Extension (not pre-declared, seeds 20117-20132, T1 and T3 only + same-seed lx3ms reference) brought T3 to a MARGINAL PASS at n=32:

| n=32 (20101-20132, seat = seed % 2) | vs lx3ms | vs g012m | gain vs g012m over lx3ms (paired, same seeds) | peak step | worst | errors |
|---|---|---|---|---|---|---|
| T3 (labour/alloc) | 23/32 = 72%, +631 (460) | 4/32, -2469 (437) | +560 (481), 19/32 better | 0.570 s | -7870 | 0 |
| T1 (all 18) | 15/32 = 47%, +102 (322) | 3/32, -2467 (448) | +563 (561), 20/32 better | 0.593 s | -8244 | 0 |
| lx3ms (reference) | - | 2/32, -3030 (376) | 0 | 0.537 s | -7839 | 0 |

- T3 meets every clause of the pass rule on the pooled n=32 (>= 60%, margin > 0, no game < -15k, peak < 0.6 s, no errors, better vs g012m
  than lx3ms's 3/32 -3269). Caveats: it failed the n=16 pre-declared run on margin (-63). The pooled margin is +1.4 se, and the pass
  depends on the extension seeds (13/16, +1325 there). Its peak of 0.570 s is close to the cap (in a vs-g012m game on a busy 4-game kernel).
  Treat T3 as "not worse than lx3ms, maybe +0.5k", not as a proven gain. It is still far below g012m head-to-head (4/32).
- T3 PACKAGE (not uploaded): `agents/final30/kval/build/submission-lx3ms-t3.tar.gz` sha256
  `b1d9a1a357f80eede41bb9b0253734f72afe53773e94b45afb83b49ac703d1ea`. main.py only (0644, uid 0, mtime 0, same layout as v183ms/lx3ms).
  main.py sha256 `b4eba98dd0560b70f82f04bbc6f7984facbc9e81400d182eb8db4fd621b2bec8` (= lx3ms eecdb8f1 + appended T3 override block;
  build/lx3ms_t3/main.py). Loader test (final30/bundle/loadtest.py, last callable, 30 steps): callable `agent`, 30 steps, peak 0.047 s, OK.
- T1 fails (47% vs lx3ms). T2 fails badly (38%, -1156, n=16, not extended).

## Pre-declared n=16 result (seeds 20101-20116)
| variant | vs lx3ms: wins, margin (se), worst | vs g012m: wins, margin (se), worst | vs g012m paired minus lx3ms-vs-g012m (same seeds) | peak step | pass? |
|---|---|---|---|---|---|
| T1 (all 18) | 7/16 = 44%, +339 (517), -4054 | 2/16, -2068 (680), -8244 | +919 (823), 12/16 better | 0.519 s | NO (win rate < 60%) |
| T2 (sales/hold) | 6/16 = 38%, -1156 (550), -6735 | 2/16, -3562 (680), -7578 | -574 (778) | 0.511 s | NO |
| T3 (labour/alloc) | 10/16 = 62%, -63 (723), -7870 | 2/16, -2720 (696), -6819 | +267 (700) | 0.570 s | NO (margin <= 0) |
| lx3ms (same-seed reference) | - | 0/16, -2987 (491), -7839 | 0 | 0.537 s | - |

- No game < -15k anywhere, 0 steps > 0.6 s, 0 errors. All variants beat lx3ms's vs-g012m record (3/32, -3269), but none meets
  the lx3ms h2h leg: T1 and T2 lose the win rate, and T3's margin is -63 (it wins 10/16 small but loses -7870 on 20116 and about -3.2k on 20102/20106).
- Read: the g012m joint move does not transplant onto lx3ms. The sales/hold half (T2) hurts; the labour/alloc half (T3) is at best neutral.
  g012m's edge over lx3ms (0/16 on these seeds) comes from its base (v183ms/ms_slot + MPC_SELL, which lx3ms does not have), not from these 18 knobs.
- Knob digest check (dg, seed 20101, cand seat 1 vs lx3ms): the baseline itself is NOT deterministic. Two lx3ms-vs-lx3ms runs gave
  different action digests, most likely because of the time-based 0.35 s micro step cap. So a changed digest does not prove a knob is live.
  HAND_W reproduced a baseline digest exactly, so it is DEAD in lx3ms. SQ_START_DAY = ALLOC_MARGIN and
  TOM_OPP_MARGIN = AMAX_TOM gave pairwise-identical digests, so those four are PROBABLY dead on this seed. The other 13 moved.
  Dead knobs do not change play, so the T1/T2/T3 results stand as-is. Dropping them would give behaviourally identical builds, so none was rebuilt.
- Variant sources: final30/kval/ds2/{T1,T2,T3}.py (sha256 prefixes T1 4f1e9009eee6, T2 0dc1d398fcfc, T3 b4eba98dd056); builder tbuild.py.

<details><summary>raw tables (pooled n=32 incl. extension) + per-game margins + digests</summary>

| variant vs opp | n | wins | win % | mean margin (se) | worst | cand peak s | cand >0.6 | errors |
|---|---|---|---|---|---|---|---|---|
| T1 vs g012m | 32 | 3 | 9% | -2467 (448) | -8244 | 0.593 | 0 | 0 |
| T1 vs lx3ms | 32 | 15 | 47% | +102 (322) | -4054 | 0.519 | 0 | 0 |
| T2 vs g012m | 16 | 2 | 12% | -3562 (680) | -7578 | 0.428 | 0 | 0 |
| T2 vs lx3ms | 16 | 6 | 38% | -1156 (550) | -6735 | 0.511 | 0 | 0 |
| T3 vs g012m | 32 | 4 | 12% | -2469 (437) | -6819 | 0.570 | 0 | 0 |
| T3 vs lx3ms | 32 | 23 | 72% | +631 (460) | -7870 | 0.471 | 0 | 0 |
| lx3ms vs g012m | 32 | 2 | 6% | -3030 (376) | -7839 | 0.537 | 0 | 0 |

Digest check (seed 20101, cand seat 1, vs lx3ms): baseline lx3ms digests ['26aa21cf2de52b12', '75c5f96bedaafba4'] (deterministic: False)
- HAND_W: DEAD (identical actions)  dig 26aa21cf2de52b12 margin -93 
- HIRE_DOWN_W: LIVE  dig d5f0f78ad60345db margin -93 
- SQ_DECAY: LIVE  dig 06b8a70fdc46fd26 margin +127 
- SQ_SPLIT: LIVE  dig ecff523f1033306b margin +975 
- SQ_W: LIVE  dig 0c0d759731b9cd8e margin -1025 
- SQ_START_DAY: LIVE  dig 5920f7a7a95af1ce margin -1 
- CARE_W: LIVE  dig 014b34ffeeba91fe margin -731 
- SELL0_MAX: LIVE  dig 009290f0248f81e8 margin -12 
- FERT_WHEAT_MAXP: LIVE  dig 1e1ba524acb66d29 margin +113 
- WHEAT_BUFFER: LIVE  dig 694bc194d1d9b38a margin -370 
- OVERFLOW_TARGET: LIVE  dig c02175dc0cd0cd2b margin -501 
- AH_V: LIVE  dig a4af7a93928eda73 margin +2305 
- LATE_HARVEST_W: LIVE  dig 56766a8b50f6a72e margin +182 
- ALLOC_MARGIN: LIVE  dig 5920f7a7a95af1ce margin -228 
- LATE_START: LIVE  dig 64cf73f35ae5d96a margin +698 
- STRAW_AB_x: LIVE  dig 88e1e5dc9dc95b67 margin -568 
- TOM_OPP_MARGIN: LIVE  dig 49255ddfb47ed23c margin +0 
- AMAX_TOM: LIVE  dig 49255ddfb47ed23c margin +0 

T1.py vs g012m.py: 20101/1 -4380, 20102/0 -5512, 20103/1 +3642, 20104/0 -376, 20105/1 +659, 20106/0 -8244, 20107/1 -864, 20108/0 -2097, 20109/1 -1172, 20110/0 -1147, 20111/1 -4433, 20112/0 -634, 20113/1 -2357, 20114/0 -2708, 20115/1 -2507, 20116/0 -964, 20117/1 -6136, 20118/0 -3122, 20119/1 -2012, 20120/0 -2305, 20121/1 -3184, 20122/0 -7835, 20123/1 -1722, 20124/0 -2291, 20125/1 -866, 20126/0 -955, 20127/1 -6029, 20128/0 -3220, 20129/1 -2052, 20130/0 -4354, 20131/1 -1702, 20132/0 +1942
T1.py vs lx3ms.py: 20101/1 -366, 20102/0 +1994, 20103/1 -1375, 20104/0 -899, 20105/1 +3297, 20106/0 -4054, 20107/1 -917, 20108/0 -33, 20109/1 +2373, 20110/0 -446, 20111/1 +3654, 20112/0 -1980, 20113/1 +1362, 20114/0 +812, 20115/1 +2291, 20116/0 -287, 20117/1 +1297, 20118/0 +234, 20119/1 +1527, 20120/0 -1090, 20121/1 -3073, 20122/0 -1854, 20123/1 +559, 20124/0 -201, 20125/1 +555, 20126/0 +1561, 20127/1 -2692, 20128/0 +861, 20129/1 +2440, 20130/0 -376, 20131/1 -1140, 20132/0 -782
T2.py vs g012m.py: 20101/1 -6674, 20102/0 -4460, 20103/1 +3293, 20104/0 -3782, 20105/1 -7578, 20106/0 -3634, 20107/1 -1902, 20108/0 +395, 20109/1 -2694, 20110/0 -3261, 20111/1 -4102, 20112/0 -2778, 20113/1 -6905, 20114/0 -5458, 20115/1 -2655, 20116/0 -4793
T2.py vs lx3ms.py: 20101/1 -1175, 20102/0 +458, 20103/1 +430, 20104/0 +1992, 20105/1 -1578, 20106/0 -6735, 20107/1 -3404, 20108/0 -1917, 20109/1 -549, 20110/0 -3396, 20111/1 +347, 20112/0 +1336, 20113/1 +1080, 20114/0 -2108, 20115/1 -1186, 20116/0 -2096
T3.py vs g012m.py: 20101/1 -2976, 20102/0 -3948, 20103/1 -935, 20104/0 +1370, 20105/1 -3627, 20106/0 -6356, 20107/1 +3238, 20108/0 -5078, 20109/1 -647, 20110/0 -1161, 20111/1 -1169, 20112/0 -5304, 20113/1 -5055, 20114/0 -3357, 20115/1 -1701, 20116/0 -6819, 20117/1 -6244, 20118/0 +1558, 20119/1 -879, 20120/0 -2049, 20121/1 -3649, 20122/0 -2060, 20123/1 -3870, 20124/0 -3733, 20125/1 -3007, 20126/0 -2145, 20127/1 -551, 20128/0 -4012, 20129/1 -625, 20130/0 -4252, 20131/1 -2091, 20132/0 +2113
T3.py vs lx3ms.py: 20101/1 +239, 20102/0 -3299, 20103/1 -291, 20104/0 +3023, 20105/1 +3001, 20106/0 -3109, 20107/1 +2064, 20108/0 +1452, 20109/1 -1264, 20110/0 +2022, 20111/1 +983, 20112/0 -1846, 20113/1 +819, 20114/0 +2723, 20115/1 +350, 20116/0 -7870, 20117/1 +4456, 20118/0 +906, 20119/1 +1553, 20120/0 -334, 20121/1 +1656, 20122/0 -4643, 20123/1 +536, 20124/0 +148, 20125/1 +1545, 20126/0 +1243, 20127/1 +1924, 20128/0 +3672, 20129/1 +3327, 20130/0 +1992, 20131/1 -419, 20132/0 +3636
lx3ms.py vs g012m.py: 20101/1 -2751, 20102/0 -4344, 20103/1 -788, 20104/0 -1788, 20105/1 -3592, 20106/0 -19, 20107/1 -1883, 20108/0 -7839, 20109/1 -1820, 20110/0 -2749, 20111/1 -2972, 20112/0 -741, 20113/1 -3696, 20114/0 -4683, 20115/1 -2725, 20116/0 -5408, 20117/1 -5813, 20118/0 +284, 20119/1 -6792, 20120/0 -3096, 20121/1 -4921, 20122/0 -1249, 20123/1 -4198, 20124/0 -1162, 20125/1 -4434, 20126/0 -4277, 20127/1 -4693, 20128/0 +1208, 20129/1 -4763, 20130/0 -3442, 20131/1 -1612, 20132/0 -187

--- n=16 only ---

| variant vs opp | n | wins | win % | mean margin (se) | worst | cand peak s | cand >0.6 | errors |
|---|---|---|---|---|---|---|---|---|
| T1 vs g012m | 16 | 2 | 12% | -2068 (680) | -8244 | 0.453 | 0 | 0 |
| T1 vs lx3ms | 16 | 7 | 44% | +339 (517) | -4054 | 0.519 | 0 | 0 |
| T2 vs g012m | 16 | 2 | 12% | -3562 (680) | -7578 | 0.428 | 0 | 0 |
| T2 vs lx3ms | 16 | 6 | 38% | -1156 (550) | -6735 | 0.511 | 0 | 0 |
| T3 vs g012m | 16 | 2 | 12% | -2720 (696) | -6819 | 0.570 | 0 | 0 |
| T3 vs lx3ms | 16 | 10 | 62% | -63 (723) | -7870 | 0.471 | 0 | 0 |
| lx3ms vs g012m | 16 | 0 | 0% | -2987 (491) | -7839 | 0.537 | 0 | 0 |

Digest check (seed 20101, cand seat 1, vs lx3ms): baseline lx3ms digests ['26aa21cf2de52b12', '75c5f96bedaafba4'] (deterministic: False)
- HAND_W: DEAD (identical actions)  dig 26aa21cf2de52b12 margin -93 
- HIRE_DOWN_W: LIVE  dig d5f0f78ad60345db margin -93 
- SQ_DECAY: LIVE  dig 06b8a70fdc46fd26 margin +127 
- SQ_SPLIT: LIVE  dig ecff523f1033306b margin +975 
- SQ_W: LIVE  dig 0c0d759731b9cd8e margin -1025 
- SQ_START_DAY: LIVE  dig 5920f7a7a95af1ce margin -1 
- CARE_W: LIVE  dig 014b34ffeeba91fe margin -731 
- SELL0_MAX: LIVE  dig 009290f0248f81e8 margin -12 
- FERT_WHEAT_MAXP: LIVE  dig 1e1ba524acb66d29 margin +113 
- WHEAT_BUFFER: LIVE  dig 694bc194d1d9b38a margin -370 
- OVERFLOW_TARGET: LIVE  dig c02175dc0cd0cd2b margin -501 
- AH_V: LIVE  dig a4af7a93928eda73 margin +2305 
- LATE_HARVEST_W: LIVE  dig 56766a8b50f6a72e margin +182 
- ALLOC_MARGIN: LIVE  dig 5920f7a7a95af1ce margin -228 
- LATE_START: LIVE  dig 64cf73f35ae5d96a margin +698 
- STRAW_AB_x: LIVE  dig 88e1e5dc9dc95b67 margin -568 
- TOM_OPP_MARGIN: LIVE  dig 49255ddfb47ed23c margin +0 
- AMAX_TOM: LIVE  dig 49255ddfb47ed23c margin +0 

T1.py vs g012m.py: 20101/1 -4380, 20102/0 -5512, 20103/1 +3642, 20104/0 -376, 20105/1 +659, 20106/0 -8244, 20107/1 -864, 20108/0 -2097, 20109/1 -1172, 20110/0 -1147, 20111/1 -4433, 20112/0 -634, 20113/1 -2357, 20114/0 -2708, 20115/1 -2507, 20116/0 -964
T1.py vs lx3ms.py: 20101/1 -366, 20102/0 +1994, 20103/1 -1375, 20104/0 -899, 20105/1 +3297, 20106/0 -4054, 20107/1 -917, 20108/0 -33, 20109/1 +2373, 20110/0 -446, 20111/1 +3654, 20112/0 -1980, 20113/1 +1362, 20114/0 +812, 20115/1 +2291, 20116/0 -287
T2.py vs g012m.py: 20101/1 -6674, 20102/0 -4460, 20103/1 +3293, 20104/0 -3782, 20105/1 -7578, 20106/0 -3634, 20107/1 -1902, 20108/0 +395, 20109/1 -2694, 20110/0 -3261, 20111/1 -4102, 20112/0 -2778, 20113/1 -6905, 20114/0 -5458, 20115/1 -2655, 20116/0 -4793
T2.py vs lx3ms.py: 20101/1 -1175, 20102/0 +458, 20103/1 +430, 20104/0 +1992, 20105/1 -1578, 20106/0 -6735, 20107/1 -3404, 20108/0 -1917, 20109/1 -549, 20110/0 -3396, 20111/1 +347, 20112/0 +1336, 20113/1 +1080, 20114/0 -2108, 20115/1 -1186, 20116/0 -2096
T3.py vs g012m.py: 20101/1 -2976, 20102/0 -3948, 20103/1 -935, 20104/0 +1370, 20105/1 -3627, 20106/0 -6356, 20107/1 +3238, 20108/0 -5078, 20109/1 -647, 20110/0 -1161, 20111/1 -1169, 20112/0 -5304, 20113/1 -5055, 20114/0 -3357, 20115/1 -1701, 20116/0 -6819
T3.py vs lx3ms.py: 20101/1 +239, 20102/0 -3299, 20103/1 -291, 20104/0 +3023, 20105/1 +3001, 20106/0 -3109, 20107/1 +2064, 20108/0 +1452, 20109/1 -1264, 20110/0 +2022, 20111/1 +983, 20112/0 -1846, 20113/1 +819, 20114/0 +2723, 20115/1 +350, 20116/0 -7870
lx3ms.py vs g012m.py: 20101/1 -2751, 20102/0 -4344, 20103/1 -788, 20104/0 -1788, 20105/1 -3592, 20106/0 -19, 20107/1 -1883, 20108/0 -7839, 20109/1 -1820, 20110/0 -2749, 20111/1 -2972, 20112/0 -741, 20113/1 -3696, 20114/0 -4683, 20115/1 -2725, 20116/0 -5408

</details>

---

# PART 1: lx3ms vs lx3 / g012m
# kval: lx3ms head-to-head validation (Kaggle kernels only)

Status 20:17 UTC: COMPLETE. Full original design ran (the coordinator's 12-game cut came back at 20:07 in ~20 min wall, games take
20-40 s each on Kaggle, so a second wave finished the design by 20:15). 96 games, 0 errors, 0 exceptions, all 719 steps DONE/DONE.
Seeds 20001-20024, lx3ms (cand) seat = seed % 2, plus the swapped seat on 20001-20008 -> 32 games per pair, seats 16/16.

## Headline (n=32 per pair; margin = cand coins - opp coins)
| pair (cand vs opp) | wins | win % | mean margin | se | worst game | cand peak step | cand steps > 0.6 s | errors |
|---|---|---|---|---|---|---|---|---|
| lx3ms vs lx3 | 25/32 | 78% | +930 | 278 | -2460 | 0.429 s | 0 | 0 |
| lx3ms vs g012m | 3/32 | 9% | -3269 | 463 | -9885 | 0.528 s | 0 | 0 |
| lx3 vs g012m (reference) | 1/32 | 3% | -4450 | 514 | -11053 | 0.600 s | 0 | 0 |

- PASS RULE for lx3ms vs lx3 (>=60%, mean margin > 0, no game < -15k, peak < 0.6 s, no errors): PASSES on all five counts.
  Seat split: seat 0 13/16 (+1136), seat 1 12/16 (+724). Seat-paired on 20001-8: 7 of 8 seeds positive over both seats, mean +985/game.
  Wave 1 alone (the 12-game cut) was 8/12, +418 se 469; wave 2 (20 games) was 17/20.
- Paired on the same (seed, seat) against g012m: lx3ms beats lx3's result by +1181 se 495 per game (n=32), consistent with the
  micro layer being worth ~+1k vs lx3.
- g012m (at12m, abef1c17) is far stronger than both head-to-head: it beats lx3ms 29/32 and lx3 31/32. If the choice is lx3ms vs
  g012m, these numbers favour g012m (this is h2h only, not a field test).
- Step-time flag for g012m (as the opponent): 2 steps > 0.6 s in 64 games (0.683 s at step 480 of 20001 seat1-of-lx3, 0.713 s at
  step 600 of 20005), both in kernel c1 (32 games, 8 rounds of 4 parallel), none > 1.0 s; g012m median per-game peak 0.428 s.
  lx3 also touched 0.600 s in c1. Likely kernel CPU contention, but g012m's tail is the thinnest of the three.
- lx3ms first call (lib decode) <= 0.373 s; no agent ever > 1.0 s.

## Package (done, not uploaded)
- `agents/final30/kval/build/submission-lx3ms.tar.gz` sha256 `854be5066e0e7fecc2abcae1e490dcae8a3a93c4ae3ba120fb820cc8dec5f5f0`
- contains only `main.py` (mode 0644, uid/gid 0, mtime 0), same layout as submission-v183ms.tar.gz (which carried no LICENSE/NOTICE)
- main.py sha256 `eecdb8f1096268fa3d4e8712ed860057bbc4d0d372881959cc3dd1e0da77ffd8` (= agents/micro/build/lx3ms/main.py)
- loader test (final30/bundle/loadtest.py: extract, get_last_callable, 30 real steps vs PASS, engine 1.32.7): callable `agent`,
  30 steps, peak 0.048 s, no error.

## Setup
- engine kaggle-environments 1.32.7, standard env (no fixed shops), one subprocess per game (719 steps), 4 parallel games per 4-CPU
  kernel, agents loaded with get_last_callable from the source files (as Kaggle does). Step times = wall time per agent call on a
  shared 4-CPU kernel; "peak" excludes the first call (reported separately, <= 0.30 s).
- dataset nulldata/kaggriculture-kval: lx3ms.py (eecdb8f1), lx3.py (e55f9a8a), g012m.py = at12m (abef1c17), kvgame.py.
- kernels nulldata/kaggriculture-kval-{a1..a5 (lx3ms-lx3), b1..b4 (lx3ms-g012m), c1 (lx3-g012m)}. Raw: kout/<k>/res.jsonl; summ.py.
- not done: no field test vs other opponents (h2h only), no seeds beyond 20024.

## Per-game tables

### lx3ms vs lx3: n=32 (errors 0), wins 25/32 = 78%, mean margin +930 se 278, worst -2460, cand peak step 0.429 s, cand steps>0.6 s 0, opp peak 0.477 s

| seed | seat | cand | opp | margin | win | cand peak s (step) | cand first s | cand >0.6 | opp peak s | exc | wall s | kernel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20001 | 1 | 92436 | 91967 | +469 | 1 | 0.358 (384) | 0.172 | 0 | 0.329 | 0/0 | 17.7 | a1 |
| 20001 | 0 | 94030 | 91811 | +2219 | 1 | 0.411 (384) | 0.363 | 0 | 0.412 | 0/0 | 28.1 | a4 |
| 20002 | 0 | 94135 | 89748 | +4387 | 1 | 0.354 (600) | 0.182 | 0 | 0.204 | 0/0 | 17.2 | a1 |
| 20002 | 1 | 89273 | 91733 | -2460 | 0 | 0.413 (504) | 0.284 | 0 | 0.477 | 0/0 | 27.2 | a4 |
| 20003 | 1 | 104344 | 105014 | -670 | 0 | 0.357 (624) | 0.170 | 0 | 0.221 | 0/0 | 16.8 | a1 |
| 20003 | 0 | 105032 | 105391 | -359 | 0 | 0.359 (648) | 0.368 | 0 | 0.293 | 0/0 | 25.7 | a4 |
| 20004 | 0 | 120833 | 118923 | +1910 | 1 | 0.352 (648) | 0.180 | 0 | 0.405 | 0/0 | 17.0 | a1 |
| 20004 | 1 | 120764 | 118818 | +1946 | 1 | 0.366 (480) | 0.284 | 0 | 0.409 | 0/0 | 26.4 | a4 |
| 20005 | 1 | 121242 | 120221 | +1021 | 1 | 0.420 (648) | 0.276 | 0 | 0.409 | 0/0 | 26.9 | a2 |
| 20005 | 0 | 92826 | 90808 | +2018 | 1 | 0.410 (408) | 0.285 | 0 | 0.411 | 0/0 | 27.4 | a4 |
| 20006 | 0 | 85234 | 84344 | +890 | 1 | 0.419 (624) | 0.286 | 0 | 0.371 | 0/0 | 26.9 | a2 |
| 20006 | 1 | 87278 | 85545 | +1733 | 1 | 0.361 (672) | 0.274 | 0 | 0.362 | 0/0 | 26.6 | a4 |
| 20007 | 1 | 108211 | 107900 | +311 | 1 | 0.411 (384) | 0.276 | 0 | 0.410 | 0/0 | 27.0 | a2 |
| 20007 | 0 | 108185 | 107871 | +314 | 1 | 0.409 (384) | 0.279 | 0 | 0.411 | 0/0 | 27.0 | a4 |
| 20008 | 0 | 120041 | 121027 | -986 | 0 | 0.409 (432) | 0.287 | 0 | 0.416 | 0/0 | 25.9 | a2 |
| 20008 | 1 | 116615 | 113605 | +3010 | 1 | 0.429 (504) | 0.293 | 0 | 0.421 | 0/0 | 26.1 | a4 |
| 20009 | 1 | 87693 | 89446 | -1753 | 0 | 0.410 (672) | 0.279 | 0 | 0.286 | 0/0 | 25.9 | a3 |
| 20010 | 0 | 131777 | 131282 | +495 | 1 | 0.422 (384) | 0.291 | 0 | 0.417 | 0/0 | 26.2 | a3 |
| 20011 | 1 | 128769 | 128680 | +89 | 1 | 0.358 (672) | 0.279 | 0 | 0.412 | 0/0 | 24.9 | a3 |
| 20012 | 0 | 90191 | 91339 | -1148 | 0 | 0.360 (624) | 0.297 | 0 | 0.326 | 0/0 | 26.0 | a3 |
| 20013 | 1 | 121224 | 119038 | +2186 | 1 | 0.346 (384) | 0.164 | 0 | 0.212 | 0/0 | 14.9 | a4 |
| 20014 | 0 | 126099 | 125795 | +304 | 1 | 0.352 (600) | 0.171 | 0 | 0.190 | 0/0 | 15.1 | a4 |
| 20015 | 1 | 113139 | 112294 | +845 | 1 | 0.361 (552) | 0.293 | 0 | 0.362 | 0/0 | 24.6 | a5 |
| 20016 | 0 | 134366 | 132484 | +1882 | 1 | 0.410 (648) | 0.307 | 0 | 0.373 | 0/0 | 24.4 | a5 |
| 20017 | 1 | 109320 | 105940 | +3380 | 1 | 0.407 (648) | 0.288 | 0 | 0.408 | 0/0 | 26.8 | a5 |
| 20018 | 0 | 98372 | 96001 | +2371 | 1 | 0.399 (648) | 0.292 | 0 | 0.410 | 0/0 | 26.3 | a5 |
| 20019 | 1 | 116954 | 114377 | +2577 | 1 | 0.355 (528) | 0.262 | 0 | 0.253 | 0/0 | 25.5 | a5 |
| 20020 | 0 | 88954 | 87757 | +1197 | 1 | 0.359 (600) | 0.286 | 0 | 0.364 | 0/0 | 26.2 | a5 |
| 20021 | 1 | 120998 | 120740 | +258 | 1 | 0.360 (384) | 0.276 | 0 | 0.408 | 0/0 | 24.4 | a5 |
| 20022 | 0 | 105198 | 102821 | +2377 | 1 | 0.388 (552) | 0.288 | 0 | 0.371 | 0/0 | 24.9 | a5 |
| 20023 | 1 | 79405 | 80763 | -1358 | 0 | 0.355 (600) | 0.170 | 0 | 0.180 | 0/0 | 15.9 | a5 |
| 20024 | 0 | 111282 | 110977 | +305 | 1 | 0.352 (528) | 0.183 | 0 | 0.221 | 0/0 | 15.0 | a5 |

### lx3ms vs g012m: n=32 (errors 0), wins 3/32 = 9%, mean margin -3269 se 463, worst -9885, cand peak step 0.528 s, cand steps>0.6 s 0, opp peak 0.478 s

| seed | seat | cand | opp | margin | win | cand peak s (step) | cand first s | cand >0.6 | opp peak s | exc | wall s | kernel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20001 | 1 | 91438 | 96389 | -4951 | 0 | 0.424 (384) | 0.281 | 0 | 0.468 | 0/0 | 40.3 | b1 |
| 20001 | 0 | 92049 | 96637 | -4588 | 0 | 0.432 (624) | 0.367 | 0 | 0.467 | 0/0 | 34.4 | b3 |
| 20002 | 0 | 96008 | 102900 | -6892 | 0 | 0.425 (408) | 0.294 | 0 | 0.457 | 0/0 | 34.0 | b1 |
| 20002 | 1 | 96384 | 103711 | -7327 | 0 | 0.421 (600) | 0.280 | 0 | 0.440 | 0/0 | 30.3 | b3 |
| 20003 | 1 | 104098 | 105833 | -1735 | 0 | 0.359 (528) | 0.283 | 0 | 0.449 | 0/0 | 36.3 | b1 |
| 20003 | 0 | 105868 | 107811 | -1943 | 0 | 0.369 (480) | 0.373 | 0 | 0.454 | 0/0 | 32.9 | b3 |
| 20004 | 0 | 113448 | 118254 | -4806 | 0 | 0.528 (504) | 0.295 | 0 | 0.476 | 0/0 | 38.0 | b1 |
| 20004 | 1 | 117385 | 122510 | -5125 | 0 | 0.360 (528) | 0.302 | 0 | 0.458 | 0/0 | 35.0 | b3 |
| 20005 | 1 | 76859 | 79621 | -2762 | 0 | 0.354 (552) | 0.172 | 0 | 0.421 | 0/0 | 20.9 | b1 |
| 20005 | 0 | 92000 | 94859 | -2859 | 0 | 0.408 (600) | 0.287 | 0 | 0.413 | 0/0 | 32.0 | b3 |
| 20006 | 0 | 83643 | 87103 | -3460 | 0 | 0.352 (600) | 0.176 | 0 | 0.360 | 0/0 | 20.3 | b1 |
| 20006 | 1 | 82677 | 85978 | -3301 | 0 | 0.362 (504) | 0.277 | 0 | 0.421 | 0/0 | 31.5 | b3 |
| 20007 | 1 | 106593 | 112829 | -6236 | 0 | 0.437 (456) | 0.266 | 0 | 0.478 | 0/0 | 30.9 | b2 |
| 20007 | 0 | 106432 | 113330 | -6898 | 0 | 0.422 (600) | 0.296 | 0 | 0.450 | 0/0 | 31.5 | b3 |
| 20008 | 0 | 123645 | 122803 | +842 | 1 | 0.418 (600) | 0.294 | 0 | 0.454 | 0/0 | 34.9 | b2 |
| 20008 | 1 | 124595 | 124235 | +360 | 1 | 0.448 (600) | 0.273 | 0 | 0.438 | 0/0 | 33.5 | b3 |
| 20009 | 1 | 86291 | 88636 | -2345 | 0 | 0.354 (600) | 0.270 | 0 | 0.396 | 0/0 | 30.9 | b2 |
| 20010 | 0 | 124656 | 127014 | -2358 | 0 | 0.422 (384) | 0.288 | 0 | 0.428 | 0/0 | 31.7 | b2 |
| 20011 | 1 | 125721 | 130715 | -4994 | 0 | 0.292 (600) | 0.161 | 0 | 0.336 | 0/0 | 18.3 | b2 |
| 20012 | 0 | 89238 | 92429 | -3191 | 0 | 0.353 (600) | 0.167 | 0 | 0.361 | 0/0 | 17.6 | b2 |
| 20013 | 1 | 120475 | 121287 | -812 | 0 | 0.356 (600) | 0.277 | 0 | 0.368 | 0/0 | 20.0 | b3 |
| 20014 | 0 | 126988 | 127616 | -628 | 0 | 0.352 (624) | 0.172 | 0 | 0.311 | 0/0 | 19.9 | b3 |
| 20015 | 1 | 111143 | 115591 | -4448 | 0 | 0.352 (600) | 0.163 | 0 | 0.364 | 0/0 | 22.6 | b4 |
| 20016 | 0 | 131731 | 133569 | -1838 | 0 | 0.352 (528) | 0.170 | 0 | 0.378 | 0/0 | 23.5 | b4 |
| 20017 | 1 | 104088 | 109528 | -5440 | 0 | 0.352 (600) | 0.161 | 0 | 0.368 | 0/0 | 23.3 | b4 |
| 20018 | 0 | 86356 | 87141 | -785 | 0 | 0.356 (384) | 0.167 | 0 | 0.367 | 0/0 | 22.1 | b4 |
| 20019 | 1 | 113005 | 114288 | -1283 | 0 | 0.354 (648) | 0.162 | 0 | 0.386 | 0/0 | 23.2 | b4 |
| 20020 | 0 | 83168 | 93053 | -9885 | 0 | 0.359 (600) | 0.163 | 0 | 0.434 | 0/0 | 22.1 | b4 |
| 20021 | 1 | 133429 | 134846 | -1417 | 0 | 0.356 (384) | 0.176 | 0 | 0.364 | 0/0 | 23.0 | b4 |
| 20022 | 0 | 108733 | 106329 | +2404 | 1 | 0.356 (504) | 0.162 | 0 | 0.376 | 0/0 | 22.3 | b4 |
| 20023 | 1 | 96960 | 99369 | -2409 | 0 | 0.327 (480) | 0.110 | 0 | 0.291 | 0/0 | 13.3 | b4 |
| 20024 | 0 | 110582 | 114076 | -3494 | 0 | 0.289 (600) | 0.104 | 0 | 0.275 | 0/0 | 12.9 | b4 |

### lx3 vs g012m (reference): n=32 (errors 0), wins 1/32 = 3%, mean margin -4450 se 514, worst -11053, cand peak step 0.600 s, cand steps>0.6 s 0, opp peak 0.713 s

| seed | seat | cand | opp | margin | win | cand peak s (step) | cand first s | cand >0.6 | opp peak s | exc | wall s | kernel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20001 | 1 | 90853 | 95348 | -4495 | 0 | 0.418 (528) | 0.278 | 0 | 0.683 | 0/0 | 36.7 | c1 |
| 20001 | 0 | 88241 | 98641 | -10400 | 0 | 0.414 (480) | 0.260 | 0 | 0.431 | 0/0 | 32.9 | c1 |
| 20002 | 0 | 87371 | 89953 | -2582 | 0 | 0.412 (672) | 0.299 | 0 | 0.439 | 0/0 | 33.9 | c1 |
| 20002 | 1 | 88507 | 95885 | -7378 | 0 | 0.416 (672) | 0.229 | 0 | 0.383 | 0/0 | 29.6 | c1 |
| 20003 | 1 | 102611 | 107490 | -4879 | 0 | 0.357 (432) | 0.281 | 0 | 0.467 | 0/0 | 35.0 | c1 |
| 20003 | 0 | 102729 | 106953 | -4224 | 0 | 0.363 (528) | 0.261 | 0 | 0.418 | 0/0 | 31.1 | c1 |
| 20004 | 0 | 116722 | 123978 | -7256 | 0 | 0.411 (432) | 0.303 | 0 | 0.515 | 0/0 | 38.0 | c1 |
| 20004 | 1 | 116715 | 123985 | -7270 | 0 | 0.371 (648) | 0.339 | 0 | 0.438 | 0/0 | 33.6 | c1 |
| 20005 | 1 | 79995 | 83103 | -3108 | 0 | 0.416 (648) | 0.249 | 0 | 0.713 | 0/0 | 31.6 | c1 |
| 20005 | 0 | 79638 | 83015 | -3377 | 0 | 0.414 (336) | 0.270 | 0 | 0.432 | 0/0 | 30.7 | c1 |
| 20006 | 0 | 90758 | 95563 | -4805 | 0 | 0.414 (456) | 0.291 | 0 | 0.379 | 0/0 | 32.6 | c1 |
| 20006 | 1 | 90469 | 96355 | -5886 | 0 | 0.423 (672) | 0.250 | 0 | 0.384 | 0/0 | 32.7 | c1 |
| 20007 | 1 | 107638 | 111822 | -4184 | 0 | 0.471 (600) | 0.250 | 0 | 0.442 | 0/0 | 33.1 | c1 |
| 20007 | 0 | 107613 | 111771 | -4158 | 0 | 0.600 (600) | 0.272 | 0 | 0.426 | 0/0 | 31.6 | c1 |
| 20008 | 0 | 112038 | 121936 | -9898 | 0 | 0.420 (528) | 0.272 | 0 | 0.447 | 0/0 | 35.2 | c1 |
| 20008 | 1 | 124681 | 123199 | +1482 | 1 | 0.427 (504) | 0.249 | 0 | 0.451 | 0/0 | 30.1 | c1 |
| 20009 | 1 | 87326 | 90587 | -3261 | 0 | 0.556 (624) | 0.244 | 0 | 0.396 | 0/0 | 30.0 | c1 |
| 20010 | 0 | 133196 | 133209 | -13 | 0 | 0.412 (624) | 0.245 | 0 | 0.440 | 0/0 | 32.1 | c1 |
| 20011 | 1 | 125570 | 130898 | -5328 | 0 | 0.405 (648) | 0.250 | 0 | 0.418 | 0/0 | 32.6 | c1 |
| 20012 | 0 | 88716 | 93512 | -4796 | 0 | 0.411 (480) | 0.323 | 0 | 0.424 | 0/0 | 29.2 | c1 |
| 20013 | 1 | 119266 | 120925 | -1659 | 0 | 0.409 (384) | 0.224 | 0 | 0.475 | 0/0 | 32.9 | c1 |
| 20014 | 0 | 125135 | 128533 | -3398 | 0 | 0.407 (480) | 0.262 | 0 | 0.446 | 0/0 | 33.1 | c1 |
| 20015 | 1 | 110405 | 116210 | -5805 | 0 | 0.415 (648) | 0.247 | 0 | 0.402 | 0/0 | 32.8 | c1 |
| 20016 | 0 | 133382 | 135106 | -1724 | 0 | 0.373 (432) | 0.271 | 0 | 0.445 | 0/0 | 34.2 | c1 |
| 20017 | 1 | 104228 | 110659 | -6431 | 0 | 0.422 (624) | 0.239 | 0 | 0.455 | 0/0 | 32.1 | c1 |
| 20018 | 0 | 92221 | 97876 | -5655 | 0 | 0.370 (672) | 0.263 | 0 | 0.430 | 0/0 | 31.5 | c1 |
| 20019 | 1 | 115766 | 116806 | -1040 | 0 | 0.431 (624) | 0.254 | 0 | 0.418 | 0/0 | 31.8 | c1 |
| 20020 | 0 | 82574 | 93627 | -11053 | 0 | 0.320 (504) | 0.268 | 0 | 0.496 | 0/0 | 30.7 | c1 |
| 20021 | 1 | 133670 | 133895 | -225 | 0 | 0.309 (600) | 0.234 | 0 | 0.397 | 0/0 | 31.0 | c1 |
| 20022 | 0 | 121693 | 123595 | -1902 | 0 | 0.347 (552) | 0.263 | 0 | 0.413 | 0/0 | 33.5 | c1 |
| 20023 | 1 | 88013 | 92864 | -4851 | 0 | 0.416 (480) | 0.249 | 0 | 0.384 | 0/0 | 29.0 | c1 |
| 20024 | 0 | 111144 | 113970 | -2826 | 0 | 0.411 (480) | 0.270 | 0 | 0.403 | 0/0 | 32.1 | c1 |

