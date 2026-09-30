# ---------------------------------------------------------------- micro: day-plan routing optimiser (agents/micro)
# Pasted verbatim into circuit_micro.py (see build_micro.py) just before `def plan_day`. Stdlib only; uses circuit globals
# (P, S, SHED, dist, nearest_shed, nn_order, two_opt, Stop, fib, log, LAST_DAY, time).
#
# Problem: prize-collecting multi-vehicle routing on the 10x10 grid. Vehicles = the units lx1 already chose (farmer + hands) with
# lx1's step limits (budget + FILL slack). A "node" is a visit to one tile carrying a subset of that tile's original actions
# (tile_stop output, in engine execution order). Cost of a route = actions + one PICKUP step per distinct carried input
# (feed wheat / fertilizer / animal) + Manhattan path from the shed tile nearest the first node (+ walk back and DROP for
# return routes) -- exactly lx1's route_cost(exact=True) model. Objective, lexicographic: (sum of over-limit steps, -value of the
# actions actually executable, total steps). Constraints: per-route step limit, the day-end shed-overflow cap on carried produce of
# non-return routes (same target as lx1), intra-tile precedence (a PLANT/BUILD needs every DIG/HARVEST before it on the tile, any
# action after a PLANT/BUILD needs it, a planting's own WATER comes with it), tile-changing bundles stay with the unit that owns the
# tile's other actions. Moves: 2-opt + or-opt inside routes, relocate / swap stops between routes, insertion of missing work
# (merged into an existing visit of the tile when possible), ejection (move one stop elsewhere to make room), replacement (drop
# lower-value independent optional actions for a higher-value missing bundle). Starts from lx1's final routes and orders, so the
# result is never worse than lx1 in the plan's own objective; returns None (lx1 plan kept) when nothing improves or on error.

_HD = {}
def _hd(p):
    v = _HD.get(p)
    if v is None: v = _HD[p] = dist(p, nearest_shed(p))
    return v

_KEY_OP = {'FEED': 'WHEAT', 'FERTILIZE': 'FERTILIZER'}
_TILE_CHANGE = ('DIG', 'PLANT', 'BUILD_COOP', 'BUILD_PASTURE', 'PLACE')

class _MT:
    """per-tile metadata of the original (untrimmed) stop"""
    __slots__ = ('pos', 'O', 'n', 'op', 'arg', 'val', 'mand', 'key', 'load', 'req', 'dep', 'tc', 'wy')
    def __init__(self, O):
        self.pos = O.pos; self.O = O; self.wy = getattr(O, 'wy', 0) or 0; A = O.acts; n = self.n = len(A)
        self.op = [a[0] for a in A]; self.arg = [a[1] for a in A]; self.val = [float(a[2]) for a in A]; self.mand = [bool(a[3]) for a in A]
        ncol = sum(1 for o in self.op if o == 'COLLECT_FERTILIZER'); nh = sum(1 for o in self.op if o == 'HARVEST')
        hl = (O.load - ncol) if nh else 0
        self.key = []; self.load = []
        for i in range(n):
            o = self.op[i]
            k = _KEY_OP.get(o)
            if o == 'PLACE': k = self.arg[i]
            self.key.append(k)
            self.load.append(1 if o == 'COLLECT_FERTILIZER' else (hl if o == 'HARVEST' and nh == 1 else 0))
        req = [set() for _ in range(n)]
        for i in range(n):
            o = self.op[i]
            if o in ('PLANT', 'BUILD_COOP', 'BUILD_PASTURE'):
                for j in range(i):
                    if self.op[j] in ('DIG', 'HARVEST'): req[i].add(j)
            for j in range(i - 1, -1, -1):
                if self.op[j] in ('PLANT', 'BUILD_COOP', 'BUILD_PASTURE'): req[i].add(j); break
            for j in range(i):
                if self.op[j] == 'HARVEST' and self.arg[j] == 'DEFER': req[i].add(j)
        ch = True
        while ch:
            ch = False
            for i in range(n):
                add = set()
                for j in req[i]: add |= req[j]
                if not add <= req[i]: req[i] |= add; ch = True
        self.req = req
        self.dep = [set(k for k in range(n) if i in req[k]) for i in range(n)]
        # a set of actions is tile-changing when it contains a DIG/PLANT/BUILD/PLACE or an action other actions depend on
        self.tc = [self.op[i] in _TILE_CHANGE or bool(self.dep[i]) or bool(req[i]) for i in range(n)]

class _MN:
    """a visit: tile metadata + the set of original action indices executed there"""
    __slots__ = ('m', 'ids', 'src', 'dirty', 'pos', 'kc')
    def __init__(self, m, ids, src=None):
        self.m = m; self.ids = set(ids); self.src = src; self.dirty = src is None; self.pos = m.pos; self.kc = None
    def nacts(self): return len(self.ids)
    def keys(self):
        if self.kc is None:
            m = self.m; self.kc = tuple(set(m.key[i] for i in self.ids if m.key[i]))
        return self.kc
    def load(self):
        m = self.m; return sum(m.load[i] for i in self.ids)
    def stop(self):
        if not self.dirty and self.src is not None: return self.src
        m = self.m; O = m.O; st = Stop(m.pos)
        for i in sorted(self.ids): st.acts.append(list(O.acts[i]))
        for i in sorted(self.ids):
            o = m.op[i]
            if o == 'FEED': st.needs['WHEAT'] = 1
            elif o == 'FERTILIZE': st.needs['FERTILIZER'] = st.needs.get('FERTILIZER', 0) + 1
            elif o == 'PLANT': st.needs['SEED:' + str(m.arg[i])] = st.needs.get('SEED:' + str(m.arg[i]), 0) + 1
            elif o == 'PLACE': st.needs[m.arg[i]] = st.needs.get(m.arg[i], 0) + 1
            elif o == 'HARVEST':
                if m.arg[i] == 'AH': st.ahy = m.load[i]
                st.prem = O.prem; st.wy = m.wy
        st.load = self.load()
        return st

def _okeys(order):
    c = set()
    for n in order: c.update(n.keys())
    return c

def _path(order, ret):
    if not order: return 0
    d = _hd(order[0].pos); px, py = order[0].pos
    for n in order[1:]:
        x, y = n.pos; d += abs(x - px) + abs(y - py); px, py = x, y
    if ret: d += _hd(order[-1].pos) + 1
    return d

def _credit_free(order, key):
    """CREDIT (lx2/lx3 lineage): wheat harvested / fertilizer collected earlier on the route covers its later FEED / FERTILIZE,
    so the route needs no PICKUP of that input (same rule as the circuit's credit_short == 0)"""
    bal = 0; use = 'FEED' if key == 'WHEAT' else 'FERTILIZE'; mg = P['CREDIT_MARGIN']
    for n in order:
        m = n.m
        for i in sorted(n.ids):
            o = m.op[i]
            if o == use:
                bal -= 1
                if bal < 0: return False
            elif key == 'WHEAT' and o == 'HARVEST' and m.wy > 0: bal += max(0, m.wy - mg)
            elif key == 'FERTILIZER' and o == 'COLLECT_FERTILIZER': bal += 1
    return True

def _ocost(order, ret):
    if not order: return 0
    ks = _okeys(order)
    if P['CREDIT']:
        for k in ('WHEAT', 'FERTILIZER'):
            if k in ks and _credit_free(order, k): ks = ks - {k}
    return sum(n.nacts() for n in order) + len(ks) * P['PICKUP_COST'] + _path(order, ret)

def _ins_delta(order, p, ret):
    """cheapest path delta and position for inserting a node at tile p into order"""
    if not order: return _hd(p) + ((_hd(p) + 1) if ret else 0), 0
    best = None
    q0 = order[0].pos
    d = _hd(p) + dist(p, q0) - _hd(q0)
    best = (d, 0)
    for k in range(1, len(order)):
        a = order[k - 1].pos; b = order[k].pos
        d = dist(a, p) + dist(p, b) - dist(a, b)
        if d < best[0]: best = (d, k)
    a = order[-1].pos
    d = dist(a, p) + ((_hd(p) - _hd(a)) if ret else 0)
    if d < best[0]: best = (d, len(order))
    return best

def _improve_route(order, ret, ops):
    """2-opt + or-opt (segments of 1-3) on an explicit order, full cost recompute (routes are short)"""
    if len(order) < 2: return order
    best = _path(order, ret); improved = True; n = len(order)
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 1, n):
                ops[0] += 1
                cand = order[:i] + order[i:j + 1][::-1] + order[j + 1:]
                c = _path(cand, ret)
                if c < best: order, best, improved = cand, c, True
        for L in (1, 2, 3):
            for i in range(n - L + 1):
                seg = order[i:i + L]; rest = order[:i] + order[i + L:]
                for k in range(len(rest) + 1):
                    if k == i: continue
                    ops[0] += 1
                    for sg in (seg, seg[::-1]) if L > 1 else (seg,):
                        cand = rest[:k] + sg + rest[k:]
                        c = _path(cand, ret)
                        if c < best: order, best, improved = cand, c, True; break
                    if improved: break
                if improved: break
            if improved: break
    return order

def micro_opt(routes, budgets, ret_flags, dropped, stops, ctx, wall=None, final=True):
    t0 = time.perf_counter()
    # hard step cap: the whole agent step (lx1 planning + every micro stage) stays under OPT_STEP_CAP seconds
    left = ctx.get('t0', t0) + P['OPT_STEP_CAP'] - t0
    wall = min(P['OPT_WALL'] if wall is None else wall, left)
    if wall < 0.01:
        S['opt_obj'] = None; S['opt_stat'] = {'nowall': 1}; return None
    try:
        return _micro_opt(routes, budgets, ret_flags, dropped, stops, ctx, t0 + wall, final)
    except Exception as e:      # noqa  -- any failure keeps lx1's plan
        if P['DEBUG']:
            import traceback; log(f"OPT d{ctx['day']} EXC {e!r}\n{traceback.format_exc()}")
        S['opt_stat'] = {'exc': 1}
        return None

def _micro_opt(routes, budgets, ret_flags, dropped, stops, ctx, deadline, final):
    day = ctx['day']; U = len(routes); ops = [0]; OPS = P['OPT_OPS']; T0 = [time.perf_counter()]
    def out_of_time(): return ops[0] > OPS or time.perf_counter() > deadline
    lim = [budgets[u] + (min(P['FILL'], P['HAND_SLACK']) if u > 0 else 0) for u in range(U)]
    meta = {s.pos: _MT(s) for s in stops}
    # ---- initial solution: lx1's final routes in the order lx1's plan builder would produce
    R = []
    for u, r in enumerate(routes):
        if not r: R.append([]); continue
        end = None
        start = nearest_shed(r[0].pos); end = start if ret_flags[u] else None
        o2 = two_opt(nn_order(r, start, end), start, end)
        start = nearest_shed(o2[0].pos); end = start if ret_flags[u] else None
        o2 = two_opt(nn_order(r, start, end), start, end)
        R.append(o2)
    # align every routed stop to its tile's original actions (op match, arg for PLANT/PLACE, original order)
    claimed = {}
    NR = [[None] * len(R[u]) for u in range(U)]
    items = sorted(((u, k) for u in range(U) for k in range(len(R[u]))), key=lambda z: -len(R[z[0]][z[1]].acts))
    for u, k in items:
        s = R[u][k]; m = meta.get(s.pos)
        if m is None: return None
        cl = claimed.setdefault(s.pos, set()); ids = []; j = 0
        for a in s.acts:
            while j < m.n and (j in cl or m.op[j] != a[0] or (a[0] in ('PLANT', 'PLACE') and m.arg[j] != a[1])): j += 1
            if j >= m.n:
                # out-of-order single action (XFILL stop): first unclaimed match anywhere
                jj = next((q for q in range(m.n) if q not in cl and q not in ids and m.op[q] == a[0]), None)
                if jj is None: return None
                ids.append(jj); continue
            ids.append(j); j += 1
        cl.update(ids)
        NR[u][k] = _MN(m, ids, s)
    R = NR
    shed_keep = ctx.get('shed_keep', 0)
    cap = P['OVERFLOW_LATE'] if P['OVERFLOW_LATE'] > 0 and day >= LAST_DAY - 2 else P['OVERFLOW_TARGET']

    def present(pos):
        s = set()
        for u in range(U):
            for n in R[u]:
                if n.m.pos == pos: s |= n.ids
        return s

    def value_of(n, pres):
        m = n.m; v = 0.0
        for i in n.ids:
            if m.req[i] <= pres: v += m.val[i]
        return v

    def state_obj():
        over = 0; val = 0.0; cost = 0
        P_ = {}
        for u in range(U):
            for n in R[u]: P_.setdefault(n.m.pos, set()).update(n.ids)
        for u in range(U):
            c = _ocost(R[u], ret_flags[u]); cost += c; over += max(0, c - lim[u])
            for n in R[u]: val += value_of(n, P_[n.m.pos])
        return over, val, cost

    base = state_obj()
    nonret = [not f for f in ret_flags]
    def exp_total(): return shed_keep + sum(n.load() for u in range(U) if nonret[u] for n in R[u])
    load_room = [cap - exp_total()]
    cost = [_ocost(R[u], ret_flags[u]) for u in range(U)]
    changed = [False]
    stat = {'repair': 0, 'relocate': 0, 'swap': 0, 'insert': 0, 'insert_v': 0.0, 'eject': 0, 'replace': 0, 'intra': 0}

    # ---- repair: a planting / building whose tile-clearing prerequisite was trimmed cannot execute (lx1 plans its steps anyway)
    for u in range(U):
        for n in list(R[u]):
            m = n.m; pres = present(m.pos)
            bad = set(i for i in n.ids if not m.req[i] <= pres)
            if bad:
                n.ids -= bad; n.dirty = True; n.kc = None; changed[0] = True; stat['repair'] += len(bad)
                if not n.ids: R[u].remove(n)
    cost = [_ocost(R[u], ret_flags[u]) for u in range(U)]

    # ---- intra-route sequencing
    def intra(u):
        if len(R[u]) < 2: return
        c0 = _path(R[u], ret_flags[u]); o = _improve_route(list(R[u]), ret_flags[u], ops)
        if _path(o, ret_flags[u]) < c0: R[u] = o; cost[u] = _ocost(o, ret_flags[u]); changed[0] = True; stat['intra'] += 1
    for u in range(U): intra(u)

    # ---- inter-route relocate / swap: total steps down, no route pushed over its limit (or further over)
    def fits(u, c): return c <= lim[u] or c <= cost[u]
    def relocate_pass():
        moved = False
        for u in range(U):
            for n in list(R[u]):
                if out_of_time(): return moved
                if n not in R[u]: continue
                a = [x for x in R[u] if x is not n]; ca = _ocost(a, ret_flags[u])
                if nonret[u] == False: pass
                best = None
                for v in range(U):
                    if v == u: continue
                    if n.load() and nonret[v] and not nonret[u] and n.load() > load_room[0]: continue
                    d, k = _ins_delta(R[v], n.pos, ret_flags[v]); ops[0] += 1
                    b = R[v][:k] + [n] + R[v][k:]
                    cb = _ocost(b, ret_flags[v])
                    if cb > lim[v]: continue
                    gain = (cost[u] + cost[v]) - (ca + cb)
                    over_b = max(0, cost[u] - lim[u]) + max(0, cost[v] - lim[v]); over_a = max(0, ca - lim[u]) + max(0, cb - lim[v])
                    if over_a > over_b or (over_a == over_b and gain <= 0): continue
                    key = (over_a - over_b, -gain)
                    if best is None or key < best[0]: best = (key, v, b, cb)
                if best:
                    _, v, b, cb = best
                    if nonret[v] != nonret[u]: load_room[0] += (n.load() if nonret[u] else -n.load())
                    R[u] = a; R[v] = b; cost[u] = ca; cost[v] = cb; moved = True; changed[0] = True; stat['relocate'] += 1
        return moved
    def swap_pass():
        moved = False
        for u in range(U):
            for v in range(u + 1, U):
                if out_of_time(): return moved
                if nonret[u] != nonret[v]: continue
                for i in range(len(R[u])):
                    for j in range(len(R[v])):
                        ops[0] += 1
                        a = R[u][:i] + [R[v][j]] + R[u][i + 1:]; b = R[v][:j] + [R[u][i]] + R[v][j + 1:]
                        ca = _ocost(a, ret_flags[u]); cb = _ocost(b, ret_flags[v])
                        if ca > lim[u] and ca > cost[u]: continue
                        if cb > lim[v] and cb > cost[v]: continue
                        over_b = max(0, cost[u] - lim[u]) + max(0, cost[v] - lim[v]); over_a = max(0, ca - lim[u]) + max(0, cb - lim[v])
                        if over_a < over_b or (over_a == over_b and ca + cb < cost[u] + cost[v]):
                            R[u] = a; R[v] = b; cost[u] = ca; cost[v] = cb; moved = True; changed[0] = True; stat['swap'] += 1
                            break
                    else: continue
                    break
        return moved

    # ---- missing work: candidate bundles per tile
    def bundles(m, pres):
        out = []
        miss = [i for i in range(m.n) if i not in pres]
        for i in miss:
            if m.mand[i] and not m.req[i]: pass        # a mandatory action outside every route (over-limit day): candidate too
            if m.val[i] < P['OPT_MIN_V'] and not m.mand[i]: continue
            B = {i} | (m.req[i] - pres)
            # mandatory dependants that become executable with B (a new planting's WATER)
            for k in miss:
                if k not in B and m.mand[k] and m.req[k] and m.req[k] <= (pres | B) and (m.req[k] & B): B.add(k)
            if any(not (m.req[j] <= (pres | B)) for j in B): continue
            v = sum(m.val[j] for j in B)
            if v < P['OPT_MIN_V']: continue
            out.append((v, frozenset(B)))
        seen = set(); res = []
        for v, B in sorted(out, key=lambda z: -z[0]):
            if B in seen: continue
            seen.add(B); res.append((v, B))
        return res

    def try_insert(m, B, v, commit=True, only=None):
        """best feasible insertion of bundle B at tile m.pos; returns (dcost, u, how) or None"""
        tc = any(m.tc[j] for j in B)
        nodes = [(u, n) for u in range(U) for n in R[u] if n.m is m]
        if tc and len(nodes) > 1: return None
        bl = sum(m.load[j] for j in B); bkeys = set(m.key[j] for j in B if m.key[j])
        best = None
        for u in (range(U) if only is None else only):
            if nonret[u] and bl > load_room[0]: continue
            rk = _okeys(R[u])
            nk = sum(1 for k in bkeys if k not in rk) * P['PICKUP_COST']
            own = next((n for uu, n in nodes if uu == u), None)
            if tc and nodes and own is None: continue
            if own is not None: dc = len(B) + nk; how = ('merge', own)
            else:
                d, k = _ins_delta(R[u], m.pos, ret_flags[u]); dc = len(B) + nk + d; how = ('new', k)
            ops[0] += 1
            if cost[u] + dc > lim[u]: continue
            if best is None or dc < best[0]: best = (dc, u, how)
        if best and commit:
            dc, u, how = best
            if how[0] == 'merge':
                old = (set(how[1].ids), how[1].dirty); how[1].ids |= set(B); how[1].dirty = True; how[1].kc = None
            else: R[u].insert(how[1], _MN(m, B))
            c2 = _ocost(R[u], ret_flags[u])
            if c2 > lim[u]:
                # exact cost (pickups / CREDIT) above the estimate: undo
                if how[0] == 'merge': how[1].ids, how[1].dirty = old; how[1].kc = None
                else: R[u].pop(how[1])
                return None
            cost[u] = c2
            if nonret[u]: load_room[0] -= bl
            changed[0] = True
        return best

    def all_cands():
        C = []
        for pos, m in meta.items():
            pres = present(pos)
            for v, B in bundles(m, pres): C.append((v, m, B))
        C.sort(key=lambda z: (-z[0], z[1].pos))
        return C

    def insert_pass():
        any_ins = False
        while not out_of_time():
            C = all_cands(); done = False
            for v, m, B in C:
                if out_of_time(): break
                r = try_insert(m, B, v)
                if r:
                    stat['insert'] += 1; stat['insert_v'] += v; any_ins = done = True; intra(r[1]); break
            if not done: break
        return any_ins

    def eject_pass():
        """a bundle that fits nowhere: move one stop of a nearly-fitting route to another route with room, then insert"""
        for v_, m, B in all_cands():
            if out_of_time(): return False
            tc = any(m.tc[j] for j in B)
            nodes = [(u, n) for u in range(U) for n in R[u] if n.m is m]
            if tc and len(nodes) > 1: continue
            for u in range(U):
                if tc and nodes and nodes[0][0] != u: continue
                for n in list(R[u]):
                    if n.m is m: continue
                    a = [x for x in R[u] if x is not n]; ca = _ocost(a, ret_flags[u])
                    for w in range(U):
                        if w == u or nonret[w] != nonret[u]: continue
                        d, k = _ins_delta(R[w], n.pos, ret_flags[w]); ops[0] += 1
                        b = R[w][:k] + [n] + R[w][k:]; cb = _ocost(b, ret_flags[w])
                        if cb > lim[w]: continue
                        sv = (list(R[u]), list(R[w]), cost[u], cost[w])
                        R[u] = a; R[w] = b; cost[u] = ca; cost[w] = cb
                        r = try_insert(m, B, v_, only=[u])
                        if r:
                            stat['eject'] += 1; stat['insert_v'] += v_; changed[0] = True; intra(u); intra(w); return True
                        R[u], R[w], cost[u], cost[w] = sv
        return False

    def replace_pass():
        """drop lower-value independent optional actions from a route to make room for a higher-value missing bundle"""
        for v_, m, B in all_cands():
            if out_of_time(): return False
            tc = any(m.tc[j] for j in B)
            nodes = [(u, n) for u in range(U) for n in R[u] if n.m is m]
            if tc and len(nodes) > 1: continue
            for u in range(U):
                if tc and nodes and nodes[0][0] != u: continue
                r = try_insert(m, B, v_, commit=False, only=[u])
                if r: continue
                own = next((n for uu, n in nodes if uu == u), None)
                if own is not None: need = len(B) + sum(1 for k in set(m.key[j] for j in B if m.key[j]) if k not in _okeys(R[u]))
                else: need = len(B) + 1 + _ins_delta(R[u], m.pos, ret_flags[u])[0]
                need = cost[u] + need - lim[u]
                if need <= 0 or need > 4: continue
                # removable: optional, independent (no dependants present, not tile-changing), cheapest value first
                rem = []
                for n in R[u]:
                    mm = n.m
                    for i in n.ids:
                        if mm.mand[i] or mm.tc[i] or (n.m is m): continue
                        rem.append((mm.val[i], n, i))
                rem.sort(key=lambda z: z[0])
                take = []; tv = 0.0
                for val, n, i in rem:
                    if len(take) >= need: break
                    take.append((n, i)); tv += val
                if len(take) < need or tv >= v_ * 0.999: continue
                sv = ([(n, set(n.ids), n.dirty) for n in R[u]], list(R[u]), cost[u], load_room[0])
                for n, i in take:
                    n.ids.discard(i); n.dirty = True; n.kc = None
                    if nonret[u]: load_room[0] += n.m.load[i]
                R[u] = [n for n in R[u] if n.ids]
                cost[u] = _ocost(R[u], ret_flags[u])
                r = try_insert(m, B, v_, only=[u])
                if r:
                    stat['replace'] += 1; stat['insert_v'] += v_ - tv; changed[0] = True; intra(u); return True
                for n, ids, dt in sv[0]: n.ids = ids; n.dirty = dt; n.kc = None
                R[u] = sv[1]; cost[u] = sv[2]; load_room[0] = sv[3]
        return False

    # ---- anytime loop
    S['opt_obj'] = base
    if not all_cands() and not changed[0]:
        S['opt_stat'] = {'skip': 1}; return None
    for _round in range(6):
        if out_of_time(): break
        c = insert_pass()
        a = relocate_pass() if not out_of_time() else False
        if a: insert_pass()
        d = P['OPT_EJECT'] and not out_of_time() and eject_pass()
        e = P['OPT_REPLACE'] and not out_of_time() and replace_pass()
        if d or e: insert_pass()
        b = swap_pass() if not out_of_time() and P['OPT_SWAP'] else False
        if not (a or b or c or d or e): break
    new = state_obj()
    stat.update(base=base, new=new, ops=ops[0], sec=round(time.perf_counter() - T0[0], 4))
    S['opt_stat'] = stat
    better = (new[0] < base[0]) or (new[0] == base[0] and (new[1] > base[1] + 1e-6 or (abs(new[1] - base[1]) <= 1e-6 and new[2] < base[2])))
    if P['DEBUG']: log(f"OPT d{day} base {base} new {new} better {better} {stat}")
    S['opt_obj'] = new if (better and changed[0]) else base
    if not better or not changed[0] or not final: return None
    # ---- materialise
    new_routes = []; orders = []
    for u in range(U):
        o = [n.stop() for n in R[u]]
        new_routes.append(o); orders.append(list(o) if o else None)
    nd = []
    for pos, m in meta.items():
        pres = present(pos)
        for i in range(m.n):
            if i not in pres and not m.mand[i]: nd.append((pos, 'DEFER' if m.arg[i] == 'DEFER' else m.op[i], m.val[i]))
    return new_routes, nd, orders, new

# ---------------------------------------------------------------- micro v2: OPT_LATE end-of-day filler (live farm state)
def _late_care_ok(t, day):
    """a CARE today banks a bonus only if the next production (after tonight's) lands by the last day with cap room"""
    a = ANIMALS[t['animal']]; prod = t['placed_day'] + a['first']
    while prod <= day + 1: prod += a['interval']
    bonus = t.get('pending_care_bonus', 0); tonight = day + 1 - t['placed_day'] - a['first']
    if tonight >= 0 and tonight % a['interval'] == 0: bonus = 0
    other = max(0, prod - day - 2)
    return prod <= LAST_DAY and 1 + bonus + other < a['max_held']

def _late_jobs(ctx):
    """value-positive actions available now on the live farm, per tile: (pos, [(op, value, load)])
    animals: CARE (fed today, not cared, bonus can still pay; value = the planner's own tile_stop value, which in V183 mode is
    the dated gate's care value), COLLECT_FERTILIZER, deferrable animal HARVEST; plants: WATER on a watering that pays (window
    crop in window, ongoing crop's production night, weed risk), ongoing-crop HARVEST. Never FEED (no wheat leaves the shed)."""
    day = ctx['day']; pr = ctx['prices']; out = []
    for y, row in enumerate(ctx['tiles']):
        for x, t in enumerate(row):
            if not isinstance(t, dict): continue
            acts = []
            if t.get('animal') in ANIMALS:
                a = ANIMALS[t['animal']]; prod = a['product']
                if t.get('fed_today') and not t.get('cared_today') and _late_care_ok(t, day):
                    v = pr[prod] * P['CARE_W']
                    try:
                        st = tile_stop(x, y, t, ctx)        # the planner's valuation (V183: dated-gate care value)
                        cv = [b[2] for b in (st.acts if st else []) if b[0] == 'CARE']
                        v = cv[0] if cv else 0.0
                    except Exception: v = 0.0
                    if v > 0: acts.append(('CARE', v, 0))
                if t.get('fertilizer_available') and pr['FERTILIZER'] >= P['COLLECT_MIN_PRICE']: acts.append(('COLLECT_FERTILIZER', float(pr['FERTILIZER']), 1))
                yu = t.get('yield_units', 0)
                if yu > 0: acts.append(('HARVEST', P['AH_V'] * yu * pr[prod], yu))
            elif t.get('kind') == 'PLANT':
                crop = t['crop']; cd = CROPS[crop]; age = day - t['planted_day']; cu = t.get('consecutive_unwatered', 0)
                if not t.get('watered_today'):
                    if cd['ongoing']:
                        k = day + 1 - t['planted_day'] - cd['first']
                        pays = k >= 0 and k % cd['interval'] == 0 and (k // cd['interval'] + 1) <= cd['max_yield']
                    else:
                        ws = (cd['maxday'] + 1) // 2
                        pays = ws <= age <= cd['maxday'] and t.get('yield_units', 0) < cd['max_yield']
                    v = (pr[crop] if pays else 0.0) + (250.0 if cu >= 1 else 0.0)
                    if v > 0: acts.append(('WATER', v, 0))
                if cd['ongoing'] and t.get('yield_units', 0) > 0 and age >= cd['first']:
                    acts.append(('HARVEST', P['LATE_HARVEST_W'] * t['yield_units'] * pr[crop], t['yield_units']))
            acts = [z for z in acts if z[1] >= P['OPT_LATE_MIN']]
            if acts: out.append(((x, y), acts))
    return out

def late_assign(plans, positions, invs, ctx, hours_left, n_units, only=None):
    """micro OPT_LATE: every unit with nothing left to do (no plan / plan done / helped / pool empty) takes the best value-per-step
    job from the live farm it can finish today; chained naturally (the unit rescans when the job is done)."""
    idle = []
    for ui in (range(n_units) if only is None else only):
        p = plans.get(ui)
        if p is not None and p['phase'] != 'done': continue
        inv = invs[ui] if ui < len(invs) else {}
        pos = positions[ui]
        if sum(v for v in inv.values() if v > 0) >= 1 and P['HOME_IDLE'] and not (p and p.get('dropped')) and dist(pos, nearest_shed(pos)) + 1 <= hours_left:
            continue   # home-drop first while it can still reach the shed (goods dropped by h22 sell today)
        idle.append(ui)
    if not idle or hours_left < 1: return
    jobs = S.get('late_cache')
    if not jobs or jobs[0] != ctx['step']: jobs = S['late_cache'] = (ctx['step'], _late_jobs(ctx))
    jobs = jobs[1]
    if not jobs: return
    claimed = set()
    for p in plans.values():
        if p is not None and p['phase'] != 'done':
            for st in p['stops'][p['idx']:]: claimed.add(st.pos)
    shed_used = sum(v for v in ctx['priv']['shed'].values() if v > 0) + sum(sum(v for v in inv.values() if v > 0) for inv in invs)
    shed_used += sum(st.load for p in plans.values() if p is not None and p['phase'] != 'done' and not p.get('ret') for st in p['stops'][p['idx']:])
    room = [P['OVERFLOW_TARGET'] - 4 - shed_used]
    for ui in idle:
        pos = positions[ui]; best = None
        for tp, acts in jobs:
            if tp in claimed: continue
            d = dist(pos, tp)
            A = [z for z in acts if z[2] == 0 or z[2] <= room[0]]
            if not A: continue
            n = len(A)
            if d + n > hours_left: continue
            v = sum(z[1] for z in A); key = v / (d + n)
            if best is None or key > best[0]: best = (key, tp, A, v)
        if best:
            _, tp, A, v = best
            st = Stop(tp)
            for op, val, ld in sorted(A, key=lambda z: {'WATER': 0, 'CARE': 1, 'COLLECT_FERTILIZER': 2, 'HARVEST': 3}[z[0]]):
                st.add(op, None, val, False); st.load += ld
            room[0] -= st.load; claimed.add(tp)
            plans[ui] = {'stops': [st], 'needs': {}, 'loaded': {}, 'ret': False, 'idx': 0, 'budget': 0, 'phase': 'work', 'unit': ui,
                         'late': True, 'start': tuple(pos)}
            S['late_n'] = S.get('late_n', 0) + 1; S['late_v'] = S.get('late_v', 0.0) + v
            if P['DEBUG']: log(f"LATE d{ctx['day']} h{ctx['hour']} u{ui} {tuple(pos)} -> {tp} {[z[0] for z in A]} v {v:.0f}")

def late_redispatch(ui, p, pos, inv, plans, positions, invs, ctx, seeds_left, hours_left, n_units):
    """micro v2: the step a plan ends (exec_unit returned PASS on its last stop) is not wasted: home-drop if carrying and the
    shed is reachable, else a live-farm job taken and started in the same step"""
    if sum(v for v in inv.values() if v > 0) >= 1 and P['HOME_IDLE'] and not p.get('dropped') and dist(pos, nearest_shed(pos)) + 1 <= hours_left:
        if tuple(pos) in SHED: p['dropped'] = True; return ['DROP']
        return step_toward(pos, nearest_shed(pos))
    late_assign(plans, positions, invs, ctx, hours_left, n_units, only=[ui])
    q = plans.get(ui)
    if q is not None and q is not p and q.get('late'):
        return exec_unit(q, pos, inv, ctx, seeds_left, hours_left)
    return None
