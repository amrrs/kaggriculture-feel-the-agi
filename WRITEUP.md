# Kaggriculture — team "feel the agi": approach, what we learned, what failed

Final submissions: **g012m** (56707760) and **g010c04** (56718703). Both are the same agent with two different tuned parameter vectors.

## The agent in one paragraph

A single-file Python agent (standard library + numpy, ~0.4 s worst step). Days 0–10 follow a **shop-keyed library of recorded openings** built from public replays of strong agents (branching on the shops unlocked at days 3 and 6, with an "evening rescue" that repairs the plan when cash or tiles drift). From day 11 a **reactive executor** takes over: it re-plans the farm every morning from the observation only (visible shops, market inventory and prices, the rival's tiles and recovered sales, own cash/shed), allocates tiles and herd by a per-product market model, sizes the daily hire count against the routed value of the work, and routes 10–13 workers with a small prize-collecting VRP local search (the "micro" layer). Market orders sell on arrival at the shed, never hold, keep the shed under the 100-item cap, and put the product most exposed to a rival lot in slot 1 of the order list (orders are processed in lockstep, slot by slot). The final parameter vectors were found by **CMA-ES over 25 behavioural knobs**, scored against 123 recorded games of the current top-12 teams plus fresh-seed games against our own previous bots, and validated on untouched seeds and held-out tapes.

## Results (offline, paired, untouched seeds)

| g012m vs | margin / game | win rate |
|---|---|---|
| previous best (v183ms) | +0.94k (480 games) | 71% |
| 123 top-12 recorded games | +0.66k | 68 wins vs 64 |
| our lx3 line (live 2714 on 27 Sep) | +4.5k | 97% |

Live the line converged around 2650–2700; the top 10 sat at 2840+.

## What we learned about the game

- **Own income is not the score.** Our farms and the top-3 farms earn the same (~105–115k coins). Games are decided by the shared market: the top teams take ~10k more from us than from each other (tomatoes we did not grow, premium goods sold before ours). Only wins count for rating.
- **Selling is denial, holding is a gift.** Every change that held stock, kept reserves, or hired less raised our revenue a little and the rival's a lot. Drip-selling, price-threshold holds, dawn delivery loops: all negative.
- **The shop draw is action-dependent.** The end-of-day RNG consumes one draw per empty tile (farm 0 then farm 1) before choosing a shop; one dig can change the next shop. Directed control needs the hidden 31-bit seed, which is not inferable in time. Credit to leoprovorov's public analysis.
- **The top 3 play one integrated controller from step 1** (herd keyed on the first three shops, land on fixed days, tomatoes from day 8 in every world, 12 hands/day, no wheat churn, premium goods sold 1–2 units after each shop tick). Grafting any piece of it onto a tape+executor agent lost every time.

## What failed (each measured, most on 48–500 paired games)

Fourth quadrant (−4k), tomato wave on our executor (−6k), top-3 opening tree on our executor (−8 to −14k), from-scratch reactive controller after one day (−30k), transformer imitation of top replays (multi-step consistency 4%), macro PPO self-play (~rank 55), rival-sale forecasting/racing, drip metering (−4.5k), leader-layout copying, CEM over macro programmes, higher micro search budgets (converged), single-knob sweeps (46 of 77 knobs never change an action).

## Tools worth reusing

Exact engine re-pricing ledgers from replays; a top-field tape judge (recorded top agents vs a candidate, paired); a fresh-seed bench with per-step timing; the CMA-ES harness; the "playbook" extraction of a team's policy from its replays; a shop-pinned bench that cuts paired noise ~8x.

## Credits

Opening library derived from public replays (recorded actions of top agents); early lineage from yhay81's *Three-Day Shop Router* (Apache-2.0); executor base by Codex (same team); order-book slot mechanic from thomastschinkel's *The 2945 Farm*; RNG analysis from leoprovorov. Built with Claude (Fable 5.1) and Codex as coding agents. Apache-2.0.
