import json, glob, collections
R = collections.defaultdict(list); D = []
for f in sorted(glob.glob('kout/t*/res.jsonl')) + sorted(glob.glob('kout/dg/res.jsonl')):
    for l in open(f):
        if not l.strip(): continue
        r = json.loads(l); r['k'] = f.split('/')[1]
        (D if r['k'] == 'dg' else R[(r['cand'], r['opp'])]).append(r)
print('| variant vs opp | n | wins | win % | mean margin (se) | worst | cand peak s | cand >0.6 | errors |'); print('|---|---|---|---|---|---|---|---|---|')
for key in sorted(R):
    rs = R[key]; ok = [r for r in rs if not r.get('error')]; n = len(ok); m = [r['margin'] for r in ok]
    mu = sum(m) / n if n else 0; se = (sum((x - mu) ** 2 for x in m) / (n - 1)) ** .5 / n ** .5 if n > 1 else float('nan'); w = sum(r['win'] for r in ok)
    print(f"| {key[0][:-3]} vs {key[1][:-3]} | {n} | {w:g} | {100 * w / max(1, n):.0f}% | {mu:+.0f} ({se:.0f}) | {min(m, default=0):+.0f} | "
          f"{max((r['cand_t']['peak'] for r in ok), default=0):.3f} | {sum(r['cand_t']['gt06'] for r in ok)} | {len(rs) - n} |")
if D:
    base = [r.get('dig') for r in D if r['cand'] == 'lx3ms.py']
    print(f'\nDigest check (seed 20101, cand seat 1, vs lx3ms): baseline lx3ms digests {base} (deterministic: {len(set(base)) == 1})')
    for r in D:
        if r['cand'] != 'lx3ms.py': print(f"- {r['cand'][2:-3]}: {'LIVE' if r.get('dig') not in base else 'DEAD (identical actions)'}  dig {r.get('dig')} margin {r.get('margin', 0):+.0f} {r.get('error', '')[:100]}")
print()
for key in sorted(R):
    print(f'{key[0]} vs {key[1]}: ' + ', '.join(f"{r['seed']}/{r['seat']} {r['margin']:+.0f}" if not r.get('error') else f"{r['seed']} ERR" for r in sorted(R[key], key=lambda r: r['seed'])))
