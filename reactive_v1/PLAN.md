# reactive_v1 — PLAN (written 30 Sep 2026 12:55 UTC; time box 6 h -> ~18:55 UTC)

Goal: a FULLY REACTIVE kaggriculture controller (no tape at any step) that plans purchases, plantings, herd, land, labour and
sales from the observation, with labour feasibility checked before every commitment. Nothing ships today; the deliverable is a
working v1 + a bench the user can iterate on daily (autotune-ready parameter dict).

## Order of work (kill points in brackets)
1. [13:30] DESIGN.md — the architecture as one piece (plan layer / economic model / labour model / task dispatcher / market).
2. [15:30] rx.py -> build/rv1/main.py (standalone, pure python, stdlib only, last callable = agent, params in one dict `P`).
   - engine facts encoded (checked against kaggriculture.py 1.32.7): water on planting day or weed, care banks +1 for the NEXT
     production night, first production gets the whole bank (cap 6/6/4), market after units in the same step (DROP + SELL same step),
     last market = step 718, PLANT atomic per crop, orders capped at 10, hires act from the next step.
3. [16:00] 2-3 local correctness games only (allowed): rv1 vs 'random'/self, 720 steps, no exceptions, step time.
4. [16:15] one RunPod CPU pod (self-destruct <= 4 h armed first, logged in final30/PODS.txt; key never printed).
   Bench = newexec/game.py (per-product ledgers, day stats) via runq.py: rv1 vs V183, v183ms, at12m, self-play; fresh seeds 18101+.
   Tape judge = tapejudge/tj_game.py on the 123 top-field tapes (baseline v183ms run on the same pod).
5. [16:15-18:30] iterate on the biggest ledger gap per round (small batches, paired on the same seeds), then a final batch.
6. [18:50] REPORT.md: milestones (a)-(d) with honest numbers, per-product ledgers, coverage/idle stats, exact next steps + commands.

## Milestones (for the user)
(a) 720 steps error-free and >= 90k coins in self-play; (b) own revenue >= v183ms's own revenue in its own games (same seeds, vs V183);
(c) >= 50% wins vs v183ms head-to-head; (d) >= v183ms on the top-field tapes (paired).

## Rules kept
No uploads. No laptop simulations beyond 2-3 correctness games. Pod(s) via API with in-pod self-destruct <= 4 h, logged in PODS.txt.
Work only in agents/reactive_v1/. Reactive to observations only (no opponent identity, no per-seed rules).
