"""fresh_score.py <cand> <opp> <seed_lo> <seed_hi> [--base v183ms] [--json]: score fresh-seed games out/**/<cand>_vs_<opp>_<seed>_<seat>.json.
Prints n, distinct games (a seat-0/seat-1 pair on one seed with identical rewards counts once), wins/draws/losses, margin (se over all; se over
seed-means), worst game, per-product SELL revenue (own/opp, k/game), peak/p99 step, steps>0.6 s, non-DONE, .err files.
--base B: paired d = cand margin - B's margin vs the same opp on the same seed/seat."""
import json, glob, os, sys, math, collections
H = os.path.dirname(os.path.abspath(__file__))
a = [x for x in sys.argv[1:] if not x.startswith('--')]
cand, opp, lo, hi = a[0], a[1], int(a[2]), int(a[3])
base = sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else None
if base: a.remove(base)
def load(c, o):
    R = {}; E = []
    for s in range(lo, hi + 1):
        for se in (0, 1):
            fs = glob.glob(f'{H}/out/**/{c}_vs_{o}_{s}_{se}.json', recursive=True)
            es = glob.glob(f'{H}/out/**/{c}_vs_{o}_{s}_{se}.json.err', recursive=True)
            if es and os.path.getsize(es[0]) > 0: E.append((s, se, open(es[0]).read()[-300:]))
            if fs:
                try: R[(s, se)] = json.load(open(fs[0]))
                except Exception: pass
    return R, E
def ms(x):
    n = len(x); m = sum(x) / n if n else 0
    return m, (math.sqrt(sum((v - m) ** 2 for v in x) / (n - 1) / n) if n > 1 else 0)
C, E = load(cand, opp)
out = dict(cand=cand, opp=opp, seeds=f'{lo}-{hi}', n=len(C), expected=2 * (hi - lo + 1), errs=len(E))
ok = {k: r for k, r in C.items() if r.get('margin') is not None}
bad = [(k, r['status']) for k, r in C.items() if r['status'][r['seat']] != 'DONE' or r.get('margin') is None]
mg = [r['margin'] for r in ok.values()]
if mg:
    m, se = ms(mg); bys = collections.defaultdict(list)
    for (s, _), r in ok.items(): bys[s].append(r['margin'])
    m2, se2 = ms([sum(v) / len(v) for v in bys.values()])
    dist = len({(s, r['rewards'][r['seat']], r['rewards'][1 - r['seat']]) for (s, _), r in ok.items()})
    w = sum(x > 0 for x in mg); d = sum(x == 0 for x in mg)
    wk = min(ok, key=lambda k: ok[k]['margin'])
    peak = max(r['step']['max'] for r in ok.values()); p99 = max(r['step']['p99'] for r in ok.values()); n06 = sum(r['step']['n_gt06'] for r in ok.values())
    n09 = sum(sum(t > 0.9 for t in r.get('times', [])) for r in ok.values())
    out.update(distinct=dist, wins=w, draws=d, losses=len(mg) - w - d, winrate=round(100 * (w + 0.5 * d) / len(mg), 1), margin=round(m), se=round(se),
               se_seed=round(se2), worst=ok[wk]['margin'], worst_at=wk, peak=peak, p99max=p99, n_gt06=n06, n_gt09=n09,
               ovg_min=min(float(r['overage_left'].get(str(r['seat']), 60) or 0) for r in ok.values()))
    P = collections.defaultdict(lambda: [0, 0])
    for r in ok.values():
        for it, (u, v) in r['sales_me'].items(): P[it][0] += v
        for it, (u, v) in r['sales_opp'].items(): P[it][1] += v
    out['prod'] = {it: (round(v[0] / len(ok)), round(v[1] / len(ok))) for it, v in sorted(P.items())}
    if base:
        B, _ = load(base, opp); ks = sorted(k for k in ok if k in B and B[k].get('margin') is not None)
        dd = [ok[k]['margin'] - B[k]['margin'] for k in ks]
        if dd:
            pm, pse = ms(dd); out.update(base=base, paired_n=len(ks), paired=round(pm), paired_se=round(pse), better=sum(x > 0 for x in dd), worse=sum(x < 0 for x in dd),
                                         base_winrate=round(100 * sum((B[k]['margin'] > 0) + 0.5 * (B[k]['margin'] == 0) for k in ks) / len(ks), 1),
                                         base_margin=round(sum(B[k]['margin'] for k in ks) / len(ks)))
            Q = collections.defaultdict(lambda: [0, 0])
            for k in ks:
                for it in set(ok[k]['sales_me']) | set(B[k]['sales_me']): Q[it][0] += ok[k]['sales_me'].get(it, [0, 0])[1] - B[k]['sales_me'].get(it, [0, 0])[1]
                for it in set(ok[k]['sales_opp']) | set(B[k]['sales_opp']): Q[it][1] += ok[k]['sales_opp'].get(it, [0, 0])[1] - B[k]['sales_opp'].get(it, [0, 0])[1]
            out['prod_d'] = {it: (round(v[0] / len(ks)), round(v[1] / len(ks))) for it, v in sorted(Q.items())}
out['bad'] = bad[:5]; out['err_tail'] = E[:3]
if '--json' in sys.argv: print(json.dumps(out, default=str)); sys.exit()
print(f"{cand} vs {opp} seeds {lo}-{hi} both seats: n={out['n']}/{out['expected']}" + (f" distinct {out['distinct']} | W/D/L {out['wins']}/{out['draws']}/{out['losses']} = {out['winrate']}% | margin {out['margin']:+d} (se {out['se']}; se over seed-means {out['se_seed']}) | worst {out['worst']:+d} at {out['worst_at']} | peak step {out['peak']:.3f} s, max p99 {out['p99max']:.3f}, steps>0.6 {out['n_gt06']}, >0.9 {out['n_gt09']}, min overage left {out['ovg_min']:.1f}" if mg else ''))
if base and 'paired' in out:
    print(f"  PAIRED vs {base}'s games vs {opp}: n={out['paired_n']} d {out['paired']:+d} (se {out['paired_se']}, z {out['paired'] / max(1, out['paired_se']):.1f}) better/worse {out['better']}/{out['worse']} | {base}: {out['base_winrate']}% margin {out['base_margin']:+d}")
if mg: print('  per-product revenue own/opp (coins/game): ' + ', '.join(f"{k[:5]} {v[0]}/{v[1]}" for k, v in out['prod'].items()))
if 'prod_d' in out: print(f'  per-product delta vs {base} own/opp: ' + ', '.join(f"{k[:5]} {v[0]:+d}/{v[1]:+d}" for k, v in out['prod_d'].items()))
if bad or E: print('  NON-DONE/ERR:', bad[:5], [(s, se, t[-200:]) for s, se, t in E[:2]])
