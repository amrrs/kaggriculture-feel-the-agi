import json, glob, math, collections
R = collections.defaultdict(list)
for f in sorted(glob.glob('kout/*/res.jsonl')):
    for l in open(f):
        if l.strip(): r = json.loads(l); r['k'] = f.split('/')[1]; R[r['k'][0]].append(r)
names = {'a': 'lx3ms vs lx3', 'b': 'lx3ms vs g012m', 'c': 'lx3 vs g012m (reference)'}
for p in sorted(R):
    rs = sorted(R[p], key=lambda r: r['seed']); ok = [r for r in rs if not r.get('error') and r.get('margin') is not None]
    n = len(ok); m = [r['margin'] for r in ok]
    mu = sum(m) / n if n else 0; se = (sum((x - mu) ** 2 for x in m) / (n - 1)) ** .5 / n ** .5 if n > 1 else float('nan')
    w = sum(r['win'] for r in ok)
    print(f"### {names[p]}: n={n} (errors {len(rs) - n}), wins {w:g}/{n} = {100 * w / max(1, n):.0f}%, mean margin {mu:+.0f} se {se:.0f}, "
          f"worst {min(m) if m else 0:+.0f}, cand peak step {max((r['cand_t']['peak'] for r in ok), default=0):.3f} s, "
          f"cand steps>0.6 s {sum(r['cand_t']['gt06'] for r in ok)}, opp peak {max((r['opp_t']['peak'] for r in ok), default=0):.3f} s\n")
    print('| seed | seat | cand | opp | margin | win | cand peak s (step) | cand first s | cand >0.6 | opp peak s | exc | wall s | kernel |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for r in rs:
        if r.get('error'): print(f"| {r['seed']} | {r['seat']} | ERROR {str(r['error'])[-200:]!r} |||||||||| {r['k']} |"); continue
        c = r['cand_t']; o = r['opp_t']
        print(f"| {r['seed']} | {r['seat']} | {r['coins']:.0f} | {r['opp_coins']:.0f} | {r['margin']:+.0f} | {r['win']:g} | {c['peak']:.3f} ({c['peak_at']}) | {c['first']:.3f} | {c['gt06']} | {o['peak']:.3f} | {r['cand_exc']}/{r['opp_exc']} | {r['wall']} | {r['k']} |")
    print()
