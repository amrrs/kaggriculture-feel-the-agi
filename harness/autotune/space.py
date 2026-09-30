"""autotune parameter space over the v183ms / ms_slot executor (embedded circuit P, updated by _XCP_B64 and the ctrl P['XC_P'])
and the ctrl (opening) P.  A candidate is a dict {knob_name: value}; build_cand.py appends it to the base main.py as
P['XC_P'] = dict(P['XC_P'], **{...}) / P.update({...}) (no code change; agent() applies XC_P at step 0).
Coordinates: every knob has z in [-1, 1], z = 0 is the base value; z<0 interpolates base->lo, z>0 base->hi
(geometric for kind 'log', linear for 'lin'/'int' (int rounds), bool flips when z < -0.5)."""
import os, re, zlib, base64, json, math, types
D = os.path.dirname(os.path.abspath(__file__)); A = os.path.abspath(os.path.join(D, '..', '..'))
BASES = {'v183ms': os.path.join(A, 'micro', 'build', 'v183ms', 'main.py'),
         'ms_slot': os.path.join(A, 'final30', 'newexec', 'build', 'ms_slot', 'main.py')}
BASE = 'ms_slot'   # MS_SLOT is itself a knob (False = v183ms action for action)

def effective(base=BASE):
    """circuit defaults <- _XCP_B64 <- ctrl P['XC_P'] (what the executor actually runs with), and the ctrl P."""
    m = open(BASES[base]).read()
    circ = zlib.decompress(base64.b64decode(re.search(r'_CIRC_B64 = "([^"]*)"', m).group(1))).decode()
    mod = types.ModuleType('c'); exec(compile(circ, 'c', 'exec'), mod.__dict__)
    P = dict(mod.P); P.update(json.loads(zlib.decompress(base64.b64decode(re.search(r'_XCP_B64 = "([^"]*)"', m).group(1))).decode()))
    g = {}; head = m.split('\ntry: HERE')[0]
    head = re.sub(r'_(LIB|CIRC)_B64 = "[^"]*"', '', head); head = re.sub(r"_CODEX_GATE_B64='[^']*'", '', head)
    exec(head, g); P.update(g['P'].get('XC_P', {}))
    return P, g['P']

# (name, target, path, kind, lo, hi)   target: 'xc' executor P / 'ctrl' opening P; path: key or (key, subkey) or (key, '*') = scale all
SCREEN = [
    # hiring
    ('HANDS_MAX', 'xc', 'HANDS_MAX', 'int', 10, 14), ('HANDS_MIN', 'xc', 'HANDS_MIN', 'int', 4, 8), ('HAND_SLACK', 'xc', 'HAND_SLACK', 'int', 0, 2),
    ('HIRE_DOWN_W', 'xc', 'HIRE_DOWN_W', 'log', 0.6, 2.4), ('HIRE_DOWN_MIN', 'xc', 'HIRE_DOWN_MIN', 'int', 3, 6),
    ('HAND_W', 'xc', 'HAND_W', 'log', 0.375, 1.5), ('LABOUR_COST', 'xc', 'LABOUR_COST', 'log', 4.0, 16.0),
    # herd / allocation sizing
    ('HERD_SHEEP_x', 'xc', ('HERD_SHEEP', '*'), 'log', 0.6, 1.6), ('HERD_SHEEP_Y1', 'xc', 'HERD_SHEEP_Y1', 'int', 5, 11),
    ('HERD_DAY_MAX', 'xc', 'HERD_DAY_MAX', 'int', 12, 17), ('HERD_LEAD', 'xc', 'HERD_LEAD', 'lin', 0.0, 2.0),
    ('ALLOC_MARGIN', 'xc', 'ALLOC_MARGIN', 'log', 75.0, 300.0),
    ('AMAX_STRAW', 'xc', ('ALLOC_MAX', 'STRAWBERRY'), 'int', 12, 28), ('AMAX_TOM', 'xc', ('ALLOC_MAX', 'TOMATO'), 'int', 8, 32),
    ('AMAX_SHEEP', 'xc', ('ALLOC_MAX', 'SHEEP'), 'int', 6, 18), ('AMAX_COW', 'xc', ('ALLOC_MAX', 'COW'), 'int', 4, 16),
    ('AMAX_GOOSE', 'xc', ('ALLOC_MAX', 'GOOSE'), 'int', 0, 10), ('AMAX_CARROT', 'xc', ('ALLOC_MAX', 'CARROT'), 'int', 10, 40),
    ('ALAST_STRAW', 'xc', ('ALLOC_LAST_DAY', 'STRAWBERRY'), 'int', 12, 18), ('ALAST_TOM', 'xc', ('ALLOC_LAST_DAY', 'TOMATO'), 'int', 17, 23),
    ('ALAST_SHEEP', 'xc', ('ALLOC_LAST_DAY', 'SHEEP'), 'int', 15, 21), ('ALAST_COW', 'xc', ('ALLOC_LAST_DAY', 'COW'), 'int', 13, 19),
    ('ALAST_GOOSE', 'xc', ('ALLOC_LAST_DAY', 'GOOSE'), 'int', 16, 24), ('ALAST_CARROT', 'xc', ('ALLOC_LAST_DAY', 'CARROT'), 'int', 21, 26),
    ('STRAW_AB_x', 'xc', ('STRAW_AB', '*'), 'log', 0.6, 1.6), ('STRAW_ADD_MAX', 'xc', 'STRAW_ADD_MAX', 'int', 6, 20),
    ('MELON_LABOUR', 'xc', 'MELON_LABOUR', 'log', 5.5, 22.0),
    ('TOM_FIRST_DAY', 'xc', 'TOM_FIRST_DAY', 'int', 12, 19), ('TOM_OPP_MARGIN', 'xc', 'TOM_OPP_MARGIN', 'lin', 0.0, 1.5),
    ('CARROT_OPP_TRIG', 'xc', 'CARROT_OPP_TRIG', 'int', 1, 12),
    # sales volume / timing (SQ, MPC, holds)
    ('SQ', 'xc', 'SQ', 'bool', None, None), ('SQ_W', 'xc', 'SQ_W', 'log', 1.0, 4.0), ('SQ_DECAY', 'xc', 'SQ_DECAY', 'lin', 0.1, 1.0),
    ('SQ_SPLIT', 'xc', 'SQ_SPLIT', 'lin', 0.0, 1.0), ('SQ_START_DAY', 'xc', 'SQ_START_DAY', 'int', 11, 17), ('SQ_MIN_GAIN', 'xc', 'SQ_MIN_GAIN', 'log', 0.5, 8.0),
    ('SQ_SHED_MAX', 'xc', 'SQ_SHED_MAX', 'int', 80, 98),
    ('MPC_SELL', 'xc', 'MPC_SELL', 'bool', None, None), ('MPC_W', 'xc', 'MPC_W', 'log', 0.5, 2.0), ('MPC_H', 'xc', 'MPC_H', 'int', 12, 60),
    ('MPC_TV', 'xc', 'MPC_TV', 'lin', 0.6, 1.0), ('MPC_DEC', 'xc', 'MPC_DEC', 'lin', 0.1, 0.9), ('MPC_ROOM', 'xc', 'MPC_ROOM', 'lin', 0.5, 1.5),
    ('MPC_SHED_MAX', 'xc', 'MPC_SHED_MAX', 'int', 80, 98),
    ('TOM_HOLD', 'xc', 'TOM_HOLD', 'bool', None, None), ('TOM_HOLD_MAX', 'xc', 'TOM_HOLD_MAX', 'int', 0, 160), ('TOM_HOLD_OPP_W', 'xc', 'TOM_HOLD_OPP_W', 'lin', 0.0, 3.0),
    ('HOLD_OPP_GATE', 'xc', 'HOLD_OPP_GATE', 'bool', None, None), ('HOLD_OPP_MIN', 'xc', 'HOLD_OPP_MIN', 'log', 1.0, 8.0),
    ('CARROT_HOLD', 'xc', 'CARROT_HOLD', 'bool', None, None), ('CARROT_HOLD_PRICE', 'xc', 'CARROT_HOLD_PRICE', 'int', 20, 50),
    ('MS_SLOT', 'xc', 'MS_SLOT', 'bool', None, None), ('MS_CAP', 'xc', 'MS_CAP', 'int', 10, 60),
    ('SELL0_MAX', 'xc', 'SELL0_MAX', 'int', 1, 8), ('COLLECT_MIN_PRICE', 'xc', 'COLLECT_MIN_PRICE', 'int', 1, 10),
    # executor economics
    ('MV_GATE', 'xc', 'MV_GATE', 'bool', None, None), ('MV_LAB', 'xc', 'MV_LAB', 'log', 5.0, 20.0),
    ('FERT_WHEAT_MAXP', 'xc', 'FERT_WHEAT_MAXP', 'log', 60.0, 240.0), ('FERT_BUY_MAXP', 'xc', 'FERT_BUY_MAXP', 'log', 60.0, 240.0),
    ('CARE_W', 'xc', 'CARE_W', 'log', 0.45, 1.8), ('LATE_HARVEST_W', 'xc', 'LATE_HARVEST_W', 'lin', 0.0, 0.6), ('AH_V', 'xc', 'AH_V', 'lin', 0.0, 1.0),
    ('WHEAT_BUFFER', 'xc', 'WHEAT_BUFFER', 'int', 0, 8), ('CASH_RESERVE', 'xc', 'CASH_RESERVE', 'log', 300.0, 2000.0),
    ('OVERFLOW_TARGET', 'xc', 'OVERFLOW_TARGET', 'int', 88, 100), ('WHEAT_KEEP_ROOM', 'xc', 'WHEAT_KEEP_ROOM', 'int', 60, 92),
    # land / endgame timing
    ('LATE_START', 'xc', 'LATE_START', 'int', 19, 26), ('LATE_RATIO', 'xc', 'LATE_RATIO', 'lin', 0.95, 1.5), ('PLANT_LAST_DAY', 'xc', 'PLANT_LAST_DAY', 'int', 24, 28),
    ('END_MIN', 'xc', 'END_MIN', 'int', 1, 6), ('ENDGAME_FEED', 'xc', 'ENDGAME_FEED', 'bool', None, None),
    ('LAND_MAX_EXTRA', 'xc', 'LAND_MAX_EXTRA', 'int', 0, 3), ('LAND_RESERVE', 'xc', 'LAND_RESERVE', 'log', 100.0, 1200.0),
    # opening -> executor handover
    ('HANDOVER', 'ctrl', 'HANDOVER', 'int', 216, 288), ('RESCUE_HOUR', 'ctrl', 'RESCUE_HOUR', 'int', 14, 21),
]
KN = {k[0]: k for k in SCREEN}

def base_value(name, EP=None, CP=None):
    if EP is None: EP, CP = effective()
    _, tgt, path, kind, lo, hi = KN[name]; src = EP if tgt == 'xc' else CP
    if isinstance(path, tuple):
        k, sub = path
        return 1.0 if sub == '*' else src[k][sub]
    return src[path]

def decode(name, z, b):
    _, tgt, path, kind, lo, hi = KN[name]; z = max(-1.0, min(1.0, float(z)))
    if kind == 'bool': return (not b) if z < -0.5 else b
    end = lo if z < 0 else hi; t = abs(z)
    if kind == 'log': v = b * (end / b) ** t if b > 0 else end * t
    else: v = b + (end - b) * t
    if kind == 'int': v = int(round(v))
    else: v = round(v, 4)
    return v

def overrides(vals, EP=None, CP=None):
    """{knob: value} -> (xc_over, ctrl_over) with full nested dicts / scaled tuples."""
    if EP is None: EP, CP = effective()
    xo, co = {}, {}
    for name, v in vals.items():
        _, tgt, path, kind, lo, hi = KN[name]; src = EP if tgt == 'xc' else CP; dst = xo if tgt == 'xc' else co
        if isinstance(path, tuple):
            k, sub = path
            if sub == '*': dst[k] = [round(x * v, 4) for x in src[k]]
            else: dst.setdefault(k, dict(src[k]))[sub] = v
        else: dst[path] = v
    return xo, co

if __name__ == '__main__':
    EP, CP = effective()
    for k in SCREEN:
        b = base_value(k[0], EP, CP)
        print('%-18s base %-10r lo %-8r hi %-8r  z-1 %r  z+1 %r' % (k[0], b, k[4], k[5], decode(k[0], -1, b), decode(k[0], 1, b)))
