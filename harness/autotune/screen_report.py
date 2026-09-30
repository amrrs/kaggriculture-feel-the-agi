"""screen report: per knob variant vs the base (same pod, det mode): digest changed on both seeds?, first divergent step, #steps differing, margin delta."""
import json, glob, os, collections
R = {}
for f in glob.glob('out/screen/*/*.json'):
    pod = f.split('/')[2]; d = json.load(open(f)); c = os.path.basename(f).rsplit('_', 2)[0]
    R[(pod, c, d['seed'])] = d
bases = {(k[0], k[2]): v for k, v in R.items() if k[1] == 'base'}
print('base digests by pod/seed:', {k: (v['digest'], v['margin']) for k, v in sorted(bases.items())})
ref = {s: bases.get(('p1', s)) or next(v for k, v in bases.items() if k[1] == s) for s in (20001, 20002)}
rows = collections.defaultdict(dict)
for (pod, c, s), d in R.items():
    if c == 'base': continue
    b = ref[s]; hs, hb = d['hs'], b['hs']
    diff = [i for i in range(min(len(hs), len(hb))) if hs[i] != hb[i]]
    rows[c][s] = dict(chg=d['digest'] != b['digest'], first=diff[0] if diff else None, n=len(diff), dm=d['margin'] - b['margin'], ok=d['status'])
live = {}
for c in sorted(rows):
    r = rows[c]; k = c[2:].rsplit('_', 1)[0]
    ch = all(r.get(s, {}).get('chg') for s in (20001, 20002))
    live.setdefault(k, []).append(ch)
    print('%-26s %s' % (c, '  '.join('%s first %4s n %3d dm %+6d' % ('CHG' if r[s]['chg'] else 'same', r[s]['first'], r[s]['n'], r[s]['dm']) if s in r else 'missing' for s in (20001, 20002))))
L = sorted(k for k, v in live.items() if any(v)); Dd = sorted(k for k, v in live.items() if not any(v))
print('\nLIVE (some variant changes both seeds):', len(L), L); print('DEAD:', len(Dd), Dd)
json.dump({'live': L, 'dead': Dd, 'rows': rows}, open('out/screen_summary.json', 'w'), indent=0)
