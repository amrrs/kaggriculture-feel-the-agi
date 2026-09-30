"""(race copy of final30/microbudget/game.py + per-product SELL revenue per farm via a _commit_unit wrapper)
one game per process (pod only): python game.py <cand main.py> <opp main.py> <seed> <seat> <out.json>
Engine loop = kaggle_environments env.run (actTimeout 1 s + remainingOverageTime enforced exactly as on Kaggle).
Records per-step wall time of both agents, rewards, margin, and the candidate circuit's S['probe'] (probe/timing builds) or
per-day S['opt_stat'] (clean builds)."""
import os, sys, json, time, hashlib
os.environ.setdefault('MPLBACKEND', 'Agg')
from kaggle_environments import make
from kaggle_environments.agent import get_last_callable

def main():
    cand, opp, seed, seat, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    t0 = time.time()
    fa = get_last_callable(open(cand).read()); fb = get_last_callable(open(opp).read())
    dstat = {}; rec = {0: [], 1: []}; opt = {}; dig = hashlib.sha256(); ov = {}
    def wrap(f, i, mine):
        def g(obs, cfg):
            s = time.perf_counter(); a = f(obs, cfg); dt = time.perf_counter() - s
            st = int(obs.get('step', 0) if hasattr(obs, 'get') else obs.step)
            rec[i].append(round(dt, 5)); ov[i] = obs.get('remainingOverageTime') if hasattr(obs, 'get') else None
            if mine:
                try:
                    dd = st // 24; hh = st % 24; ds = dstat.setdefault(dd, dict(mv=0, act={}, n=0))
                    for ua in [a.get('farmer')] + list(a.get('hands') or []):
                        if not ua: continue
                        ds['n'] += 1
                        if ua[0] in ('NORTH', 'SOUTH', 'EAST', 'WEST'): ds['mv'] += 1
                        else: ds['act'][ua[0]] = ds['act'].get(ua[0], 0) + 1
                    if hh == 23:
                        me_ = obs['farms'][obs['player']]; na = nf = nc = npl = nw = 0
                        for row in me_['tiles']:
                            for t_ in row:
                                if isinstance(t_, dict) and 'animal' in t_: na += 1; nf += t_['fed_today']; nc += t_['cared_today']
                                elif isinstance(t_, dict) and t_.get('kind') == 'PLANT': npl += 1; nw += t_['watered_today']
                        ds['h23'] = [na, nf, nc, npl, nw, sum(obs['private']['shed'].values()), round(me_['money'])]
                except Exception as ex: dstat['err'] = repr(ex)
                dig.update(json.dumps(a, sort_keys=True, default=str).encode())
                try:
                    x = f.__globals__['xc'](); o = x.S.get('opt_stat')
                    if o is not None:
                        opt[st] = {k: (list(v) if isinstance(v, tuple) else v) for k, v in o.items()}; x.S['opt_stat'] = None
                except Exception: pass
            return a
        return g
    agents = [None, None]; agents[seat] = wrap(fa, seat, True); agents[1 - seat] = wrap(fb, 1 - seat, False)
    import kaggle_environments.envs.kaggriculture.kaggriculture as K
    buys = [{}, {}]; sales = [{}, {}]; sday = [{}, {}]; cur = {'farms': None, 'step': 0}
    _pm, _cu = K._process_market, K._commit_unit
    def pm(state, env_):
        cur['farms'] = state[0].observation.farms; cur['step'] = int(state[0].observation.get('step', 0))
        return _pm(state, env_)
    def cu(op, item, price, farm, private, market, cap=100):
        ok = _cu(op, item, price, farm, private, market, cap)
        if ok and op != 'SELL' and cur['farms'] is not None:
            p = next((i for i, f in enumerate(cur['farms']) if f is farm), None)
            if p is not None:
                d = buys[p].setdefault(op + ':' + item, [0, 0]); d[0] += 1; d[1] += price
                k = 'B%s_%d' % (item[:2], cur['step'] // 24); e = sday[p].setdefault(k, [0, 0, 0]); e[0] += 1; e[1] += price; e[2] += cur['step'] % 24
        if ok and op == 'SELL' and cur['farms'] is not None:
            p = next((i for i, f in enumerate(cur['farms']) if f is farm), None)
            if p is not None:
                d = sales[p].setdefault(item, [0, 0]); d[0] += 1; d[1] += price
                if True:
                    k = '%s_%d' % (item[:2], cur['step'] // 24); e = sday[p].setdefault(k, [0, 0, 0]); e[0] += 1; e[1] += price; e[2] += cur['step'] % 24
        return ok
    K._process_market, K._commit_unit = pm, cu
    if os.environ.get('PIN_SHOPS', '1') == '1':
        # variance reduction: the shop sequence is drawn from its own RNG keyed on the seed only (same distribution as the
        # engine: uniform with replacement), so it no longer depends on the weed draws that our own layout changes.
        import random as _random
        _r = _random.Random(seed * 7919 + 17); PIN = [_r.choice(sorted(K.SHOPS)) for _ in range(K.MAX_SHOP_INSTANCES)]
        _eod0 = K._end_of_day
        def _eod(state, env_, day):
            town = state[0].observation.town; n0 = len(town['unlocked_shops'])
            _eod0(state, env_, day)
            if len(town['unlocked_shops']) > n0: town['unlocked_shops'][-1] = PIN[n0]
        K._end_of_day = _eod
    env = make('kaggriculture', configuration={'seed': seed})
    env.run(agents)
    stt = env.steps[-1]
    rw = [s.reward for s in stt]; status = [s.status for s in stt]
    rw = [round(r) if r is not None else None for r in rw]
    snap = {}
    try:
        for d in (10, 11, 13, 15, 18, 20, 25):
            st_ = env.steps[min(len(env.steps) - 1, d * 24 + 12)][seat]['observation']
            f_ = st_['farms'][seat]; c_ = {}
            for row in f_['tiles']:
                for t_ in row:
                    if isinstance(t_, dict):
                        k_ = t_.get('crop') or t_.get('animal') or t_.get('kind'); c_[k_] = c_.get(k_, 0) + 1
            snap[d] = dict(q=len(f_.get('unlocked_quadrants', [])), hands=len(f_.get('hands', [])), money=round(f_['money']), c=c_)
        fb = 0; hires = 0; wb = 0
        for t in range(1, len(env.steps)):
            a_ = env.steps[t][seat].get('action') or {}
            for o in (a_.get('market') or []):
                if o and o[0] == 'BUY_PRODUCT' and o[1] == 'FERTILIZER': fb += o[2]
                if o and o[0] == 'BUY_PRODUCT' and o[1] == 'WHEAT': wb += o[2]
                if o and o[0] == 'HIRE': hires += 1
        snap['fert_buy_orders'] = fb; snap['hire_orders'] = hires; snap['wheat_buy_orders'] = wb
    except Exception as ex: snap['err'] = repr(ex)
    nxlog = None; nxerr = None; rtrace = None
    try:
        S_ = fa.__globals__['S']; nxlog = S_.get('log'); rtrace = S_.get('trace') or S_.get('tb'); nxerr = [S_.get('err', 0), S_.get('last_err')]
    except Exception as ex: nxerr = ['noload', repr(ex)]
    probe = None
    try: probe = fa.__globals__['xc']().S.get('probe')
    except Exception: pass
    def stat(L):
        s = sorted(L); n = len(s)
        return dict(n=n, max=s[-1], p99=s[int(0.99 * n)], p999=s[min(n - 1, int(0.999 * n))], mean=sum(s) / n, n_gt035=sum(v > 0.35 for v in s),
                    n_gt05=sum(v > 0.5 for v in s), n_gt06=sum(v > 0.6 for v in s)) if n else {}
    r = dict(cand=cand, opp=opp, seed=seed, seat=seat, rewards=rw, status=status,
             margin=(rw[seat] - rw[1 - seat]) if None not in rw else None,
             win=(int(rw[seat] > rw[1 - seat]) - int(rw[seat] < rw[1 - seat])) if None not in rw else None,
             digest=dig.hexdigest(), step=stat(rec[seat]), step_opp=stat(rec[1 - seat]), overage_left=ov,
             sales_me=sales[seat], buys_me=buys[seat], buys_opp=buys[1 - seat], sales_opp=sales[1 - seat], sday_me=sday[seat], sday_opp=sday[1 - seat], snap=snap, times=rec[seat], opt=opt, probe=probe, nxlog=nxlog, dstat=dstat, nxerr=nxerr, trace=rtrace, sec=round(time.time() - t0, 1), cpu=os.sched_getaffinity(0).__repr__())
    json.dump(r, open(out + '.tmp', 'w'), default=str); os.replace(out + '.tmp', out)
    print(os.path.basename(out), r['margin'], r['rewards'], nxerr, r['status'], 'max %.3f p99 %.3f' % (r['step'].get('max', 0), r['step'].get('p99', 0)), r['sec'], flush=True)

if __name__ == '__main__':
    main()
