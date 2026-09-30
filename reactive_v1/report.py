"""python report.py <outdir> [<outdir> ...] [--base TAG]  : per tag@opp: n, win%, margin (se), own/opp coins, worst, peak step,
errors; paired d vs the base tag's games vs the same opp (same seed/seat); per-product own/opp revenue; coverage (fed/cared per
animal-day, watered per plant-day d11-28, from the candidate's own day log; only for rx builds) and idle/moves per day."""
import sys, json, glob, math, collections
args = [a for a in sys.argv[1:] if not a.startswith('--')]
base = sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else 'v183ms'
if base in args: args.remove(base)
R = collections.defaultdict(dict)
for D in args:
    for f in glob.glob(D + '/*.json'):
        try: r = json.load(open(f))
        except Exception: continue
        b_ = f.split('/')[-1][:-5]; tag, rest = b_.split('_vs_'); opp = rest.rsplit('_', 2)[0]
        R[(tag, opp)][(r['seed'], r['seat'])] = r
def ms(x):
    n = len(x); m = sum(x) / n if n else 0
    return m, (math.sqrt(sum((v - m) ** 2 for v in x) / (n - 1) / n) if n > 1 else 0)
PR = ['WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER']
for (tag, opp) in sorted(R):
    G = R[(tag, opp)]; ks = sorted(G); mar = [G[k]['margin'] for k in ks if G[k]['margin'] is not None]
    if not mar: continue
    own = [G[k]['rewards'][k[1]] for k in ks]; op_ = [G[k]['rewards'][1 - k[1]] for k in ks]
    wins = sum((G[k]['win'] or 0) > 0 for k in ks) / len(ks)
    m, se = ms(mar); pk = max(G[k]['step'].get('max', 0) for k in ks)
    err = sum(((G[k].get('nxerr') or [0])[0] or 0) for k in ks if isinstance((G[k].get('nxerr') or [0])[0], int))
    B = R.get((base, opp), {})
    pd = [G[k]['margin'] - B[k]['margin'] for k in ks if k in B and B[k]['margin'] is not None]
    po = [G[k]['rewards'][k[1]] - B[k]['rewards'][k[1]] for k in ks if k in B]
    pm, pse = ms(pd) if pd else (0, 0); pom, pose = ms(po) if po else (0, 0)
    print(f"{tag}@{opp}: n={len(ks)} win={100*wins:.1f}% margin={m:+.0f} ({se:.0f}) own={sum(own)/len(own):.0f} opp={sum(op_)/len(op_):.0f} worst={min(mar):+.0f} peak={pk:.3f}s err={err}"
          + (f" | paired vs {base}@{opp}: margin {pm:+.0f} ({pse:.0f}) own {pom:+.0f} ({pose:.0f}) n={len(pd)} better={sum(d > 0 for d in pd)}" if pd and tag != base else ''))
    rv = {p: [0, 0, 0, 0] for p in PR}
    for k in ks:
        for p in PR:
            a = G[k]['sales_me'].get(p, [0, 0]); b = G[k]['sales_opp'].get(p, [0, 0])
            rv[p][0] += a[0]; rv[p][1] += a[1]; rv[p][2] += b[0]; rv[p][3] += b[1]
    n = len(ks)
    print('   rev own/opp k (units): ' + ', '.join(f"{p[:5]} {rv[p][1]/n/1000:.1f}/{rv[p][3]/n/1000:.1f} ({rv[p][0]/n:.0f}/{rv[p][2]/n:.0f})" for p in PR))
    bu = collections.Counter(); bo = collections.Counter()
    for k in ks:
        for kk, v in G[k]['buys_me'].items(): bu[kk.split(':')[0]] += v[1]
        for kk, v in G[k]['buys_opp'].items(): bo[kk.split(':')[0]] += v[1]
    print('   spend own/opp k: ' + ', '.join(f"{kk} {bu[kk]/n/1000:.1f}/{bo[kk]/n/1000:.1f}" for kk in sorted(set(bu) | set(bo))))
    cov = [0, 0, 0, 0, 0, 0]; idle = mv = nd = 0
    for k in ks:
        L = G[k].get('nxlog') or {}
        for d, g in L.items():
            d = int(d); h = g.get('h23')
            if 11 <= d <= 28 and h:
                cov[0] += h['anim']; cov[1] += h['fed']; cov[2] += h['cared']; cov[3] += h['plants']; cov[4] += h['watered']
            if 11 <= d <= 28: idle += g.get('idle', 0); mv += g.get('moves', 0); nd += 1
    if cov[0]:
        print(f"   coverage d11-28: fed {cov[1]/cov[0]:.2f} cared {cov[2]/cov[0]:.2f} watered {cov[4]/max(1,cov[3]):.2f} | animals/day {cov[0]/nd:.1f} plants/day {cov[3]/nd:.1f} | idle {idle/nd:.0f} moves {mv/nd:.0f} unit-steps/day")
# losses: plants weeded overnight / animals escaped (rx builds only)
for (tag, opp) in sorted(R):
    G = R[(tag, opp)]; w = e = wv = n = 0
    for k, r in G.items():
        for d, g in (r.get('nxlog') or {}).items():
            w += g.get('weeded', 0); wv += g.get('weeded_v', 0); e += g.get('escaped', 0)
        n += 1
    if n and (w or e): print(f"{tag}@{opp}: per game plants weeded {w/n:.1f} (value ~{wv/n:.0f}), animals escaped {e/n:.1f}")
