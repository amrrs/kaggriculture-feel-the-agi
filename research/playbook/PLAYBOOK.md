# PLAYBOOK — what M&M&P&Q / DSM / DECEM (and Vadim, Victor) actually do (v1, 30 Sep ~05:45 UTC)

Source: the 117 fieldnow live replays (29 Sep subs). Farms: MMPQ 11, DSM 15, DECEM 11 (= **T3**, n 37), Vadim 11, Victor 11 (= VV), V183 28.
Method: `extract.py` re-runs the engine's market lockstep on every step (same code path as fieldnow/parse.py, money reproduced there on 111/117 replays)
and records EXECUTED orders with revenue, EFFECTIVE unit actions with the tile they hit, shed/seed stocks, and end-of-day tile maps -> `ev/<ep>.json`.
Raw action tapes (incl. moves) of every target farm: `tapes_all.json` (key `<ep>_<p>`; fields tag, shops, shop_days, acts[0..718]).
Machine-readable: `playbook.json` (opening_hourly d0-d2 and d3-d10 per team, daily_mean per team d0-d29, ledger, sell summary, `rules`); `rules.json` = the rules block.
Supporting tables: `tab/hourly_<team>.txt` (d0-d2), `tab/hourly_d3_10_<team>.txt`, `tab/layout_<team>.txt` (modal 10x10 maps d0..d27),
`tab/daily.md`, `tab/daily2.md`, `tab/opening_days.md`, `tab/late.md`, `tab/money.md`, `tab/sell_hours.txt`, `tab/sell_threshold.txt`, `tab/misc.txt`.
Coordinates: x = column (east +), y = row (south +). NW x0-4 y0-4, NE x5-9 y0-4, SW x0-4 y5-9, SE x5-9 y5-9. Shed access (4,4),(5,4),(4,5),(5,5).
"hour h" = step 24d+h; the market (HIRE/BUY_LAND first per order index, then unit-by-unit lockstep) runs after unit actions; shop consumption runs after the market at h%4==0,
so **h%4==1 is the first market after each shop tick**.

## 0. The one-paragraph answer
All three run the SAME architecture (DSM and MMPQ are near-identical; DECEM is a variant): a fixed d0 calendar (DECEM 11/11 identical raw actions, DSM 15/15 to h21),
then a cash-driven greedy opener (animals/seeds/land bought the first hour cash allows), land NE d6 / SW d8-9 / **SE d10 paid by the d10 melon sale**,
herd and crop volumes **proportional to shop demand of the first 3 shops**, **tomatoes from d8 in every world**, 12 hires/day from d10 (8 at h0 + 4 at h1),
fertiliser from collection only, and **drip selling** of premium goods (1-2 units at each post-tick hour, holding the rest in the shed) instead of sell-on-harvest.
Nothing observed depends on opponent identity. Vadim/Victor share the opening and selling but mostly skip SE (5/22 farms) and plant few tomatoes (T18 ~11 vs 18).

## 1. OPENING d0-d10

### 1.1 Day 0 (fixed calendar; DSM 15/15, DECEM 11/11, MMPQ 11/11 to h8 then money-shifted by 1 h)
Executed orders / effective unit actions, DSM (the most common family; MMPQ differs only as noted):
| h | market (executed) | units |
|---|---|---|
| 0 | BUY_ANIMAL COW 1, BUY_ANIMAL SHEEP 1 x3 (three orders), BUY_PRODUCT WHEAT 5 (MMPQ: COW 1 + WHEAT 5 only; DECEM: COW 1 + SHEEP 1 + WHEAT 5) | - |
| 1 | HIRE x5 (MMPQ/DECEM x4), BUY_ANIMAL COW 1 (MMPQ also SHEEP 3; DECEM also SHEEP 1), SELL WHEAT 1 | - |
| 2 | SELL WHEAT 1 | BUILD_PASTURE (4,4) |
| 3 | SELL WHEAT 1, BUY WHEAT 1 | PLACE COW (4,4) |
| 4 | BUY WHEAT 1 (DECEM: BUY SHEEP 1) | BUILD_PASTURE (3,4) |
| 5 | BUY_SEED MELON 2, BUY WHEAT 1 | BUILD_PASTURE (4,3), PLACE SHEEP (3,4) |
| 6 | BUY_SEED MELON 2 | PLACE SHEEP (4,3) (MMPQ also BUILD_PASTURE (3,3)) |
| 7 | - | BUILD_PASTURE (4,2), BUILD_PASTURE (2,4) [MMPQ: (3,3) sheep], PLANT MELON (4,1) |
| 8 | BUY_SEED WHEAT 1 | PLACE COW (4,2), PLACE SHEEP (2,4) |
| 9-13 | MELON 2 at h10; WHEAT seeds 1,1,3,1 | MELON (2,3),(1,4),(3,3),(0,4),(3,2); WHEAT (4,0),(3,1),(2,2),(3,0),(2,1) |
| 14 | SELL WHEAT 2 | - |
| 15-20 | BUY_SEED WHEAT 1 per hour | WHEAT (1,1),(2,0),(0,2),(0,1),(1,0),(1,2),(0,0) |
| 21-23 | - | (water) |
End of d0: 2 cows + 3 sheep on 5 pastures along the shed corner (4,4),(3,4),(4,3),(4,2),(2,4) [MMPQ/DECEM: (3,3) instead of (2,4)],
6 melons, 12-13 wheat, cash ~5. Every new plant is WATERed by a hand in the same or next hour; each animal is FED and CAREd right after PLACE.
Full hourly tables with shares: `tab/hourly_{DSM,MMPQ,DECEM}.txt`, JSON `opening_hourly`. For an exact d0 copy, replay any DSM raw tape from `tapes_all.json` (15/15 identical raw actions incl. moves to h21).

### 1.2 Day 1-2 (money-driven, same order every farm)
- d1 h0 HIRE 2-4 (cash ~5-10). h2 SELL FERTILIZER 1 + BUY WHEAT 2-3; h6 FERT 1 + WHEAT 2; h8 FERT 2 + WHEAT 2; h9-10 BUY_SEED MELON 1+1 (MMPQ: MELON 2 at h10).
  Plant 1.6 melons (DSM at (1,3),(0,3); MMPQ (0,4),(0,2)). No other spend. Collect fertiliser from all 5 animals every morning (h0-h6) and sell it 1-2 per step (~100 coins each).
- d2 h0 HIRE 5-6 + SELL WHEAT 1; h2/h5 SELL FERT 1-2; **h6-8 BUY_ANIMAL COW 1** (3rd cow); **h12-14 BUY_SEED STRAWBERRY 1** (first strawberry, 112/123 top farms on d2);
  build a pasture for the cow at (3,1) DSM / (2,4) DECEM / (3,2)|(4,1) MMPQ; plant strawberry at (1,0)/(2,0), a 2nd one ~h18 if cash >= 100; replant harvested d0 wheat tiles with wheat.
- V183 difference: d2 = 1.9 geese + 1 melon seed; 0 strawberries until d3-4; 3 cows + 2 sheep on d0.

### 1.3 Day 3-10 per day (T3 mean per farm; per team in `tab/opening_days.md`)
| d | hires (h0) | buy C/S/G | seeds W/S/M/T | tiles W/S/M/T | herd C/S/G | quads | wheat bought | cash eod |
|---|---|---|---|---|---|---|---|---|
| 3 | 5.6 | 0.9/0.2/0 | 0.2/3.1/0.2/0 | 3.8/4.5/9.1/0 | 3.9/3.2/0 | 1 | 0.1 | 23 |
| 4 | 6.0 | 1.1/0.2/0 | 0.1/2.1/0/0 | 0.8/6.3/9.1/0 | 5.0/3.4/0 | 1 | 1.3 | 52 |
| 5 | 5.7 | 0.3/0.2/0 | 0.1/0.8/0/0 | 0.1/6.9/9.1/0 | 5.2/3.6/0 | 1 | 4.7 | 370 |
| 6 | 9.0 | 1.3/1.4/2.2 | 4.5/11.9/2.5/0 | 3.4/19.0/11.6/0 | 6.6/5.0/2.2 | 2 (NE) | 7.0 | 93 |
| 7 | 8.1 | 0.1/0.1/0.3 | 1.1/0.6/0/0 | 4.2/19.7/11.7/0 | 6.7/5.1/2.4 | 2 | 15.1 | 335 |
| 8 | 9.4 | 0.1/0.7/1.4 | 10.2/0.2/0.2/2.1 | 12.3/20.1/11.9/1.9 | 6.7/5.7/3.8 | 2.7 (SW) | 12.7 | 514 |
| 9 | 10.5 | 1.5/0.2/1.7 | 8.5/2.1/0/2.3 | 16.9/21.9/11.9/3.7 | 8.1/6.0/5.4 | 3 | 15.4 | 505 |
| 10 | 12.2 | 0.1/0.2/1.6 | 12.1/2.4/0/4.3 | 28.2/24.3/5.9/7.0 | 8.2/6.2/7.1 | 4 (SE) | 29.4 | 2852 |
Rules that reproduce it:
- **d3-d5 priority with the cash from fertiliser/wheat sales**: (1) the cow(s) (1 per day, h5-h8 or h14), each with a new pasture on the NW west/north edge
  ((4,0),(2,2),(1,2),(2,1) DSM); (2) strawberry seeds 1 at a time from h11-h19 whenever cash >= 100; wheat tiles harvested on d2-4 are replanted with STRAWBERRY
  (NW rows y0-2 become strawberries: 7 tiles by d5 vs V183 4). Sell wheat harvest in lots (d3 h0 SELL WHEAT 7). Keep ~0-50 coins eod.
- **d6 (NE unlock day)**: h0 HIRE 9. h3 SELL WOOL 6 (first wool of the d0 sheep) + BUY_LAND NE in the same market list at h3-h5 (first hour cash+proceeds >= 1000).
  Then in that hour and the next: BUY_SEED STRAWBERRY 8-9 in one list, cow/sheep 1, then geese 1 at a time (h7-h12), melon 2+2 (h8,h10). NE layout (DSM modal): strawberries
  on NE y0-1 x5-9, y2 x7-9, (9,3); melons (6,3),(7,3),(7,4),(8,4),(9,4); coop/pasture at (5,2),(6,2),(5,3),(5,4),(6,4) next to the shed (geese (5,2),(6,2), cows (5,3),(5,4), sheep (6,4)). d6 plant 12.1 S + 2.5 M + 3.3 W.
- **d7**: HIRE 8 (h0); buy wheat 5+5+3 early, fert sales, occasional goose/strawberry. Cash builds to ~300.
- **d8**: h1 SELL MILK 6 (first milk, d0 cows) -> **BUY_LAND SW at d8 h6** (else d9 h3-5); SW gets wheat (10.2 seeds) + **TOMATO from d8** (2.1 seeds; SW column x0-1, rows 7-9)
  + coops for geese at (2,5),(3,5),(4,6),(4,7) and 1-2 geese.
- **d9**: third shop draw is known: finish the herd to its keyed target (1.5 cows, 1.7 geese), 8.5 wheat, 2.3 tomato, 2.1 strawberry.
- **d10**: h0 HIRE 9 + h1 HIRE 3; harvest the d0 melons (6 per tile) and **SELL MELON + BUY_LAND SE in the same step, h9-h12 (37/37 T3 farms)**; SE gets wheat on row 5
  and x5 strawberries (x5,y6-9), later tomatoes/carrots (13 wheat at d11, 7 strawberries by d15). Melon tiles (NW x0-3,y2-4) are replanted with WHEAT (7/farm) and TOMATO (1.6).
  12.1 wheat + 4.3 tomato + 2.4 strawberry seeds. Cash eod 2.9k (V183 8.9k: it has no SE and no tomatoes).

### 1.4 Branching on shop draws (the keys) — fitted on the 37 T3 farms
`dX_k` = units per 4 h that the first k drawn shops demand of product X (single-product shop YARN_STORE/PET_CAFE counts 2, multi-product shops 1). Shops unlock d3, d6, d9, d12, ...
| decision (observed at) | rule (T3) | R2 / rmse | V183 |
|---|---|---|---|
| sheep at d10 | 3.0 + 3.7 x dW3 | 0.97 / 0.7 | 2.7 + 4.9 x dW2 (2 shops only) |
| cows at d10 | 3.9 + 3.3 x dM3 | 0.91 / 0.8 | 5.0 + 3.2 x dM2 |
| geese at d10 | 4.3 + 3.6 x dE3 | 0.69 / 1.7 | ~5.9 flat (bought d2) |
| strawberry tiles d6 | 12.5 + 6.9 x dS2 | 0.73 / 2.9 | 10.5 + 6.9 x dS2 |
| strawberry tiles d10 | 15.6 + 9.2 x dS2 | 0.76 / 3.6 | 10.7 + 10.5 x dS2 |
| tomato tiles d18 | 10.5 + 6.8 x dT5 (min ~7 with zero tomato shops) | 0.88 / 2.7 | ~0 |
| herd after d10 | frozen (C/S/G at d20 = d10 within 0.3) | | same |
- Fixed calendar (identical across worlds): the whole d0, first strawberry d2, land days (NE d6, SW d8-9, SE d10), tomato start d8-10, hire counts, melon d0/d6 only.
- Keyed: animal counts (on d3/d6/d9 shops), strawberry volume (d3/d6 shops), tomato volume (d3..d15 shops), SW purchase hour (cash).
- Market prices do not visibly change the opening beyond cash timing (not determined further).

## 2. LATE GAME d10-d29 (T3 mean per farm, end of day; full table `tab/late.md`)
| d | W | C | T | S | M | cow | sheep | goose | hires | water/plant | feed/animal |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 28.2 | 0.2 | 7.0 | 24.3 | 5.9 | 8.2 | 6.2 | 7.1 | 12.2 | 0.7 | 0.8 |
| 12 | 32.9 | 0.9 | 10.7 | 28.6 | 3.0 | 8.6 | 6.5 | 7.2 | 11.7 | 0.8 | 0.8 |
| 14 | 28.6 | 3.0 | 11.2 | 30.8 | 2.8 | 8.6 | 6.5 | 7.2 | 11.7 | 0.8 | 0.9 |
| 16 | 25.3 | 2.4 | 13.6 | 32.4 | 0.3 | 8.5 | 6.8 | 7.2 | 12.3 | 0.7 | 0.8 |
| 18 | 23.4 | 2.2 | 18.1 | 30.4 | 0 | 8.4 | 6.4 | 7.2 | 12.2 | 0.7 | 0.6 |
| 20 | 25.8 | 5.7 | 15.8 | 25.5 | 0 | 8.3 | 6.2 | 7.2 | 12.0 | 0.7 | 0.8 |
| 22 | 30.5 | 11.7 | 10.0 | 17.8 | 0 | 8.0 | 6.0 | 7.0 | 12.1 | 0.7 | 0.7 |
| 24 | 34.8 | 14.5 | 8.0 | 12.0 | 0 | 8.0 | 5.5 | 7.0 | 11.9 | 0.9 | 0.7 |
| 26 | 33.4 | 18.5 | 7.0 | 9.1 | 0 | 7.7 | 4.4 | 7.0 | 11.9 | 0.9 | 0.7 |
| 27 | 28.6 | 14.7 | 6.2 | 7.8 | 0 | 7.6 | 3.8 | 7.0 | 11.6 | 0.9 | 0.7 |
| 28 | 16.5 | 6.8 | 5.0 | 7.0 | 0 | 7.0 | 0.3 | 6.8 | 11.0 | 1.3 | 0.3 |
V183 for comparison: T 0-1.3 all game, S 34 d13-19, W 16-20 d13-19, C <=2.5 until d21, 3 quadrants.
- **Tile targets**: strawberry plantings continue d10-d15 (0.8-3.6/day) to peak 32 tiles d15-17; tomato plantings 1.2-2.7/day d15-d18, last d17-19, peak 18 tiles d18;
  wheat 6-11 plantings/day all game (the filler: every freed tile not claimed goes to wheat), carrots 0.5-7/day from d12, mostly d19-d26.
- **Replant map** (per farm; `tile old -> new @ planting days`): melon -> wheat 7.0 + tomato 1.6 (d10-14), wheat 2.6 (d15-19);
  strawberry (finished) -> wheat 10.5 + carrot 2.6 (d20-24), tomato 1.5 + wheat 2.0 (d15-19), carrot/wheat 1.4/1.5 (d25-29);
  tomato -> carrot 4.6 + wheat 3.5 (d20-24); carrot -> carrot/wheat; wheat -> wheat ~26-29 per 5-day block, -> tomato 2.9 (d10-14) + 5.6 (d15-19), -> strawberry 5.1 (d10-14).
  V183: melon -> wheat only; no tomato anywhere.
- **Herd**: no animal bought after d10-11 except rare cows/sheep (last BUY_ANIMAL median d9, max d15-21). No culling/selling of animals. Sheep are abandoned from d22
  (6.2 at d21 -> 4.4 d26 -> 0.3 d28); cows and geese kept to the end.
- **Feed gate (dated)**: last FEED = the animal's last production night <= d28: cows d27 (192/301), d28 (69); geese d27-28; sheep d26 (129/230), 42 sheep stop one cycle
  (3 days) earlier, ~26 stop 4-7 days earlier. V183 already does the same gate (cows/sheep/geese last feed = last production night in 161/227, 127/154, 64/198+116 at -1).
  The extra early sheep release is the only gate difference; its trigger is NOT determined (hypothesis: wool price vs cost of 3 feed wheat).
- **CARE**: every fed animal, ~0.7-0.9 per animal-day; last CARE d27-28 (sheep d25-26).
- **Hires**: 12/day d10-d27 (8-9 HIRE orders at h0 + 3-4 at h1; the h0 market list is ~8-9 HIRE + 1-2 SELL = the 10-order cap), 11 on d28, 10 on d29. ~7.7k coins/game (V183 5.3k).
- **Fertilizer** (collected only, bought 0-60 coins/game; ~490 collected, ~250 applied, ~240 sold): WHEAT at age 2 (99/farm; +9 at age 1, +20 at age 3), STRAWBERRY at ages 9 and 13
  (2 applications cover the 4 production nights), TOMATO at ages 7 and 10, CARROT at age 2, MELON never. Last FERTILIZE d28.
- **Coverage**: WATER 0.7-0.9 of plant tiles per day, FEED 0.7-0.9 of animals, CARE 0.7-0.9 — the same as V183 (0.5-1.0). Not a gap.

## 3. SELLING (d11-d28 unless stated; `tab/sell_hours.txt`, `tab/sell_threshold.txt`)
| product | when (P(sell any | stock>0) by hour) | lot | price behaviour | V183 |
|---|---|---|---|---|---|
| STRAWBERRY | h1 .37, h5 .65, h9 .69, h13 .71, h17 .77, h21 .89, h0 .34, else <.25 | median 2 if stock >= 6, 1 if < 6; sold/stock 0.40 | hold the rest; sold fraction 0.07 at p<0.1 base, 0.2-0.3 at 0.2-0.8, 0.35-0.40 at >= 0.9 | sells whole stock (sold/stock 1.00), h0-1 and h17-23 |
| MILK | h1 .47, h5 .26, h9 .52, h13 .54, h17 .69, h21 .87 | 1-2 (6 at first sale); sold/stock 0.67 | sold fraction 0.15 (p<0.1b) -> 0.4-0.48 (p>=0.7b) | whole stock |
| WOOL | h1 .52, h5 .57, h9 .60, h13 .63, h17 .59, h21 .55 | 0 if stock<3, 1 if 6-11, 2 if >= 12; sold/stock 0.33 | sells even at 0.1 base (decile-10 price 0.12 base) | whole stock h0-1/h17-23 |
| TOMATO | h22 .86, h23 .75, h18 .33, h0 .28, h14 .26 | 1-2 or whole (10) | 0.7-1.3 base, no hold | - (no tomatoes) |
| EGG | h22 .89, h23 .82, h2 .24 | 8-10 or 1-2 | always ~0.8 base (egg floor) | every hour 0.8-1.0 |
| CARROT | h23 .84, h22 .64, h0 .39 | 13, 9, 1 | 0.8-1.4 base | h0 whole stock |
| MELON | on harvest d10-d18, h0 and h6-h11 | 6 (one tile) | 0.5-1.0 base | same |
| FERTILIZER | d<=12: whenever held (P .85-1.0 at 0.7-1.0 base); later h0/h2/h22 1-2 per step, P .14-.22 at the floor | 1-2 | sells at floor late | also buys ~100 and resells |
| WHEAT | every hour, peaks h22 (94 u/farm), h0 75, h1 77, h2 50, h18-20 ~28 | < 10 per order | 0.8-1.6 base | h0 211 u + h20-23 |
- Implementation rule (fits the premium sales): at each h in {1,5,9,13,17,21} (plus h0 on harvest mornings) sell strawberry k = 2 if stock >= 6 else 1;
  milk k = 2 if stock >= 6, 1 if 3-5, 0-1 if < 3; wool k = 0-1 if stock < 6 (sells in ~50% of ticks), 1 if 6-11, 2 if >= 12. At h%4==1 with stock >= 3 they sell in
  ~65% (straw), ~55% (milk), ~60% (wool) of ticks; the skip trigger is NOT determined (tested: 4 h price change, price vs own last sale, sold at previous tick —
  none separates; only a weak monotone price slope). Premium sales at h%4==2/3 are rare (strawberry h14 .36, h18 .23, h10 .17, others <= .17).
- At the floor: they keep dripping (they do not hold out for recovery): wool 11% of stock-steps at <0.3 base still sell.
- **Last day d29**: sell everything (per farm: wheat 97, carrot 37, egg 22, strawberry 16, tomato 15, milk 12, fertiliser 12, wool 6). Premium holdings are already small by d29
  (they drip to near-zero through d25-28).
- **Wheat**: the opening churn is absent: T3 buy ~100 wheat d0-d10 (8,6,0,0,1,5,7,15,13,15,29) vs V183 ~900 (62,39,7,26,46,128,97,82,120,140,158);
  after d10 they buy ~5k coins in lots of 13 at h0-h1 only when short. Feed reserve in the shed at end of day = 1.7-2.3 wheat per animal (d11-15), 1.2-1.7 (d16-27),
  intra-day minimum 0 (just-in-time feeding). They are net wheat SELLERS: 541-681 units sold/game at ~30 (grown on 25-35 tiles), V183 1200 units sold / 1100 bought.

## 4. ENDGAME d26-d29 (median last day per op, T3)
PLANT strawberry d14-15, tomato d17-19, carrot d26-27, wheat d27; BUY_SEED wheat d27, carrot d26; BUY_ANIMAL none after ~d11 (max d15-21); BUILD_COOP d10, BUILD_PASTURE d12;
FEED sheep d26 / cow, goose d28; CARE d27-28; FERTILIZE d28 (all crops); WATER strawberry/tomato d28, wheat/carrot d29; COLLECT_FERTILIZER d29; DIG d26-27; SELL everything d29.
Hires 11 on d28 and 10 on d29 (they keep full crews to harvest and sell).

## 5. Per-day money (mean per farm, end of day) — clone check (`tab/money.md`)
| d | MMPQ | DSM | DECEM | T3 mean | T3 median | V183 mean | T3-V183 |
|---|---|---|---|---|---|---|---|
| 0 | 5 | 7 | 1 | 4 | 4 | 41 | -36 |
| 2 | 20 | 50 | 22 | 33 | 42 | 19 | +13 |
| 5 | 333 | 251 | 568 | 370 | 461 | 16 | +353 |
| 6 | 51 | 121 | 97 | 93 | 41 | 16 | +76 |
| 8 | 432 | 501 | 614 | 514 | 282 | 269 | +244 |
| 9 | 313 | 366 | 888 | 505 | 301 | 182 | +323 |
| 10 | 3054 | 2281 | 3428 | 2852 | 2595 | 8941 | -6089 |
| 11 | 6969 | 6509 | 6518 | 6648 | 6429 | 12804 | -6155 |
| 12 | 13195 | 11560 | 13317 | 12568 | 12522 | 15500 | -2931 |
| 13 | 17302 | 16347 | 18250 | 17197 | 17371 | 22180 | -4983 |
| 14 | 23276 | 22660 | 23960 | 23230 | 24165 | 26083 | -2853 |
| 15 | 26922 | 27524 | 27800 | 27427 | 27593 | 29601 | -2174 |
| 16 | 36912 | 37069 | 35659 | 36603 | 37121 | 34483 | +2119 |
| 18 | 50114 | 51287 | 48961 | 50247 | 49571 | 48542 | +1704 |
| 20 | 62158 | 63534 | 60151 | 62119 | 62960 | 60769 | +1350 |
| 22 | 71905 | 74079 | 69828 | 72169 | 72686 | 70300 | +1868 |
| 24 | 80567 | 83145 | 78182 | 80903 | 81552 | 79284 | +1619 |
| 26 | 90056 | 92811 | 86410 | 90089 | 89739 | 89349 | +739 |
| 28 | 102223 | 105518 | 97627 | 102192 | 102927 | 98901 | +3291 |
| 29 | 110795 | 113062 | 105267 | 110070 | 111251 | 107982 | +2088 |
(All 30 days in `tab/money.md` and playbook.json daily_mean.) Note: cross-world means; the shop-matched gap in fieldnow/REPORT.md is +4.1k (TOP1-3 - ours).

## 6. The 10 differences from V183, ordered by coin impact
Coin figures: "matched" = fieldnow shop-matched TOP1-3 minus our V183/v183ms farms (se in fieldnow/REPORT.md); "raw" = this ledger (`ledger.json`, cross-world means).
1. **Tomatoes from d8 in every world** (SW x0-1 rows 7-9, then melon tiles and freed wheat tiles; 18 tiles at d18 = 10.5 + 6.8 x dT5; last plant d17-19;
   fertilise ages 7 and 10; sell h22-h0). Tomato net **+6.2k matched** (raw revenue 8.8k vs 2.3k). V183: 0-1.3 tiles.
2. **Strawberry: d2 start + drip selling.** First seed d2 h12-14, 7 tiles by d5 (V183 4, start d3-4); then sell 1-2 per post-tick hour holding the rest
   (V183 sells the whole stock). Same-world realised price 142 vs our 118-134 => **+4.1k (se 0.6)**; strawberry net +4.2k matched.
3. **Wheat economy: no opening churn, grow-and-sell.** ~100 wheat bought d0-10 vs ~900; 25-35 wheat tiles all game (V183 16-20 d13-21), sold in < 10-unit lots every hour.
   Wheat net **+3.8k matched** (raw: rev 17.8k - buys 4.9k - seed 1.9k = +11.0k vs V183 40.8-32.0-1.6 = +7.2k).
4. **4th quadrant SE bought d10 h9-12 with the melon sale** (4000 coins; 37/37). Cost **-4.0k**, pays back via items 1 and 3 (SE row 5 wheat, x5 strawberries, later tomato/carrot).
   Note beta b0-b7 refuted SE alone for V183; here it is part of the bundle (tomato + wheat volume).
5. **Wool: sheep keyed on the first 3 shops (3.0 + 3.7 x dW3) and drip-sold 1 per tick; sheep released from d22.** Same-world wool price gap **+2.0k (se 0.5), +3.0k vs >= 2700**; raw wool revenue +4.6k.
6. **Hires: 12/day from d10 (8 at h0 + 4 at h1), 9 on d6, 9-10 on d8-9.** Cost **-2.4k matched** (7.7k vs 5.3k); it is what executes items 1-3.
7. **Geese late (d6-d10, keyed 4.3 + 3.6 x dE3) instead of 2 geese on d2.** Egg line **-1.4k matched / -2.2k raw for them** (our current edge), but it frees 600 coins on d2
   for the 3rd cow + first strawberry.
8. **Cows keyed on 3 shops (3.9 + 3.3 x dM3); 3rd cow on d2, cows 4-5 on d3-4; milk drip-sold 1-2 per tick.** Milk **-2.0k matched for them** (our edge; raw -0.4k).
9. **Fertiliser from collection only** (0-60 coins bought vs V183 6.7k bought + resold); net fertiliser line T3 12.3k vs V183 12.8k => **~-0.5k** (neutral), but it removes 100+ market orders.
10. **Endgame/herd release**: sheep 6.2 -> 0.3 over d21-28 (one extra cycle skipped for ~30% of sheep), full crews to d29, wheat/carrot planted to d27/d26-27. Size not separable (< 0.5k, not determined).

## 7. NOT determined / flags
- Exact skip trigger of the premium drip (which post-tick hours they skip); only the hour pattern, lot size by stock and a weak price slope are established.
- Carrot planting trigger (first carrot day d10-26, volume 5-108 plantings; weak link to carrot shops).
- Why ~30% of sheep are abandoned 3-7 days before their last production night.
- d3-d9 intra-day order is cash-driven; `tab/hourly_d3_10_*.txt` gives the modal hour-by-hour sequence with shares (DSM ~45-73% identical raw actions d2-d5, 9-22% after d6).
- Whether their movement/assignment of hands differs from ours (only effective actions were analysed; coverage rates are equal).
- The 3 teams are not identical: DECEM buys sheep 1+1+1 over h0-h4 on d0, MMPQ holds 3 sheep to h1; DECEM plants 22 strawberries at d10 vs 25-27 and grows more wheat (42 tiles d25).
- n: 37 T3 farms, all vs >= 2700 opponents on 29 Sep; V183's 28 farms are from 28 Sep vs the opponents' previous subs.
