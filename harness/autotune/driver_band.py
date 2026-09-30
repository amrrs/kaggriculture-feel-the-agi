"""driver_band.py: CMA-ES with the BAND objective (coordinator 12:35): win the >= 2850 band.
  python driver_band.py init        -> state/cma_band.json: mean = g012m's z, sigma 0.2, lambda 12, generation counter from 100
  python driver_band.py run [STOP]  -> generations until STOP (HH:MM UTC); every 2 generations a holdout validation (validate.py) of the
                                       current mean + best sample of those 2 generations, with g012m as the reference
Objective per candidate (paired vs v183ms within pod):
  band tapes = the 44 search tapes of M & M & P & Q, DSM, DECEM, Victor @ Tufa Labs, Unknown Mother-Goose (band_split.json; Boey / CDE have
  no tapes; 16 band tapes held out = the ones never used by any search)
  score = 0.7 x BW / 2 + 0.3 x BM / 500 - tail/step penalties, BW = cand band-tape wins - v183ms wins, BM = band paired margin;
  CONSTRAINTS: FV (paired vs V183, fresh) < -300 or MH (H2H vs v183ms, fresh) < -300 -> score = -1000 (rejected).
Fresh games per generation: 36 distinct seeds (seat = seed % 2) vs V183 and vs v183ms, block 40001 + 36 (g - 100).
Validation round k (after generations 101, 103, ...): seeds 19301 + 48 k .. + 47 (seat = seed % 2) vs V183 / v183ms / lx3 + the 16 held-out band tapes."""
import os, sys, json, time, datetime
import numpy as np
from common import *
import space, cma, eval_cand, driver, validate
ST = driver.ST; LAM = 12; NSEED = 36; SEED0 = 40001; G0 = 100
BAND = json.load(open(os.path.join(D, 'band_split.json')))
log = driver.log
def part(L, P):
    wsum = sum(p['w'] for p in P); out = {}; acc = 0.0; i = 0
    for p in P:
        acc += p['w'] / wsum; j = round(acc * len(L)); out[p['name']] = L[i:j]; i = j
    return out
def make_gen(g, cands, P):
    G = f'gens/g{g:03d}'; os.makedirs(G, exist_ok=True)
    TP = part(BAND['search'], P); S = list(range(SEED0 + NSEED * (g - G0), SEED0 + NSEED * (g - G0) + NSEED)); SD = part(S, P)
    spec = {'gen': g, 'obj': 'band', 'cands': cands, 'assign': {}, 'keys': {}, 'seeds': SD, 't': driver.utc().isoformat()}
    for p in P:
        pn = p['name']; jobs = []; keys = []
        for t in TP[pn]:
            if not os.path.exists(f"out/basetapes/{pn}/{t['ep']}_{t['seat']}.json"): jobs.append(dict(k='tape', c=OPP['v183ms'], ep=t['ep'], seat=t['seat'], out=f"{RD}/out/basetapes/{pn}/{t['ep']}_{t['seat']}.json"))
        for s in SD[pn]:
            jobs.append(dict(k='fresh', c=OPP['v183ms'], o=OPP['V183'], seed=s, seat=s % 2, out=f"{RD}/out/g{g:03d}/{pn}/base/f_V183_{s}_{s % 2}.json"))
            keys += [f'f_V183_{s}_{s % 2}', f'f_v183ms_{s}_{s % 2}']
        keys += [f"t_{t['ep']}_{t['seat']}" for t in TP[pn]]
        cj = []
        for cid in cands:
            c = f'{RD}/cands/{cid}/main.py'
            for s in SD[pn]:
                cj.append(dict(k='fresh', c=c, o=OPP['V183'], seed=s, seat=s % 2, out=f"{RD}/out/g{g:03d}/{pn}/{cid}/f_V183_{s}_{s % 2}.json"))
                cj.append(dict(k='fresh', c=c, o=OPP['v183ms'], seed=s, seat=s % 2, out=f"{RD}/out/g{g:03d}/{pn}/{cid}/f_v183ms_{s}_{s % 2}.json"))
            for t in TP[pn]: cj.append(dict(k='tape', c=c, ep=t['ep'], seat=t['seat'], out=f"{RD}/out/g{g:03d}/{pn}/{cid}/t_{t['ep']}_{t['seat']}.json"))
        cj.sort(key=lambda j: j['k'] != 'fresh'); jobs += cj
        json.dump({'build': cands, 'jobs': jobs}, open(f'{G}/jobs_{pn}.json', 'w'))
        spec['assign'][pn] = list(cands); spec['keys'][pn] = keys
    json.dump(spec, open(f'{G}/spec.json', 'w'), indent=0); return G
def band_score(comp):
    BW, BM = comp['TW'], comp['T']
    sc = 0.7 * BW / 2 + 0.3 * BM / 500 - comp['pen']
    rej = comp['FV_n'] > 0 and comp['FV'] < -300 or comp['MH_n'] > 0 and comp['MH'] < -300
    return round(-1000.0 if rej else sc, 4), rej
def validate_round(k, cids, P):
    games = [(s, s % 2) for s in range(19301 + 48 * k, 19301 + 48 * k + 48)]
    allt = [dict(t, hold=1) for t in BAND['holdout']]
    tag = f'b{k}'; G = validate.make(tag, cids, P, games=games, allt=allt)
    fin, dt = driver.run_gen(G, P, tmax=1800)
    out = validate.report(tag); log('validation', tag, 'done in %.0fs' % dt, {c: (o.get('v183ms', {}).get('paired'), o.get('tapes_holdout', {}).get('wins'), o.get('tapes_holdout', {}).get('base_wins'), o.get('tapes_holdout', {}).get('paired')) for c, o in out.items()})
    return out
def main():
    cmd = sys.argv[1]; knobs = driver.final_space(); EP, CP = space.effective(); base = {n: space.base_value(n, EP, CP) for n in knobs}
    def vals_of(z): return {n: space.decode(n, zi, base[n]) for n, zi in zip(knobs, z) if space.decode(n, zi, base[n]) != base[n]}
    cf = os.path.join(ST, 'cma_band.json')
    if cmd == 'init':
        z0 = next(json.loads(l)['z'] for l in open('evals.jsonl') if json.loads(l)['cid'] == 'g012m')
        c = cma.CMA(len(knobs), x0=z0, sigma=0.2, lam=LAM, seed=7); c.g = G0; c.save(cf); log('band init at g012m z, sigma 0.2'); return
    stop = sys.argv[2] if len(sys.argv) > 2 else '15:00'; recent = []
    while driver.utc().strftime('%H:%M') < stop:
        c = cma.CMA.load(cf); g = int(c.g); P = pods()
        X = c.ask(); cands = {}; Z = {}
        for i, x in enumerate(X): cid = f'g{g:03d}c{i:02d}'; cands[cid] = vals_of(x); Z[cid] = x
        mz = np.clip(c.m, -1, 1); cands[f'g{g:03d}m'] = vals_of(mz); Z[f'g{g:03d}m'] = mz
        cands[f'g{g:03d}b'] = {}; Z[f'g{g:03d}b'] = np.zeros(len(knobs))
        cands[f'g{g:03d}r'] = vals_of(np.array(next(json.loads(l)['z'] for l in open('evals.jsonl') if json.loads(l)['cid'] == 'g012m')))  # g012m reference
        Z[f'g{g:03d}r'] = None
        G = make_gen(g, cands, P); log('band gen', g, 'sigma %.3f' % c.sigma, len(cands), 'cands')
        fin, dt = driver.run_gen(G, P)
        spec = json.load(open(f'{G}/spec.json')); R, BT = eval_cand.gen_results(G.split('/')[-1]); E = eval_cand.expected(spec); rows = []
        for cid in cands:
            comp = eval_cand.score(cid, R, BT, {pod: ks for pod, ks in E.get(cid, {}).items() if pod in fin})
            bs, rej = band_score(comp); comp['band_score'] = bs; comp['rejected'] = rej
            rows.append(dict(gen=g, obj='band', cid=cid, z=None if Z[cid] is None else [round(float(v), 4) for v in Z[cid]], vals=cands[cid], comp=comp, t=driver.utc().strftime('%H:%M')))
        with open(os.path.join(D, 'evals.jsonl'), 'a') as f:
            for r in rows: f.write(json.dumps(r) + '\n')
        sc = {r['cid']: r['comp']['band_score'] for r in rows}
        c.tell([Z[f'g{g:03d}c{i:02d}'] for i in range(LAM)], [-sc[f'g{g:03d}c{i:02d}'] for i in range(LAM)]); c.save(cf)
        rb = {r['cid']: (r['comp']['TW'], r['comp']['T'], r['comp']['MH'], r['comp']['FV'], r['comp']['rejected']) for r in rows if r['cid'][-1] in 'mbr'}
        log('band gen', g, 'done in %.0fs' % dt, 'best', max(sc.items(), key=lambda kv: kv[1]), 'mean/base/ref (BW, BM, MH, FV, rej):', rb)
        recent += [r for r in rows if r['cid'][-1] not in 'br']
        if (g - G0) % 2 == 1:
            best = max((r for r in recent if r['cid'][-1] != 'm'), key=lambda r: r['comp']['band_score'])
            try: validate_round((g - G0) // 2, [f'g{g:03d}m', best['cid'], 'g012m'], P)
            except Exception as ex: log('validation fail', ex)
            recent = []
if __name__ == '__main__':
    main()
