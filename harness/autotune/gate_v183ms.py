"""Dated relative value of the next usable animal care bonus.

Public-state economic approximation, adapted from Codex V144's forecast model.
No future observations, identity features or fixture-specific action rules.
"""
import time


def install(C, action):
    raw_plan = C.plan_day
    raw_tile = C.tile_stop
    raw_gate = C.mv_marginal
    current = {}
    cache = {}
    C.INVEST_LOG = []

    def price(product, inventory):
        base, scale, low, low_w, high, high_w = C.MP[product]
        delta = inventory - 10000.0
        if delta < 0:
            return base + low_w*base*C.shape(low, -delta, scale)/C.shape(low, scale, scale)
        return max(1.0, base - high_w*base*C.shape(high, delta, scale)/C.shape(high, scale, scale))

    def supply(tiles, day):
        out = {p: [0.0]*(C.LAST_DAY+1-day) for p in C.PRODUCTS}

        def add(p, when, units):
            if day <= when <= C.LAST_DAY:
                out[p][when-day] += units

        for row in tiles:
            for t in row:
                if not isinstance(t, dict):
                    continue
                if t.get('animal') in C.ANIMALS:
                    a = C.ANIMALS[t['animal']]
                    p = a['product']
                    add(p, min(C.LAST_DAY, day+1), t.get('yield_units', 0))
                    bonus = t.get('pending_care_bonus', 0)
                    for night in range(day, C.LAST_DAY):
                        age = night + 1 - t['placed_day']
                        if age >= a['first'] and (age-a['first']) % a['interval'] == 0:
                            add(p, min(C.LAST_DAY, night+2), min(a['max_held'], 1+bonus))
                            bonus = 0
                        bonus += 1
                elif t.get('crop') in C.CROPS:
                    p = t['crop']
                    cd = C.CROPS[p]
                    add(p, min(C.LAST_DAY, day+1), t.get('yield_units', 0))
                    if cd['ongoing']:
                        for j in range(cd['max_yield']):
                            production = t['planted_day']+cd['first']+j*cd['interval']
                            if day < production <= C.LAST_DAY:
                                add(p, min(C.LAST_DAY, production+1), 2)
        return out

    def scenarios(shops, day, product):
        dates = [d for d in range(3, 25, 3) if d > day][:max(0, 8-len(shops))]
        types = [s for s in C.SHOPS if product in C.SHOPS[s]]
        prob = len(types)/8.0
        unit = 12.0 if types and all(len(C.SHOPS[s]) == 1 for s in types) else 6.0
        base = 1.0 + sum(12.0 if len(C.SHOPS[s]) == 1 else 6.0
                         for s in shops if product in C.SHOPS[s])
        if not types:
            return [(1.0, [base]*(C.LAST_DAY+1-day))]
        out = []
        for mask in range(1 << len(dates)):
            k = mask.bit_count()
            weight = prob**k*(1-prob)**(len(dates)-k)
            demand = [base+unit*sum(bool(mask & (1 << j)) and d <= when
                                    for j, d in enumerate(dates))
                      for when in range(day, C.LAST_DAY+1)]
            out.append((weight, demand))
        return out

    def prepare(ctx):
        day = ctx['day']
        cache.clear()
        cache['day'] = day
        own = supply(ctx['tiles'], day)
        opponent = supply(ctx['opp_tiles'], day)
        values = {}
        for product in ('STRAWBERRY', 'TOMATO', 'MILK', 'WOOL', 'EGG'):
            u, v = own[product], opponent[product]
            u[0] += ctx['shed'].get(product, 0)
            n = len(u)
            value = [0.0]*n
            for probability, demand in scenarios(ctx['shops'], day, product):
                inv = float(ctx['inv'][product])
                prices, slopes = [], []
                for i in range(n):
                    mid = inv + .5*(u[i]+v[i]) - .5*demand[i]
                    prices.append(price(product, mid))
                    slopes.append((price(product, mid+1)-price(product, mid-1))/2)
                    inv += u[i]+v[i]-demand[i]
                future = 0.0
                for i in range(n-1, -1, -1):
                    net = u[i]-v[i]
                    value[i] += probability*(prices[i]+.5*net*slopes[i]+future)
                    future += net*slopes[i]
            values[product] = value
        cache['values'] = values
        record = dict(day=day, action=action, values=values, changes=[], model_seconds=0.0)
        cache['record'] = record
        C.INVEST_LOG.append(record)

    def care_value(t, ctx):
        animal = C.ANIMALS[t['animal']]
        product = animal['product']
        day = ctx['day']
        production = t['placed_day']+animal['first']
        # Today's CARE is banked after tonight's production.
        while production <= day+1:
            production += animal['interval']
        bonus = t.get('pending_care_bonus', 0)
        tonight = day+1-t['placed_day']-animal['first']
        if tonight >= 0 and tonight % animal['interval'] == 0:
            bonus = 0
        other_cares = max(0, production-day-2)
        room = 1+bonus+other_cares < animal['max_held']
        if not room or production > C.LAST_DAY:
            return 0.0, production, None
        sale = min(C.LAST_DAY, production+1)
        return cache['values'][product][sale-day], production, sale

    def plan(ctx):
        start = time.perf_counter()
        prepare(ctx)
        elapsed = time.perf_counter()-start
        cache['record']['model_seconds'] = elapsed
        ctx['t0'] += elapsed
        return raw_plan(ctx)

    def gate(product, kind, ctx):
        old = raw_gate(product, kind, ctx)
        t = current.get('tile')
        if cache.get('day') != ctx['day'] or not isinstance(t, dict) or t.get('animal') != kind:
            C.GATE_FALLBACKS = getattr(C, 'GATE_FALLBACKS', 0)+1
            return old
        value, production, sale = care_value(t, ctx)
        threshold = ctx['prices']['WHEAT']+C.P['MV_LAB']
        cache['record']['changes'].append(dict(pos=list(current['pos']), kind=kind, product=product,
            old=old, new=value, production=production, sale=sale, threshold=threshold,
            old_skip=old<threshold, new_skip=value<threshold, applied=action != 'audit'))
        return old if action == 'audit' else value

    def tile(x, y, t, ctx):
        previous = dict(current)
        current.update(tile=t, pos=(x,y))
        try:
            stop = raw_tile(x,y,t,ctx)
        finally:
            current.clear(); current.update(previous)
        if action == 'dated_joint' and stop is not None and isinstance(t,dict) and t.get('animal') in C.ANIMALS and cache.get('day') == ctx['day']:
            value, production, sale = care_value(t, ctx)
            for a in stop.acts:
                if a[0] == 'CARE' and not a[3]:
                    a[2] = max(0.0, value*C.P['CARE_W'])
        return stop

    C.plan_day = plan
    C.tile_stop = tile
    C.mv_marginal = gate
