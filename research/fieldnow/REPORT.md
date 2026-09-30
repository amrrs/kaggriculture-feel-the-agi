# final30/fieldnow — coin-by-coin picture of the current top field vs our builds (live replays only)

FINAL (29 Sep ~22:30 UTC; checkpoint 1 was folded into this). Read-only: Kaggle API episode lists + `kaggle competitions replay`.
No simulations, no engine stepping, no code changes to any agent, no uploads. Every number is pure JSON accounting over live replays.

## Sample
- Current top-15 active subs found by BFS from our 9 subs (`field_subs_now.json`; every top-12 team's two newest subs are from 28-29 Sep).
  The field listed in agents/topfield/field_subs.json is fully stale: none of those 26 Sep subs is among the current active ones.
- 117 COMPLETED public replays: top-1..5 8 games each, top-6..12 4 each (latest games vs opponents rated >= 2700, mixed seats, <= 2 per opponent team)
  -> **123 top-12 farm records** (top-vs-top games count twice); **V183 28 farms** (56641767: all 19 losses + all 5 wins vs >= 2700; 56686499: 4 newest),
  **v183ms 13** (56686494; it has NO public game vs >= 2600 yet, its 3 losses are vs 2520-2596), **lx3 8** (vs >= 2700). 62 other farms (opponents).
- Caveat: V183's games vs >= 2700 are from 28 Sep, i.e. against the opponents' previous subs; v183ms's games are vs weaker opponents.

## Answers (numbers first; se over our farms)

### (a) The three largest coin differences, TOP1-5 vs our V183 / v183ms, similar shop draws
Shop-matched = each of our farms against the mean of its 3 nearest TOP1-5 farms by shop-demand vector (units the town consumes of each product
over the game given the recorded shop draws and their unlock days; z-scored). Net line = revenue minus that product's own inputs.

| rank | line | TOP1-5 - V183+v183ms (se), n 41 | same, our games vs >= 2700 only (n 33) | TOP1-3 - ours | same-world check (our 49 games, opponent - us) |
|---|---|---|---|---|---|
| 1 | **tomato net** | **+4.5k (0.9)** | +5.6k | +6.2k | opponents sell 69 tomato units per game vs our 8 (d20-29); we have 0-2 tomato tiles to d20 |
| 2 | **strawberry net** | **+4.8k (1.7)** | +2.0k | +4.2k | realised price 118 vs 135 on equal units (248 vs 241): **+4.1k/game (se 0.6)**; vs >= 2700 **+4.9k (0.8)**; 90% of it is *day-mix* (`decomp.md`) |
| 3 | **wheat net** (rev - buys - seed) | **+2.3k (0.5)** | +2.8k | +3.8k | we churn 930-1120 wheat units through the market (buy 32-38k, sell 41-48k), they buy ~139 |
| (4) | wool net | +0.4k (1.4) | +0.5k | +0.0k | same-world price gap +2.0k (0.5); vs >= 2700 **+3.0k (0.5)**, day-mix +2.5k |
| offsets | land / hires | -2.8k (0.2) / -1.5k (0.2) | -2.8k / -1.4k | -4.0k / -2.4k | TOP1-3 buy SE on d10 h9-12 in 37/37 farms; 11.1 units/day vs our 10.3 |
| our edges | milk / egg | -2.0k (1.4) / -1.4k (0.6) | -1.6k / -1.6k | | we sell eggs first in 47/49 games (d6 vs opp d11.9) |
| | **FINAL coins** | **+4.4k (2.6)** | +4.3k | +4.1k | |

Robustness by build (TOP1-5 matched): strawberry +2.8k (V183), +9.2k (v183ms), -0.4k (lx3) -> the cross-world strawberry gap is not stable; the
same-world price gap is (+5.6k V183, +2.2k v183ms, +1.5k lx3). Tomato is stable (+4.4..+6.1k) and wheat (+1.2..+3.2k). Against TOP6-12 the
final gap is only +1.2..+2.5k and the lines are tomato +1.5..+3.3k, wool +0.5..+2.8k, wheat -0.1..+2.3k, strawberry -1.2..+5.3k.

### (b) Built before day 11 or after (`timing.md`: cumulative matched gap to end of day D)
| line | D=5 | D=10 | D=13 | D=16 | D=20 | D=25 | D=29 | built |
|---|---|---|---|---|---|---|---|---|
| strawberry net | -0.3 | +0.1 | +0.3 | **+4.3** | +3.9 | +2.7 | +4.8 | decision in the opening (d2-4 plantings), cash d13-16 and d26-29 |
| tomato net | 0.0 | -0.3 | -0.5 | -0.6 | +0.9 | +3.4 | +4.5 | TOP1-3: planted from d8-10 (opening); TOP4-12: from d14-17 (after); cash d17-29 |
| wheat net | +0.7 | +0.6 | +0.4 | +1.5 | +2.0 | +2.8 | +2.3 | after d11, steady |
| land | 0 | -2.8 | -2.8 | -2.8 | -2.8 | -2.8 | -2.8 | d10 (SE quadrant, 4000) |
| coins | +0.4 | -4.2 | -4.1 | +2.1 | +1.1 | +2.4 | +4.4 | |

Strawberry opening detail (`straw.md` H-K, `opening.md` L):
- First strawberry PLANT day: **118/123 top-12 farms on d<=2 (112 exactly d2)**, 54/62 other opponents on d<=2; **V183/v183ms/lx3 0/49 on d2**
  (d3 28, d4 21). Tiles by d5: 7.1 (top) vs 4.0 (ours); equal again by d8 (20.5 vs 18-22; we plant more on d6-9).
- The d2 basket is where V183 differs: field d2 = 1 cow + 1.6-1.9 strawberry seeds; V183 d2 = 1.9 geese + 1 melon seed. (t0 also differs:
  field 2 cows + 3 sheep + 12 wheat + 6 melons; V183 3 cows + 2 sheep + 13 wheat + 7 melons.) The field reaches our goose count by d10 (7.2 vs 7.1);
  our egg lead is exactly that timing (-1.2k at d10, -1.9k at d16, -1.4k final).
- Their early tiles sell in the d13-16 window: vs >= 2700 opponents, harvest d12-15 opp 25.7 units vs ours 10.9; sales d14-16 36 u @206 vs our 15 u @202.
- Natural experiment inside our own games: when V183/v183ms/lx3 start strawberries on **d4 (n 21)** the same-world strawberry price gap is
  **+5.2k (se 0.9)** vs **+3.2k (se 0.8)** when they start on **d3 (n 28)**; opp - us units sold d12-16 +28 vs +19. Across games,
  opp - us strawberry revenue in d12-16 = 2.6k + 0.54k x (opp - us strawberry tiles at d5).
- The rest of the day-mix is the one-day sale lag that final30/race already measured: on the big harvest days (d16/18/20/22) the opponent
  sells 61-100% of the wave the same day, we sell 24-56% and the rest next morning (e.g. d16: opp harvest 29.6 / sold 23.4, us 31.8 / 7.7, d17 us 28.3).
  race's counterfactual prices that at +1.7-2.4k margin before labour, mostly through the opponent's price.

### (c) Our losses to >= 2700 (`losses.md` M-O; 28 losses: 25 vs >= 2700, 3 v183ms vs 2520-2596)
- The margin flips late: **median flip day 19** (last day our coin gap is >= 0; 5, 11, 14x4, 15x3, 16x2, 18x3, 20x2, 21x2, 22, 24, 25, 26x2, 27x3, 28, 29).
  Typical curve: we lead +2..+8k at d10-15 (cash held while they pay for SE and tomatoes), level near d20, lose d20-29.
- After the flip (opponent - us, net, mean per loss): **tomato +4.7k**, strawberry +3.0k, wool +1.4k, carrot +1.4k, milk +1.3k, wheat +1.1k; eggs -1.3k.
  Whole game: tomato +6.5k, strawberry +4.0k, wool +2.7k, wheat +2.6k, milk +1.3k; eggs -3.7k; they spend 2.0k more on land.
- **It is the opponent's revenue rising, not ours falling.** After the flip our revenue equals that of our 3 shop-nearest own games (mean -0.2k,
  median -0.9k, below in 15/28); the opponent's is **+9.9k above** its 3 shop-nearest TOP1-12 farms (median +9.1k, above in 20/28).
  Their tomato lot sells into a market where we supply none; their early strawberries sell before ours.
- The 4-quadrant marker: opponent had 4 quadrants in 14 of our 29 losses vs 2 of 20 wins; **we won 2 of 16 games against a 4-quadrant opponent.**

### (d) Anything nobody in agents/*/REPORT.md has tried?
Blunt answer: **nothing that is both new and small enough for today.** Every difference above maps to a CLOSED item: tomato fill (famcal, Track A,
t1-t5, M2/M3), 4th quadrant (beta b0-b7), calendar openings (famcal, Codex V107-V112), strawberry hold / sell timing / dawn selling, cull.
Two things I could not find tested in that exact form:
1. **The d2 basket swap: V183 minus its 2 d2 geese, plus 2-3 strawberries on d2-4 (+1 cow d2).** It is the one opening line where V183 differs
   from 118/123 top-12 farms. final30/race (c) priced only the *timing* (same units 24 steps earlier: -62/+188 margin) and noted the gap is volume;
   this audit shows what funds the volume (600 coins of d2 geese) and that our own d4-start games lose +2.0k more same-world strawberry value
   than d3-start games. famcal tested more early geese (geese2 -12.2k) and a whole strawberry-heavy calendar (searly3 -11.6k), not this swap.
   Expected size from the data: strawberry day-mix +3-4k minus egg timing 1.4-1.9k, i.e. ~+1.5-2.5k gross, before any shared-price reaction.
   It changes the recorded d0-10 tape tree, so it is inside the CLOSED "calendar openings" class. Flag only; needs a paired fresh-seed test.
2. The **bundle** run by the only three teams above 2910 (MMPQ, DSM, DECEM): SE quadrant on d10 + tomatoes from d8 + 11 units/day, in 37/37 farms.
   TOP4-12 run none of it. Each piece is CLOSED for us individually; nobody tested the bundle. Not a last-day item.

Other observations (no action implied): top farms release sheep gradually from d22 (TOP1-5 sheep 6.0 d20 -> 4.1 d26), ours hold to d27;
nobody fertilises melons (window-water fertilised 0-7% everywhere); fertilised share of strawberry / tomato production events is 95% / 86% (top)
vs 89-97% / 85-87% (ours), so fertiliser is not a gap; nobody in the top-12 buys fertiliser (0-9 units) while we buy 97-136 and resell.

## Per-team profile (top-12 current active subs + our builds; mean per farm; u@p = units sold @ mean realised price, (revenue k))
| team (rating) | active subs | farms | W% | coins d10/d20/final k | herd C/S/G d5 | d10 | d15 | d20 | d25 | crops W/C/T/S/M d10 | d15 | d20 | d25 | quads | hires | straw u@p (k) | milk u@p (k) | wool u@p (k) | melon u@p (k) | tomato u@p (k) | egg k | wheat net k | fert collected/applied/bought |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M & M & P & Q (3025) | 56680759 56679033 | 11 | 100 | 3.1/62.2/110.8 | 5.5/3.3/0.0 | 9.0/5.0/8.1 | 9.5/5.5/8.2 | 9.0/5.3/8.2 | 8.3/3.7/8.2 | 27/1/7/27/6 | 25/2/12/33/3 | 24/7/16/27/0 | 33/15/9/10/0 | 4.0 | 304 | 250@146 (36.5) | 224@104 (23.3) | 119@125 (14.9) | 75@202 (15.1) | 140@61 (8.6) | 11.1 | +12.0 | 505/253/0 |
| DSM (2936) | 56675988 56681605 | 15 | 47 | 2.3/63.5/113.1 | 5.4/3.8/0.0 | 7.7/7.5/5.9 | 8.1/8.0/6.0 | 7.9/7.2/5.9 | 7.2/5.3/5.5 | 28/0/5/25/6 | 25/3/11/34/4 | 24/7/16/27/0 | 29/21/8/14/0 | 4.0 | 303 | 248@143 (35.5) | 203@110 (22.3) | 171@133 (22.8) | 71@198 (14.0) | 130@65 (8.5) | 8.3 | +11.7 | 480/246/1 |
| DECEM (2914) | 56679168 56654377 | 11 | 55 | 3.4/60.2/105.3 | 4.6/3.6/0.0 | 8.1/5.6/7.8 | 8.3/6.5/7.8 | 8.2/5.6/7.8 | 7.8/4.4/7.8 | 29/0/11/22/5 | 25/4/15/29/2 | 31/3/15/23/0 | 42/12/6/9/0 | 4.0 | 303 | 212@134 (28.3) | 197@106 (20.9) | 137@130 (17.7) | 68@204 (13.9) | 146@65 (9.5) | 11.4 | +15.4 | 493/250/0 |
| Vadim Vasilenko (2912) | 56667936 56678397 | 11 | 82 | 7.7/65.0/111.9 | 5.7/3.3/0.0 | 7.5/5.2/6.9 | 7.7/6.3/6.9 | 7.2/6.3/6.8 | 6.6/3.9/6.5 | 25/0/1/24/6 | 18/1/4/32/4 | 19/4/11/24/0 | 28/16/7/7/0 | 3.2 | 285 | 232@153 (35.5) | 188@103 (19.4) | 139@137 (19.1) | 71@203 (14.5) | 78@78 (6.1) | 10.8 | +10.6 | 466/217/0 |
| Victor @ Tufa Labs (2889) | 56682386 56680736 | 11 | 82 | 6.5/61.3/106.9 | 5.9/3.0/0.0 | 8.4/4.2/7.8 | 8.5/4.9/7.8 | 7.7/5.2/7.8 | 6.9/3.2/7.7 | 26/0/1/24/6 | 18/3/4/34/3 | 21/3/11/27/0 | 27/17/8/10/0 | 3.4 | 289 | 253@134 (34.0) | 198@99 (19.6) | 105@137 (14.4) | 74@200 (14.9) | 84@76 (6.4) | 12.0 | +10.3 | 469/222/0 |
| Unknown Mother-Goo (2873) | 56671443 56658433 | 12 | 50 | 8.9/66.6/109.9 | 5.4/3.8/0.0 | 8.3/6.6/5.5 | 8.2/7.1/5.5 | 8.1/6.9/5.5 | 6.8/5.5/5.4 | 28/0/0/20/6 | 17/2/5/27/4 | 17/5/14/20/0 | 29/12/9/6/0 | 3.1 | 284 | 193@139 (27.0) | 202@107 (21.6) | 160@156 (25.0) | 71@202 (14.4) | 101@65 (6.6) | 9.0 | +10.1 | 466/213/0 |
| Anton Tikhonov (2856) | 56639636 56650047 | 7 | 57 | 8.8/63.6/102.7 | 5.6/3.4/0.0 | 8.4/5.6/5.4 | 8.4/6.1/5.4 | 8.1/6.0/5.4 | 7.6/4.0/5.3 | 28/0/0/22/6 | 17/2/4/28/4 | 20/5/10/20/0 | 27/14/9/6/0 | 3.0 | 281 | 209@140 (29.3) | 207@97 (20.1) | 130@118 (15.3) | 72@202 (14.6) | 72@80 (5.8) | 8.7 | +11.6 | 454/217/0 |
| Yizhou (2853) | 56668630 56676365 | 7 | 14 | 8.8/57.8/94.8 | 4.6/3.4/0.0 | 5.9/5.3/8.0 | 5.9/5.6/8.1 | 5.6/5.6/8.1 | 4.9/4.7/8.1 | 27/2/0/19/6 | 18/7/2/25/4 | 21/7/12/16/0 | 25/14/12/4/0 | 3.0 | 280 | 169@130 (21.9) | 138@85 (11.6) | 135@141 (19.0) | 73@200 (14.5) | 80@59 (4.7) | 13.2 | +10.1 | 449/217/0 |
| Majkel1337 (2849) | 56663502 56663513 | 9 | 44 | 3.9/54.8/99.4 | 4.6/2.7/0.2 | 6.4/6.1/5.4 | 6.2/8.6/5.6 | 5.3/9.2/5.6 | 4.9/7.8/5.6 | 28/1/3/21/7 | 23/5/8/24/2 | 23/10/13/15/0 | 32/15/9/5/0 | 3.7 | 287 | 156@120 (18.8) | 142@83 (11.8) | 194@153 (29.6) | 80@195 (15.6) | 120@64 (7.7) | 9.5 | +11.4 | 444/221/9 |
| tetsuya & yuanzhe  (2849) | 56672335 56652886 | 11 | 45 | 8.8/64.1/104.0 | 5.5/3.3/0.0 | 7.3/6.1/7.0 | 7.2/7.2/7.0 | 6.7/7.2/6.8 | 6.5/5.5/6.8 | 28/1/0/19/6 | 17/4/0/28/4 | 23/6/4/20/0 | 28/14/4/8/0 | 3.0 | 283 | 204@132 (26.9) | 176@95 (16.8) | 165@138 (22.8) | 71@203 (14.5) | 30@83 (2.5) | 10.9 | +10.6 | 478/222/0 |
| monsaraida (2832) | 56682174 56672002 | 7 | 43 | 8.0/68.2/115.5 | 5.9/3.0/0.0 | 8.7/4.4/6.3 | 8.9/4.7/6.3 | 8.9/4.6/6.3 | 8.3/3.9/6.1 | 26/0/0/24/5 | 18/0/0/33/4 | 23/1/7/25/0 | 33/8/7/8/0 | 3.0 | 283 | 250@133 (33.3) | 234@124 (29.0) | 107@164 (17.5) | 69@206 (14.1) | 48@103 (4.9) | 10.0 | +12.2 | 462/218/0 |
| Zenith (2831) | 56673678 56662753 | 11 | 45 | 8.1/63.2/113.0 | 5.7/3.0/0.0 | 7.5/3.5/8.2 | 7.7/3.8/8.2 | 7.4/3.8/8.1 | 6.8/2.6/8.1 | 24/0/0/26/6 | 14/3/0/35/4 | 17/5/8/26/0 | 28/11/8/10/0 | 3.0 | 281 | 268@161 (43.1) | 184@111 (20.5) | 78@111 (8.7) | 69@205 (14.2) | 53@95 (5.0) | 12.9 | +10.3 | 453/218/0 |
| V183 | 56641767 56686499 | 28 | 25 | 8.9/60.8/108.0 | 5.5/2.5/2.3 | 7.8/3.4/7.1 | 8.0/5.3/7.1 | 8.1/5.5/7.1 | 8.1/5.5/7.1 | 22/0/0/25/4 | 18/2/0/34/1 | 20/2/1/31/0 | 30/11/1/9/0 | 3.0 | 278 | 267@134 (35.8) | 208@108 (22.5) | 119@120 (14.3) | 66@209 (13.8) | 9@248 (2.3) | 12.2 | +8.8 | 422/191/105 |
| v183ms | 56686494 | 13 | 77 | 9.2/60.8/98.9 | 4.5/2.8/2.6 | 7.2/3.5/7.1 | 7.7/5.8/7.2 | 7.7/5.9/7.2 | 7.7/5.9/7.2 | 24/1/0/23/4 | 22/2/0/28/1 | 22/5/2/24/0 | 30/14/2/6/0 | 3.0 | 279 | 211@98 (20.7) | 199@105 (20.9) | 130@135 (17.5) | 66@206 (13.7) | 11@224 (2.6) | 13.0 | +10.1 | 427/202/136 |
| lx3 | 56584428 | 8 | 38 | 8.9/60.9/105.7 | 4.6/3.0/2.6 | 6.5/5.6/6.9 | 7.2/5.9/6.9 | 7.2/6.6/6.9 | 7.2/6.8/6.9 | 22/1/0/22/4 | 21/2/0/31/1 | 20/6/0/27/0 | 30/10/0/10/0 | 3.0 | 283 | 243@138 (33.5) | 211@109 (23.1) | 161@104 (16.7) | 68@198 (13.4) | 0@0 (0.0) | 11.9 | +7.8 | 435/195/97 |

More tables: `profile.md` (A coins/costs/fertiliser, B herd and crops d5-d25, C revenue and units by product, D strawberry timing and fertiliser
shares, E actions per day by type), `ledger.md` (F full coin ledger, G net lines), `straw.md` (H plant-day distribution, I our 49 games strawberry
race per game, J premium units/price by day window, K who sells first), `opening.md` (L purchases per day d0-11), `losses.md` (M per-loss flip
table, N whole-game gaps, O cumulative gaps), `shopkey.md` (P shop-keying slopes, Q/R strawberry and wool by world), `pricegap.md` (S),
`decomp.md` (T), `timing.md` (U), `quad.json` (per-quadrant tiles; SE use of 4-quadrant farms: 13 wheat at d11, 7 strawberries by d15).

## Method
- `crawl.py`: BFS from our 9 subs over `competition_list_episodes` (agents carry submissionId / teamId) -> `crawl_cache.json`,
  `field_subs_now.json`, `rating.json` (LB 29 Sep 22:05 UTC in `lb/`). Active subs = the two with the latest episode per team.
- `select.py` -> `selection.json`; `dl.sh` -> `replays/` (117 files, 2.8 GB; can be deleted, `games/` holds everything derived).
- `parse.py`, per replay: for every step rebuild each player's pre-market shed (recorded pre-step shed + that step's DROP / PICKUP / PLACE of each
  unit, using the recorded unit inventories and positions), then run the engine's per-unit lockstep market (`_process_market` semantics, the
  engine's own `market_price`, HIRE/BUY_LAND first, opponent's same-index order interleaved unit by unit). Order quantities are never counted
  (SELL x 100000 = sell-all). Checks: simulated post-market money == recorded money on every step in 111/117 replays (1-2 steps off in 6); shed after
  the market == recorded shed on every non-end-of-day step in 100/117 (1-2 steps off in 17); final coins reproduced 117/117; ledger identity
  (3000 + revenue - costs = final) within 2 coins for 228/234 farms. Per day it also records tiles by crop / animal / empty coop-pasture / weed /
  empty, quadrants, units per day, hires and hire cost, effective FERTILIZE by crop (+ redundant), WATER, HARVEST units by product, FEED,
  COLLECT_FERTILIZER, actions by type, seeds / animals / wheat / fertiliser bought, units sold and revenue per product, end-of-day shed, first
  strawberry / tomato / melon plant day, first strawberry harvest and sale day, fertilised share of ongoing-crop production events, fertilised
  share of window-crop waterings.
- Raw per-game JSON: `games/<episode>.json`; one record per farm with all per-day arrays: `farms.jsonl`; ledger per farm: `ledger.json`.
- Tables: `prof.py` (-> farms.jsonl), `table.py`, `teams.py`, `ledger.py`, `straw.py`, `opening.py`, `losses.py`, `shopkey.py`, `pricegap.py`,
  `decomp.py`, `timing.py`, `quad.py`.

## Not done / limits
- No counterfactuals: every "value" is a same-world price or matched-world ledger difference, not a what-if. The day-mix price gap in particular is
  an upper bound for what we could capture (selling earlier would lower the price for both farms; race's counterfactual gives own +0.2-0.3k).
- Shop matching is on the town-demand vector only; opponent strength differs between our sample (vs >= 2700 on 28 Sep, v183ms vs ~2500) and
  the top farms' (vs >= 2700 on 29 Sep).
- Only 6 of our 49 games are against a current top-12 team (V183 losses to tetsuya, monsaraida, Mother-Goose, Anton Tikhonov; lx3 loss to DSM;
  V183 win vs Yizhou; all vs their pre-29 Sep subs),
  so direct same-world top-vs-us evidence is thin.
- Sell hours / intra-day order were not analysed beyond the within-day component (+0.3k strawberry, +0.35k wool); final30/race covers that.
