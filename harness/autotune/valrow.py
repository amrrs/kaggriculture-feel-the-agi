"""valrow.py <tag>: one markdown row per candidate of out/val_<tag>.json"""
import json, sys
o = json.load(open(f'out/val_{sys.argv[1]}.json'))
for c, d in o.items():
    f = lambda k: d.get(k, {})
    h, v, l, t = f('v183ms'), f('V183'), f('lx3'), f('tapes_holdout')
    worst = min([f(k).get('worst', 0) for k in ('V183', 'v183ms', 'lx3') if f(k)])
    print(f"| {c} | {('%+d (%d), %.3f' % (h['paired'], h['paired_se'], h['win'])) if h.get('paired') is not None else '0'} | "
          f"{('%+d (%d), %.3f' % (v['paired'], v['paired_se'], v['win'])) if v.get('paired') is not None else 'win %.3f' % v.get('win', 0)} | "
          f"{('%+d (%d), %.3f' % (l['paired'], l['paired_se'], l['win'])) if l.get('paired') is not None else 'win %.3f' % l.get('win', 0)} | "
          f"{'%+d (%d), %d' % (t.get('paired', 0), t.get('se', 0), t.get('wins', 0))} | {worst} | {d['peak_step']['max']:.3f} / {d['peak_step']['p95']:.3f} |")
