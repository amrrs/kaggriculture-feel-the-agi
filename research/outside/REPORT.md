# Outside sweep: what other teams have shared (final30/outside)

Final report, 08:30 UTC 30 Sep. The agent was launched at 08:14 UTC, not 07:10, so there was no 07:50 checkpoint; this is the only report. No uploads, no simulations.
Artefacts in this folder:
- `k/`: 9 freshly pulled notebooks.
- `forum_all.txt`: the raw text of 40 of the 120 forum threads.
- `forum_topics/`: raw JSON for those threads.

The forum was read through Kaggle's internal API (`discussions.DiscussionsService/GetForumTopicById`, forumId 11548702). The 80 other threads got HTTP 429. The titles and vote counts of all 120 threads are known; see the list at the end.

## Blunt bottom line
1. **No top-10 team has published code or a write-up.** The forum is full of RL diaries and tooling threads. On strategy, the public record stops at the ~2945 tape lineage, and our v183 line already contains that lineage (grep finds the v9/4 circuit in agents/micro, beta, search2, race).
2. The one concrete public statement of the top-10 edge is from the author of the strongest public bot: *"We lead until day 10... and lose it all after day 11."* The biggest hole is **tomatoes**: top farms buy about 9 tomato seeds from day ~12, hold about 10 tomato tiles on day 20, and sell about 71 tomatoes at ~$114. Tape bots sell about 7. Tomato overlays on a tape lost (0/85, 0/56) because the crews are fully booked. His conclusion: *"a tomato program needs a different labour plan, not just a different crop choice."* (thomastschinkel/the-2945-farm..., section 6, pulled.)
3. Replay forensics support this. The top agents are **adaptive from turn 1, not tapes**. Divergence over steps 0-72: THIRD FARM CLUB 0.004 (a tape), **Majkel1337 0.424**. The first step at which 25% of winning games diverge: **Majkel1337 step 4, SpaTaro 2, M&M&P&Q 1**. *"M & M & P & Q, the shortest script here, has the highest average winning score in the sample."* (leoprovorov/a-song-of-ice-and-fire-fixed-flexible, 29 Sep, pulled; built from 461 winning games of Majkel1337.)
4. The engine has not changed since 15 Aug (1.32.7 is current). There is **no late rule change or open exploit** to use.

## Final-ranking rules confirmed by Kaggle staff on the forum (these change the endgame plan)
- **Topic 742571**: the final Bradley-Terry fit *"will run over all episodes ever played between submissions that are still active"*. Episodes played now count, but only games against opponents who are still active at the end.
- **Topic 739410**: *"The team score is based on the better of its two submissions... The second slot can be viewed as a hedge with no downside. Ties are counted as half wins for each side."* The post-deadline play rate is not committed.
- **Topic 739874**: the two agents run in parallel, so the 1200 s runTimeout is safe. Overage is 60 s per episode and actTimeout is 1 s.

## (b) Public code stronger than 2700
| Agent | Where | Evidence |
|---|---|---|
| **The 2945 Farm v9/4** (Thomas Tschinkel) | kaggle.com/code/thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots, pulled to `k/` | live **2944.7** (sub 56269928), predecessor 2956.6; 519-21 vs the 10 top public notebooks; **0-36 vs 7 top-10 teams (15-17 Sep)**. Already in our lineage. |
| Demand-Preserving Turn Sale Timing (tetsutani) | pulled | best public score 2750.2; loses 55-5 to v9/4 |
| Harvest Ledger V93 (haodou092, 30 Sep 07:02) | pulled | only local results; this is the same demand-preserving lineage |
| Master Engine V4 "TOP 2", Kaggriculture 2900+, Multi-Route | pulled | the titles are not backed by ratings; these are replay clones or route libraries at or below V48 |
| GitHub | Ashee-Softworks, Amritesh/kaggiculture, Applied-Agent-Works, diffmap/kaggicultureRL, debmalyaroy (Rust simulator) | nothing claims above about 2700. Amritesh claims *"~168 milk a season at roughly 315/unit into a market no other agent supplies"* and was 64-16 vs its own older version. |

## (a) Mechanics and strategies ranked by how likely they are to be something we lack
1. **Tomato programme from day ~12, with the crew planned around it** (2945 Farm section 6; see above). This is the only directly measured gap to the top 10: about 71 tomatoes at $114 vs about 7. It needs a labour re-plan: a tomato is ongoing with 4 yields at ages 8-11 and needs watering every day.
2. **Adaptive from step 1** (Ice and Fire). The top 3 react to board, shops and market from the first turns. Tape-plus-reflex bots cap at about 2945, and the same author's 2945 bot went 0-36 against them.
3. **The shop RNG can be causally changed by your own farm actions** (leoprovorov/god-s-mode-hacked-stores, 29 Sep). Claim: *"A legal one-cell DIG immediately before an unlock changed the next shop in 98 of 128 paired interventions (76.6%)"*. Directed control reaches only about 10-18% of matches and its score impact is *"not measured"*. Forum 739388 and 739084 hint at the same thing (weed spawns leak the seed). **Not buildable today.**
4. **Order-slot priority** (ORDERPRI2): lists settle in lockstep, one unit per slot, so put the product most exposed to a rival batch first. **Race** premium sales using the exact identity `rival_sold = inv' - inv + town_draw - own_sold`. PREDICT uses 451k recorded rival sales. All of this is in v9/4 already.
5. **Care economics**: a cared cow gives 3 milk, a sheep 4 wool and a goose 2 eggs per production. An animal unfed on its production day loses its whole bank. The stored cap is 6/6/4, so harvest before it overflows (CAPHARV, +20/-0). In v9/4.
6. **Sheep placed on day 11 get a 5th production** (days 17, 20, 23, 26, 29). Skip CARE on day 28 and feed and care on day 29 (VE1, VT1). In v9/4.
7. **Hire cost is fib(n-1)**, so hires 12 and 13 cost $377 a day. Use one hand, not two, on non-wool days (SL2, +15/-0).
8. **Opening**: the tape's turn-0 wheat round trip had $6 of slack and collapsed against opponents dumping wheat. Use **BUY 20 / SELL 15** (+107/-0).
9. **Leaderboard dynamics** (forum 740437, 737955): at about 2400, 25 of 26 opponents replayed known public tapes. Elo converges to *"the average of the crowd replaying tapes"*. A fixed policy is cloned within 24 h; *"Only truly adaptive policies stand a chance."*
10. **Evaluation traps**: Kaggle runs the **last callable** in main.py. The notebook image ships engine 1.29.3. Identical code scored 2686 and 2579 in two notebooks, so a single submission's rating noise is about ±100.
11. **Minor quirks** (forum 741907, READMEs):
    - The farmer respawns at (4,4) each day, which costs about 15 percentage points of walking.
    - Two units issuing PLANT with 1 seed plants nothing.
    - FEED needs wheat in the unit's inventory.
    - Melon max_yield_day is 12 in the code (the README says 10).
    - Land order is fixed NE, SW, SE at $1k, $2k, $4k.
    - The #1 team does plant SE in some games (forum 742449, with screenshots).

## (c) Engine history (Kaggle/kaggle-environments)
- Engine commits since late July: #1381 moving onto locked tiles (3 Aug), **#1386 shed capacity enforced on market BUY (4 Aug)**, #1392 shed actions from locked shed-access tiles (6 Aug), #1394 town rebalance (7 Aug), #1397 interactive drift (12 Aug), #1399 underused resources made situational (15 Aug). **Nothing since.**
- **Open PR #1418 (29 Sep, docs only)** lists places where the engine differs from its docs:
  - Mid-day **PLACE into a full shed moves min(n, room) and keeps the rest** in the unit's inventory. Only DROP and the midnight drop destroy items.
  - HARVEST before the first yield day is a no-op.
  - **FERTILIZE counts its own day** (day, day+1, day+2).
  - BUY_PRODUCT is priced at `market_price(inv-1)`, so a buy/sell round trip nets zero.
  - Orders beyond 10 are dropped.
  - Price shapes include log10 and hinge.

  None is an exploit. They matter only if our executor models them differently.


## Forum additions (read after the first draft)
- **743384 "Question for M & M & P & Q and Boey"** (25 Sep, no replies): *"Around a week ago, you guys were at the top, and then both of you guys dropped dramatically low... M & M & P & Q obtain a negative score."* This points to top teams **parking their best agents** to avoid being cloned. Their true strength may be hidden until they resubmit near the deadline. Expect the top of the live board to shift in the final hours.
- **736219 (Ryo Hasegawa, previously #1)**:
  - Rating is Elo-like and counts W/L only.
  - K starts at about 200 and decays; a commenter measured a flat ~220 for 10 games, a cliff to ~50 by game 20, and a floor of ~8.5 by game 80.
  - A new submission starts at 600, plays a burst of ~15 games/hour, and is ~90% converged after ~60 games (about 5 h).
  - Residual noise is ±25-50 points; byte-identical copies ended 300-1400 apart (topic 734000).
  - He says the final BT uses only post-deadline episodes. **Staff in 742571 contradict him: all episodes between still-active submissions count.**
- **742856 (Avineesh Arora)**:
  - The local 1.32.7 engine reproduces ladder games to the coin (71,345 / 72,013 on both).
  - `competitions.EpisodeService/GetEpisode` returns the seed, so any ladder game can be replayed exactly.
  - Against 2250+ opponents the **median gap was $177; 40% of games were decided by under $100 and 78% by under $1,000**. Win rate beats margin: agent B, with $1,967 less margin but +6 pp win rate, was the better ship.
  - A candidate that was 82-84% vs the 2250+ band **stalled near 1,800** because it won only 56.5% below 2000. **An agent must survive the climb from 600.**
  - Strong public agents form non-transitive cycles.
- **743231 (Yujin Cha)**:
  - The seed matters far more than the seat, so treat the seed as the unit of evidence.
  - Results are non-transitive (the v7 shop-router beats hybrid2965 12/12 but loses 0/12 to V53).
  - hybrid2965 plays a **different opening depending on the opponent's turn-0 market orders**.
  - In a mirror of tape forks, the game is decided by sale timing on days 17-25 (wool swung from 226 to 1).
  - Splitting the endgame `SELL x 1000` into slices lost about $1k.
- **739273 (sobameshi)**:
  - A round-robin of 14 public implementations on 96 seeds found *no intransitive triple*; the newer one beat the older in 86 of 91 pairs.
  - Cloning a recent strong public tape is enough for about the top 10%.
  - A commenter: 3 of 4 v40 losses came from 2 cows dying on day 1 (a tape missed a FEED), costing $12-32K per cow.
- **741743 (Snorlax)**: reached rank ~55 (silver) *mainly with RL*. No details.
- **743993**: a top-50 commenter believes the leaders combine IL+RL models with deterministic guard rules and search at key moments. The observation shows the opponent's farm (tiles, animals, money, units); only their shed is hidden.
- **739179 (destbreso, 3 Sep) "Why are the strongest agents being retired"**:
  - The #1 at the time was *"the most adaptive agent I have measured... first divergence at t=0, all three channels moving, and a 40-0 ledger with a median margin of +13,065. Rating 2,977 after 77 episodes"*. It was then withdrawn by its team.
  - The next #1 was *"a near-fixed route with small repairs"*, with a fork at t=72-144.
  - Commenter: *"Kagglers learned not to leave on LB their strongest agents."*

  **This confirms that top teams hide their best agents.**
- **738619 (Mark Schatza, PPO to 80k)**:
  - A commenter who says he is *"current at 8 TH place and not using rl"* is *"trying a strategy that ml a model to sell things on correct timing"*. So a learned **sale-timing** model is used by a top-10 team.
  - Hybrid design reported to work: *"a 5 turn look ahead where the policy chose the intent for each plot of land (e.g. wheat and a boolean for boost and harvest)"*, with an executor doing the micro-actions and the policy doing purchases and sales.
- **743716 (dzjiann, RL on 196 cores)**: RL beat public scripts about 90% of the time but plateaued around the top 100. It was *weaker against strong players than his earlier "mathematical reasoning and dynamic programming" agents*.
- **740847 and 737736 (low tier; for completeness)**:
  - The README's "town demand escalates 2x after day 10, 4x after day 20" *does not exist in the shipped engine (1.32.6+)*; consumption is flat.
  - Fertilizer only decays in price, so sell it at once.
  - Premium goods peak on about days 9-14, and a melon on day 25 is worth about 1/5 of one on day 12.
  - Wheat, carrot and egg *appreciate* late (wheat 25 to 45 by d21).
  - Any `__file__` reference crashes silently on Kaggle's evaluator.

## What this means for the last 15 hours (outside view)
1. Nothing public beats the 2945 tape family, and we already contain it. **There is no public drop-in above our line.**
2. The only documented edge of the top 3 is second-half adaptivity: a tomato programme and crew planning from day 11. It cannot be built and validated safely by 23:59 without simulations. The honest lever left is **final-pair selection**:
   - Best-of-two counts and ties are half wins.
   - All episodes against still-active opponents count.
   - Keep the submission that already has many games against opponents who will stay active.
   - Use the second slot as a no-downside hedge that is **robust on the climb from 600** (it must win below 2000, not only at 2700).
3. Top teams (M&M&P&Q, Boey) appear to have parked their strongest agents, so the live board understates them. Do not calibrate "10th ~2930" off the live board alone.

## Forum threads fetched (titles of all 120 known; content of 40)
Highest-voted threads with no content (429): 736219 (Ryo Hasegawa, "1st Place(previously) - Submission Strategy", 91 votes), 741743 (Snorlax, RL to silver), 739273 (sobameshi, replay-measurement pipeline), 738079 (BC), 734000 (path dependence of rating), 738619 (PPO to 80k), 743716 (RL on 196 cores), **743384 ("Question for M & M & P & Q and Boey", -17 votes)**, 742856 ("What actually predicted the ladder, and 15 things that didn't"), 743231 ("Six things I wish I'd known before trusting my local win rates"). Rerun `get.sh <id>` in the scratchpad once the 429 clears if these are wanted.
