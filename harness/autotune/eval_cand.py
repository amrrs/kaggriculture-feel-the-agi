"""eval_cand.py: objective of every candidate of a generation (paired, common random numbers, per pod).
  python eval_cand.py <gen>      prints the table; used by driver.py (score_gen)
Components (all paired vs v183ms on the SAME pod, same tape / seed / seat):
  T   = mean over search tapes of (cand margin - v183ms margin)            [top-field paired margin, coins]
  TB  = the same over both-intact tapes;  TW = cand tape wins - v183ms tape wins (same tapes)
  FV  = paired margin vs V183 (cand margin - v183ms margin vs V183, fresh seeds of this generation)
  WV  = cand win-rate vs V183 - v183ms win-rate vs V183;  WH = cand win-rate vs v183ms - 0.5;  MH = H2H margin vs v183ms
  score = 0.5 x T/300 + 0.3 x ((WV + WH)/2)/0.10 + 0.2 x TW/4 - 0.25 x (#fresh games < -15k) - 0.25 x (#tapes with paired < -15k)
          - 1.0 if p95 of per-game peak step > 0.55 s and > v183ms's p95 + 0.03 s.
Crashed / unfinished games count as margin -20000, loss."""
import os, sys, json, glob, math
BAD = -20000
def load(pat):
    out = {}
    for f in glob.glob(pat):
        try: out[f] = json.load(open(f))
        except Exception: pass
    return out
def mse(x):
    n = len(x)
    if n == 0: return (0.0, 0.0, 0)
    m = sum(x) / n; s = math.sqrt(sum((v - m) ** 2 for v in x) / (n - 1) / n) if n > 1 else 0.0
    return (m, s, n)
def wr(w): return (1.0 if w > 0 else 0.5 if w == 0 else 0.0)
def p95(L):
    L = sorted(L); return L[min(len(L) - 1, int(0.95 * len(L)))] if L else 0.0
def gen_results(gen, out='out'):
    """-> {cid: {'tape': {(pod,ep,seat): d}, 'fresh': {(pod,opp,seed,seat): d}}}, base tapes, base fresh"""
    R = {}
    for f in glob.glob(f'{out}/{gen}/*/*/*.json'):
        pod, cid, fn = f.split('/')[-3:]
        try: d = json.load(open(f))
        except Exception: continue
        R.setdefault(cid, {}).setdefault(pod, {})[fn[:-5]] = d
    BT = {}
    for f in glob.glob(f'{out}/basetapes/*/*.json'):
        pod, fn = f.split('/')[-2:]
        try: BT[(pod, fn[:-5])] = json.load(open(f))
        except Exception: pass
    return R, BT
def score(cid, R, BT, expect=None):
    C = R.get(cid, {}); B = R.get('base', {})
    T, TB, tw_c, tw_b, tbad = [], [], 0, 0, 0
    FV, WVc, WVb, WH, MH, bad, steps, bsteps = [], [], [], [], [], 0, [], []
    exp = expect or {}
    for pod, games in C.items():
        keys = set(games) | set(exp.get(pod, ()))
        for k in keys:
            d = games.get(k)
            m = d['margin'] if d and d.get('margin') is not None else BAD
            if k.startswith('t_'):
                b = BT.get((pod, k[2:]))
                if not b or b.get('margin') is None: continue
                dd = m - b['margin']; T.append(dd); tbad += dd < -15000
                if d and d.get('intact') and b.get('intact'): TB.append(dd)
                tw_c += m > 0; tw_b += b['margin'] > 0
            else:
                _, opp, seed, seat = k.split('_')
                w = d['win'] if d and d.get('win') is not None else -1
                if d and d.get('step', {}).get('max') is not None: steps.append(d['step']['max'])
                bad += m < -15000
                if opp == 'V183':
                    b = B.get(pod, {}).get(k)
                    if not b or b.get('margin') is None: continue
                    FV.append(m - b['margin']); WVc.append(wr(w)); WVb.append(wr(b['win']))
                else:
                    WH.append(wr(w)); MH.append(m)
    for pod, games in B.items():
        for k, b in games.items():
            if b.get('step', {}).get('max') is not None: bsteps.append(b['step']['max'])
    t, tse, tn = mse(T); tb, tbse, tbn = mse(TB); fv, fvse, fvn = mse(FV); mh, mhse, mhn = mse(MH)
    wv = (sum(WVc) - sum(WVb)) / len(WVc) if WVc else 0.0; wh = (sum(WH) / len(WH) - 0.5) if WH else 0.0
    tw = tw_c - tw_b; pk, pkb = p95(steps), p95(bsteps)
    pen = 0.25 * bad + 0.25 * tbad + (1.0 if pk > 0.55 and pk > pkb + 0.03 else 0.0)
    sc = 0.5 * t / 300 + 0.3 * ((wv + wh) / 2) / 0.10 + 0.2 * tw / 4 - pen
    return dict(score=round(sc, 4), T=round(t, 1), T_se=round(tse, 1), T_n=tn, TB=round(tb, 1), TB_se=round(tbse, 1), TB_n=tbn, TW=tw, tw_c=tw_c, tw_b=tw_b,
                FV=round(fv, 1), FV_se=round(fvse, 1), FV_n=fvn, WV=round(wv, 4), WH=round(wh, 4), MH=round(mh, 1), MH_se=round(mhse, 1), MH_n=mhn,
                bad=bad, tbad=tbad, pk95=round(pk, 3), pk95_base=round(pkb, 3), pkmax=round(max(steps), 3) if steps else None, pen=pen)
def expected(spec):
    """{cid: {pod: [game keys]}} from a generation spec (so missing games count as crashes)."""
    E = {}
    for pod, cids in spec['assign'].items():
        for cid in cids: E.setdefault(cid, {})[pod] = spec['keys'][pod]
    return E
if __name__ == '__main__':
    gen = sys.argv[1]; spec = json.load(open(f'gens/{gen}/spec.json')); R, BT = gen_results(gen); E = expected(spec)
    for cid in spec['cands']:
        print(cid, score(cid, R, BT, E.get(cid)))
