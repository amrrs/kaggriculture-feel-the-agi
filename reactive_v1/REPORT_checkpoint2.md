# reactive_v1 — REPORT (checkpoint 2, 14:40 UTC 30 Sep; updated at each milestone)

## Checkpoint 2 (14:40 UTC): build rv1b (sha256 67efc715...), fresh seeds 18401-18412 both seats, PINNED shop sequence (see harness), n=24 per row
| row | win% | margin (se) | own | opp | worst | peak step |
|---|---|---|---|---|---|---|
| rv1b vs V183 | 0.0 | -31596 (1618) | 84.4k | 116.0k | -44.9k | 0.19 s |
| rv1b vs v183ms (H2H) | 0.0 | -33045 (1572) | 83.6k | 116.6k | -43.6k | 0.19 s |
| rv1b vs at12m | 0.0 | -34437 (1562) | 84.2k | 118.6k | -45.6k | 0.20 s |
| rv1b self-play | 50 (mirror) | 0 | **97.5k** | 97.5k | | 0.16 s |
| ref v183ms vs V183 (same seeds) | 70.8 | +1028 (344) | 107.1k | 106.1k | -3.1k | 0.38 s |
| tape judge (123 tapes) | 20% wins | -24802 (3117) all / -36438 intact-only | 89.5k | 114.3k | | 0.18 s |
Paired vs v183ms (vs V183, same seed/seat): margin -32.6k (se 1.6k), own -22.7k (se 1.9k), 0/24 better. Tape judge paired vs v183ms
-44.0k (se 4.6k), both-intact -34.8k (se 2.0k), 11/123 better. 0 controller errors.
Milestones now: (a) MET (720 steps, 0 errors, 97.5k self-play). (b) NO (own -22.7k vs v183ms). (c) NO (0/24). (d) NO (-44k).
Progress since rv1a (+16k margin vs V183) came from the pinned-shop screening rounds (see "Rounds" below).

## Checkpoint 1: build rv1a = rx.py @ 14:45, sha256 b5067ab3...; fresh seeds 18101-18112 both seats, n=24 per row; pod env.run, actTimeout 1 s)
| row | win% | margin (se) | own coins | opp coins | worst | peak step |
|---|---|---|---|---|---|---|
| rv1a vs V183 | 0.0 | -47756 (2294) | 69.0k | 116.8k | -69.8k | 0.17 s |
| rv1a vs v183ms | 0.0 | -49667 (2119) | 69.4k | 119.0k | -73.5k | 0.19 s |
| rv1a vs at12m | 0.0 | -50104 (2037) | 68.6k | 118.7k | -73.5k | 0.19 s |
| rv1a self-play | 45.8 (mirror) | 0 | 74.2k | 74.2k | | 0.16 s |
| reference: v183ms vs V183 (same seeds) | 75.0 | +961 (242) | 103.8k | 102.8k | -0.6k | 0.36 s |
| top-field tape judge (123 tapes) | 15% wins | -37316 (2809) all / -49148 intact | 83.6k | 120.9k | | 0.31 s |
Paired vs v183ms (same seed/seat vs V183): margin -48.7k (se 2.4k), own -34.8k (se 4.1k), 0/24 better. Tape judge paired vs v183ms:
-56.5k (se 4.0k), both-intact -49.8k (se 1.9k), 8/123 better. 0 controller errors in 219 games, 720 steps each.

Milestones: (a) 720 steps error-free YES; >= 90k self-play NO (74k). (b) own revenue >= v183ms's own NO (-34.8k).
(c) >= 50% vs v183ms NO (0%). (d) >= v183ms on tapes NO (-56.5k).
