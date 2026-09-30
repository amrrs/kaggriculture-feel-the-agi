# final30 — last-day sprint (written 29 Sep 2026 ~22:15 UTC by the coordinator, Claude Fable)

Competition: Kaggle "kaggriculture" (turn-based farming, two farms, shared market). Submissions close 30 Sep 2026 23:59 UTC.
After the close, episodes continue for ~2 weeks and a Bradley-Terry fit over those games gives the FINAL leaderboard.
Only our latest 2 submissions count; team score = best of the two. Cash prize for the top 10. User's stated ambition: 3000.

## Where we are (facts, 29 Sep 22:00 UTC)
- Public LB: #1 M&M&P&Q 3021, #2 DSM 2944, #3 Vadim 2912, #4 DECEM 2910, #5 Victor 2889, ... #10 ~2841, #20 ~2776. 10,177 teams.
- Our team "feel the agi" (teamId 16805699), rank 88 at 2557 because both live bots are 2 hours old:
  - 56686499 = Codex V183 exact re-upload (archive research/codex/2026-09-05/v179-gate-loader/build/dated_gate/agent.tar.gz,
    main 80d3cfc8). Its original 56641767 converged at 2687 over 114 games: 2500-2700 band 32-18, 2700-2900 band 4-21.
  - 56686494 = v183ms = V183 + Claude micro-execution routing layer (agents/micro; main cba37327; 0.35 s step cap).
    Offline: 68.4% vs V183 on fresh seeds (n=288), +823/game on 141 top-tier tape games.
- Retired but re-uploadable (tarballs exist): lx3 56584428 (agents/lateexec/build/submission-lx3.tar.gz, live 2714, band 14-16,
  2500-2700 40-40), lx1 (submission-lx1.tar.gz), mrh 56661366 = lx1+micro (agents/micro/build/submission-mrh.tar.gz),
  hybrid 56655050, comb1, lx4, plus micro ports lx3m / v183m in agents/micro/build (never uploaded).
- Engine: kaggle_environments 1.32.7 in /Users/1littlecoder/kaggriculture/.venv (activate with `source .venv/bin/activate`).
- Live-episode tooling: experiments/live.py <sub ids...> (read-only Kaggle API; prints W/L by opponent rating band and losses).
  Replay JSON: steps[t][player]['observation'] has farms[i].tiles (10x10; None / 'LOCKED' / dict with kind PLANT|COOP|PASTURE|WEED),
  money, unlocked_quadrants, hands; market.prices / market.inventory; town.unlocked_shops; steps[t][player]['action'].
  Download: `kaggle competitions replay <EPISODE_ID> -p <dir>`; episodes of a sub: `kaggle competitions episodes <SUB_ID> -v`.
- Memory of what was tried (READ before proposing anything; all in research/claude/2900/agents/*/REPORT.md|RESULTS.txt):
  micro/DESIGN.txt+RESULTS.txt (the one lever that worked, +0.8..2.3k/game), wild/ledger (gap decomposition from day-11 positions:
  ~70% of the leaders' 11.2k edge = supply volume lowering the OPPONENT's premium prices), rebuild/RESULTS.txt (leader layout mimic
  with micro executor: no gain), beta/RESULTS.txt (live-loss ledger of V183: premium prices -9.4k, tomato -6.9k, 4th quadrant -7.5k;
  4th-quadrant builds b0-b7 refuted), topfield/REPORT.md (26 Sep matchup matrix + archetype table of the top 30), final29/DECISION_RULE.md.
  CLOSED (do not retry blindly): macro plan search, CEM, layout copy, opponent sell forecasting/timing, strawberry hold, tomato/carrot
  fill, animal-coverage mandates (a1), 4th quadrant, wheat/fert keep, cull, hand caps, premium loops, DL/BC imitation, hybrid switch,
  lean herd, calendar openings (famcal, Codex V107-V112), undercut, dawn selling, premium sell-after-shop-tick oracle (+0.2k).

## Binding rules
1. NO Kaggle competition submissions. Only the coordinator uploads, only with the user's explicit go.
2. No game simulations on this laptop (it overheated earlier). Light JSON parsing / scoring is fine. Simulations run on RunPod
   (key in ~/runpod.env; create cpu pods via the GraphQL API; EVERY pod must carry an in-pod self-destruct <= 4 h, see
   agents/micro/run_batch.sh and the pods scripts under /private/tmp/claude-501/-Users-1littlecoder-kaggriculture/*/scratchpad/runpod/
   for the pattern; record every pod id/ip in agents/final30/PODS.txt) or in Kaggle kernels (<= 2 per agent; see agents/fable/kaggle/).
   Never print the RunPod key. Stopping a CPU pod deletes it.
3. Everything must be reactive to in-game observations only (no opponent identity, no per-seed rules). Judge on fresh seeds, both seats,
   paired, with worst-case tails, plus peak step time (< 0.6 s; actTimeout is 1 s on ~1.6 vCPU).
4. Work only inside your own directory agents/final30/<agent>/. Report in REPORT.md there: numbers first, se and n, what was NOT done.
   Update REPORT.md at each checkpoint so the coordinator can read partial progress. Time boxes are kill points, not targets.
5. Deadline for anything that could be uploaded: results in the coordinator's hands by 30 Sep 14:00 UTC (validation queue has taken
   up to 4.5 h; upload cut-off 18:00 UTC). Pair decision at 30 Sep 16:00 UTC.
