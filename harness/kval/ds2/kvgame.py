"""kvgame.py <candfile> <oppfile> <seed> <candseat>: one full game, agents loaded like Kaggle (get_last_callable on the source,
no __file__), per-step wall time recorded for both agents. Prints one JSON line."""
import os, sys, json, time, traceback, hashlib
os.environ.setdefault('MPLBACKEND', 'Agg')
from kaggle_environments import make
from kaggle_environments.agent import get_last_callable
cf, of, seed, seat = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
def load(p):
    src = open(p).read()
    try: return get_last_callable(src, path=p)
    except TypeError: return get_last_callable(src)
res = {'cand': os.path.basename(cf), 'opp': os.path.basename(of), 'seed': seed, 'seat': seat}
try:
    fa, fb = load(cf), load(of)
    times = {0: [], 1: []}; errs = {0: 0, 1: 0}; acts = []
    def timed(f, who):
        def g(obs, cfg):
            t = time.perf_counter()
            try:
                r = f(obs, cfg)
                if who == 0: acts.append(json.dumps(r, sort_keys=True, default=str))
            except Exception:
                errs[who] += 1; raise
            finally: times[who].append(time.perf_counter() - t)
            return r
        return g
    env = make('kaggriculture', configuration={'seed': seed})
    A = timed(fa, 0); B = timed(fb, 1)   # 0 = cand, 1 = opp
    t0 = time.time()
    env.run([A, B] if seat == 0 else [B, A])
    st = [s.status for s in env.state]; coins = [s.reward for s in env.state]
    c, o = coins[seat], coins[1 - seat]
    def stats(ts):
        if not ts: return {}
        rest = ts[1:] or [0.]
        return {'n': len(ts), 'first': round(ts[0], 3), 'peak': round(max(rest), 3), 'peak_at': 1 + rest.index(max(rest)),
                'gt06': sum(x > 0.6 for x in rest), 'gt1': sum(x > 1.0 for x in rest), 'mean': round(sum(ts) / len(ts), 4)}
    res.update(status=st, coins=c, opp_coins=o, margin=(None if c is None or o is None else c - o),
               win=(None if c is None or o is None else float(c > o) + 0.5 * (c == o)),
               cand_t=stats(times[0]), opp_t=stats(times[1]), cand_exc=errs[0], opp_exc=errs[1], wall=round(time.time() - t0, 1),
               dig=hashlib.sha256('\n'.join(acts).encode()).hexdigest()[:16], shops=list(env.state[0].observation.town.unlocked_shops))
    if st != ['DONE', 'DONE']: res['error'] = str(st)
except Exception:
    res['error'] = traceback.format_exc()[-1500:]
print(json.dumps(res), flush=True)
