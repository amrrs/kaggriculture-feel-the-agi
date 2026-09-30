"""python dlog.py <game json>: per-day diagnostics of the rx candidate (h23 state, acts, idle, sells) + ledger"""
import sys, json
r = json.load(open(sys.argv[1]))
print('rewards', r['rewards'], 'seat', r['seat'], 'margin', r['margin'], 'err', r.get('nxerr'), 'peak', r['step'].get('max'))
if r.get('trace'): print(r['trace'][-1500:])
L = r.get('nxlog') or {}
for d in sorted(L, key=int):
    g = L[d]; h = g.get('h23') or {}
    print(f"d{int(d):2d} $%6s q%s herd %s tgt %s | an %s fed %s cared %s | pl %s wat %s crops %s | idle %d mv %d hires %d | acts %s | sold %s" % (
        h.get('money'), h.get('quads'), h.get('herd'), h.get('htgt'), h.get('anim'), h.get('fed'), h.get('cared'), h.get('plants'), h.get('watered'),
        h.get('crops'), g['idle'], g['moves'], g['hires'], g['acts'], g['sold']))
sm, so = r['sales_me'], r['sales_opp']
print('SALES me :', {k: (v[0], round(v[1])) for k, v in sorted(sm.items())}, 'tot', round(sum(v[1] for v in sm.values())))
print('SALES opp:', {k: (v[0], round(v[1])) for k, v in sorted(so.items())}, 'tot', round(sum(v[1] for v in so.values())))
print('BUYS me :', {k: (v[0], round(v[1])) for k, v in sorted(r['buys_me'].items())})
print('BUYS opp:', {k: (v[0], round(v[1])) for k, v in sorted(r['buys_opp'].items())})
