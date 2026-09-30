"""reactive_v1 (rx): a fully reactive kaggriculture controller (30 Sep 2026, agents/reactive_v1).
No tape. Every step: plan (targets for herd / crops / land / hires from shops, prices, rival, own farm) -> labour model ->
task list with coin values -> greedy unit dispatch -> market list (built after unit actions, so DROP + SELL share a step).
All tunables in P. Standard library only. The last callable in this file is `agent` (Kaggle loader rule)."""
import math

# ----------------------------------------------------------------------------------------------------------------- constants
SHED = ((4, 4), (5, 4), (4, 5), (5, 5))
CROPS = {
    "WHEAT": dict(seed=10, first=2, maxd=4, interval=0, maxy=6, ongoing=False),
    "CARROT": dict(seed=20, first=2, maxd=3, interval=0, maxy=4, ongoing=False),
    "TOMATO": dict(seed=50, first=8, maxd=8, interval=1, maxy=4, ongoing=True),
    "STRAWBERRY": dict(seed=100, first=10, maxd=10, interval=2, maxy=4, ongoing=True),
    "MELON": dict(seed=80, first=10, maxd=12, interval=0, maxy=6, ongoing=False),
}
ANIM = {"GOOSE": dict(cost=300, st="COOP", first=4, interval=1, held=4, prod="EGG"),
        "COW": dict(cost=400, st="PASTURE", first=8, interval=2, held=6, prod="MILK"),
        "SHEEP": dict(cost=500, st="PASTURE", first=6, interval=3, held=6, prod="WOOL")}
BASE = {'WHEAT': 25, 'CARROT': 35, 'TOMATO': 60, 'STRAWBERRY': 120, 'MELON': 250, 'EGG': 50, 'MILK': 160, 'WOOL': 200, 'FERTILIZER': 100}
MP = {"WHEAT": (25, 400, "sqrt", 0.80, "log", 0.20), "CARROT": (35, 450, "hinge", 1.00, "sqrt", 0.70),
      "TOMATO": (60, 200, "hinge", 0.40, "sqrt", 0.60), "STRAWBERRY": (120, 100, "sqrt", 0.70, "linear", 1.60),
      "MELON": (250, 300, "log", 0.20, "sq", 3.60), "EGG": (50, 332, "hinge", 0.40, "log", 0.20),
      "MILK": (160, 122, "sqrt", 0.60, "linear", 1.60), "WOOL": (200, 105, "log", 0.20, "sq", 3.20),
      "FERTILIZER": (100, 200, "linear", 0.40, "linear", 0.40)}
SHOPS = {'BAKERY': ['EGG', 'WHEAT'], 'PIZZA_SHOP': ['MILK', 'TOMATO', 'WHEAT'], 'BRUNCH_SPOT': ['EGG', 'WHEAT', 'STRAWBERRY'],
         'YARN_STORE': ['WOOL'], 'ICE_CREAM_SHOP': ['STRAWBERRY', 'MILK', 'WHEAT'], 'PET_CAFE': ['CARROT'],
         'SMOOTHIE_SHOP': ['STRAWBERRY', 'MILK'], 'FARMERS_MARKET': ['WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY']}
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
PREMIUM = ('STRAWBERRY', 'MILK', 'WOOL', 'MELON', 'TOMATO', 'EGG', 'CARROT')
LAND_PRICES = (1000, 2000, 4000)
LAND_ORDER = ('NE', 'SW', 'SE')
LAST_STEP = 718          # last processed step (d29 h22)
LAST_NIGHT = 28          # last production night whose output can still be sold (harvest d29)


def _exp_shop_dem():
    """expected demand (units / 4 h) that one not-yet-drawn shop adds per product (shops drawn uniformly with replacement)"""
    e = {}
    for s, pr in SHOPS.items():
        m = 2 if len(pr) == 1 else 1
        for x in pr: e[x] = e.get(x, 0.0) + m / len(SHOPS)
    return e


EXP_SHOP = _exp_shop_dem()

# ----------------------------------------------------------------------------------------------------------------- parameters
P = dict(
    # dispatch
    LAM=30.0, STICK=20.0, OFFSET=500.0, W_LOT=6, F_LOT=4, VCAP=200.0, ADMIT_K=0.45, ONWAY=True, ONWAY_MIN=0.5, FEED_R=1, URG_B=0.0, URG_PV=60.0, SHED_PASS_DROP=True, SPD_MIN=20.0, CARE_CAP=True, CARE_SLACK=5.0, CARE_MARGIN=1, FERT2=True, FINISH_B=0.0, AFIN_B=0.0, PFIN_B=0.0, EARLY_WH_LAST=5, SEED_FIRST=True, LAM_F=20.0, MUST_MIN=15.0, HV_NO=0.7, FEED_URG_H=24, CARE_URG_H=24,
    # hires: schedule for d0..d10 (playbook), then labour-driven between H_LO and H_MAX
    H_SCHED=[5, 3, 5, 5, 6, 6, 9, 8, 9, 10, 12], H_LO=9, H_MAX=12, H_H0=8, H29=9, H28=11,
    # labour model (unit-steps / day)
    A_L=4.0, C_L=1.9, W_L=2.1, OV_U=2.0, EFF=0.7, STEPS_U=22.0,
    # herd (playbook keyed targets at d10) + growth after d10
    HS0=3.0, HS1=3.7, HC0=3.9, HC1=3.3, HG0=2.3, HG1=2.0, H_ROUND=0.35,
    HERD_GROW=True, HERD_LAST=15, HERD_MIN=600.0, HERD_CAP=26, HERD_CASH=1200,
    # crops
    S_LAST=15, S6_0=12.5, S6_1=6.9, S10_0=15.6, S10_1=9.2, S14_0=18.0, S14_1=10.0, S_MAX=34,
    T_FIRST=8, T_LAST=18, T0=6.0, T1=6.8, T_MIN=7.0, T_MAX=18, T_RAMP=10.0,
    M_D0=6, M_D1=8, M_NE=3, M_LAST=7,
    C_FIRST=12, C_LAST=26, C0=4.0, C1=6.0, C_MAX=24, CAR_K=1.05,
    W_LAST=27, W_MIN=0, W_MIN_DAY=10, PREM_K=0.5, LAB_COIN=5.0,
    # land
    LAND_DAY=(6, 8, 10), LAND_RES=(0, 60, 150), LAND_SAVE_H=12,
    # task values
    FEED_V=60.0, FEED_CARE=1.0, FEED_RES_D=0.5, FERT_DELIV_P=25, FEED_URG=900.0, CARE_K=1.0, HV_K=0.55, HV_OVF=1.0, COL_K=0.85, COL_MIN=6.0, WATER_KEEP=0.0,
    PLANT_V=45.0, BUILD_V=160.0, PLACE_V=320.0, DIG_V=60.0, FERT_OPP=1.0, DROP_K=0.5, DROP_MIN=30.0,
    FETCH_K=0.8,
    # market
    HOLD_FLOOR=2, W_RES=0.5, W_RES_H=18, SHED_SAFE=94, SEED_BUF_W=2, ANIMAL_HOUR=12, ANIMAL_RES_LAST=-1, BUY_AHEAD=5,
    SELL_FERT_EARLY=True, D29_SELL_ALL=True,
)
S = {}


# ----------------------------------------------------------------------------------------------------------------- helpers
def _shape(f, x, T):
    x = max(0.0, x)
    if f == "linear": return x
    if f == "sq": return x * x
    if f == "sqrt": return math.sqrt(x)
    if f == "log": return math.log(1.0 + x)
    if f == "hinge":
        u = x / T
        return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x


def mprice(item, inv):
    b, T, bf, bt, af, at = MP[item]; I0 = 10000
    if inv < I0:
        p = b + bt * b / _shape(bf, T, T) * _shape(bf, I0 - inv, T)
    else:
        p = b - at * b / _shape(af, T, T) * _shape(af, inv - I0, T)
    return max(1, int(round(p)))


def fib(n):
    a, b = 1, 1
    for _ in range(n): a, b = b, a + b
    return a


def md(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])


def shed_d(p): return min(abs(p[0] - s[0]) + abs(p[1] - s[1]) for s in SHED)


def near_shed(p): return min(SHED, key=lambda s: abs(p[0] - s[0]) + abs(p[1] - s[1]))


def quad(x, y): return ("N" if y < 5 else "S") + ("W" if x < 5 else "E")


def step_toward(p, q, flip):
    dx, dy = q[0] - p[0], q[1] - p[1]
    if dx == 0 and dy == 0: return None
    if flip and dy != 0 or dx == 0:
        return ['SOUTH'] if dy > 0 else ['NORTH']
    return ['EAST'] if dx > 0 else ['WEST']


def demand(shops):
    c = {}
    for s in shops:
        pr = SHOPS.get(s, [])
        m = 2 if len(pr) == 1 else 1
        for x in pr: c[x] = c.get(x, 0) + m
    return c


def dem_k(shops, k, prod):
    """playbook key dX_k: demand of the first k shops, unknown shops at their expectation"""
    d = 0.0
    for i in range(k):
        if i < len(shops):
            pr = SHOPS.get(shops[i], [])
            if prod in pr: d += 2 if len(pr) == 1 else 1
        else:
            d += EXP_SHOP.get(prod, 0.0)
    return d


def anim_nights(a, placed, d0, d1=LAST_NIGHT):
    A = ANIM[a]; out = []
    for n in range(max(d0, 0), d1 + 1):
        k = n + 1 - placed - A['first']
        if k >= 0 and k % A['interval'] == 0: out.append(n)
    return out


def plant_nights(crop, pd, d0, d1=LAST_NIGHT):
    c = CROPS[crop]; out = []
    for n in range(d0, d1 + 1):
        k = n + 1 - pd - c['first']
        if k < 0 or k % c['interval']: continue
        if k // c['interval'] + 1 > c['maxy']: continue
        out.append(n)
    return out


# ----------------------------------------------------------------------------------------------------------------- economics
def supply_rates(tiles):
    """expected units / day per product from a farm's tiles (animals cared; plants on their clocks)"""
    r = dict.fromkeys(PRODUCTS, 0.0)
    for row in tiles:
        for t in row:
            if not isinstance(t, dict): continue
            a = t.get('animal')
            if a:
                A = ANIM[a]; r[A['prod']] += (1.0 + A['interval']) / A['interval']; r['FERTILIZER'] += 1.0; r['WHEAT'] -= 1.0
            elif t.get('kind') == 'PLANT':
                c = t['crop']
                r[c] += {'WHEAT': 1.0, 'CARROT': 1.0, 'TOMATO': 0.45, 'STRAWBERRY': 0.3, 'MELON': 0.5}[c]
    return r


class Econ:
    def __init__(s, inv, shops, day, own_tiles, riv_tiles):
        s.inv = inv; s.day = day
        dem = demand(shops)
        n_future = max(0, min(8, 9) - len(shops))
        s.drain = {}
        for x in PRODUCTS:
            s.drain[x] = 0.0 if x == 'FERTILIZER' else 6.0 * dem.get(x, 0) + 1.0
        s.dshop = {x: (0.0 if x == 'FERTILIZER' else 6.0 * EXP_SHOP.get(x, 0.0)) for x in PRODUCTS}   # per new shop per day
        s.nshops = len(shops)
        so = supply_rates(own_tiles); sr = supply_rates(riv_tiles)
        s.net = {x: so[x] + sr[x] - s.drain[x] for x in PRODUCTS}
        s.cache = {}

    def fp(s, x, t, extra=0.0):
        """forecast price of x in t days (market inventory drift from both farms' supply and the shops' drain)"""
        key = (x, int(t * 4), int(extra * 10))
        v = s.cache.get(key)
        if v is not None: return v
        t = max(0.0, t)
        # new shops unlock every 3 days (d3, d6, ...) up to 8 instances
        add = 0.0
        if x != 'FERTILIZER':
            k = s.nshops; dd = s.day
            while k < 8:
                ud = 3 * (k + 1)
                if ud > s.day + t: break
                add += s.dshop[x] * max(0.0, s.day + t - max(ud, dd)); k += 1
        inv = s.inv.get(x, 10000) + (s.net[x] + extra) * t - add
        v = mprice(x, inv); s.cache[key] = v
        return v


def crop_rate(E, c, day):
    """coins per tile-day of planting crop c today (forecast prices, seed, labour)"""
    left = LAST_NIGHT + 1 - day
    L = P['LAB_COIN']
    if c == 'WHEAT':
        if left < 2: return -99
        u = 4.0 if left >= 4 else 2.0 + (left - 2); dur = min(4.5, left); lab = 7
    elif c == 'CARROT':
        if left < 2: return -99
        u = 3.0 if left >= 3 else 2.0; dur = min(3.5, left); lab = 6
    elif c == 'TOMATO':
        n = len(plant_nights('TOMATO', day, day)); u = 1.4 * n; dur = min(11.5, left); lab = 16
    elif c == 'STRAWBERRY':
        n = len(plant_nights('STRAWBERRY', day, day)); u = 1.6 * n; dur = min(16.5, left); lab = 20
    else:
        if left < 11: return -99
        u = 6.0; dur = 10.5; lab = 12
    if u <= 0: return -99
    tm = {'WHEAT': 4, 'CARROT': 3, 'TOMATO': 9, 'STRAWBERRY': 12, 'MELON': 10}[c]
    return (u * E.fp(c, tm) - CROPS[c]['seed'] - lab * L) / dur


# ----------------------------------------------------------------------------------------------------------------- state
def reset(): S.clear()


def _track_rival(obs, me_i, inv, shops, step, riv_tiles):
    """rival_sold = inv' - inv + town_draw - own_sold (exact above the $1 floor); rival harvests from its visible tiles"""
    pv = S.get('prev')
    rs = S.setdefault('rsold', dict.fromkeys(PRODUCTS, 0.0)); rh = S.setdefault('rharv', dict.fromkeys(PRODUCTS, 0.0))
    if pv and pv['step'] == step - 1:
        ps = pv['step']; dem = demand(pv['shops'])
        for x in PRODUCTS:
            draw = 0
            if ps % 4 == 0: draw += dem.get(x, 0)
            if ps % 24 == 0 and x != 'FERTILIZER': draw += 1
            own = pv['sold'].get(x, 0) - pv['bought'].get(x, 0)
            rn = inv.get(x, 0) - pv['inv'].get(x, 0) + draw - own
            if rn > 0: rs[x] += rn
        pt = pv['rt']
        for y in range(10):
            for x_ in range(10):
                a = pt[y][x_]; b = riv_tiles[y][x_]
                if not isinstance(a, tuple) or a[2] <= 0: continue
                an, cr, ya, kd, mls = a
                prod = ANIM[an]['prod'] if an else cr
                if not prod: continue
                if isinstance(b, dict) and b.get('animal') == an and b.get('crop') == cr:
                    yb = b.get('yield_units', 0)
                    if yb < ya and not (kd == 'PLANT' and mls >= 0 and step - 1 >= mls):
                        rh[prod] += ya - yb
                elif b is None and kd == 'PLANT':
                    rh[prod] += ya
    return {x: max(0.0, rh[x] - rs[x]) for x in PRODUCTS}


# ----------------------------------------------------------------------------------------------------------------- the agent
def act(obs):
    step = int(obs['step']); day = step // 24; hour = step % 24
    pl = obs['player']; me = obs['farms'][pl]; rv = obs['farms'][1 - pl]
    priv = obs['private']; tiles = me['tiles']
    shed = dict(priv['shed']); seeds = dict(priv['seeds'])
    prices = dict(obs['market']['prices']); inv = dict(obs['market']['inventory'])
    shops = list(obs['town']['unlocked_shops'])
    money = float(me['money'])
    quads = list(me['unlocked_quadrants'])
    pos = [tuple(me['farmer'])] + [tuple(h) for h in me['hands']]
    nU = len(pos)
    invs = [dict(i) for i in (list(priv.get('inventories') or [{}]) + [{}] * nU)[:nU]]
    if S.get('day') != day:
        S['day'] = day; S['tgt'] = {}
        S.setdefault('log', {})
    lg = S['log'].setdefault(day, dict(idle=0, moves=0, acts={}, sold={}, bought={}, hires=0, err=0))
    rstock = _track_rival(obs, pl, inv, shops, step, rv['tiles'])
    E = Econ(inv, shops, day, tiles, rv['tiles'])
    fert_p = prices['FERTILIZER']

    # ------------------------------------------------------------------ farm inventory
    animals = []           # (x, y, tile)
    empty_st = {'COOP': [], 'PASTURE': []}
    plants = []            # (x, y, tile)
    free = []              # plantable None tiles
    weeds = []
    cnt_crop = dict.fromkeys(CROPS, 0)
    herd = dict.fromkeys(ANIM, 0)
    for y in range(10):
        for x in range(10):
            t = tiles[y][x]
            if t == 'LOCKED': continue
            if t is None: free.append((x, y)); continue
            k = t.get('kind')
            if t.get('animal'):
                animals.append((x, y, t)); herd[t['animal']] += 1
            elif k in ('COOP', 'PASTURE'):
                empty_st[k].append((x, y))
            elif k == 'PLANT':
                plants.append((x, y, t))
                c = t['crop']
                if CROPS[c]['ongoing']:
                    if plant_nights(c, t['planted_day'], day): cnt_crop[c] += 1
                else:
                    cnt_crop[c] += 1
            elif k == 'WEED':
                weeds.append((x, y))
    in_shed_an = {a: shed.get(a, 0) for a in ANIM}
    in_hand_an = {a: sum(iv.get(a, 0) for iv in invs) for a in ANIM}

    # ------------------------------------------------------------------ plan: herd targets
    dW3 = dem_k(shops, 3, 'WOOL'); dM3 = dem_k(shops, 3, 'MILK'); dE3 = dem_k(shops, 3, 'EGG')
    t10 = {'SHEEP': P['HS0'] + P['HS1'] * dW3, 'COW': P['HC0'] + P['HC1'] * dM3, 'GOOSE': P['HG0'] + P['HG1'] * dE3}
    sched = {'COW': ((0, 2), (2, 3), (3, 4), (4, 5), (6, 6), (9, 99)), 'SHEEP': ((0, 3), (6, 5), (8, 6), (9, 99)),
             'GOOSE': ((0, 0), (6, 2), (8, 4), (9, 99))}
    htgt = {}
    for a in ANIM:
        cap = 0
        for d_, v in sched[a]:
            if day >= d_: cap = v
        htgt[a] = int(min(cap, math.floor(t10[a] + P['H_ROUND'])))
    have = {a: herd[a] + in_shed_an[a] + in_hand_an[a] for a in ANIM}
    n_anim = sum(have.values())

    # ------------------------------------------------------------------ labour model
    def load_of(n_an, crop_counts, n_units):
        L = n_an * P['A_L'] + P['OV_U'] * n_units
        for c, n in crop_counts.items(): L += n * (P['W_L'] if c == 'WHEAT' else P['C_L'])
        return L
    n_crop_tiles = dict(cnt_crop)
    L_now = load_of(n_anim, n_crop_tiles, 1 + P['H_MAX'])
    CAP_MAX = P['EFF'] * (1 + P['H_MAX']) * P['STEPS_U']

    # herd growth after d10 (economic model + labour feasibility)
    if P['HERD_GROW'] and 10 <= day <= P['HERD_LAST'] and n_anim < P['HERD_CAP']:
        best = None; bv = P['HERD_MIN']
        for a in ANIM:
            A = ANIM[a]; nights = anim_nights(a, day, day)
            if not nights: continue
            val = 0.0
            for i, n in enumerate(nights):
                u = min(A['held'], 1 + 0.9 * (n - day)) if i == 0 else 1 + 0.9 * A['interval']
                val += u * E.fp(A['prod'], n + 1 - day, extra=(1.0 + A['interval']) / A['interval'])
            days_fed = nights[-1] - day + 1
            val += days_fed * max(3.0, 0.6 * fert_p) * 0.5
            val -= days_fed * E.fp('WHEAT', days_fed / 2.0) + days_fed * P['A_L'] * P['LAB_COIN'] + A['cost']
            if val > bv and L_now + P['A_L'] <= CAP_MAX: best, bv = a, val
        if best is not None and have[best] >= htgt[best]:
            htgt[best] = have[best] + 1
    S['htgt'] = htgt

    # ------------------------------------------------------------------ plan: crop targets
    dS2 = dem_k(shops, 2, 'STRAWBERRY'); dT5 = dem_k(shops, 5, 'TOMATO'); dC = demand(shops).get('CARROT', 0) + 0.0
    if day < 2: sT = 0
    elif day <= 5: sT = {2: 2, 3: 4, 4: 6, 5: 7}[day]
    elif day <= 9: sT = P['S6_0'] + P['S6_1'] * dS2
    elif day <= 12: sT = P['S10_0'] + P['S10_1'] * dS2
    else: sT = P['S14_0'] + P['S14_1'] * dS2
    if day > P['S_LAST']: sT = 0
    sT = min(P['S_MAX'], sT)
    tT = 0.0
    if P['T_FIRST'] <= day <= P['T_LAST']:
        tfin = min(P['T_MAX'], max(P['T_MIN'], P['T0'] + P['T1'] * dT5))
        tT = max(2.0, tfin * min(1.0, (day - P['T_FIRST'] + 1) / P['T_RAMP']))
    mT = 0
    if day == 0: mT = P['M_D0']
    elif day <= 5: mT = P['M_D1']
    elif day <= P['M_LAST']: mT = P['M_D1'] + (P['M_NE'] if 'NE' in quads else 0)
    cT = 0.0
    vw = crop_rate(E, 'WHEAT', day)
    if P['C_FIRST'] <= day <= P['C_LAST']:
        vc = crop_rate(E, 'CARROT', day)
        if vc > vw * P['CAR_K']: cT = min(P['C_MAX'], P['C0'] + P['C1'] * dC)
    ctgt = {'STRAWBERRY': sT, 'TOMATO': tT, 'MELON': mT, 'CARROT': cT, 'WHEAT': 999 if day <= P['W_LAST'] else 0}
    # premium crops must still be worth a tile compared with wheat
    for c in ('STRAWBERRY', 'TOMATO', 'MELON'):
        if ctgt[c] > 0 and crop_rate(E, c, day) < P['PREM_K'] * vw: ctgt[c] = 0

    # ------------------------------------------------------------------ plan: structures + tile reservation
    st_need = {'COOP': 0, 'PASTURE': 0}
    for a in ANIM:
        st_need[ANIM[a]['st']] += max(0, htgt[a] - herd[a])
    st_short = {k: max(0, st_need[k] - len(empty_st[k])) for k in st_need}
    cand_st = sorted(free + weeds, key=lambda p: (shed_d(p), p[1], p[0]))
    build_plan = {}        # tile -> kind
    i = 0
    for k in ('PASTURE', 'COOP'):
        for _ in range(st_short[k]):
            while i < len(cand_st) and cand_st[i] in build_plan: i += 1
            if i >= len(cand_st): break
            build_plan[cand_st[i]] = k; i += 1
    # crop plan for free tiles: nearest-first gets the scarcest target first (premium near the shed)
    plan_crop = {}
    if hour <= 22:
        deficit = {c: ctgt[c] - cnt_crop[c] for c in CROPS}
        order = ('STRAWBERRY', 'MELON', 'TOMATO', 'CARROT', 'WHEAT')
        if day >= P['W_MIN_DAY'] and cnt_crop['WHEAT'] < P['W_MIN']:
            order = ('STRAWBERRY', 'MELON', 'WHEAT', 'TOMATO', 'CARROT')
        L_plan = L_now
        for p in sorted(free, key=lambda p: (shed_d(p), p[1], p[0])):
            if p in build_plan: continue
            for c in order:
                if deficit[c] >= 1 if c != 'WHEAT' else deficit[c] > 0:
                    dl = P['W_L'] if c == 'WHEAT' else P['C_L']
                    if L_plan + dl > CAP_MAX: break
                    if c == 'WHEAT' and vw <= 0: continue
                    plan_crop[p] = c; deficit[c] -= 1; L_plan += dl
                    break

    # ------------------------------------------------------------------ budget (cash reserved for land / animals)
    reserve = 0.0
    nq = len(quads) - 1
    land_due = None
    if nq < 3:
        ld = P['LAND_DAY'][nq]
        if day >= ld or (day == ld - 1 and hour >= P['LAND_SAVE_H']):
            reserve += LAND_PRICES[nq] + P['LAND_RES'][nq]
            if day >= ld: land_due = nq
    want_an = []
    for a in sorted(ANIM, key=lambda a: -(htgt[a] - have[a])):
        if htgt[a] > have[a]: want_an.append(a)
    if want_an and hour <= P['ANIMAL_HOUR'] and day <= P['ANIMAL_RES_LAST']:
        reserve += min(ANIM[a]['cost'] for a in want_an)
    n_feed_all = len(animals) + sum(in_shed_an.values()) + sum(in_hand_an.values())
    w_stock = shed.get('WHEAT', 0) + sum(iv.get('WHEAT', 0) for iv in invs)
    fert_in = len(animals) * fert_p * 0.8 if fert_p >= 20 else 0.0     # tomorrow morning's fertiliser income
    feed_res = max(0.0, max(0, n_feed_all * (1 + P['FEED_RES_D']) - w_stock) * (prices['WHEAT'] + 1) - fert_in)
    reserve += feed_res
    budget = money - reserve     # spendable on seeds without delaying land/animals/feed

    # ------------------------------------------------------------------ tasks
    wheat_p = prices['WHEAT']
    tasks = []   # dict(pos, op, arg, val, need, key)
    feeds_needed = 0
    feed_list = []
    for (x, y, t) in animals:
        a = t['animal']; A = ANIM[a]; pp = prices[A['prod']]
        nights = anim_nights(a, t['placed_day'], day)
        tonight = bool(nights) and nights[0] == day
        later = [n for n in nights if n > day]
        # does today's care still raise the next (capped) production? bank for the next night after today
        care_need = True
        if P['CARE_CAP'] and later:
            nn = later[0]; bank = 0 if tonight else t.get('pending_care_bonus', 0)
            if bank + (nn - day - 1) >= A['held'] - 1 + P['CARE_MARGIN']: care_need = False
        if not t['fed_today'] and nights:
            v = P['FEED_V'] + (P['FEED_URG'] if t['consecutive_unfed'] >= 1 else 0.0)
            if tonight: v += t.get('pending_care_bonus', 0) * pp
            if later and care_need: v += P['FEED_CARE'] * pp
            tasks.append(dict(pos=(x, y), op='FEED', val=v, need='WHEAT', key=(x, y, 'FEED'), urg=t['consecutive_unfed'] >= 1 or hour >= P['FEED_URG_H']))
            feeds_needed += 1; feed_list.append((x, y))
        if not t['cared_today'] and later:
            cap_ok = t['yield_units'] + 1 + t.get('pending_care_bonus', 0) < A['held'] + 1
            v = P['CARE_K'] * pp * (1.0 if cap_ok else 0.3) if care_need else P['CARE_SLACK']
            tasks.append(dict(pos=(x, y), op='CARE', val=v, need=None, key=(x, y, 'CARE'), urg=hour >= P['CARE_URG_H'] and t['fed_today']))
        yu = t['yield_units']
        if yu > 0:
            v = yu * pp * P['HV_K']
            if tonight and yu + 1 + t.get('pending_care_bonus', 0) > A['held']:
                v += P['HV_OVF'] * (yu + 1 + t.get('pending_care_bonus', 0) - A['held']) * pp
            if day == 29: v = yu * pp + 50
            tasks.append(dict(pos=(x, y), op='HARVEST', val=v, need=None, key=(x, y, 'HARVEST')))
        if t['fertilizer_available'] and day <= 29:
            v = max(P['COL_MIN'], P['COL_K'] * fert_p)
            if day == 29 and step > 710: v = 0
            if v > 0: tasks.append(dict(pos=(x, y), op='COLLECT_FERTILIZER', val=v, need=None, key=(x, y, 'COL')))
    fert_tasks = 0
    s_short = (ctgt['STRAWBERRY'] - cnt_crop['STRAWBERRY']) - sum(1 for c_ in plan_crop.values() if c_ == 'STRAWBERRY')
    # cash the planned premium plantings need (reserved before animal purchases)
    seed_cash = sum(CROPS[c_]['seed'] for c_ in plan_crop.values() if c_ in ('STRAWBERRY', 'MELON', 'TOMATO')) if P['SEED_FIRST'] else 0.0
    seed_cash = max(0.0, seed_cash - sum(seeds.get(c_, 0) * CROPS[c_]['seed'] for c_ in ('STRAWBERRY', 'MELON', 'TOMATO')))
    for (x, y, t) in plants:
        c = t['crop']; C = CROPS[c]; pc = prices[c]; age = day - t['planted_day']; yu = t['yield_units']
        fert_on = t.get('fertilized_until_day', -1) >= day
        # value of the plant's remaining output
        if C['ongoing']:
            pn = plant_nights(c, t['planted_day'], day); rem = len(pn)
            pv = (rem * 1.2 + yu) * pc
            fut = (int(math.ceil((pn[-1] - day) / 2.0)) + rem) if pn else 0
        else:
            pv = max(yu, min(C['maxy'], yu + max(0, C['maxd'] - age + 1))) * pc - (0 if age >= C['first'] else 0)
            fut = int(math.ceil(max(0, C['maxd'] - age) / 2.0)) + 1
        keep = pv - P['LAM_F'] * fut        # value of keeping the plant alive net of the labour it still needs
        # WATER
        if not t['watered_today'] and day <= 29:
            must = t['consecutive_unwatered'] >= 1
            v = 0.0
            if not C['ongoing']:
                ws = (C['maxd'] + 1) // 2
                if ws <= age <= C['maxd'] and yu < C['maxy']:
                    v = min(C['maxy'] - yu, 2 if fert_on else 1) * pc
            else:
                if plant_nights(c, t['planted_day'], day, day) and fert_on: v = pc
            if must: v = max(v, max(P['MUST_MIN'], keep))
            if v <= 0: v = P['WATER_KEEP'] if day < 29 else 0.0
            if day == 29 and not (not C['ongoing'] and v > P['WATER_KEEP']): v = 0.0
            if v > 0: tasks.append(dict(pos=(x, y), op='WATER', val=v, need=None, key=(x, y, 'WATER'), urg=must and keep >= P['URG_PV']))
        # HARVEST
        if yu > 0 and age >= C['first']:
            ripe = False
            if C['ongoing']:
                ripe = True
            else:
                if yu >= C['maxy'] or age > C['maxd'] or (age == C['maxd'] and t['watered_today']) or day == 29:
                    ripe = True
                if step >= t.get('max_lifespan_step', 10 ** 9) - 1: ripe = True
                # nothing more to gain before the end
                if day >= 28 and (age >= C['maxd'] or t['watered_today']): ripe = True
                if c == 'WHEAT' and day <= P['EARLY_WH_LAST'] and yu >= 2 and s_short > 0: ripe = True
            if ripe:
                v = yu * pc * (P['HV_NO'] if not C['ongoing'] else P['HV_K']) + 10
                urg_h = False
                if not C['ongoing'] and step >= t.get('max_lifespan_step', 10 ** 9) - 3: urg_h = True
                if C['ongoing'] and plant_nights(c, t['planted_day'], day, day) and yu + (2 if fert_on else 1) > C['maxy']: urg_h = True
                if day == 29: v = yu * pc + 40; urg_h = True
                tasks.append(dict(pos=(x, y), op='HARVEST', val=v, need=None, key=(x, y, 'HARVEST'), urg=urg_h))
        # finished ongoing plant with nothing left -> DIG for replant
        if C['ongoing'] and yu == 0 and not plant_nights(c, t['planted_day'], day) and day <= P['W_LAST']:
            tasks.append(dict(pos=(x, y), op='DIG', val=P['DIG_V'], need=None, key=(x, y, 'DIG')))
        # FERTILIZE (engine gain x price - opportunity)
        if day <= 28 and not fert_on:
            gain = 0.0
            if not C['ongoing']:
                ws = (C['maxd'] + 1) // 2
                wl = [a_ for a_ in range(max(age, ws), C['maxd'] + 1) if not (a_ == age and t['watered_today'])]
                wf = [a_ for a_ in wl if a_ <= age + 2]
                g0 = min(C['maxy'], yu + len(wl)); g1 = min(C['maxy'], yu + len(wl) + len(wf))
                gain = (g1 - g0) * (0.8 if c != 'MELON' else 0.0)
            else:
                nw = len(plant_nights(c, t['planted_day'], day, min(day + 2, LAST_NIGHT)))
                if P['FERT2'] and nw < 2 and len(plant_nights(c, t['planted_day'], day)) > nw: nw = 0
                gain = 0.85 * nw
            v = gain * pc - P['FERT_OPP'] * fert_p
            if gain > 0 and v > 5:
                tasks.append(dict(pos=(x, y), op='FERTILIZE', val=v, need='FERTILIZER', key=(x, y, 'FERT')))
                fert_tasks += 1
    # PLANT / BUILD / DIG on free tiles (s_short computed before the plant loop)
    seed_left = dict(seeds); bud = budget
    for p, c in plan_crop.items():
        cost = CROPS[c]['seed']
        if seed_left.get(c, 0) > 0:
            seed_left[c] -= 1
        elif bud >= cost:
            bud -= cost
        else:
            continue
        rate = crop_rate(E, c, day)
        tasks.append(dict(pos=p, op='PLANT', arg=c, val=P['PLANT_V'] + max(0.0, min(150.0, 4.0 * rate)), need=None, key=(p[0], p[1], 'PLANT')))
    for p, k in build_plan.items():
        t = tiles[p[1]][p[0]]
        if t is None:
            tasks.append(dict(pos=p, op='BUILD_COOP' if k == 'COOP' else 'BUILD_PASTURE', val=P['BUILD_V'], need=None, key=(p[0], p[1], 'BUILD')))
        else:
            tasks.append(dict(pos=p, op='DIG', val=P['BUILD_V'] * 0.6, need=None, key=(p[0], p[1], 'DIG')))
    for p in weeds:
        if p in build_plan: continue
        if day <= P['W_LAST'] and hour <= 21:
            tasks.append(dict(pos=p, op='DIG', val=P['DIG_V'], need=None, key=(p[0], p[1], 'DIG')))
    # PLACE animals onto empty structures
    for k in ('COOP', 'PASTURE'):
        for p in empty_st[k]:
            tasks.append(dict(pos=p, op='PLACE', arg=k, val=P['PLACE_V'], need='ANIMAL:' + k, key=(p[0], p[1], 'PLACE'), urg=True))
    # planned structures being built this step can also be targeted next step; animals follow

    # ------------------------------------------------------------------ shed pseudo tasks
    # wheat in hand only covers feeds if the carrier is near an unfed animal (harvesters far away do not feed)
    carried_w = 0
    for u in range(nU):
        w_ = invs[u].get('WHEAT', 0)
        pk = S.get('tgt', {}).get(u)
        feeder = pk is not None and (pk[-1] == 'FEED' or pk[:2] == ('S', 'W'))
        if w_ > 0 and feed_list and (feeder or min(md(pos[u], q) for q in feed_list) <= P['FEED_R']):
            carried_w += min(w_, P['W_LOT'])
    carried_f = sum(iv.get('FERTILIZER', 0) for iv in invs)
    unc_feed = max(0, feeds_needed - carried_w)
    unc_fert = max(0, fert_tasks - carried_f)
    avg_feed = (sum(tk['val'] for tk in tasks if tk['op'] == 'FEED') / max(1, feeds_needed)) if feeds_needed else 0.0
    fts = [tk['val'] for tk in tasks if tk['op'] == 'FERTILIZE']
    avg_fert = sum(fts) / len(fts) if fts else 0.0
    shed_tasks = []
    n_urg_feed = max(0, sum(1 for tk in tasks if tk['op'] == 'FEED' and tk.get('urg')) - carried_w)
    if unc_feed > 0 and shed.get('WHEAT', 0) > 0:
        n = int(math.ceil(min(unc_feed, shed['WHEAT']) / float(P['W_LOT'])))
        for i in range(n):
            shed_tasks.append(dict(op='FETCH', arg='WHEAT', val=P['FETCH_K'] * avg_feed * min(P['W_LOT'], unc_feed), key=('S', 'W', i), urg=n_urg_feed > i * P['W_LOT']))
    if unc_fert > 0 and shed.get('FERTILIZER', 0) > 0:
        n = int(math.ceil(min(unc_fert, shed['FERTILIZER']) / float(P['F_LOT'])))
        for i in range(n):
            shed_tasks.append(dict(op='FETCH', arg='FERTILIZER', val=P['FETCH_K'] * avg_fert * min(P['F_LOT'], unc_fert), key=('S', 'F', i)))
    for a in ANIM:
        k = ANIM[a]['st']
        n = min(shed.get(a, 0), max(0, len(empty_st[k]) - in_hand_an_kind(invs, k)))
        for i in range(n):
            shed_tasks.append(dict(op='FETCH', arg=a, val=P['PLACE_V'] * 0.9, key=('S', a, i)))

    # ------------------------------------------------------------------ assignment
    # triage: admit the most valuable tile tasks that fit into the unit-steps left today, then global greedy on
    # min(value, VCAP) - LAM * distance (close to nearest-first inside the admitted set)
    cap_left = nU * (24 - hour) * P['ADMIT_K']
    order_v = sorted(range(len(tasks)), key=lambda i: -(tasks[i]['val'] + (1e4 if tasks[i].get('urg') else 0)))
    admitted = set(order_v[:max(nU, int(cap_left))])
    prev_t = S.get('tgt', {})
    anim_pos = {(x, y) for (x, y, t) in animals}
    pairs = []
    for u in range(nU):
        p = pos[u]; iv = invs[u]
        has_w = iv.get('WHEAT', 0) > 0; has_f = iv.get('FERTILIZER', 0) > 0
        an_kinds = {ANIM[a]['st'] for a in ANIM if iv.get(a, 0) > 0}
        carry_val = sum(iv.get(x, 0) * prices[x] for x in PREMIUM)
        if fert_p >= P['FERT_DELIV_P'] and fert_tasks == 0: carry_val += iv.get('FERTILIZER', 0) * fert_p
        for ti, tk in enumerate(tasks):
            if ti not in admitted and tk['pos'] != p: continue
            nd = tk['need']
            if nd == 'WHEAT' and not has_w: continue
            if nd == 'FERTILIZER' and not has_f: continue
            if nd and nd.startswith('ANIMAL:') and nd[7:] not in an_kinds: continue
            d = md(p, tk['pos'])
            if tk['val'] <= 0: continue
            sc = P['OFFSET'] + min(tk['val'], P['VCAP']) + (P['URG_B'] if tk.get('urg') else 0.0) - P['LAM'] * d
            if d == 0:
                sc += P['FINISH_B'] + (5.0 if tk['op'] == 'FERTILIZE' else 0.0)
                if tk['pos'] in anim_pos: sc += P['AFIN_B']
                elif tk['op'] in ('FERTILIZE', 'WATER', 'HARVEST'): sc += P['PFIN_B']
            if prev_t.get(u) == tk['key']: sc += P['STICK']
            if sc > 0: pairs.append((sc, u, ti))
        sd = shed_d(p)
        for si, tk in enumerate(shed_tasks):
            if tk['arg'] == 'WHEAT' and iv.get('WHEAT', 0) >= P['W_LOT']: continue
            if tk['arg'] in ANIM and an_kinds: continue
            sc = P['OFFSET'] + min(tk['val'], P['VCAP']) + (P['URG_B'] if tk.get('urg') else 0.0) - P['LAM'] * sd
            if prev_t.get(u) == tk['key']: sc += P['STICK']
            if sc > 0: pairs.append((sc, u, 1000 + si))
        # delivery of premium cargo to the shed (sell on arrival)
        endgame = day == 29
        if carry_val >= P['DROP_MIN'] or (endgame and carry_val + iv.get('WHEAT', 0) + iv.get('FERTILIZER', 0) > 0):
            v = carry_val * P['DROP_K'] + (carry_val + 500 if endgame and hour >= 14 else 0)
            if hour >= 21 and carry_val > 0: v += carry_val * 0.1
            sc = P['OFFSET'] + min(v, P['VCAP'] * (1 if not endgame else 10)) - P['LAM'] * sd
            if endgame and step + sd + 1 >= LAST_STEP - 1: sc += 100000
            if sc > 0: pairs.append((sc, u, 2000 + u))
    pairs.sort(key=lambda z: -z[0])
    assign = {}; used = set()
    for sc, u, ti in pairs:
        if u in assign or ti in used: continue
        assign[u] = ti; used.add(ti)
    # on-the-way: a unit heading to a tile task or the shed first does any unassigned admitted task lying on a shortest path
    if P['ONWAY']:
        by_pos = {}
        for ti in admitted:
            if ti in used: continue
            tk = tasks[ti]
            if tk['val'] < P['ONWAY_MIN']: continue
            by_pos.setdefault(tk['pos'], []).append(ti)
        for u in range(nU):
            ti = assign.get(u)
            if ti is None: continue
            p = pos[u]; iv = invs[u]
            if ti >= 1000: tgt = near_shed(p)
            else: tgt = tasks[ti]['pos']
            D = md(p, tgt)
            if D == 0: continue
            best = None; bd = 99
            for q, lst in by_pos.items():
                dq = md(p, q)
                if dq >= bd or dq + md(q, tgt) > D: continue
                for tj in lst:
                    if tj in used: continue
                    nd = tasks[tj]['need']
                    if nd == 'WHEAT' and iv.get('WHEAT', 0) <= 0: continue
                    if nd == 'FERTILIZER' and iv.get('FERTILIZER', 0) <= 0: continue
                    if nd and nd.startswith('ANIMAL:'): continue
                    if best is None or dq < bd or tasks[tj]['val'] > tasks[best]['val']:
                        best, bd = tj, dq
            if best is not None:
                used.add(best); assign[u] = best
                S.setdefault('onway', 0); S['onway'] += 1

    # a unit passing the shed with premium cargo drops it now (sell on arrival) unless it carries feed/animals it still needs
    if P['SHED_PASS_DROP']:
        for u in range(nU):
            if pos[u] not in SHED: continue
            ti = assign.get(u)
            if ti is not None and ti >= 1000: continue
            iv = invs[u]
            if any(iv.get(a, 0) for a in ANIM) or iv.get('WHEAT', 0) or iv.get('FERTILIZER', 0): continue
            cv = sum(iv.get(x, 0) * prices[x] for x in PREMIUM)
            if cv >= P['SPD_MIN']: assign[u] = 2000 + u
    # opportunistic wheat pickup: a unit standing at the shed with little wheat takes some while feeds are uncovered
    tot_w = sum(iv.get('WHEAT', 0) for iv in invs)
    spare = feeds_needed - tot_w
    for u in range(nU):
        if spare <= 0 or shed.get('WHEAT', 0) <= 0: break
        if pos[u] in SHED and invs[u].get('WHEAT', 0) < 2 and not any(invs[u].get(a, 0) for a in ANIM):
            ti = assign.get(u)
            if ti is not None and ti >= 1000: continue
            n = min(P['W_LOT'], spare)
            assign[u] = 3000 + n; spare -= n
    # ------------------------------------------------------------------ execute
    actions = [['PASS'] for _ in range(nU)]
    pshed = dict(shed)                 # predicted shed after unit actions (market runs after them)
    plant_cnt = {}
    new_tgt = {}
    endgame_rush = day == 29
    for u in range(nU):
        ti = assign.get(u)
        p = pos[u]; iv = invs[u]
        if ti is None:
            lg['idle'] += 1; continue
        if ti >= 3000:          # opportunistic pickup at the shed
            n = min(ti - 3000, pshed.get('WHEAT', 0))
            if n > 0: actions[u] = ['PICKUP', 'WHEAT', n]; pshed['WHEAT'] -= n; new_tgt[u] = ('S', 'W', 99)
            continue
        if ti >= 2000:          # deliver cargo
            new_tgt[u] = ('S', 'DROP', u)
            if p in SHED:
                has_anim = any(iv.get(a, 0) > 0 for a in ANIM)
                keep_w = iv.get('WHEAT', 0) > 0 and unc_feed > 0 and not endgame_rush
                keep_f = iv.get('FERTILIZER', 0) > 0 and fert_tasks > 0 and not endgame_rush
                if has_anim or keep_w or keep_f:
                    best = max((x for x in PREMIUM if iv.get(x, 0) > 0), key=lambda x: iv[x] * prices[x], default=None)
                    if best is None and endgame_rush:
                        best = next((x for x in PRODUCTS if iv.get(x, 0) > 0), None)
                    if best:
                        n = iv[best]; room = 100 - sum(pshed.values()); n = min(n, room)
                        if n > 0:
                            actions[u] = ['PLACE', best, n]; pshed[best] = pshed.get(best, 0) + n
                else:
                    room = 100 - sum(pshed.values())
                    for x, n in iv.items():
                        if n <= 0: continue
                        tk_ = min(n, room); room -= tk_
                        if tk_ > 0: pshed[x] = pshed.get(x, 0) + tk_
                    actions[u] = ['DROP']
            else:
                actions[u] = step_toward(p, near_shed(p), (u + step) % 2 == 1)
                mb = lg.setdefault('mv_by', {}); mb['DROP'] = mb.get('DROP', 0) + 1
            continue
        if ti >= 1000:
            tk = shed_tasks[ti - 1000]; new_tgt[u] = tk['key']
            if p in SHED:
                it = tk['arg']
                if it == 'WHEAT':
                    n = min(pshed.get('WHEAT', 0), max(1, min(P['W_LOT'], unc_feed)))
                    unc_feed -= n
                elif it == 'FERTILIZER':
                    n = min(pshed.get('FERTILIZER', 0), max(1, min(P['F_LOT'], unc_fert)))
                    unc_fert -= n
                else:
                    n = min(pshed.get(it, 0), 1)
                if n > 0:
                    actions[u] = ['PICKUP', it, n]; pshed[it] -= n
            else:
                actions[u] = step_toward(p, near_shed(p), (u + step) % 2 == 1)
                mb = lg.setdefault('mv_by', {}); mb['FETCH_' + str(tk['arg'])[:1]] = mb.get('FETCH_' + str(tk['arg'])[:1], 0) + 1
            continue
        tk = tasks[ti]; new_tgt[u] = tk['key']
        if p == tk['pos']:
            op = tk['op']
            if op == 'PLANT':
                c = tk['arg']
                if plant_cnt.get(c, 0) < seeds.get(c, 0):
                    plant_cnt[c] = plant_cnt.get(c, 0) + 1; actions[u] = ['PLANT', c]
                else:
                    actions[u] = ['PASS']; S.setdefault('wait_seed', {})[c] = S.get('wait_seed', {}).get(c, 0) + 1
            elif op == 'PLACE':
                k = tk['arg']
                a = next((a for a in ANIM if ANIM[a]['st'] == k and iv.get(a, 0) > 0), None)
                actions[u] = ['PLACE', a] if a else ['PASS']
            else:
                actions[u] = [op]
            lg['acts'][op] = lg['acts'].get(op, 0) + 1
        else:
            actions[u] = step_toward(p, tk['pos'], (u + step) % 2 == 1); lg['moves'] += 1
            mb = lg.setdefault('mv_by', {}); mb[tk['op']] = mb.get(tk['op'], 0) + 1
    # diag: re-targeting while en route (previous target not reached and still valid, unit now heads elsewhere)
    for u, k in new_tgt.items():
        pk = prev_t.get(u)
        if pk is not None and pk != k and isinstance(pk[0], int) and tuple(pos[u]) != (pk[0], pk[1]):
            lg['switch'] = lg.get('switch', 0) + 1
    S['tgt'] = new_tgt

    # ------------------------------------------------------------------ market
    # list = [sells (rival-exposure order)] + [land] + [hires] + [animals] + [seeds] + [feed wheat]; <= 10 orders.
    cash = money
    sold = {}; bought = {}
    walk = {}
    sells = []
    def sell(x, n):
        nonlocal cash
        n = int(min(n, pshed.get(x, 0)))
        if n <= 0: return
        i0 = inv.get(x, 10000) + walk.get(x, 0); rev = 0
        for j in range(n): rev += mprice(x, i0 + j)
        walk[x] = walk.get(x, 0) + n
        sells.append(['SELL', x, n]); cash += rev * 0.97; sold[x] = sold.get(x, 0) + n; pshed[x] -= n
    carried = sum(sum(v for v in iv.values()) for iv in invs)
    w_need = max(0, feeds_needed - carried_w - (shed.get('WHEAT', 0) - pshed.get('WHEAT', 0)))
    n_tomorrow = sum(1 for (x, y, t) in animals if anim_nights(t['animal'], t['placed_day'], day + 1))
    last_call = step >= LAST_STEP - 1 or (day == 29 and P['D29_SELL_ALL'])
    prem = [x for x in PREMIUM if pshed.get(x, 0) > 0]
    prem.sort(key=lambda x: -(rstock.get(x, 0) * prices[x] + 0.01 * prices[x] * pshed[x]))
    for x in prem:
        if prices[x] <= P['HOLD_FLOOR'] and not last_call and sum(pshed.values()) + carried < P['SHED_SAFE']:
            continue
        sell(x, pshed[x])
    keep_f = 0 if last_call else max(0, fert_tasks - carried_f)
    if not last_call and day <= 3 and P['SELL_FERT_EARLY']: keep_f = 0
    if pshed.get('FERTILIZER', 0) > keep_f and (prices['FERTILIZER'] > 1 or last_call):
        sell('FERTILIZER', pshed['FERTILIZER'] - keep_f)
    n_unplaced = sum(in_shed_an.values()) + sum(in_hand_an.values())
    keep_w = 0 if last_call else w_need + n_unplaced + (int(math.ceil(P['W_RES'] * n_tomorrow)) if hour >= P['W_RES_H'] else 0)
    if pshed.get('WHEAT', 0) > keep_w:
        sell('WHEAT', pshed['WHEAT'] - keep_w)
    if hour >= 20 and not last_call:
        over = sum(pshed.values()) + carried - P['SHED_SAFE']
        for x in ('WHEAT', 'FERTILIZER') + PREMIUM:
            if over <= 0: break
            n = min(over, pshed.get(x, 0))
            if n > 0: sell(x, n); over -= n
    # merge duplicate sells of one product
    ms = {}
    for o in sells: ms[o[1]] = ms.get(o[1], 0) + o[2]
    sells = [['SELL', x, ms[x]] for x in dict.fromkeys(o[1] for o in sells)]
    # hires (fib cost), 8 at h0 + rest at h1-h2
    if day <= 10: h_today = P['H_SCHED'][day]
    elif day == 29: h_today = P['H29']
    elif day == 28: h_today = P['H28']
    else:
        need_u = int(math.ceil(L_now / (P['EFF'] * P['STEPS_U']))) - 1
        h_today = max(P['H_LO'], min(P['H_MAX'], need_u))
    hired = int(me.get('hires_today', len(me['hands'])))
    if hour == 0: h_now = min(h_today, P['H_H0'])
    elif hour <= 2: h_now = h_today
    else: h_now = 0
    if day == 0 and hour == 0: h_now = h_today
    n_h = max(0, h_now - hired)
    land = []
    if land_due is not None and day <= 20 and L_now <= CAP_MAX * 1.2:
        land_cost = LAND_PRICES[land_due] + P['LAND_RES'][land_due]
        if cash >= land_cost:
            land = [['BUY_LAND']]; cash -= LAND_PRICES[land_due]
    # slots: keep hires and land; sells take what is left (at least 2)
    n_h = min(n_h, 10 - len(land) - min(2, len(sells)))
    sells = sells[:max(0, 10 - len(land) - n_h)]
    hires = []
    for j in range(n_h):
        c_ = fib(hired + j)
        if cash - c_ < 0: break
        hires.append(['HIRE']); cash -= c_; lg['hires'] += 1
    orders = sells + land + hires
    # wheat for feeding (just in time)
    w_short = w_need - pshed.get('WHEAT', 0)
    if day == 0 and hour == 0: w_short = max(w_short, 5)
    if w_short > 0 and not last_call and hour <= 22 and len(orders) < 10:
        n = min(w_short, int(max(0.0, cash) // max(1, wheat_p + 2)), 100 - sum(pshed.values()))
        if n > 0:
            orders.append(['BUY_PRODUCT', 'WHEAT', int(n)]); cash -= n * (wheat_p + 1); bought['WHEAT'] = n
    # seeds just in time: units about to plant (distance <= 1) + small wheat buffer
    need_seed = {}
    for u, ti in assign.items():
        if ti < 1000 and tasks[ti]['op'] == 'PLANT':
            c = tasks[ti]['arg']
            dd = md(pos[u], tasks[ti]['pos'])
            if dd <= 1 or (dd <= 2 and c == 'WHEAT'):
                need_seed[c] = need_seed.get(c, 0) + 1
    for c in ('MELON', 'STRAWBERRY', 'TOMATO', 'CARROT', 'WHEAT'):
        n = need_seed.get(c, 0) - (seeds.get(c, 0) - plant_cnt.get(c, 0))
        if c == 'WHEAT' and need_seed.get(c, 0) > 0 and day > 0: n += P['SEED_BUF_W']
        if n <= 0 or len(orders) >= 10: continue
        cost = CROPS[c]['seed']
        n = min(n, int(max(0.0, cash - reserve) // cost))
        if n > 0:
            orders.append(['BUY_SEED', c, int(n)]); cash -= n * cost
    # animals (herd plan)
    sh_an = sum(pshed.get(a, 0) for a in ANIM)
    for a in want_an:
        if len(orders) >= 10: break
        if sh_an >= P['BUY_AHEAD']: break
        k = ANIM[a]['st']
        slots = len(empty_st[k]) + sum(1 for (p, kk) in build_plan.items() if kk == k) - in_shed_an[a] - in_hand_an[a]
        n = min(htgt[a] - have[a], max(0, slots), P['BUY_AHEAD'] - sh_an)
        if day <= 1: n = min(htgt[a] - have[a], P['BUY_AHEAD'] - sh_an)
        if n <= 0: continue
        if L_now + P['A_L'] > CAP_MAX and day > 10: continue
        cost = ANIM[a]['cost']
        res_land = (LAND_PRICES[land_due] + P['LAND_RES'][land_due]) if land_due is not None and not land else 0
        n = min(n, int(max(0.0, cash - res_land - feed_res - seed_cash) // cost), 99 - sum(pshed.values()))
        if n > 0:
            orders.append(['BUY_ANIMAL', a, int(n)]); cash -= cost * n; sh_an += n
    orders = orders[:10]
    for x, n in sold.items(): lg['sold'][x] = lg['sold'].get(x, 0) + n
    S['prev'] = dict(step=step, inv=inv, sold={x: (n if prices[x] > 1 else 0) for x, n in sold.items()},
                     bought={x: n for x, n in bought.items() if x in PRODUCTS}, shops=shops, rt=[[(t.get('animal'), t.get('crop'), t.get('yield_units', 0), t.get('kind'), t.get('max_lifespan_step', -1)) if isinstance(t, dict) else t for t in r] for r in rv['tiles']])
    if hour == 12: lg['px'] = dict(prices)
    if hour in (6, 12, 18, 22):
        lg.setdefault('hx', {})[hour] = dict(unfed=feeds_needed, cw=sum(iv.get('WHEAT', 0) for iv in invs), cov=carried_w, sw=shed.get('WHEAT', 0),
                                             fetch=sum(1 for t_ in shed_tasks if t_['arg'] == 'WHEAT'), adm=len(admitted), ntask=len(tasks),
                                             feeders=sum(1 for u in range(nU) if assign.get(u) is not None and assign[u] < 1000 and tasks[assign[u]]['op'] == 'FEED'))
    if hour == 23:
        S['p23'] = {(x, y): (t['crop'], t['yield_units'], t['consecutive_unwatered'], t['watered_today']) for (x, y, t) in plants}
        S['a23'] = {(x, y): t['animal'] for (x, y, t) in animals}
    if hour == 0 and S.get('p23'):
        lost = 0; lostv = 0.0; esc = 0
        for (x, y), (c, yu_, cu_, w_) in S['p23'].items():
            t = tiles[y][x]
            if isinstance(t, dict) and t.get('kind') == 'WEED': lost += 1; lostv += prices[c] * max(1, yu_)
        for (x, y), a in S.get('a23', {}).items():
            t = tiles[y][x]
            if isinstance(t, dict) and not t.get('animal'): esc += 1
        lg['weeded'] = lost; lg['weeded_v'] = round(lostv); lg['escaped'] = esc
    if hour == 23:
        lg['h23'] = dict(anim=len(animals), fed=sum(t['fed_today'] for (_, _, t) in animals), cared=sum(t['cared_today'] for (_, _, t) in animals),
                         plants=len(plants), watered=sum(t['watered_today'] for (_, _, t) in plants), money=round(money),
                         crops={c: n for c, n in cnt_crop.items() if n}, herd=dict(herd), htgt=dict(htgt), quads=len(quads))
    return {'farmer': actions[0], 'hands': actions[1:], 'market': orders}


def in_hand_an_kind(invs, k):
    return sum(iv.get(a, 0) for iv in invs for a in ANIM if ANIM[a]['st'] == k)


def agent(obs, config=None):
    try:
        if int(obs['step']) == 0: reset()
        return act(obs)
    except Exception as ex:
        S['err'] = S.get('err', 0) + 1; S['last_err'] = repr(ex)
        try:
            import traceback; S['tb'] = traceback.format_exc()
        except Exception:
            pass
        return {'farmer': ['PASS'], 'hands': [], 'market': []}

P.update({'S14_0': 24.0, 'S_LAST': 16, 'EFF': 0.8})
