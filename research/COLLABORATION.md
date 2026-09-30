# Kaggriculture shared work agreement

## Current Codex user steering — 28 September 2026

The user again requires generalization and says the solution cannot hardcode
things. Fixed day/count interventions in Codex V147/V148 are private diagnostic
treatments only, not deployment policies. Any proposed candidate must choose
from observed game state and demonstrate improvement on unseen seeds, shop
sequences and opponent sources; no episode-, seed-, team- or fixture-specific
rules. A flip of an exposed recorded loss does not qualify for submission.

The user re-emphasizes that weaker opponents are already handled reasonably;
the competitive target is the 2700–2900 band, where our reported live win rate
is about35% versus competitors'80%+. Keep that cohort separate in every decision.
Do not use overall wins or a public notebook's title as proof of closing this gap.
The current V144 field set has39 strict-band cases and one2912-rated case, which
must be reported separately. Replay win rates remain an optimistic diagnostic,
not a measurement of live strength.

Latest follow-up: the user is going to sleep, delegates decisions to Codex, and
says to submit even if Codex only remotely believes the candidate can reach 3000.
This relaxes the confidence threshold below to a plausible, evidence-grounded
shot at 3000; it does not remove the **one competition submission maximum**.
Continue private experiments without waiting for answers. Record the uncertainty
and slot-retirement decision; do not claim a rating that has not been observed.

The user's latest instruction is to cancel every pre-existing Kaggle workload
and reclaim its resources. Codex stopped search-scr1 and churn-ch2; Kaggle
acknowledged both cancellations. search-fid1 had already completed. The pending
Claude fx1 launcher (PID 61253 and its sleep child 61926) was terminated before
it launched the notebook. Preserve completed results and sources; do not restart
these old jobs. New Codex validation remains authorized.

Latest clarification in the current task: private Kaggle benchmark notebooks are
explicitly authorized to continue. The user also conditionally authorizes **one
competition submission at most**, only if Codex judges the evidence to support
breaching 3000. No current V144/V145 result qualifies. This supersedes the older
blanket no-submission wording for this task only; it is not permission to upload
an unproven candidate. Before using this one opportunity, verify current active
entries, exact frozen artifact, diverse fresh validation, generalization and
runtime evidence, and record which entry would retire. Submission count used by
this Codex task: **1 of 1**. Submitted 56641767 on 28 September at13:13UTC,
exact frozen V179/V183 dated_gate archive SHA256
`afa68661de1a04757504c64d7b10cfa1d46de3997aaccc0c3976d5a80cde11d7`.
The CLI confirmed success and history confirmed the new ID; validation initially
PENDING. This replaces lx4 (56613772) in the latest pair and retainscomb1
(56618739). **Do not submit again under this authorization.**
Kaggle validation passed: COMPLETE at13:18UTC, validation episode114709445
finished with90178 coins for each copy; default initialrating600. No opponent
matches at that snapshot. The3000/top-five goal is unverified; observe live
status and target-band episodes.

The user prioritizes generalization and a final top-five result, and explicitly
permits building on the strongest existing lx4/comb1 agent including its opening
when asked about the older borrowed-opening prohibition. This supersedes that
prohibition for the current Codex task. Competition rules still apply. Preserve
the Kaggle-only simulation constraint recorded on 27 September. V144 research
is isolated under research/codex/2026-09-05/v144-relative-work/. No competition
submission has been made by this research experiment. Private compute uploads
do not count as competition submissions.

## Current intent

Target: strengthen local performance toward the approximately 2718.9 silver
score target. Live leaderboard results remain unproven. The user requested a
broad review of public Kaggle solutions, local hill climbing, and shared learning
with Claude. **This research round does not submit agents.**

## Ownership and coordination

- Codex writes new work under `research/codex/2026-09-05/`.
- Claude may use its own directory and link its results below.
- Neither agent should overwrite the other's candidates or edit root `main.py`
  during parallel research. Root `main.py` is not a reliable experiment baseline;
  benchmark immutable snapshots identified by SHA-256.
- Keep raw trial results. Append findings with agent name, source, candidate hash,
  engine version, opponents, seed split, wins/ties/losses, and limitations.
- Public notebook rankings and claimed scores are discovery hints, not evidence
  that the downloaded code is stronger in today's environment.
- Shared comparisons should use identical engine/configuration, both seats, and
  per-player isolated state. Do not use public holdout results to tune repeatedly.
- Compare against current candidates from **both agents** once their paths are
  known. Never infer that a candidate beats Claude's work without testing it.

## Submission lessons and handoff

Codex previously submitted v4 (56020371) and v5 (56020483), retiring the established
v3 (55952112) without first establishing their live strength. A new bot's rating
starts at 600; the early rating drop is not conclusive evidence of weaker play.
Nevertheless, local wins over a narrow opponent pool were insufficient evidence
for the submission-slot decision. Do not represent a local win rate as a live
rank or a promised medal.

No further upload is part of the current research run. A future submission
decision must explicitly account for which existing active bot would be retired,
its live evidence, the candidate's untouched validation, and opponent diversity.

## Existing evidence

- `experiments/baseline.py`: original v3 heuristic, preserved unchanged.
- `experiments/round2/v4.py`: submitted v4 snapshot.
- `experiments/round2/market_candidate.py`: v5 development source; enable
  `PROJECT_DROPS=True`, leave `SALE_SORT` disabled.
- `experiments/final_validation.json`: v4 held-out results (144 games).
- `experiments/round2/validation.json`: v5 held-out results (144 games).
- `experiments/round2/REPORT.md`: four public pipeline benchmarks and caveats.
- `research/codex/2026-09-05/`: broad catalog, source audit, new experiments.

## Claude handoff

Claude's candidate and result paths are not yet known to Codex. Add paths and
hashes here or in a separate Claude handoff file; do not replace this document's
existing evidence. Codex has asked the user for the location.

## Claude location supplied by user

Read `claudefindings.md` (Claude-owned). Codex replies in `codexfindings.md` and
`research/codex/2026-09-05/`. Claude benchmark harness is `experiments/bench.py`.
Its pool label `v4` points at mutable root `main.py`; after the earlier Codex v5
upload that label does not guarantee v4 bytes. Reconcile by SHA, not file label.

## Completed Codex local round

Final evidence: `research/codex/2026-09-05/REPORT.md`; compact cross-agent notes:
`codexfindings.md`. Frozen experimental source: `research/codex/2026-09-05/frozen-candidate.py`
(SHA 73fab8ceaa9be3d5ff13e599000e0d443ec1eb592a4e0485362d33e2aa4e6816).
It won 31/32 against v5 and 86/96 against the remaining validation pool versus
v5's 78/96. The donor diagnostic did not improve win rate. Retained for local
comparison; no promotion to root main.py and no submission in this round.

## Live rating update supplied by user — 5 September 2026

The user reports v5 submission **56020483** at **1406.4**, up **247.2**
from the last API snapshot of 1159.2. This update is user-observed, not a new
API verification. It supersedes that older snapshot as the latest reported
rating; it does not change the recorded local validation results. Preserve v5
while gathering stronger evidence for any future submission-slot decision.

## Version naming clarification

Use “Codex submitted v5” (56020483), “Claude experimental v5” (source/hash
not yet identified), and “Codex frozen local candidate” (73fab8ceaa9b).
See codexfindings.md for the user-relayed Claude bugs and evaluation checks.
The predicted ~2500 rating is not an observed result.

## Latest user-observed live rating — 5 September 2026

Codex submitted v5 (56020483) has reached **1650**, per the user. This is
**+243.6** since the previous user observation of 1406.4. It is the latest
reported rating, not a fresh API verification or a settled-rating estimate.
Historical observations remain above for provenance. Local candidate results
and the proposed v6 design are unchanged.

## Target clarified by user

The user wants **3000**, replacing the earlier silver-score target as the
research ambition. Codex is running isolated production experiments in
`research/codex/2026-09-05/v6-production/`. Submitted v5 stays intact.
Claude c6 was snapshotted for comparison without editing its active file.

## V6 production round completed

The conditional livestock branch failed the fresh holdout and is rejected.
See `research/codex/2026-09-05/v6-production/REPORT.md`. Shared learning:
score production choices by their relative effect on both players' cash,
not solely our farm's revenue. Codex submitted v5 is preserved, with a latest
API snapshot of 1858.5. The research ambition remains 3000.

## User-observed submitted-v5 rating update

The user reports the previous Kaggle submission at **1968**, following the
1858.5 API snapshot. In this conversation that refers to Codex submitted v5
(56020483); this new value is user-observed, not freshly API-verified. The
increase is 109.5. No experimental candidate has been uploaded.

## Market diagnostic completed

On selected seed 13372107, both seats, restoring baseline wool inventory
reduced the production candidate's loss from 2,105 to 250 coins. Restoring
wool and egg inventories yielded +160. These artificial interventions support
the relative-revenue mechanism for this matchup; they are not promotion games.
See `research/codex/2026-09-05/v6-production/causal-check/REPORT.md` and
codexfindings.md. The production candidate remains rejected; submitted v5 is intact.

## Milestone staging: 2800 first, then 3000

User proposes 2800 as the next milestone after submitted v5 passed 2000.
Latest read-only CLI snapshot this turn: v5 (56020483) 2074.6; v4 (56020371)
1574.4. Kaggle overview/FAQ and staff topic 739410 were checked in-browser:
latest two submissions are active; better submission supplies the team score.
With this ordering one new submission displaces v4 and preserves v5, but check
again immediately before uploading because either collaborator could submit.

Prepared the unchanged frozen timing source (73fab8ceaa9b) in
research/codex/2026-09-05/stage-2800/submission-timing.tar.gz. No upload made.
Additional 144 games on 12 fresh seeds, both seats: timing and v5 each 55/72,
with every paired outcome identical. Boatlee 24/24 each; two-shop 8/24 each;
Claude c7 default snapshot (day-11 handover, pinned c6 dependency) 23/24 each.
Boatlee's small margin regression persists. Two-shop is the clearest remaining
local weakness. Do not portray these results as 2800-level validation.
Earlier timing wins (31/32 vs v5; 86/96 vs other original holdout opponents,
v5 78/96) remain valid but do not establish a rating jump.

Archive attribution retained and exact source hash checked; two complete
native-file-loader games on extracted main.py matched the benchmark in both
seats. Root main.py and Claude's active files untouched. Recommendation is
an incremental live experiment with this package, not a claimed 2800 bot.
For the larger gain, diagnose the two-shop losses and fix a measured cause,
accounting for opponent revenue before altering production. Report, hashes,
source snapshots and all raw results: stage-2800/REPORT.md and manifest.json.

## User submission constraint — 14 September 2026

The user explicitly prohibits submission until we have the best next candidate
with a substantial improvement and strong evidence of generalization, targeting
the top of the leaderboard (approximately 3200, user-reported). This supersedes
the earlier recommendation for an incremental live experiment. Continue local
research only; V39 failed its promotion gate and is not eligible for submission.
Evaluate frozen candidates on untouched seeds, both seats and diverse opponents;
report uncertainty and material regressions. Local validation cannot guarantee a
3200 live rating. This constraint does not itself authorize a future upload.

## User clarification — 15 September 2026

The user rejects retaining the opening tape in the next candidate. New candidate
work must make decisions from observations starting at step zero, without a
recorded opening action stream or tape fallback. Taped incumbents remain useful
only as benchmark opponents/controls. This supersedes the V51 late-controller
research direction. No submission is authorized.

## Latest user steering — independently authored fixed opening

The user subsequently explicitly proposed our own fixed early-game sequence,
with less upfront melon/wheat spending, a lean hiring calendar and SW expansion
on day 9. This permits independently designed and compiled schedules; it does
not permit borrowing Claude's or another competitor's recorded opening.
Retain useful market, purchase-recovery and herd-selection logic after checking
its compatibility with the new schedule. This supersedes the broader earlier
interpretation that every early action must be chosen adaptively. No submission
is authorized. Current implementation and evidence: Codex V73 directory.

## Claude circ12 round — 17 September 2026

Claude's newest candidate is circ_v12 (`research/claude/2900/agents/circ12/`,
REPORT.md; built main.py SHA-256
e4d2c9f0f8df83ff0dd6a5e3ee348243097bc78270e2ae8663229b6b12203b89, engine
1.32.7). It is circ_v11 with four executor knob changes; paired on 84 recorded
circ_v11 games against 2900+ opponents it gains +0.6-0.7k/game (6 of 60 losses
flip), mirrors and donor opponents are neutral-to-slightly-positive. Claude
rates this a small, consistent gain, not the substantial improvement the
upload gate asks for. No submission was made; the upload decision is the user's.

18 Sep addendum (`research/claude/2900/agents/cashopen/REPORT.md`): the
"opening built for early cash" idea was checked and closed. Our prefix's day 0
already matches the top tier's (12 melons, 2 cows, 2 sheep, all $3000 spent;
same $150-2k cash through day 10). An observation-driven day 9-10 phase that
buys the SW quadrant two days earlier nets −1.1k (loss set) / −2.3k (win set)
paired against circ_v12: own coins +0.3-0.6k at best, the recorded opponents
gain +1.5-1.9k through shared milk/wool/melon prices. circ_v12 remains the
candidate; nothing was uploaded.

- 18 Sep 19:28 UTC (Claude, on the user's instruction): circ_v12 uploaded as submission 56338865 (main.py SHA-256 e4d2c9f0…), retiring circ_v9. Top-5 study (agents/cashopen 'Top-5 profile', agents/famtape) found no executor-level route; see claudefindings.md.
- 21 Sep 09:56 UTC (Claude, on the user's instruction after the team fell to rank 38 / 2888): circ_v13 uploaded as submission 56425190 (`research/claude/2900/agents/circ12/build_circ_v13/`, main.py SHA-256 1ba789db0a24b22706cd6ad005e875f288287bfc718f2581d4e5c1eac85402fc), retiring circ_v11. v13 = v12 + TOM_FIRST_DAY 16 (tomato allocation to day 20), SQ_SPLIT 0.5, GOOSE_MAX 4. Nothing in v11/v12 had broken: the 2890-3010 band filled with new entries, many running our lineage's d0-d10 opening. Evidence in agents/circ12/REPORT.md "Round 3" (clone set 197 games +999/game paired, tier set 215 +112, holdout h2h +770 / +509). A melon-rush executor path (MELON_RUSH, default off) was a dead end: mirror farms make the melon race symmetric.

## Codex local round — 23 September 2026

V114 architecture review and V115 adaptive-opening service transfer followed the
round report. V115 source SHA `780983d4348f2d25990a9f84e93f686262d2ecca87b9d6eae6a5bc507026d56a`
combines V90's no-tape observation-driven opening with V102's late wool credit
and 22-animal cap. On exposed 24201–24208, both seats versus exact frozen
circ_v13, it won 0/16 and gained 740 mean paired cash margin over V90.
It is a diagnostic, not a promotion candidate. Raw rows and details are in
`research/codex/2026-09-05/v115-adaptive-service/`. No holdout or submission.

The later V116 dated-obligation audit found a V90 day-ten sheep purchase whose
required BUILD_PASTURE was trimmed from its route, leaving a paid $500 sheep
unplaced. Ten early FEED/CARE misses also cost five physical animal product
units on the saved exact opening prefix. V117–V123 tested financing twelve
day-zero melons with an independently authored opening. Physical delivery
succeeded on exposed worlds, but a predeclared fresh 8-seed, both-seat panel
versus frozen circ_v13 rejected V123: 0/16 wins and paired mean margin −2,852
versus V90. Source/evidence reports are in the respective version directories.
No protected holdout or submission was used.

V121 repaired the observed day-ten dropped-build dependency without changing
V90's first 240 actions; it buys and places two sheep instead of buying three
and placing two. Tiny exposed v13 screen on two seeds, both seats improved two
cash margins by 3,305/2,474 and left two identical; all four remained losses.
Keep it as a mechanical fix, not a promotion. See `v121-day10-certificate/`.

The V95 late-setting transfer improved the independently authored V92 opening
14/16 in a fresh direct comparison, but remained 0/8 and then 0/16 versus
frozen circ_v13. V96's mathematically corrected future-shop timing regressed
both V92 and V95 by over 6k mean margin on the exposed panel. A clean late-only
transfer to the stronger own V90 opening (V97) also regressed. V98 compiled a
day-nine SW cow pair for all ten authored herd programs, but its relative-value
gate rejected every preserved diagnostic observation; the accepting branch was
not engine-tested. Exact hashes, raw results, limits and reports are under
`research/codex/2026-09-05/v95-late-transfer/` through `v98-day9-cow-pair/`.
No candidate qualifies for submission; root and Claude sources are unchanged.

Read-only Kaggle CLI snapshot this turn: latest two active submissions v13
(56425190) 2804.3 and v12 (56338865) 2815.6; the fifth leaderboard row was
3046.1. These ratings can change. The September 30 final submission deadline
is listed in Kaggle's competition overview. No upload was made.

## Codex continued local round — 23 September 2026

All new work stays under `research/codex/2026-09-05/`, uses independently
authored opening routes, and preserves Claude, root `main.py`, immutable
controls and protected validation. No Kaggle upload occurred. The goal remains
active and unmet; neither a top-five rating nor a cash-prize outcome is
supported by these local results.

V95 earlier-herd moved two own V92 cows from day seven to day six; the route
executed all buys but missed six day-six melon waterings. Its controlled
seed-12049 margin regressed from V92 −4,902 to −7,306, though a later fresh
v13 screen found it materially stronger than V92 on average. V103 statically
restored all six waterings across ten programs, but delayed wool receipts
prevented the extra day-six cows from being bought, and both detailed audits
regressed. See `v95-earlier-herd/REPORT.md` and `v103-early-herd-melon/REPORT.md`.

V101 gave full opponent-wool credit to late sheep and overbought, displacing
carrots and lowering own wool prices. V102 capped greedy additions at a
22-animal service load. It improved relative margin on one common-shop audit
and in 24201–08 fresh native games versus v13, but only 2/16 wins in
24401–08 and 4/48 across three fresh panels; some cases and one parent win
regressed. The completed paired V95 comparison is 3/48 wins and −10,899
mean margin versus V102's 4/48 and −9,454, across 24 distinct seeds and
both seats; this is far short of qualification. V104's transfer of v13 late settings into V102 lost both parent
wins on its panel. V105's dynamic workload cap tied V102 in six v13 games and
has uncorrected missed CARE actions. Reports and raw results are in the
corresponding version directories. None qualifies for promotion.

V98's previously untested day-nine two-cow branch was exercised in two
three-milk-buyer states. Actual purchases, placements and service worked.
With revealed shops pinned equal to V92's path, relative margins improved
+2,488 and +6,570; native shop draws diverged and both fresh accepting
cases regressed. Across fresh 24401–08, V98 was −710 mean versus V92 and
V109 (V98 plus bounded late service) remained far below V102. The controlled
gains are mechanism evidence, not generalizable rating evidence. See
`v106-v13-gap/REPORT.md` and `v109-cowpair-service/REPORT.md`.

V107's own twelve-melon day-zero calendar compiled all ten programs and
harvested 72 melon units, but failed to fund its third sheep in time and
clipped later herd buys. V110 deferred two day-two strawberry seeds, bought
and placed that sheep in its audit, yet still lacked day-seven herd capital;
66 of 72 melon units sold on day eleven, after the herd purchase deadlines.
The native and controlled results diverged strongly, so this opening is not
promoted. See `v107-twelve-melon-opening/REPORT.md` and
`v110-financed-melons/REPORT.md`. V111's read-only two-sheep alternative
still misses day-seven cow/seed funding. V112 delivered all 72 melons by
day-ten hour 23 but retained the financing failure and displaced later crops;
its native margin regressed substantially. See V111/V112 reports.

For a consistent older control, V90 isolated_late11 was run against circ_v13
on the same 24 fresh seeds and both seats: 2/48 wins, −8,210 mean margin.
V102 had 4/48 wins and −9,454 mean margin; V95 earlier-herd 3/48 and
−10,899. V90 has better mean cash margin, V102 more wins. None qualifies for
promotion, a 3000+ estimate, or protected validation. The aggregate and
exact V90 rows are in `round-2026-09-23/REPORT.md`.

## Claude — 28 September 2026 23:45 UTC: lx1 re-uploaded (user-delegated)

The user (asleep) delegated the upload decision to Claude. Submitted `submission-lx1.tar.gz` (main.py SHA 8408db9d,
engine 1.32.7) as 56654841, retiring comb1 56618739. Active pair: Codex V183 56641767 + lx1 56654841.
Reason (live public games, 2700-2900 band by current opponent rating): lx1 7-2, lx3 24-30, lx4 10-19, comb1 6-14,
V183 7-23 (V183 is strong below 2700: 39-13 vs 2500-2700). Our replay judges ranked lx4/comb1/V183 above lx3, the
reverse of live; treat non-reactive replay judges as unreliable for supply/price-protection changes.
Claude's ledger (research/claude/2900/agents/wild/ledger): from V169 day-11 positions, ~70% of the leaders' 11.2k/game
edge is supply volume lowering shared prices for the opponent; layout copy wins 4/20 — macro/allocation action banks
(V201) are unlikely to close it. Next upload would retire V183 and is gated by
research/claude/2900/agents/final29/DECISION_RULE.md (must clearly beat both lx1 and V183).

## Claude — 29 September 2026 00:20 UTC: user request to Codex
The user asked that ALL Codex Kaggle sessions be stopped and that Kaggle compute be left to Claude for the final build.
Please do not launch new Kaggle kernels or submissions. (Claude cannot cancel kernels via the API; the user will stop the
running V205/V208 training sessions from the Kaggle UI.) Active pair: lx1 56654841 + hybrid 56655050; no further
upload without the user's explicit approval.

## Claude — 29 September 2026 03:30 UTC: mrh uploaded (user-approved), retiring lx1
mrh 56661366 = lx1 + micro-execution routing layer (research/claude/2900/agents/micro, main.py SHA 8934fbae). Active pair:
hybrid 56655050 + mrh 56661366. Micro routing adds +0.8..2.3k/game on every base tested (lx1, lx3, V183, hybrid).

## Claude — 29 Sep 2026 20:03 UTC: V183 restored + v183ms (user-approved)
Live autopsy showed the hybrid's lx3 mode lost (0-8 vs >=2700); V183 style is the stronger live base. Uploaded v183ms
56686494 (V183 + Claude micro routing, main cba37327) and Codex's exact V183 archive 56686499 (afa68661). These replace the
hybrid and mrh. Apologies for retiring V183 on 28 Sep — it was the better build.

## opencode — 30 Sep 2026 ~10:50 UTC: final-build sprint verdict (third agent, user-delegated)

User instruction: build the most powerful new agent toward 3000, learning from both agents' failures. Full report:
research/opencode/2026-09-30/REPORT.md. All 2,055+ validation games on RunPod pod kc3dgbjihpdlqh (L40S 32 vCPU,
self-destruct armed, now DELETED; logged in final30/PODS.txt); engine 1.32.7; laptop used for builds/scoring only.

- New builds ox1 (v183ms + MS_SLOT + rd8b dawn loop, sha 4903b85e...) and ox2 (+ MS_SLOT_TAPE, sha 423c6f9c...):
  the strongest fresh-seed profiles of the day (ox1 H2H vs v183ms +994 (226) 72.9%; vs V183 paired +990 (276);
  no lx1 regression) but REFUTED by the 123 top-12 tape judge: ox1 -814 (93), ox2 -849 (92) vs v183ms. The dawn
  loop's value was a lineage-only effect; against the top-12 books it costs ~-850/game.
- Delivered the missing verdict on the coordinator's mx1 (mall + rd8b, sha a4d3305a...): best fresh H2H of the
  day (+1525 (236) 75.0% vs v183ms; vs V183 paired +1379 (303)) but tape judge -1078 (110), 17/106 better —
  REFUTED. MS_RACE + dawn loop both lose vs the top field; MS_OVERFLOW/MS_CAPHARV capture nothing on v183ms.
- The maximal build that survives every judge is mslot = v183ms + MS_SLOT (main.py sha 808670930fa21312...,
  package research/claude/2900/agents/final30/microstructure/build/submission-mslot.tar.gz archive sha
  809cae1c..., independently re-loader-tested on my pod: callable agent, peak 0.129 s, ACTIVE/ACTIVE; verified
  copy in research/opencode/2026-09-30/handover/). On fresh never-used seeds 19001-19048 (both seats, n=96/row):
  vs v183ms H2H 77.1% +483 (114), paired +368 (121) 68/96; vs V183 75.0% +844 (248), paired +117 (151);
  vs lx1 99.0% (+159); vs hybrid 90.6% (+363 (84)); vs r9 100.0% (+193 (102)); vs farm2945 100.0% (-5 (52));
  worst -8848, peak step 0.41-0.49 s, 0 steps >0.6 s, 0 errors. Tape judge paired vs v183ms across three
  independent pods: +43 (21), +54 (19), +42 (22). Pooled H2H over three batches ~+500/game.
- Recommendation (upload decision is the coordinator's/user's): the one upload worth making is
  submission-mslot.tar.gz, retiring the older slot v183ms 56686494; final pair V183re 56686499 + mslot — a
  strict superset of the live build, positive-or-neutral on every judge, no regression anywhere. It does NOT
  meet the strict "+1k vs top field" bar (nothing measured today does); honest 3000 odds remain low — the
  top-5 gap (~4-6k/game, opening-borne tomato/strawberry day-mix, wheat, SE land) has no validated route left
  inside the deadline. No submission was made by this agent. The coordinator's autotune fleet (XC_P tuning on
  the mslot base) stacks on this, not instead of it.

## opencode — 30 Sep ~14:00 UTC: the innovative 2900 round (family-gated denial + model-status) — all refuted; mslot stands

Full report: research/opencode/2026-09-30/REPORT.md (round 2). User pushed for innovative/model-based routes to 2900.
- Learning status: the opponent-lot forecaster MLP (the one trained model that pays) is already embedded in the live
  executor's MPC sells; BC imitation (16% per-step error) and RL selectors are measured-closed; PPO infeasible
  (~1k env-steps/s). No trainable component with a positive measured bound remains un-deployed.
- ox3/ox3x = mslot + family-gated strawberry h0 denial (detector: rival strawberry tiles >= 6 over d4-d5; measured
  separation Boey max 6 vs family min 4/mean 6.27; override: sq_plan hour 0 for SQ_FAM_ITEMS): tape judge paired vs
  mslot **-944 (98)** / **-1778 (151)**; fresh = mslot exactly (gate never fires vs our lineage). REFUTED. Mechanism
  closed: v183ms already sells strawberries at next-morning h0; the family sells at h0 too; their +4.8k strawberry
  edge is planted-in-the-opening volume (race's own d5-tile data) — the closed route. Fifth sell-policy angle refuted.
- One implementation lesson recorded: injecting a partial S['ms'] dict at the handover crashes ms_observe (KeyError
  'prev') -> safe_agent PASSes silently -> own revenue 28k/game. Any future handover injection must carry the full
  {'stock','prev','rsold','stat'} structure (fixed in ox3 v2).
- Coordinator's autotune CMA-ES (5 generations, ~12k games, 25 knobs) independently confirms: the optimum is sharp at
  mslot; every multi-knob vector loses 0.4-3.2k/game. Combined with today's refutations (dawn loop, mx1/mall, h0
  denial), the entire reachable lever set is exhausted.
- FINAL: the strongest existing build is mslot (main 80867093, archive 809cae1c, twice loader-tested, +42..+54 vs
  top-12 across three pods, ~+500/game vs the lineage band, no regression anywhere). It does not reach 2900 — no
  measured lever does; the top-3's +4.4k/game is opening-borne and closed. Recommendation unchanged: the one upload
  worth making is submission-mslot.tar.gz (retires v183ms 56686494; pair = V183re 56686499 + mslot). No submission
  made by this agent; pod hjtt9abej7pejq deleted, all results synced.

## opencode — 30 Sep 12:11 UTC: mslot UPLOADED as 56706960 (user: "do it")

User gave the explicit go. Pre-flight re-verified immediately before upload (archive SHA 809cae1c, main 80867093,
latest actives unchanged: 56686499 newer + 56686494 older). Uploaded
research/opencode/2026-09-30/handover/submission-mslot.tar.gz as submission 56706960; validation COMPLETE at ~12:16 UTC,
initial rating 600 (fresh entries converge; the final leaderboard is the Bradley-Terry fit over post-deadline episodes,
so only the code matters). This retires v183ms 56686494 as planned. **Active pair: V183re 56686499 + mslot 56706960.**
4 submissions remain today. Full evidence: research/opencode/2026-09-30/REPORT.md.

## Claude — 30 Sep 2026 12:49 UTC: g012m uploaded (user-approved), retiring V183 56686499
56707760 = g012m: mslot (v183ms + MS_SLOT order-book slot flag) + 20 behavioural parameters set by a CMA-ES search (research/claude/2900/agents/final30/autotune,
267 vectors, objective = current top-12 recorded games + reactive holdouts). Holdout pooled (108 games/opp) paired vs v183ms: H2H +1.17k, vs V183 +1.33k,
vs lx3 +0.7k; 123 top-field tapes +675 (68 vs 64 wins), held-out 33 tapes +782; worst -4.4k; step p95 0.38 s. Active pair after validation: mslot 56706960
(uploaded by the opencode session 12:11 UTC) + g012m 56707760. Next upload retires mslot. A band-objective search (2850+ teams' tapes) is still running; a
fully reactive controller project has started in research/claude/2900/agents/reactive_v1/ (post-deadline work).

## opencode — 30 Sep ~17:05 UTC: C++ sim harness built + fresh 2800+ band scored (the user's "new sim in c++")

Full report: research/opencode/2026-09-30/REPORT.md round 3; harness in research/opencode/2026-09-30/cppsim/.
- The verified 788-line C++ engine port (sim.hpp, SHA f483219c) now has a complete evaluation harness: kaggle-format obs
  builder, action codec, tape runner with pinned shops, a Python-agent bridge (any main.py runs through the C++ sim
  unmodified). Parity: 5/5 replays EXACT; the full 123-game tape judge reproduced the Python engine to the coin
  (mean per-game diff 70 coins = mslot's own wall-clock noise). 123-tape judge now ~4 min on one pod (~4x faster);
  self-play 1.68M steps/s/core — the RL compute path is open (winner's setup ran 17K SPS).
- Fresh band: today's top-15 active subs crawled (M&M 3038 -> Anton 2807); 145 tape games scored through the C++ sim:
  mslot 50% all / 30% intact (-3.4k); g012m (autotune's 12:48 upload) 52% / 32% (-2.8k), +684 (z 5.6) paired vs mslot —
  the CMA gain is real; V183re (retired) 48% / 26% (-4.4k) — the retirement was correct. The live pair (g012m + mslot)
  is the right pair for the freeze; no action needed before 23:59.
- Per-team holes on today's band: M&M -7.9k, Mother-Goose -3.9k, 吃白饭的大肥鱼 -7.7k (the archetype gaps, consistent
  with all prior findings); we crush CDE/Anton/Yizhou (+38..65k).
- Pod orzvzuxdx329s0 (L40S 128 vCPU $1.09/h, self-destruct armed ~19:40 UTC) — in PODS.txt.

## Claude — 30 Sep 2026 21:04 UTC: g010c04 uploaded (user-approved), retiring mslot 56706960
56718703 = g010c04 (autotune's strongest reactive vector; tarball research/claude/2900/agents/final30/autotune/build/submission-at10c4.tar.gz, archive 811d15cf, main c4507819).
Final pair for the close: g012m 56707760 + g010c04 56718703 (both v183ms + MS_SLOT + CMA-ES parameter vectors). Kaggle-kernel head-to-heads today:
g012m beat lx3 31-1 (+4.5k) and lx3ms 29-3 (+3.3k); lx3ms beat lx3 25-7 (+0.9k); g012m knob transplants onto lx3ms did not transfer. lx line not re-uploaded.
