"""tj_game.py <ep> <cand_seat> <cand main.py> <out.json> : one tape-judge game (derived from topfield/autopsy_tf.py).
The recorded agent of seat 1-cand_seat replays its recorded actions (harness/tape_agent.py, guard + sweep OFF = pure tape) with the recorded
seed and the recorded shop order pinned; the candidate plays cand_seat live through kaggle_environments env.run (actTimeout / overage as
Kaggle; candidate loaded with get_last_callable like Kaggle). Writes one JSON: rewards, recorded rewards, parity, margin (cand - tape),
intact (tape keeps >= 90% of its recorded coins), per-seat revenue/units by product, spend, land days, step-time stats."""
import os, sys, json, time, hashlib, collections, importlib.util, random as _random
os.environ.setdefault('MPLBACKEND', 'Agg')
H = os.path.dirname(os.path.abspath(__file__))
TAPE_AGENT = os.environ.get('TJ_TAPE_AGENT', os.path.join(H, 'tape_agent.py'))
DATA = os.environ.get('TJ_DATA', os.path.join(H, 'data'))
from kaggle_environments import make
from kaggle_environments.agent import get_last_callable
import kaggle_environments.envs.kaggriculture.kaggriculture as K

eid, me, src, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
t0 = time.time()
meta = json.load(open(f'{DATA}/live_meta/{eid}.json')); SHOPS = list(meta['shops']); live = [round(r) for r in meta['rewards']]
tapef = f'{DATA}/live_pairs/{eid}_s{1 - me}.json'; seed = json.load(open(tapef))['seed']

CUR = {'farms': [None, None]}
_pm = K._process_market
def pm(state, env):
    CUR['farms'] = [state[0].observation.farms[i] for i in range(2)]; CUR['step'] = state[0].observation['step']; return _pm(state, env)
K._process_market = pm
REV = [collections.Counter(), collections.Counter()]; UNITS = [collections.Counter(), collections.Counter()]; SPEND = [collections.Counter(), collections.Counter()]
FAILS = [0, 0]
def pid(farm): return next((i for i, f in enumerate(CUR['farms']) if f is farm), -1)
_cu = K._commit_unit
def cu(op, item, price, farm, private, market, shed_capacity=100):
    ok = _cu(op, item, price, farm, private, market, shed_capacity); p = pid(farm)
    if 0 <= p < 2:
        if ok:
            if op == 'SELL': REV[p][item] += price; UNITS[p][item] += 1
            else: SPEND[p][op + ':' + item] += price
        elif op.startswith('BUY'): FAILS[p] += 1
    return ok
K._commit_unit = cu
LAND = [[], []]
_land = K._do_buy_land
def land2(farm, board_size):
    n = len(farm['unlocked_quadrants']); _land(farm, board_size); p = pid(farm)
    if 0 <= p < 2 and len(farm['unlocked_quadrants']) > n: LAND[p].append(CUR.get('step', 0) // 24)
K._do_buy_land = land2
HIRES = [0, 0]
_hire = K._do_hire
def hire2(farm, private, board_size, mult=K.FARM_HAND_COST_MULT):
    n = farm['hires_today']; _hire(farm, private, board_size, mult); p = pid(farm)
    if 0 <= p < 2 and farm['hires_today'] > n: HIRES[p] += 1
K._do_hire = hire2
def _end_of_day(state, env, day):   # engine 1.32.7 _end_of_day with the recorded shop order pinned
    obs0 = state[0].observation; cfg = env.configuration
    board_size = int(K.get(cfg, "boardSize", 10)); turns_per_day = max(1, int(K.get(cfg, "turnsPerDay", 24)))
    weed_chance = float(K.get(cfg, "weedSpawnChance", 0.005)); shed_cap = int(K.get(cfg, "shedCapacity", 100)); shop_interval = max(1, int(K.get(cfg, "townShopUnlockInterval", 3)))
    rng = _random.Random((env.info.get("seed", 0) * 1_000_003) ^ day)
    for player_id, farm in enumerate(obs0.farms):
        private = state[player_id].observation.private
        K._daily_refresh_plants(farm, day, turns_per_day); K._daily_refresh_animals(farm, day)
        K._spawn_weeds(farm, board_size, weed_chance, rng); K._drop_inventories_to_shed(private, shed_cap)
        farm["farmer"] = list(K._default_spawn(board_size)); farm["hands"] = []; farm["hires_today"] = 0
        private["inventories"] = [{}]
    next_day = day + 1; town = obs0.town
    if next_day > 0 and next_day % shop_interval == 0 and len(town["unlocked_shops"]) < K.MAX_SHOP_INSTANCES:
        idx = len(town["unlocked_shops"])
        if idx < len(SHOPS): town["unlocked_shops"].append(SHOPS[idx])
K._end_of_day = _end_of_day

os.environ['KAG_TAPE'] = tapef
spec = importlib.util.spec_from_file_location('tape_mod', TAPE_AGENT); tm = importlib.util.module_from_spec(spec); spec.loader.exec_module(tm)
tm._load_tape(); tm.P['GUARD_INTERVAL'] = 0; tm.P['TERMINAL_SWEEP'] = False; os.environ.pop('KAG_TAPE', None)
code = open(src).read(); sha = hashlib.sha256(code.encode()).hexdigest()
fa0 = get_last_callable(code)
TIMES = []
def fa(obs, cfg):
    s = time.perf_counter(); r = fa0(obs, cfg); TIMES.append(time.perf_counter() - s); return r
agents = [fa, tm.agent] if me == 0 else [tm.agent, fa]
env = make('kaggriculture', configuration={'seed': seed}); env.run(agents)
rw = [round(s.reward) if s.reward is not None else None for s in env.steps[-1]]
st = [s.status for s in env.steps[-1]]
ok = None not in rw
T = sorted(TIMES)
r = dict(ep=int(eid), cand_seat=me, seed=seed, cand=src, sha=sha, rewards=rw, live=live, parity=rw == live, status=st,
         margin=(rw[me] - rw[1 - me]) if ok else None, own=rw[me], opp=rw[1 - me],
         intact=bool(ok and rw[1 - me] >= 0.9 * live[1 - me]), opp_frac=round(rw[1 - me] / live[1 - me], 4) if ok and live[1 - me] else None,
         rev=[dict(REV[p]) for p in (0, 1)], units=[dict(UNITS[p]) for p in (0, 1)], spend=[dict(SPEND[p]) for p in (0, 1)],
         buyfail=FAILS, land=LAND, hires=HIRES, shops=list(env.steps[-1][0]['observation']['town']['unlocked_shops']),
         step=dict(n=len(T), max=round(T[-1], 4) if T else None, p99=round(T[int(0.99 * len(T))], 4) if T else None,
                   mean=round(sum(T) / len(T), 4) if T else None, n_gt06=sum(v > 0.6 for v in T)),
         sec=round(time.time() - t0, 1), cpu=repr(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else None)
json.dump(r, open(out + '.tmp', 'w')); os.replace(out + '.tmp', out)
print(os.path.basename(out), 'margin', r['margin'], 'rw', rw, 'live', live, 'parity', r['parity'], 'intact', r['intact'], 'max %.3f' % (r['step']['max'] or 0), r['sec'], flush=True)
