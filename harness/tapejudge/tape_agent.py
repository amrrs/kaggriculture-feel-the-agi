# SPDX-License-Identifier: Apache-2.0
"""Tape-replay agent with a cash guard, early sales and a final sweep.

Budget guard, presale and terminal sweep logic derive from the Apache-2.0
Three-Day Shop Router (Yusuke Hayashi) port in experiments/router_market.py.
The tape itself is a public Kaggle episode action history (see TAPE_META).
"""
import base64, json, math, os, zlib

ITEMS = ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER','GOOSE','COW','SHEEP')
P = {'GUARD_INTERVAL': 24, 'GUARD_HORIZON': 72, 'TERMINAL_SWEEP': True, 'MIN_SALE_PRICE': 2,
     'GUARD_CASH_MULT': 1.0, 'PRESELL_LOOKAHEAD': 0, 'PRESELL_START': 72, 'SWEEP_FROM': 718,
     'MARKET_MODE': 'tape', 'HOLD_FRAC': 0.0, 'SHED_HI': 85, 'RESERVE_HORIZON': 72, 'MIN_LOT_PRICE': 2,
     'DEMAND_HOLD': True, 'LIQ_DAY': 29}
MP = {'WHEAT': (25, 400, 'sqrt', 0.8, 'log', 0.2), 'CARROT': (35, 450, 'hinge', 1.0, 'sqrt', 0.7), 'TOMATO': (60, 200, 'hinge', 0.4, 'sqrt', 0.6),
      'STRAWBERRY': (120, 100, 'sqrt', 0.7, 'linear', 1.6), 'MELON': (250, 300, 'log', 0.2, 'sq', 3.6), 'EGG': (50, 332, 'hinge', 0.4, 'log', 0.2),
      'MILK': (160, 122, 'sqrt', 0.6, 'linear', 1.6), 'WOOL': (200, 105, 'log', 0.2, 'sq', 3.2), 'FERTILIZER': (100, 200, 'linear', 0.4, 'linear', 0.4)}
SHOPS = {'BAKERY': ['EGG', 'WHEAT'], 'PIZZA_SHOP': ['MILK', 'TOMATO', 'WHEAT'], 'BRUNCH_SPOT': ['EGG', 'WHEAT', 'STRAWBERRY'], 'YARN_STORE': ['WOOL'],
         'ICE_CREAM_SHOP': ['STRAWBERRY', 'MILK', 'WHEAT'], 'PET_CAFE': ['CARROT'], 'SMOOTHIE_SHOP': ['STRAWBERRY', 'MILK'], 'FARMERS_MARKET': ['WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY']}

def _shape(f, x, T):
    x = max(0.0, x)
    if f == 'linear': return x
    if f == 'sq': return x * x
    if f == 'sqrt': return math.sqrt(x)
    if f == 'log': return math.log(1.0 + x)
    if f == 'hinge':
        u = x / T; return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x

def price_at(item, inv):
    base, T, bf, bt, af, at = MP[item]
    if inv < 10000:
        p = base + bt * base / _shape(bf, T, T) * _shape(bf, 10000 - inv, T)
    else:
        p = base - at * base / _shape(af, T, T) * _shape(af, inv - 10000, T)
    return max(1, int(round(p)))

def demand_per_day(shops):
    d = {p: 1 for p in ITEMS[:8]}; d['FERTILIZER'] = 0
    for s in shops:
        prods = SHOPS.get(s, []); m = 2 if len(prods) == 1 else 1
        for p in prods: d[p] += 6 * m
    return d
TAPE_META = {}
TAPE_B64 = ''  # filled by build step
TAPE = None

def _load_tape():
    global TAPE, TAPE_META
    if TAPE is not None:
        return TAPE
    path = os.environ.get('KAG_TAPE')
    if path:
        d = json.load(open(path)); TAPE = d['actions']; TAPE_META = {k: v for k, v in d.items() if k != 'actions'}
    else:
        TAPE = json.loads(zlib.decompress(base64.b64decode(TAPE_B64)))
    return TAPE

def fib(n):
    a = b = 1
    for _ in range(n): a, b = b, a + b
    return a

SEED_COST = dict(zip(ITEMS[:5], [10, 20, 50, 100, 80]))
ANIMAL_COST = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}

def budget_guard(obs, config, action, step, tape):
    me = obs['farms'][obs['player']]; priv = obs['private']; shed = priv['shed']; prices = obs['market']['prices']
    balance = {p: 0 for p in ITEMS}; reserve = {p: 0 for p in ITEMS}; hires = {}; budget = 0.
    quadrants = len(me['unlocked_quadrants'])
    for t in range(step, min(len(tape), step + P['GUARD_HORIZON'])):
        a = tape[t]
        for op in [a['farmer'], *a['hands']]:
            item = 'WHEAT' if op[0] == 'FEED' else 'FERTILIZER' if op[0] == 'FERTILIZE' else op[1] if op[0] == 'PLACE' and len(op) > 1 else None
            if item:
                n = max(1, op[2]) if op[0] == 'PLACE' and len(op) > 2 else 1
                balance[item] -= n; reserve[item] = max(reserve[item], -balance[item])
        for o in a['market']:
            op = o[0]; n = max(1, o[2]) if len(o) > 2 and isinstance(o[2], int) else 1
            if op == 'HIRE':
                d = (t - step) // 24; hires[d] = hires.get(d, 0) + 1
            elif op == 'BUY_LAND' and quadrants < 4:
                budget += [1000, 2000, 4000][quadrants - 1]; quadrants += 1
            elif op == 'BUY_SEED' and o[1] in SEED_COST: budget += SEED_COST[o[1]] * n
            elif op == 'BUY_PRODUCT' and o[1] in prices: budget += prices[o[1]] * n; balance[o[1]] += n
            elif op == 'BUY_ANIMAL' and o[1] in ANIMAL_COST: budget += ANIMAL_COST[o[1]] * n; balance[o[1]] += n
    for d, n in hires.items():
        first = me['hires_today'] if d == 0 else 0
        budget += sum(fib(first + i) for i in range(n)) * config.get('farmHandCostMult', 1)
    orders = action['market']
    existing = {p: sum(o[2] for o in orders if o[0] == 'SELL' and o[1] == p and len(o) > 2 and o[2] > 0) for p in ITEMS[:9]}
    cash = me['money'] + sum(min(shed.get(p, 0), existing[p]) * prices[p] for p in ITEMS[:9])
    short = budget * P['GUARD_CASH_MULT'] - cash
    if short <= 0: return
    candidates = []
    for i, p in enumerate(ITEMS[:9]):
        carried = sum(max(0, inv.get(p, 0)) for inv in priv['inventories'])
        available = max(0, shed.get(p, 0) - max(0, reserve[p] - carried) - existing[p])
        if available > 0 and prices[p] >= P['MIN_SALE_PRICE']: candidates.append((-prices[p], i, p, available))
    added = False
    for neg, _, p, n in sorted(candidates):
        if short <= 0: break
        q = min(n, math.ceil(short / -neg)); prev = next((o for o in orders if o[0] == 'SELL' and o[1] == p), None)
        if prev is not None: prev[2] += q
        elif len(orders) < config.get('maxMarketOrdersPerTurn', 10): orders.append(['SELL', p, q])
        else: continue
        short -= q * -neg; added = True
    if added: orders.sort(key=lambda o: o[0] != 'SELL')

def reserves(tape, step, priv):
    need = {p: 0 for p in ITEMS}; bal = {p: 0 for p in ITEMS}
    for t in range(step, min(len(tape), step + P['RESERVE_HORIZON'])):
        a = tape[t]
        for op in [a['farmer'], *a['hands']]:
            item = 'WHEAT' if op[0] == 'FEED' else 'FERTILIZER' if op[0] == 'FERTILIZE' else op[1] if op[0] == 'PLACE' and len(op) > 1 else None
            if item:
                n = max(1, op[2]) if op[0] == 'PLACE' and len(op) > 2 else 1
                bal[item] -= n; need[item] = max(need[item], -bal[item])
        for o in a['market']:
            if o[0] in ('BUY_PRODUCT', 'BUY_ANIMAL') and len(o) > 2 and o[1] in bal: bal[o[1]] += max(1, o[2])
    for p in ITEMS:
        carried = sum(max(0, inv.get(p, 0)) for inv in priv['inventories'])
        need[p] = max(0, need[p] - carried)
    return need

def smart_sell(obs, config, action, step, tape):
    me = obs['farms'][obs['player']]; priv = obs['private']; shed = priv['shed']; mk = obs['market']
    inv = mk['inventory']; day = step // 24; hour = step % 24
    need = reserves(tape, step, priv)
    dem = demand_per_day(obs['town']['unlocked_shops'])
    total = sum(shed.values()); room_pressure = total >= P['SHED_HI']
    smart_items = [p for p in ITEMS[:9] if p not in P.get('KEEP_TAPE_SELL', ('WHEAT', 'FERTILIZER'))]
    orders = [o for o in action['market'] if not (o[0] == 'SELL' and o[1] in smart_items)]
    sells = []
    liquidate = day >= P['LIQ_DAY']
    for p in sorted(smart_items, key=lambda q: -mk['prices'][q]):
        avail = shed.get(p, 0) - need.get(p, 0)
        if liquidate and step >= config.get('episodeSteps', 720) - 2: avail = shed.get(p, 0)
        if avail <= 0: continue
        base = MP[p][0]
        # hold glutted goods that shops will consume, unless shed is filling or season ending
        q = 0; cur = inv[p]
        for k in range(avail):
            pr = price_at(p, cur + k)
            if pr < P['MIN_LOT_PRICE'] and not liquidate: break
            if not liquidate and not room_pressure and P['DEMAND_HOLD'] and dem[p] > 1 and pr < P['HOLD_FRAC'] * base: break
            q += 1
        if q > 0: sells.append(['SELL', p, q])
    action['market'] = (sells + orders)[:config.get('maxMarketOrdersPerTurn', 10)]

def agent(obs, config=None):
    config = config or {}; step = obs.get('step', 0); tape = _load_tape()
    if step < 0 or step >= len(tape): return {'farmer': ['PASS'], 'hands': [], 'market': []}
    a = tape[step]
    action = {'farmer': list(a['farmer']), 'hands': [list(x) for x in a['hands']], 'market': [list(x) for x in a['market']]}
    if P['MARKET_MODE'] == 'smart': smart_sell(obs, config, action, step, tape)
    if P['GUARD_INTERVAL'] and step % P['GUARD_INTERVAL'] == 0: budget_guard(obs, config, action, step, tape)
    lookahead = P.get('PRESELL_LOOKAHEAD', 0)
    if lookahead and step >= P.get('PRESELL_START', 72):
        scheduled = {}
        for t in range(step + 1, min(len(tape), step + lookahead + 1)):
            for order in tape[t]['market']:
                if order[0] == 'SELL' and order[1] in ITEMS[1:8]:
                    scheduled[order[1]] = scheduled.get(order[1], 0) + max(0, order[2])
        shed = obs['private']['shed']
        for p, n in scheduled.items():
            existing = next((o for o in action['market'] if o[0] == 'SELL' and o[1] == p), None)
            q = min(n, max(0, shed.get(p, 0) - (existing[2] if existing else 0)))
            if q <= 0: continue
            if existing: existing[2] += q
            elif len(action['market']) < config.get('maxMarketOrdersPerTurn', 10): action['market'].append(['SELL', p, q])
    if P['TERMINAL_SWEEP'] and step >= P['SWEEP_FROM'] and step == config.get('episodeSteps', 720) - 2:
        existing = {o[1] for o in action['market'] if o[0] == 'SELL'}
        for o in action['market']:
            if o[0] == 'SELL': o[2] = 1000000
        for p in ITEMS[:9]:
            if p not in existing and len(action['market']) < config.get('maxMarketOrdersPerTurn', 10): action['market'].append(['SELL', p, 1000000])
    return action
