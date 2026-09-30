# reactive_v1 — DESIGN (the controller as one piece)

One stateless-per-step controller (`rx.py`, embedded in `build/<tag>/main.py`) that rebuilds its whole plan from the observation every
step. Memory is limited to (i) per-unit sticky targets, (ii) rival-sales bookkeeping (needs the previous step's market inventory),
(iii) a daily diagnostics log. There is NO recorded tape: day 0 is a *plan* (targets + a hire schedule) that the same machinery executes.
All tunables live in one dict `P` (autotune can search it: `P.update({...})` appended to main.py, see "Parameters").

## 0. Engine facts the design is built on (checked in kaggriculture.py, engine 1.32.7)
- Order of a step: unit actions (farmer, then hands) -> market (per order index: HIRE/BUY_LAND atomics, then SELL/BUY lockstep,
  one unit per player per round) -> shop tick (step%4==0) / town centre (step%24==0) -> plant decay -> end of day (step%24==23).
  => a DROP and a SELL of the dropped goods work in the SAME step; seeds/wheat/animals bought at t are usable at t+1; a hand hired
  at t acts from t+1; the last processed step is 718 (d29 h22) -> everything must be sold by then.
- Plants: a new plant has consecutive_unwatered=1 -> it MUST be watered on its planting day or it weeds that night; afterwards at
  least every other day. Non-ongoing yield: 1 at planting, +1 per watering (+2 if fertilised) on ages ceil(maxd/2)..maxd
  (wheat 2-4 -> 4 units, carrot 2-3 -> 3, melon 6-12 -> 6 at age 10), harvestable from first_yield_day, decays 1 unit / 2 steps from
  day planted+maxd+1. FERTILIZE covers day..day+2 and must precede that day's WATER. Ongoing: tomato nights age 7..10, strawberry
  ages 9,11,13,15; +1 per night (+2 if watered that day AND fertilised).
- Animals: feed daily (2 unfed nights -> escape); production night every `interval` from first_yield; yield += 1 + care bank
  (bank only if fed that day), then today's fed+cared adds +1 to the bank for the NEXT night. The first night pays the whole
  bank (cap 6/6/4): a cow placed at d gives 6 milk on night d+7 then 3 per 2 days; sheep 6 on d+5 then 4 per 3; goose 4 on d+3
  then 2 per day. Every animal offers 1 fertiliser per morning (COLLECT).
- Market: price(inv) curves from MARKET_PARAMS; inventory = I0 + all sales - buys - town drain; shop instance drains 1 (2 for
  single-product shops) per product every 4 steps; town centre 1/day/product (not fertiliser); sales at $1 add no inventory.
  Fertiliser has no drain: its price only falls. Hire n-th of the day costs fib(n) (12 hands = 376/day). Shed cap 100 incl.
  animals; midnight drop destroys overflow; PLACE into a full shed keeps the rest in hand.

## 1. Plan layer (every step; the "daily plan" is the h0 evaluation, re-checked each hour as cash/tiles change)
Inputs: day/hour, shops known so far, prices + market inventory, own farm (tiles, cash, quadrants, units), shed, seeds, rival farm.
- Demand model: dem[X] = units per 4 h from the shops; drain/day = 6*dem + 1; expected future demand adds, per not-yet-drawn shop
  slot (d3, d6, ... <= 8 shops), E[dem] per shop (W .25, M .375, E .25, S .5, T .25, C .375, wheat .625).
  dX_k (playbook keys) = demand of the first k shops, unknown shops replaced by their expectation.
- Herd targets (playbook, T3 fit): d10 target sheep 3.0+3.7*dW3, cows 3.9+3.3*dM3, geese 4.3+3.6*dE3; early schedule caps
  (cows 2 d0, 3 d2, 4 d3, 5 d4, 6 d6; sheep 3 d0, 5 d6, 6 d8; geese 2 d6, 4 d8; full target from d9).
  After d10 the herd GROWS while it pays: add species X if NV_X > HERD_MIN (NV below) and labour is feasible, until HERD_LAST.
  Economic cap (all days >= 3): no more animals of a species whose product is forecast (own + rival supply vs drain, 8 days)
  below HERD_PMIN=0.4 x base — e.g. milk worlds where both farms flood milk to $5-30. Geese damped (HG0 2.3, HG1 2.0).
  Cash order: land reserve > feed reserve > planned premium seeds (SEED_FIRST) > animals.
- Crop targets (tiles): strawberry d2:2, d5:7, d6: 12.5+6.9*dS2, d10: 15.6+9.2*dS2, d13+: +S_LATE (cap S_MAX, last plant S_LAST);
  tomato from d8 ramping to 10.5+6.8*dT5 (min T_MIN) by d18 (last plant T_LAST); melon 6 on d0, 8 by d1-2, +MELON_NE on d6-7;
  carrot d12-26 where the carrot tile value beats wheat (economic model) up to 4+6*dC; wheat = filler for every other crop tile to W_LAST.
- Layout: animal structures take the free tiles nearest the shed (reactive: nearest free tile at the time the structure is needed);
  the k nearest free tiles are reserved from planting, k = structures still needed for the herd plan. Crops take the rest, premium
  crops (strawberry/tomato) nearer than wheat.
- Land: NE from LAND_DAY[0]=6, SW from 8, SE disabled in v1 (LAND_DAY[2]=99; 4 quadrants measured -1.6k at our labour cap), bought the first hour cash (incl. this step's sales) >= price + LAND_RES and
  the labour model says the new tiles can be worked; savings for the next quadrant are reserved from the evening before.
- Hires: schedule H_SCHED[d] (playbook 5,3,5,5,6,6,9,8,9,10,12...,11,10) capped by the labour need (below) and by cash;
  8 at h0 + rest at h1 (orders <= 10 per step).

## 2. Labour model (feasibility before every commitment)
Daily load L (unit-steps) = sum over assets of per-day costs: animal A_L (feed+care+collect+harvest/interval+walk), growing plant
C_L[crop] (water + walk + plant/harvest amortised), plus shed-trip overhead SHED_OV per unit. Capacity = units x steps left x EFF.
Before planting a new tile, buying an animal or land: require L + dL <= EFF * (1 + H_MAX) * 22 (13 units). EFF=0.7 in v1:
the plan is deliberately sized BELOW what 13 units could nominally do (measured: more crops -> lower coverage -> lower margin). The hire count is
max(schedule floor, ceil(L / (EFF*22.5)) - 1) capped at H_MAX and by cash (fib cost), so labour is bought for the plan and the
plan is sized to the labour that can be bought.

## 3. Economic model (per product) driving allocation
fp(X, t, extra) = price(inv + (S_own + S_rival + extra - drain) * t): own and rival supply rates are read from the tiles (animals
by species/care, plants by crop/age), drain from the shops (+expected new shops). Uses:
- crop value per tile-day V_c = (sum of expected units x fp at their harvest days - seed - labour x LAB_COIN) / days occupied;
  decides carrot vs wheat, and whether strawberry/tomato targets are still worth planting (V_c > V_wheat * K).
- herd growth NV_X = sum over remaining production nights of units x fp(product) + fert credit - feed wheat x fp(WHEAT) - labour - cost.
- selling: sell on arrival (below); the model only gates the $1-floor case (hold only if price <= HOLD_FLOOR and room/time remain).

## 4. Task dispatcher (every step) — as implemented in v1
Tasks per tile with coin values (marginal value of doing it today):
- FEED (needs wheat in hand): 20 + 0.5 x fertiliser price + FEED_CARE x product price when today's care still raises the next
  (capped) production + the care bank on a production night; +FEED_URG x (product price / base) if the animal was unfed yesterday
  (escape tonight). Only while a production night <= d28 remains.
- CARE: CARE_K x product price if it raises the next production (CARE_CAP: a cow's first cycle banks 7 cares for a cap of 5,
  so early cares are slack), else CARE_SLACK. Only if a production night after today remains (VT1).
- HARVEST animal: HV_K x units x price (+ overflow value if tonight's production would exceed the cap).
- COLLECT_FERTILIZER: max(COL_MIN, COL_K x fertiliser price).
- WATER: in-window yield gain x price; production night with fertiliser x price; must-water (would weed tonight) =
  keep value = plant value - LAM_F x unit-steps the plant still needs (marginal, not the whole plant value); no keep-waters.
- HARVEST crop when nothing more can be gained (max yield, or age == maxd and watered today, or decaying), ongoing crops whenever
  units are ready; early wheat (<= d5, >= 2 units) is harvested when strawberries need the tile (top-3 trick).
- FERTILIZE (needs fertiliser): engine gain x price - fertiliser price; ongoing crops only when the 3-day window covers >= 2
  production nights (strawberry ages 9/11/13, tomato 7-9) or the last one.
- PLANT (crop from the plan; seeds bought just in time when the unit is <= 1 step away), BUILD / DIG (structure plan), PLACE.
- Shed pseudo-tasks: FETCH wheat (lot W_LOT for uncovered feeds, counting only wheat carried by feeders), FETCH fertiliser,
  FETCH animal, DELIVER cargo (sell on arrival; value DROP_K x cargo value, forced on d29 before step 718).
Assignment: triage admits the most valuable tile tasks that fit in ADMIT_K x unit-steps left today; global greedy on
OFFSET + min(value, VCAP) + cluster bonus (CL_B x admitted neighbours) - LAM x distance (+STICK for the previous target).
Then: on-the-way (a unit heading somewhere first does any unassigned task lying on a shortest path: the single most valuable
routing rule, -28k when disabled), shed-pass delivery, opportunistic wheat pickup at the shed. Units act on their tile or move.
Rejected in screening (pinned-shop bench, paired): urgency tiers, keep-waters, finish-the-tile bonuses, stickiness > 20,
angular zones (-2..-9k), W_LOT 10-12, more hires (13-14 units), more crops (EFF 0.8-0.95), 2 quadrants (-9k), 4th quadrant (-1.6k).

## 5. Market (built AFTER the unit actions so the shed prediction includes this step's drops/pickups)
Order list (<= 10): SELL premium goods in the order of rival exposure (rival stock estimate = rival harvests seen on its tiles
minus rival sales from `rival_sold = inv' - inv + town_draw - own_sold`), then wheat surplus (above the uncovered feed need +
W_RES night reserve), fertiliser surplus (above planned applications), then HIRE, BUY_LAND, BUY_ANIMAL, BUY_SEED (just in time for
units about to plant), BUY_PRODUCT WHEAT (feed shortfall only). Cash is simulated through the list (sell proceeds first).
Shed guard: from h20 keep shed + carried cargo <= SHED_SAFE (96) by selling the lowest-value surplus; d29: sell everything, all
units walk cargo to the shed and DROP by step 718.

## 6. Endgame
Feed an animal only while a production night <= d28 remains; care only if a production night strictly after today remains (VT1);
no planting that cannot be harvested by d29 h20; last fertilise d28; d29 hires = harvest need; sell-all d29.

## Parameters
`P` in rx.py (one dict). Tuning: autotune/space.py-style knobs can be expressed as `P.update({...})` appended to main.py.
