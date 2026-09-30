# pairselect: which two builds should be active at the 30 Sep 23:59 UTC close

Written 29 Sep 2026, 22:05-22:40 UTC. Data pulled 22:05 UTC. No uploads, no simulations, no agent code changed.
The only new code is read-only analysis in this folder.

## 0. Answer (numbers first)
- **Recommended final pair: lx1 + v183ms.** This takes two uploads (U1 lx1, then U2 v183ms re-upload; plan in §5).
  - Model value E[team] = 2682 (sd 59) in current-LB units.
  - Status quo (V183re + v183ms) = 2673; V183re + lx1 = 2671; V183 twin = 2659; lx1 twin = 2654; V183 + lx3 = 2662; V183 + comb1 = 2664.
  - Across all 7 sensitivity settings, lx1 + v183ms is best or tied-best: +7 to +33 over the status quo.
  - **The gain is small.** Every pair lands at 2650-2720, and 10th place is about 2850. The choice of pair moves the expected score by ≤ 30 points.
- **Runner-up: V183re + lx1.** This is the state after U1 alone. Use it if the live micro check (§5) comes out ≤ -60, or if U2 cannot be validated in time.
- **Twin or diverse pick?** Diverse wins here.
  - The two lineages are statistically tied: V183 2646-2684 and lx1 2646-2674 on the random-effects fit, with se 38-77.
  - Our uncertainty about each build's true strength (±40-55) is larger than the post-deadline measurement noise (±15-40). Two independent lineages therefore carry more option value than two copies of one.
  - A byte-identical twin only diversifies the BT measurement noise. It is worth about +14 points, which is 10-25 points below the diverse pair in every setting.
  - A twin would win only if one build led the others by more than ~1.5 combined se. None does.
- **No counter-archetype pick exists** (§3). Every candidate is weakest against the same programmes: the late tomato/carrot "t1-idle Majkel-style" and "family v1" archetypes, about 80% of the top-30 field. The second slot is chosen for independence of estimation error, not for matchup.
- **Probability of the final team score** (recommended pair; model in §4; central case, with the range over settings):

| threshold | P, central | P, range |
|---|---|---|
| ≥ 2800 | 2.6% | 1-9%; 9% only if the final table lands on Kaggle's own pre-deadline scale for us (+35-45) |
| ≥ 2900 | < 0.1% | ≤ 0.2% |
| ≥ 3000 | ~0 | ~0 |
| top 10 | ~0.5% | 0.2-2% |

  None of our builds has ever shown 2800-level strength against the current top-30 field live. Against labelled top-field archetypes, V183 is 1-15 and lx3 is 2-19.

## 1. Data (live2.py → games.json; lb_now.json = LB at 22:05 UTC)
- **Pull.** Every public episode of 13 of our submissions since 25 Sep: 1551 games.
- **Kept per game:** episode id, end time, seat, both rewards, margin, opponent team id and name, opponent submission id, the opponent's current LB team rating and rank.
- **No per-game rating.** The API returns no updatedScore, so per-game ratings at game time are not available.
- **LB now:**
  - #1 MMPQ 3025, #2 DSM 2936, #3 DECEM 2914, #4 Vadim 2912, #5 Victor 2889, #10 tetsuya 2849, #20 feles99 2775, #30 2720.
  - Ours: 2557, rank 90.
  - Top teams upload new subs daily. All top-15 active subs are from 28-29 Sep (see fieldnow/field_subs_now.json).

### Band table (W-L by opponent's CURRENT rating; all games)

| build | n | W-L | <2300 | 2300-2500 | 2500-2600 | 2600-2700 | 2700-2800 | 2800-2900 | 2900+ | 2700+ mean margin |
|---|---|---|---|---|---|---|---|---|---|---|
| V183re 56686499 | 34 | 28-6 | 18-0 | 4-1 | 4-4 | 2-1 | - | - | - | n 0 |
| v183ms 56686494 | 32 | 29-3 | 19-0 | 5-0 | 5-3 | - | - | - | - | n 0 |
| V183 56641767 | 114 | 71-43 | 20-2 | 15-3 | 12-5 | 19-14 | 4-13 | 1-6 | - | -8.3k (24) |
| hybrid 56655050 | 166 | 104-62 | 43-3 | 24-7 | 28-23 | 8-18 | 1-6 | 0-5 | - | -5.9k (12) |
| mrh 56661366 | 138 | 84-54 | 23-4 | 31-6 | 26-33 | 4-9 | 0-1 | 0-1 | - | -10.9k (2) |
| lx1re 56654841 | 92 | 84-8 | 81-8 | 1-0 | 1-0 | 1-0 | - | - | - | n 0 |
| lx1 56580159 | 59 | 47-12 | 24-0 | 6-5 | 10-3 | 4-2 | 1-0 | 2-2 | - | -0.1k (5) |
| lx3 56584428 | 177 | 107-70 | 28-5 | 25-9 | 26-12 | 16-28 | 9-10 | 3-5 | 0-1 | +0.6k (28) |
| lx2 56582790 | 172 | 124-48 | 57-8 | 28-10 | 23-10 | 9-10 | 4-5 | 3-3 | 0-2 | -0.7k (17) |
| lx4 56613772 | 148 | 93-55 | 31-4 | 23-3 | 23-16 | 13-18 | 2-8 | 1-6 | - | -5.5k (17) |
| comb1 56618739 | 170 | 112-58 | 38-3 | 24-11 | 26-15 | 18-17 | 4-5 | 2-7 | - | -3.0k (18) |

The per-team table (build × current top 30) is in `live_tables.md`. Totals against the current top 30:

| build | vs top 30: W-L | mean margin | vs top 10: W-L |
|---|---|---|---|
| V183 | 3-15 | -9.6k | 1-3 |
| hybrid | 1-9 | - | 0-3 |
| lx1 | 3-2 | - | 0-2 |
| lx3 | 6-11 | +0.3k | 0-1 |
| lx2 | 3-8 | - | - |
| lx4 | 1-10 | - | - |
| comb1 | 4-11 | - | 0-5 |
| V183re, v183ms | 0 games so far | - | - |

## 2. Live strength estimates (logistic Bradley-Terry, opponents anchored)
Opponent anchors are current LB team ratings. The scale is fitted by profile likelihood: 120-160 points per logit (95% interval 100-320) when opponents are ≥ 2300-2600. The Elo-400 scale (174) is also shown.

| build | A: opp ≥ 2500, s=120 | A: opp ≥ 2500, s=174 | A, burn-in (games 21+) excluded, s=160 | B: opp-sub RE, τ=150, all games | B: τ=100, opp ≥ 2300 | B: τ=250, opp ≥ 2300 | n (opp ≥ 2500) |
|---|---|---|---|---|---|---|---|
| V183 (orig) | 2661 ± 30 | 2659 ± 42 | 2660 ± 39 | 2646 ± 41 | 2664 ± 38 | 2684 ± 47 | 74 |
| V183 + V183re pooled | 2652 ± 32 (s=140) | 2652 ± 39 | - | - | - | - | 85 |
| V183re | 2590 ± 74 | 2600 ± 106 | - | 2629 ± 92 | 2612 ± 90 | 2633 ± 111 | 11 |
| v183ms | 2601 ± 88 | 2629 ± 127 | - | 2709 ± 115 | 2690 ± 112 | 2735 ± 134 | 8 |
| lx1 | 2760 ± 58 | 2805 ± 81 | 2793 ± 75 | 2662 ± 68 | 2674 ± 64 | 2646 ± 77 | 24 |
| lx2 | 2660 ± 32 | 2675 ± 44 | 2671 ± 41 | 2587 ± 36 | 2645 ± 36 | 2626 ± 45 | 69 |
| lx3 | 2643 ± 24 | 2642 ± 34 | 2643 ± 32 | 2602 ± 32 | 2633 ± 30 | 2632 ± 38 | 110 |
| comb1 | 2641 ± 26 | 2649 ± 37 | 2645 ± 35 | 2598 ± 34 | 2620 ± 32 | 2613 ± 40 | 94 |
| lx4 | 2599 ± 27 | 2590 ± 39 | 2592 ± 36 | 2590 ± 35 | 2617 ± 34 | 2621 ± 42 | 87 |
| hybrid | 2559 ± 27 | 2544 ± 38 | 2544 ± 36 | 2562 ± 34 | 2572 ± 33 | 2589 ± 41 | 89 |
| mrh | 2515 ± 29 | 2495 ± 42 | 2505 ± 39 | 2541 ± 35 | 2562 ± 34 | 2575 ± 43 | 74 |

Model A anchors each opponent at its current team rating. Model B (`fit4.py`) gives each opponent submission its own strength, with prior N(current team rating, τ²). Shared opponents then link our builds directly.

Paired differences from the model B fits (τ = 150 / 100 / 250):

| difference | τ=150 | τ=100 | τ=250 |
|---|---|---|---|
| lx1 − V183 | +16 ± 79 | +10 ± 75 | -38 ± 90 |
| mrh − lx1 | -122 ± 76 | -112 ± 73 | -71 ± 87 |
| v183ms − V183 | +62 ± 122 | +26 ± 118 | +52 ± 142 |
| hybrid − V183 | -84 | -92 | -95 |
| lx3 − V183 | -44 | -31 | -52 |

A joint fit with half-day offsets on the opponent anchors (`fit3.py`) finds no significant drift (all offsets within -53..+3, se 50-90). Its estimates match the table: V183 2645, lx1 2756 ± 109, mrh 2481, hybrid 2519.

Biases and how they were handled:
1. **lx1's 59 games all came in its climb phase** (26 Sep 13:26-16:51 UTC) against a field that has since been re-uploaded.
   - Only 5 of those games were against opponents ≥ 2700 (3-2); 24 were against ≥ 2500 (17-7).
   - It is the maximum of about 12 noisy build estimates, so a winner's curse applies.
   - Offline evidence points the other way: V183 beats lx1 89.6% head-to-head on fresh seeds (micro b2), and the tape judge gives V183 +5.1k/game over lx1.
   - With soft opponent effects (model B) its lead over V183 disappears. Used: **lx1 = 2655 ± 50**.
2. **V183re and v183ms have 34 and 32 games** (8-11 against ≥ 2500). They carry no information yet. V183re is pooled with V183 orig: **V183 lineage = 2660 ± 38**.
3. **The micro delta, live, is +10 ± 45.** Three pieces of evidence were combined:
   - offline prior +40 ± 50: tape judge +823/game (win 0.68 → 0.72), minus the ~40-point calibration haircut from the replay judges;
   - live mrh − lx1 = -71..-122 ± 75-87 (micro on the lx1 lineage, including OPT_HIRE);
   - live v183ms − V183 = +26..+62 ± 120-140.

   Precision-weighted, this gives +10..+15 ± 42. **There is no live sign yet that micro helps.** mrh's own coins were 101.7k (se 2.4) against the 2500-2700 band vs lx1's 109.9k (4.5).
4. **Fresh uploads of strong code look like weak teams.**
   - Several "weak" teams (current rating 600-2300) score 120-141k against us. These are fresh uploads of strong code or since-retired subs; that is why the global logistic scale is flat (> 390/logit). Fits therefore use opponents ≥ 2300 or ≥ 2500.
   - The lx lineage loses more often to such teams (lx1re 8/89, mrh 4/27, lx3 5/33) than the V183 lineage does (5/105). This is a mild signal only, not significant.
   - Old games anchored at today's team ratings bias older builds up slightly. Kaggle's frozen scores for our subs sit 30-110 above these estimates because the LB has deflated (#10 was 2882 on 26 Sep; it is 2849 now).

## 3. Candidate × archetype matrix (current top field)
Archetype labels come from topfield/archetypes.json (26 Sep): the exact sub where known, otherwise the team's majority label.
- Of 209 live games against opponents ≥ 2650, 132 are against teams or subs that have no label (new since 26 Sep). This is why no live matrix exists for V183re or v183ms.
- The "tape" figures are intact-game replay judges, which are known to be optimistic by ~40 points and to misrank against live results.

| archetype (share of 26 Sep top-30 subs) | V183 / v183ms | lx3 / lx3m | lx1 / mrh | hybrid | comb1 / lx4 |
|---|---|---|---|---|---|
| Majkel-style t1 idle, late tomato/melon (19/59) | live V183 0-7 -13.8k; tape (Majkel 124-game set, intact) V183 49%, v183ms 53% | live lx3 0-11 -9.9k; tape lx3 37%, lx3m 38%; topfield lx3 58% pooled, Majkel 56577255 16% | live lx1 1-0; tape lx1 29% (worst), mrh 38%; topfield lx1 top-10 27% | live 2-2 -6.1k; tape 38% (hybm 38%) | live comb1 0-2, lx4 1-2 |
| family v1 (Majkel/DSM opening, tomatoes d12+) (28/59) | live V183 1-6 -9.8k, V183re 0-1 | live lx3 2-3 -0.6k; topfield 67% | live lx1 0-3 -8.0k, mrh 0-1; topfield lx1 58% | 1-2 | comb1 0-6 -11.5k, lx4 0-3 |
| family v2 (MMPQ / Vadim / DECEM newest) (5/59) | - | topfield lx3 54% | topfield lx1 42% | - | - |
| Boey programme (1/59) | - | topfield lx3 32% | topfield lx1 28% | - | - |
| wheat churn (2/59) | live 0-1 | live lx3 0-4 -11.9k; topfield 77% | - | 0-1 | lx4 0-1 |
| unlabelled (new subs), opp ≥ 2650 | live V183 7-14 -5.4k | live lx3 20-16 +1.7k | live lx1 6-0, mrh 0-4 | 3-8 | comb1 8-7, lx4 8-15 |

Weakest archetype per candidate. For every candidate it is the Majkel-style t1-idle programme, then family v1: late tomato/carrot/strawberry waves that overtake us in the last 5-8 days.

| candidate | weakest against | evidence |
|---|---|---|
| V183 / v183ms / v183m | Majkel-style | live 0-7 |
| lx3 / lx3m | Majkel-style, plus the Boey programme on tapes | live 0-11 |
| lx1 / mrh | Majkel-style | worst tape figure, 29% |
| hybrid | Majkel-style and family v1 | the step-264 switch fires into lx3 mode against these |
| comb1 / lx4 | family v1 | 0-6 / 0-3 |

**Field-mixture sensitivity.** Every build's win rate against every labelled archetype is ≤ 50% live, so shifting the mixture (more top-10 weight, more family v1, more Majkel-style) lowers all builds together and does not reorder them. The BT ranking is mixture-invariant by construction, and the per-archetype live samples (n 1-11) cannot overturn it. The topfield result from 26 Sep (lx3 > lx2 > lx1 > f3 under every mixture) says the same.

**Implied win probability** at s = 160 for a build at 2660:
- against a 2750 opponent: 36%;
- against 2850: 23%;
- against 2950: 14%.

## 4. Pair model (`pairmc.py`; Monte Carlo over our uncertainty, not a game simulation)
**Assumptions:**
- True strengths (current-LB units):

| build | strength |
|---|---|
| V183 lineage | N(2660, 38) |
| v183ms | V183 + N(10, 45) |
| lx1 | N(2655, 50), independent of V183 |
| lx3 | N(2640, 35) |
| lx2 | N(2665, 40) |
| comb1 | N(2643, 38) |
| mrh | 2505 ± 39 |
| hybrid | 2544 ± 36 |
| lx4 | 2592 ± 36 |

  lx2, lx3 and comb1 share a lineage term N(0, 20).
- A common final-day field shift of N(-15, 30).
- Post-deadline BT noise per bot of N(0, 25), since ~300 games near p = 0.5 give about 19.
- 10th place ~ N(2855, 25).
- Team score = max of the two bots. 400k draws per setting.

E[team] by setting (P(≥ 2800) in brackets):

| setting | status quo V183re + v183ms | V183re + lx1 (1 upload) | **lx1 + v183ms (2 uploads)** | V183 twin | lx1 twin | V183 + lx3m |
|---|---|---|---|---|---|---|
| base (micro +10, lx1 2655) | 2673 (2.1%) | 2671 (0.8%) | **2682 (2.6%)** | 2659 (0.4%) | 2654 (0.9%) | 2671 (1.2%) |
| micro -30 | 2656 (0.6%) | 2671 (0.8%) | 2663 (1.0%) | 2659 | 2654 | 2658 |
| micro +40 | 2693 (5.3%) | 2671 | **2701 (5.7%)** | 2659 | 2654 | 2685 |
| BT noise 15 | 2670 | 2669 | **2680** | 2653 | 2648 | 2669 |
| BT noise 40 | 2679 | 2676 | **2686** | 2668 | 2662 | 2676 |
| lx1 2690, V183 2650 | 2663 | 2688 | **2696 (3.8%)** | 2649 | 2689 | 2666 |
| Kaggle-score scale (V183 2695, lx1 2700) | 2708 (6.7%) | 2711 (4.7%) | **2721 (9.0%)** | 2694 | 2699 | - |

- P(≥ 2900) ≤ 0.2% and P(≥ 3000) ≈ 0 in every setting.
- Full tables: `mc_*.txt`, `pairmc_*.json`.
- hybrid, mrh and lx4 lose to every alternative, and so do V183 + lx3 / comb1 (2657-2664).

## 5. Operational plan (every upload needs the user's explicit go; only the coordinator uploads)
**Active now:** v183ms 56686494 and V183re 56686499.
- Both were submitted 29 Sep 20:03, and v183ms has the lower id, so **v183ms is the OLDER slot and the next upload retires v183ms, not V183re.**
- So the recommended pair needs two sequential uploads.
- V183re is Codex's frozen V183. Retiring it in U2 should be agreed with Codex (COLLABORATION.md).

| step | package | SHA-256 (archive / main.py) | retires | when |
|---|---|---|---|---|
| U1 | lx1: `agents/lateexec/build/submission-lx1.tar.gz` (validated COMPLETE twice before) | 394d7954bbe0 / 8408db9d2a65 | v183ms 56686494 | 30 Sep 06:00-10:00 UTC. The earlier the better: U1 happens in both branches and gives lx1 a few hours of live evidence. Latest 12:00 UTC. |
| U2 | v183ms: `agents/micro/build/submission-v183ms.tar.gz`, byte-identical to 56686494 | 2c3d9470d4ba / cba37327077b | V183re 56686499 | Only after U1 shows COMPLETE and after the 14:00 check. Latest upload 18:00 UTC. |
| (U3, only on hard failure) | V183 exact: `research/codex/2026-09-05/v179-gate-loader/build/dated_gate/agent.tar.gz` | afa68661de1a / 80d3cfc8 | lx1 | Only if lx1 shows ERROR/timeout episodes, or R < 2500 on ≥ 25 games against ≥ 2500. Must be uploaded by 18:00. |

Why these times:
- Validation took 10 min on 29 Sep 20:03 and 4.5 h for mrh on 29 Sep 03:29. An upload at 18:00 is COMPLETE by 22:30 even in the worst case.
- Never have two uploads pending at once. If U1 errors and U2 is already queued, U2 would retire V183re and leave an untested pair.
- If U2 is not COMPLETE-able by 18:00, stop. The final pair is then V183re + lx1, the runner-up, which is about equal to the status quo (2671 vs 2673).
- Engine for all packages: kaggle_environments 1.32.7.

Live evidence at 30 Sep 14:00 UTC that would change the decision. To re-run: `python live2.py && python ana.py && python fit4.py 150 160 2300 && python fit2.py`.
- **Micro check.** Compute v183ms − V183re on the same window (29 Sep 20:00 → U1 time), model B, opp ≥ 2300, ≥ 40 games each against ≥ 2500.
  - ≤ -60: skip U2. Final: V183re + lx1.
  - ≥ -60: do U2. Final: lx1 + v183ms.
  - If U1 happens early, this window is ~10-14 h, about 100+ games each. That is enough only for a catastrophe-level check (se ~60-80).
- **lx1 check** (after U1): its share of losses against opponents rated < 2300 now. If it is ≥ 15% over ≥ 40 games, or model B R < 2550 on ≥ 20 games against ≥ 2500, lx1 is failing live. Replace it via U3 if time allows, otherwise accept V183re + lx1 → v183ms + lx1 as planned.
- **Keep the status quo instead (no uploads)** if the user prefers zero upload risk. The cost is about -10 points E[team] and -0.5 pp P(≥ 2800).
- **Only one thing would move P(top 10) meaningfully:** a new build from another final30 agent with live R ≥ 2800 on ≥ 40 games against ≥ 2700 before 14:00. That would take slot U2's place. No existing candidate is close.

## 6. Not done / caveats
- **Archetypes of the current top field.** The 28-30 Sep top subs were not classified from replays; the labels are from 26 Sep, and 63% of the relevant games are unlabelled. No replays were downloaded.
- **Opponent ratings at game time** are not available from the API. Current team ratings are used as anchors, and model B treats them as noisy priors.
- **Untested builds.** lx3m and v183m were never live and have no tarballs (main.py only). They appear only in the model, as parent + micro delta.
- **No game simulations; no Kaggle kernels or pods were used.**
- **Model form.** The MC is a stylised model of our uncertainty. Its absolute probabilities depend mostly on the assumption that the final BT uses the current-LB scale; the Kaggle-scale row shows the upside.

## Files (all in this folder)
| file | contents |
|---|---|
| `live2.py` | extended read-only episode puller |
| `games.json`, `lb_now.json`, `lb/` | pulled games and the leaderboard snapshot |
| `ana.py` → `live_tables.md` | band, top-30 and anchored BT tables |
| `fit2.py` | floors and scale profile |
| `fit3.py` | day-offset fit |
| `fit4.py` | opponent-sub random-effects fit |
| `arch_live.py` | live results by archetype |
| `pairmc.py` → `mc_*.txt` | pair Monte Carlo |
