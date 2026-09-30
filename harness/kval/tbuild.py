"""tbuild.py: lx3ms + g012m knob transplant variants T1/T2/T3 via the autotune override block (space.py / build_cand.py)."""
import sys, os, json, hashlib
sys.path.insert(0, '/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/autotune')
import space, build_cand
space.BASES['lx3ms'] = '/Users/1littlecoder/kaggriculture/research/claude/2900/agents/micro/build/lx3ms/main.py'
G = json.load(open('/Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/autotune/build/at12m/AUTOTUNE.json'))['vals']
EP, CP = space.effective('lx3ms'); EG, _ = space.effective('ms_slot')
ok = {}
for k, v in G.items():
    path = space.KN[k][2]; key = path[0] if isinstance(path, tuple) else path
    have = key in EP
    print('%-16s g012m %-10r lx3ms-base %-28r v183ms/ms_slot-base %-28r %s' % (k, v, EP.get(key), EG.get(key), 'OK' if have else 'ABSENT'))
    if have: ok[k] = v
if 'MPC_SELL' not in EP: ok.pop('MPC_W', None); ok.pop('MPC_H', None); print('no MPC_SELL in lx3ms -> MPC_W/MPC_H skipped')
else: print('MPC_SELL', EP['MPC_SELL'])
T2k = {'SQ_W', 'SQ_DECAY', 'SQ_SPLIT', 'SQ_START_DAY', 'SELL0_MAX', 'OVERFLOW_TARGET', 'AH_V', 'LATE_HARVEST_W'}
T3k = {'HIRE_DOWN_W', 'HAND_W', 'CARE_W', 'FERT_WHEAT_MAXP', 'WHEAT_BUFFER', 'ALLOC_MARGIN', 'STRAW_AB_x', 'LATE_START', 'TOM_OPP_MARGIN', 'AMAX_TOM'}
V = {'T1': dict(ok), 'T2': {k: v for k, v in ok.items() if k in T2k}, 'T3': {k: v for k, v in ok.items() if k in T3k}}
print('unassigned', set(ok) - T2k - T3k)
os.makedirs('ds2', exist_ok=True)
for n, vals in V.items():
    t = build_cand.text(vals, 'lx3ms', EP, CP); compile(t, n, 'exec'); open(f'ds2/{n}.py', 'w').write(t)
    print(n, len(vals), hashlib.sha256(t.encode()).hexdigest()[:12], sorted(vals))
    print('   ', t.split('# ---- autotune overrides (final30/autotune) ----')[1].strip().splitlines()[1][:600])
# one-knob probes for the digest check
for k, v in ok.items():
    open(f'ds2/K_{k}.py', 'w').write(build_cand.text({k: v}, 'lx3ms', EP, CP))
json.dump(V, open('variants.json', 'w'), indent=1)
