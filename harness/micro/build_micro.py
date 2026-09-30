"""agents/micro build: python build_micro.py

1. circuit_micro.py = lx1's embedded circuit (_lx1_embedded_circuit.py, extracted from lateexec/build/lx1/main.py) + mechanical
   patches (PATCHES below: P defaults, micro_opt.py pasted before `def plan_day`, three hooks inside `_plan_day`).
   Every new flag defaults off -> flag-off circuit behaves exactly like lx1's.
2. build/<tag>/main.py = lx1's main.py with _CIRC_B64 replaced by circuit_micro.py and XC_P extended by the tag's flags:
     m0     : no new flag (parity build, must equal lx1)
     mr     : OPT_ROUTE + OPT_ASSIGN (routing optimiser + time-matched plan assignment; hire count = lx1's)
     mro    : OPT_ROUTE only;  ma : OPT_ASSIGN only (component checks)
     mrh    : OPT_ROUTE + OPT_HIRE (optimiser also picks the hire count by marginal routed value vs wage)
"""
import os, re, json, zlib, base64, hashlib, sys
D = os.path.dirname(os.path.abspath(__file__))
LX1 = os.path.join(D, '..', 'lateexec', 'build', 'lx1', 'main.py')

DEFAULTS = ("'OPT_ROUTE': False, 'OPT_WALL': 0.2, 'OPT_OPS': 20000, 'OPT_MIN_V': 1.0, 'OPT_EJECT': True, 'OPT_REPLACE': True, 'OPT_SWAP': True, "
            "'OPT_ASSIGN': False, 'OPT_STEP_CAP': 0.5, 'OPT_LATE': False, 'OPT_LATE_MIN': 5.0, 'OPT_HIRE': False, 'OPT_HIRE_W': 1.0, 'OPT_HIRE_WALL': 0.05, 'OPT_HIRE_OPS': 4000, 'OPT_HIRE_MAX': 2,")

HIRE_HOOK = '''    over, dval, hands, routes, dropped, budgets, ret_flags, loops = best_plan
    if P['OPT_HIRE'] and day < LAST_DAY and not loops and not ctx.get('replan'):
        # micro OPT_HIRE: the routing optimiser values each hand count (routed value of the executable actions); one more hand
        # while the value it adds exceeds its wage (fib), one fewer while the value lost stays under the wage saved
        h_lx1 = hands; hsave = (B['ops'], B['hit'], B['deadline'])
        try:
            def _ev(pl):
                micro_opt(pl[3], pl[5], pl[6], pl[4], stops, ctx, wall=P['OPT_HIRE_WALL'], final=False)
                if S.get('opt_obj') is None: raise RuntimeError('no time')
                return S['opt_obj']
            cur = (hands, best_plan, _ev(best_plan))
            hmin = P['HANDS_MIN'] if day < LAST_DAY - 1 else max(P['HIRE_DOWN_MIN'], 3)
            for direction in (1, -1):
                moved = False
                for _k in range(P['OPT_HIRE_MAX']):
                    h2 = cur[0] + direction
                    if h2 > hmax or h2 < hmin: break
                    if time.perf_counter() - ctx['t0'] > P['OPT_STEP_CAP'] - P['OPT_WALL'] - 2 * P['OPT_HIRE_WALL']: break
                    B['ops'] = P['PLAN_OPS'] - P['OPT_HIRE_OPS']; B['hit'] = None; B['deadline'] = time.perf_counter() + P['OPT_HIRE_WALL']
                    pl = build(h2); ob = _ev(pl); co = cur[2]
                    if direction > 0: ok = ob[0] < co[0] or (ob[0] == co[0] and ob[1] - co[1] > P['OPT_HIRE_W'] * fib(h2 - 1))
                    else: ok = ob[0] <= co[0] and co[1] - ob[1] < P['OPT_HIRE_W'] * fib(cur[0] - 1)
                    if not ok: break
                    cur = (h2, pl, ob); moved = True
                if moved: break
            if cur[0] != hands:
                best_plan = cur[1]; over, dval, hands, routes, dropped, budgets, ret_flags, loops = best_plan
        except Exception as e:      # noqa  -- keep lx1's hand count
            if P['DEBUG']: log(f"OPT_HIRE d{day} EXC {e!r}")
        B['ops'], B['hit'], B['deadline'] = hsave
        S['opt_hire'] = (day, h_lx1, hands)
        if P['DEBUG']: log(f"OPT_HIRE d{day} lx1 {h_lx1} -> {hands}")
'''

ROUTE_HOOK = '''    opt_orders = None
    if P['OPT_ROUTE'] and day < LAST_DAY and not loops:
        # micro OPT_ROUTE: prize-collecting VRP local search over lx1's final routes (micro_opt); None keeps lx1's plan
        _res = micro_opt(routes, budgets, ret_flags, dropped, stops, ctx)
        if _res is not None: routes, dropped, opt_orders = _res[0], _res[1], _res[2]
    _FILLREF.clear()
    plans = []
'''

ORDER_OLD = '''        if r:
            start = nearest_shed(r[0].pos) if not order else order[-1].pos'''
ORDER_NEW = '''        if r and opt_orders is not None and opt_orders[u]:
            order = order + opt_orders[u]           # micro OPT_ROUTE: the optimiser's explicit visiting order
        elif r:
            start = nearest_shed(r[0].pos) if not order else order[-1].pos'''

ASSIGN_OLD = """    n_units = len(positions)
    for ui in range(1, n_units):
        if ui not in S['unit_plans']:"""
ASSIGN_NEW = """    n_units = len(positions)
    if P['OPT_ASSIGN']:
        # micro OPT_ASSIGN: hands appearing this hour (all with the same hours left) take the free plans that fill those hours
        # best (longest first, capped at the hours left; less overrun on ties), each plan going to the new hand that reaches its
        # route soonest from its spawn tile; later (shorter-time) hands get the shorter plans
        newu = [ui for ui in range(1, n_units) if ui not in S['unit_plans']]
        free = plan['hands_free']
        if newu and free:
            H = (24 - hour) if day < LAST_DAY else max(0, 23 - hour)
            rc = {id(q): remaining_cost(q, q['start']) for q in free}
            chosen = sorted(free, key=lambda q: (-min(rc[id(q)], H), rc[id(q)]))[:len(newu)]
            left = list(newu)
            for q in chosen:
                uj = min(left, key=lambda z: (remaining_cost(q, positions[z]), z))
                left.remove(uj); free.remove(q); q['unit'] = uj; S['unit_plans'][uj] = q
    for ui in range(1, n_units):
        if ui not in S['unit_plans']:"""

LATE_OLD = """    if idle and hour >= 2: help_assign(idle, plans, positions, ctx, hours_left)
"""
LATE_NEW = LATE_OLD + """    if P['OPT_LATE'] and day < LAST_DAY: late_assign(plans, positions, invs, ctx, hours_left, n_units)   # micro v2 OPT_LATE
"""

EXEC_OLD = """        acts.append(exec_unit(p, pos, inv, ctx, seeds_left, hours_left) or ['PASS'])
"""
EXEC_NEW = """        a_ = exec_unit(p, pos, inv, ctx, seeds_left, hours_left) or ['PASS']
        if P['OPT_LATE'] and a_[0] == 'PASS' and p['phase'] == 'done' and day < LAST_DAY:   # micro v2: no PASS on the step a plan ends
            a_ = late_redispatch(ui, p, pos, inv, plans, positions, invs, ctx, seeds_left, hours_left, n_units) or a_
        acts.append(a_)
"""

def patch(src):
    a = "    'DEBUG': bool(os.environ.get('CIRCUIT_LOG')),\n"
    assert src.count(a) == 1; src = src.replace(a, a + '    # micro (agents/micro) flags, all off = lx1\n    ' + DEFAULTS + '\n')
    a = '\ndef plan_day(ctx):\n'
    assert src.count(a) == 1; src = src.replace(a, '\n' + open(os.path.join(D, 'micro_opt.py')).read() + '\n' + a)
    a = '    over, dval, hands, routes, dropped, budgets, ret_flags, loops = best_plan\n'
    assert src.count(a) == 1; src = src.replace(a, HIRE_HOOK)
    a = '    _FILLREF.clear()\n    plans = []\n'
    assert src.count(a) == 1; src = src.replace(a, ROUTE_HOOK)
    assert src.count(ORDER_OLD) == 1; src = src.replace(ORDER_OLD, ORDER_NEW)
    assert src.count(ASSIGN_OLD) == 1; src = src.replace(ASSIGN_OLD, ASSIGN_NEW)
    assert src.count(LATE_OLD) == 1; src = src.replace(LATE_OLD, LATE_NEW)
    assert src.count(EXEC_OLD) == 1; src = src.replace(EXEC_OLD, EXEC_NEW)
    return src

TAGS = {'m0': {}, 'mr': {'OPT_ROUTE': True, 'OPT_ASSIGN': True}, 'mro': {'OPT_ROUTE': True}, 'ma': {'OPT_ASSIGN': True},
        'mrh': {'OPT_ROUTE': True, 'OPT_ASSIGN': True, 'OPT_HIRE': True},
        'mrh2': {'OPT_ROUTE': True, 'OPT_ASSIGN': True, 'OPT_HIRE': True, 'OPT_LATE': True, 'OPT_STEP_CAP': 0.35, 'OPT_WALL': 0.12, 'OPT_HIRE_WALL': 0.04},
        'mr2': {'OPT_ROUTE': True, 'OPT_ASSIGN': True, 'OPT_LATE': True, 'OPT_STEP_CAP': 0.35}, 'm02': {}}

def build(tag, extra):
    circ = patch(open(os.path.join(D, '_lx1_embedded_circuit.py')).read())
    open(os.path.join(D, 'circuit_micro.py'), 'w').write(circ)
    compile(circ, 'circuit_micro', 'exec')
    m = open(LX1).read()
    b64 = base64.b64encode(zlib.compress(circ.encode(), 9)).decode()
    m2, n = re.subn(r'_CIRC_B64 = "[^"]*"', lambda _: f'_CIRC_B64 = "{b64}"', m); assert n == 1
    xl = "'LATE_HARVEST_W': 0.1}})"
    assert m2.count(xl) == 1
    if extra:
        m2 = m2.replace(xl, "'LATE_HARVEST_W': 0.1}})\nP['XC_P'].update(" + repr(extra) + ")  # micro flags")
    out = os.path.join(D, 'build', tag); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'main.py'), 'w').write(m2)
    for f in ('LICENSE', 'NOTICE'):
        src = os.path.join(os.path.dirname(LX1), f)
        if os.path.exists(src): open(os.path.join(out, f), 'wb').write(open(src, 'rb').read())
    h = hashlib.sha256(m2.encode()).hexdigest()
    print(tag, 'main.py sha256', h, 'circuit sha256', hashlib.sha256(circ.encode()).hexdigest()[:16])
    return h

if __name__ == '__main__':
    tags = sys.argv[1:] or list(TAGS)
    for t in tags: build(t, TAGS[t])
