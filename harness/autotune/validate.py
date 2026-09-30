"""validate.py: holdout validation of chosen vectors (phase 4; never used during search).
  python validate.py <tag> <cid> [<cid> ...]      cids from evals.jsonl (or 'ms_slot')
Games: holdout seeds 19001-19048 both seats vs V183, v183ms, lx3 (96 each) + all 123 tapes (90 search + 33 held out);
v183ms plays the same seeds vs V183 / lx3 and the same tapes (paired baseline, same pod). Seeds and tapes are split across the pods.
Output out/val_<tag>/<pod>/<cid>/..., report printed + out/val_<tag>.json."""
import os, sys, json, time, glob, math
from common import *
import driver, eval_cand
def cand_vals(cid):
    for ln in open('evals.jsonl'):
        r = json.loads(ln)
        if r['cid'] == cid: return r['vals']
    raise SystemExit('unknown ' + cid)
# holdout games: seat = seed % 2 on 19001-19048 (48 distinct games) + the other seat on 19001-19012 (12 mirror checks)
GAMES = [(s, s % 2) for s in HOLDOUT_SEEDS] + [(s, 1 - s % 2) for s in HOLDOUT_SEEDS[:12]]
if os.environ.get('VAL_SEEDS'):   # confirmation block, e.g. VAL_SEEDS=19201-19248 (seat = seed % 2 only)
    a, b = map(int, os.environ['VAL_SEEDS'].split('-')); GAMES = [(s, s % 2) for s in range(a, b + 1)]
NO_TAPES = os.environ.get('VAL_TAPES') == '0'
def make(tag, cids, P, games=None, allt=None):
    G = f'gens/val_{tag}'; os.makedirs(G, exist_ok=True); GAMES_ = games or GAMES
    if allt is None:
        tapes = json.load(open('tape_split.json')); allt = [] if NO_TAPES else [dict(t, hold=0) for t in tapes['search']] + [dict(t, hold=1) for t in tapes['holdout']]
    wsum = sum(p['w'] for p in P); tp = {}; sp = {}; acc = 0.0; i = 0; j0 = 0; acc2 = 0.0
    for p in P:
        acc += p['w'] / wsum; j = round(acc * len(allt)); tp[p['name']] = allt[i:j]; i = j
        k = round(acc * len(GAMES_)); sp[p['name']] = GAMES_[j0:k]; j0 = k
    build = {c: (cand_vals(c) if c not in OPP else None) for c in cids}
    for p in P:
        pn = p['name']; jobs = []
        for cid in ['v183ms'] + cids:
            c = cand_path(cid)
            for s, se in sp[pn]:
                if True:
                    for o in ('V183', 'v183ms', 'lx3'):
                        if cid == 'v183ms' and o == 'v183ms': continue
                        jobs.append(dict(k='fresh', c=c, o=OPP[o], seed=s, seat=se, out=f"{RD}/out/val_{tag}/{pn}/{cid}/f_{o}_{s}_{se}.json"))
            for t in tp[pn]: jobs.append(dict(k='tape', c=c, ep=t['ep'], seat=t['seat'], out=f"{RD}/out/val_{tag}/{pn}/{cid}/t_{t['ep']}_{t['seat']}.json"))
        jobs.sort(key=lambda j: j['k'] != 'fresh')
        json.dump({'build': {c: v for c, v in build.items() if v is not None}, 'jobs': jobs}, open(f'{G}/jobs_{pn}.json', 'w'))
    json.dump({'cids': cids, 'tapes': tp, 'seeds': sp, 'vals': build}, open(f'{G}/spec.json', 'w'), indent=0)
    return G
def mse(x):
    n = len(x); m = sum(x) / n if n else 0; s = math.sqrt(sum((v - m) ** 2 for v in x) / (n - 1) / n) if n > 1 else 0; return m, s, n
def report(tag):
    spec = json.load(open(f'gens/val_{tag}/spec.json')); hold = {(t['ep'], t['seat']): t['hold'] for L in spec['tapes'].values() for t in L}
    R = {}
    for f in glob.glob(f'out/val_{tag}/*/*/*.json'):
        pod, cid, fn = f.split('/')[-3:]
        try: R.setdefault(cid, {})[(pod, fn[:-5])] = json.load(open(f))
        except Exception: pass
    B = R.get('v183ms', {}); out = {}
    for cid in ['v183ms'] + spec['cids']:
        C = R.get(cid, {}); o = {}
        for opp in ('V183', 'v183ms', 'lx3'):
            ks = [k for k in C if k[1].startswith(f'f_{opp}_')]
            if not ks: continue
            M = [C[k]['margin'] if C[k]['margin'] is not None else -20000 for k in ks]
            W = [eval_cand.wr(C[k]['win'] if C[k]['win'] is not None else -1) for k in ks]
            d = dict(n=len(ks), win=round(sum(W) / len(W), 3), margin=round(mse(M)[0]), margin_se=round(mse(M)[1]), worst=min(M))
            if opp != 'v183ms' and cid != 'v183ms':
                P_ = [C[k]['margin'] - B[k]['margin'] for k in ks if k in B and B[k]['margin'] is not None and C[k]['margin'] is not None]
                m, s, n = mse(P_); d.update(paired=round(m), paired_se=round(s), paired_n=n, z=round(m / s, 2) if s else None,
                                            base_win=round(sum(eval_cand.wr(B[k]['win']) for k in ks if k in B) / max(1, sum(k in B for k in ks)), 3))
            elif opp == 'v183ms': d.update(paired=d['margin'], paired_se=d['margin_se'], z=round(d['margin'] / d['margin_se'], 2) if d['margin_se'] else None)
            o[opp] = d
        tk = [k for k in C if k[1].startswith('t_')]
        for sub, flt in (('tapes_all', lambda h: True), ('tapes_holdout', lambda h: h == 1), ('tapes_search', lambda h: h == 0)):
            ks = [k for k in tk if flt(hold.get(tuple(int(x) for x in k[1][2:].split('_')), 0)) and k in B]
            if not ks: continue
            P_ = [C[k]['margin'] - B[k]['margin'] for k in ks]; m, s, n = mse(P_)
            bi = [C[k]['margin'] - B[k]['margin'] for k in ks if C[k].get('intact') and B[k].get('intact')]
            o[sub] = dict(n=n, paired=round(m), se=round(s), wins=sum(C[k]['margin'] > 0 for k in ks), base_wins=sum(B[k]['margin'] > 0 for k in ks),
                          both_intact=round(mse(bi)[0]) if bi else None, both_intact_n=len(bi), worst_paired=min(P_) if cid != 'v183ms' else None)
        st = [C[k]['step']['max'] for k in C if C[k].get('step', {}).get('max') is not None]
        st.sort(); o['peak_step'] = dict(max=st[-1] if st else None, p95=st[int(0.95 * len(st))] if st else None, n_gt06=sum(v > 0.6 for v in st))
        if cid != 'v183ms':
            prod = {}
            for k in C:
                if not k[1].startswith(('f_V183', 'f_lx3')) or k not in B: continue
                for side, key in (('own', 'sales_me'), ('opp', 'sales_opp')):
                    for it, (u, rev) in C[k].get(key, {}).items(): prod.setdefault(it, {}).setdefault(side, []).append(rev)
                    for it, (u, rev) in B[k].get(key, {}).items(): prod.setdefault(it, {}).setdefault(side + '_b', []).append(rev)
            n = max(1, sum(1 for k in C if k[1].startswith(('f_V183', 'f_lx3')) and k in B))
            o['coins_vs_v183ms_per_game'] = {it: dict(own=round((sum(d.get('own', [])) - sum(d.get('own_b', []))) / n), opp=round((sum(d.get('opp', [])) - sum(d.get('opp_b', []))) / n)) for it, d in sorted(prod.items())}
        o['vals'] = spec['vals'].get(cid); out[cid] = o
    json.dump(out, open(f'out/val_{tag}.json', 'w'), indent=1)
    for cid, o in out.items():
        print('==', cid, o.get('vals'))
        for k, v in o.items():
            if k != 'vals': print('   ', k, v)
    return out
if __name__ == '__main__':
    if sys.argv[1] == 'report': report(sys.argv[2]); sys.exit()
    tag, cids = sys.argv[1], sys.argv[2:]; P = pods(); G = make(tag, cids, P)
    fin, dt = driver.run_gen(G, P, tmax=3600)
    for p in P: rsync_from(p, f"{RD}/out/val_{tag}/", f"out/val_{tag}/")
    print('finished', fin, round(dt)); report(tag)
