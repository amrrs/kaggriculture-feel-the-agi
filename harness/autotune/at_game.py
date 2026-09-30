"""autotune fresh-seed game (pod only): python at_game.py <cand main.py> <opp main.py> <seed> <seat> <out.json> [det]
Engine loop = kaggle_environments 1.32.7 env.run (actTimeout 1 s + overage as Kaggle), agents loaded with get_last_callable.
det: both agents get wall-clock planning caps lifted (PLAN_WALL/OPT_WALL/OPT_STEP_CAP huge -> ops-bounded, reproducible)
and a large actTimeout; used only by the knob screen (action digests). Records per-step action hashes of the candidate,
rewards, margin, win, per-product sales, step-time stats. (Derived from final30/microstructure/game.py.)"""
import os, sys, json, time, hashlib
os.environ.setdefault('MPLBACKEND', 'Agg')
from kaggle_environments import make
from kaggle_environments.agent import get_last_callable
DET = {'PLAN_WALL': 60.0, 'OPT_WALL': 30.0, 'OPT_STEP_CAP': 100.0, 'OPT_HIRE_WALL': 5.0}
def load(path, det):
    f = get_last_callable(open(path).read())
    if det:
        g = f.__globals__
        if isinstance(g.get('P'), dict) and 'XC_P' in g['P']: g['P']['XC_P'] = dict(g['P']['XC_P'], **DET)
    return f
def main():
    cand, opp, seed, seat, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    det = len(sys.argv) > 6 and sys.argv[6] == 'det'
    t0 = time.time()
    fa = load(cand, det); fb = load(opp, det)
    rec = {0: [], 1: []}; hs = []
    def wrap(f, i, mine):
        def g(obs, cfg):
            s = time.perf_counter(); a = f(obs, cfg); dt = time.perf_counter() - s
            rec[i].append(round(dt, 4))
            if mine: hs.append(hashlib.sha1(json.dumps(a, sort_keys=True, default=str).encode()).hexdigest()[:8])
            return a
        return g
    agents = [None, None]; agents[seat] = wrap(fa, seat, True); agents[1 - seat] = wrap(fb, 1 - seat, False)
    import kaggle_environments.envs.kaggriculture.kaggriculture as K
    sales = [{}, {}]; cur = {'farms': None}
    _pm, _cu = K._process_market, K._commit_unit
    def pm(state, env_):
        cur['farms'] = state[0].observation.farms; return _pm(state, env_)
    def cu(op, item, price, farm, private, market, cap=100):
        ok = _cu(op, item, price, farm, private, market, cap)
        if ok and op == 'SELL' and cur['farms'] is not None:
            p = next((i for i, f in enumerate(cur['farms']) if f is farm), None)
            if p is not None: d = sales[p].setdefault(item, [0, 0]); d[0] += 1; d[1] += price
        return ok
    K._process_market, K._commit_unit = pm, cu
    cfg = {'seed': seed}
    if det: cfg.update(actTimeout=60, remainingOverageTime=6000)
    env = make('kaggriculture', configuration=cfg)
    env.run(agents)
    stt = env.steps[-1]
    rw = [round(s.reward) if s.reward is not None else None for s in stt]; status = [s.status for s in stt]
    def stat(L):
        s = sorted(L); n = len(s)
        return dict(n=n, max=s[-1], p99=s[int(0.99 * n)], mean=round(sum(s) / n, 5), n_gt06=sum(v > 0.6 for v in s)) if n else {}
    r = dict(cand=cand, opp=opp, seed=seed, seat=seat, det=det, rewards=rw, status=status,
             margin=(rw[seat] - rw[1 - seat]) if None not in rw else None,
             win=(int(rw[seat] > rw[1 - seat]) - int(rw[seat] < rw[1 - seat])) if None not in rw else None,
             digest=hashlib.sha256(''.join(hs).encode()).hexdigest()[:16], hs=hs, step=stat(rec[seat]), step_opp=stat(rec[1 - seat]),
             sales_me=sales[seat], sales_opp=sales[1 - seat], sec=round(time.time() - t0, 1))
    json.dump(r, open(out + '.tmp', 'w'), default=str); os.replace(out + '.tmp', out)
    print(os.path.basename(out), r['margin'], r['status'], 'max %.3f' % r['step'].get('max', 0), r['sec'], flush=True)
if __name__ == '__main__':
    main()
