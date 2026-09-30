"""driver.py: CMA-ES generations over the pods (local side; no games run locally).
  python driver.py init            -> state/cma.json from space_final.json (x0 = base = z 0, sigma SIGMA0)
  python driver.py run [STOP_UTC]  -> loop: ask -> spec -> launch on every pod -> poll -> pull -> score -> tell -> log, until STOP (HH:MM UTC)
Per generation: LAM candidates + the CMA mean (+ in gen 0 the unchanged base 'mean' = ms_slot and v183ms as a control).
Work split by pod (fixed): each pod plays a fixed slice of the search tapes and a slice of this generation's fresh seeds for EVERY
candidate, plus v183ms vs V183 on its seeds (the fresh baseline); v183ms on its tape slice once (out/basetapes). Pairing is within pod.
Fresh seeds of generation g: 30001 + 12 g .. + 11, both seats, vs V183 and vs v183ms (never the holdout 19001-19048).
Everything evaluated goes to evals.jsonl (one line per candidate: gen, cid, z, values, components, score)."""
import os, sys, json, time, datetime, subprocess
import numpy as np
from common import *
import space, cma, eval_cand
ST = os.path.join(D, 'state'); os.makedirs(ST, exist_ok=True)
LAM = 12; SIGMA0 = 0.6; OAT_PER_GEN = 4          # 0.3 of the [-1, 1] range
NSEED = 36; SEED0 = 30001   # from gen 5: 24 distinct seeds, seat = seed % 2 (both seats of one seed mirror the same game)
def utc(): return datetime.datetime.now(datetime.timezone.utc)
def log(*a):
    s = utc().strftime('%H:%M:%S') + ' ' + ' '.join(str(x) for x in a); print(s, flush=True); open(os.path.join(ST, 'driver.log'), 'a').write(s + '\n')
def final_space():
    F = json.load(open(os.path.join(D, 'space_final.json')))
    for n, (lo, hi) in F.get('ranges', {}).items():
        k = list(space.KN[n]); k[4], k[5] = lo, hi; space.KN[n] = tuple(k)
    return F['knobs']
def partition(P):
    split = json.load(open(os.path.join(D, 'tape_split.json')))['search']
    wsum = sum(p['w'] for p in P); tp = {p['name']: [] for p in P}
    acc = 0.0; i = 0
    for p in P:
        acc += p['w'] / wsum; j = round(acc * len(split)); tp[p['name']] = split[i:j]; i = j
    return tp
def seeds_for(g, P):
    S = list(range(SEED0 + NSEED * g, SEED0 + NSEED * g + NSEED)) if g >= 7 else list(range(SEED0 + 24 * g, SEED0 + 24 * g + 24)) if g >= 5 else list(range(SEED0 + 12 * g, SEED0 + 12 * g + 12)); wsum = sum(p['w'] for p in P); out = {}; acc = 0.0; i = 0
    for p in P:
        acc += p['w'] / wsum; j = round(acc * len(S)); out[p['name']] = S[i:j]; i = j
    return out
def make_gen(g, cands, P, basetapes=False):
    """cands: {cid: vals}; writes gens/g{g}/jobs_<pod>.json + spec.json"""
    G = f'gens/g{g:03d}'; os.makedirs(G, exist_ok=True); TP = partition(P); SD = seeds_for(g, P)
    spec = {'gen': g, 'cands': cands, 'assign': {}, 'keys': {}, 'seeds': SD, 't': utc().isoformat()}
    for p in P:
        pn = p['name']; jobs = []; keys = []
        for t in TP[pn]:
            if not os.path.exists(f"out/basetapes/{pn}/{t['ep']}_{t['seat']}.json"): jobs.append(dict(k='tape', c=OPP['v183ms'], ep=t['ep'], seat=t['seat'], out=f"{RD}/out/basetapes/{pn}/{t['ep']}_{t['seat']}.json"))
        for s in SD[pn]:
            for se in (s % 2,): jobs.append(dict(k='fresh', c=OPP['v183ms'], o=OPP['V183'], seed=s, seat=se, out=f"{RD}/out/g{g:03d}/{pn}/base/f_V183_{s}_{se}.json"))
        for s in SD[pn]:
            for se in (s % 2,): keys += [f'f_V183_{s}_{se}', f'f_v183ms_{s}_{se}']
        keys += [f"t_{t['ep']}_{t['seat']}" for t in TP[pn]]
        cj = []
        for cid in cands:
            c = cand_path(cid) if cid in OPP else f'{RD}/cands/{cid}/main.py'
            for s in SD[pn]:
                for se in (s % 2,):
                    cj.append(dict(k='fresh', c=c, o=OPP['V183'], seed=s, seat=se, out=f"{RD}/out/g{g:03d}/{pn}/{cid}/f_V183_{s}_{se}.json"))
                    cj.append(dict(k='fresh', c=c, o=OPP['v183ms'], seed=s, seat=se, out=f"{RD}/out/g{g:03d}/{pn}/{cid}/f_v183ms_{s}_{se}.json"))
            for t in TP[pn]: cj.append(dict(k='tape', c=c, ep=t['ep'], seat=t['seat'], out=f"{RD}/out/g{g:03d}/{pn}/{cid}/t_{t['ep']}_{t['seat']}.json"))
        # interleave candidates (long fresh games first) so a late pod still has partial data for every candidate
        cj.sort(key=lambda j: (j['k'] != 'fresh',)); jobs += cj
        json.dump({'build': {cid: v for cid, v in cands.items() if cid not in OPP}, 'jobs': jobs}, open(f'{G}/jobs_{pn}.json', 'w'))
        spec['assign'][pn] = list(cands); spec['keys'][pn] = keys
    json.dump(spec, open(f'{G}/spec.json', 'w'), indent=0)
    return G
def run_gen(G, P, tmax=1800):
    t0 = time.time(); live = []
    for p in P:
        try: r = launch(p, f"{G}/jobs_{p['name']}.json"); ok = 'started' in r.stdout
        except Exception as ex: ok = False; log('launch fail', p['name'], ex)
        if ok: live.append(p)
        else: log('pod unavailable', p['name'])
    fin = {}; last = {}
    while len(fin) < len(live) and time.time() - t0 < tmax:
        time.sleep(20)
        for p in live:
            if p['name'] in fin: continue
            try: s = done(p, f"{G}/jobs_{p['name']}.json")
            except Exception: s = 'err'
            last[p['name']] = s
            if s == 'yes': fin[p['name']] = time.time() - t0
        # a pod that is >2.0x slower than the first finisher (and 5 min behind) is cut off; its partial games still count
        if fin and len(fin) < len(live) and time.time() - t0 > max(2.0 * min(fin.values()), min(fin.values()) + 300): break
    for p in live:
        if p['name'] not in fin:
            log('cut off', p['name'], last.get(p['name']))
            try: ssh(p, "pkill -f [p]od_run.py; pkill -f [a]t_game.py; pkill -f [t]j_game.py")
            except Exception: pass
    for p in live:
        try: rsync_from(p, f"{RD}/out/{G.split('/')[-1]}/", f"out/{G.split('/')[-1]}/"); rsync_from(p, f"{RD}/out/basetapes/", 'out/basetapes/')
        except Exception as ex: log('pull fail', p['name'], ex)
    return fin, time.time() - t0
def best_update(rows):
    f = os.path.join(ST, 'best.json'); B = json.load(open(f)) if os.path.exists(f) else []
    B = sorted(B + rows, key=lambda r: -r['comp']['score'])[:10]; json.dump(B, open(f, 'w'), indent=0); return B
def main():
    cmd = sys.argv[1]; knobs = final_space(); EP, CP = space.effective(); base = {n: space.base_value(n, EP, CP) for n in knobs}
    def vals_of(z): return {n: space.decode(n, zi, base[n]) for n, zi in zip(knobs, z) if space.decode(n, zi, base[n]) != base[n]}
    if cmd == 'init':
        c = cma.CMA(len(knobs), sigma=SIGMA0, lam=LAM, seed=int(sys.argv[2]) if len(sys.argv) > 2 else 1); c.save(os.path.join(ST, 'cma.json')); log('init', len(knobs), 'knobs'); return
    stop = sys.argv[2] if len(sys.argv) > 2 else '15:00'
    while True:
        now = utc()
        if now.strftime('%H:%M') >= stop: log('stop time reached'); break
        c = cma.CMA.load(os.path.join(ST, 'cma.json')); g = int(c.g); P = pods()
        X = c.ask(); cands = {}; Z = {}
        for i, x in enumerate(X): cid = f'g{g:03d}c{i:02d}'; cands[cid] = vals_of(x); Z[cid] = x
        mz = np.clip(c.m, -1, 1); cands[f'g{g:03d}m'] = vals_of(mz); Z[f'g{g:03d}m'] = mz
        if g == 0: cands['v183ms'] = None; Z['v183ms'] = None
        if g >= 6: cands[f'g{g:03d}b'] = {}; Z[f'g{g:03d}b'] = np.zeros(len(knobs))   # base control (ms_slot unchanged) every generation
        # one-at-a-time landscape probes (not told to CMA): OAT_PER_GEN per generation from state/oat_queue.json
        qf = os.path.join(ST, 'oat_queue.json'); Q = json.load(open(qf)) if os.path.exists(qf) else []
        for j, (kn, zz) in enumerate(Q[:OAT_PER_GEN]):
            z = np.zeros(len(knobs)); z[knobs.index(kn)] = zz; cid = f'g{g:03d}o{j}'; cands[cid] = vals_of(z); Z[cid] = z
        oat_used = Q[:OAT_PER_GEN]
        G = make_gen(g, {k: (v if v is not None else {}) for k, v in cands.items()}, P)
        log('gen', g, 'sigma %.3f' % c.sigma, len(cands), 'cands', {p: len(v) for p, v in json.load(open(f'{G}/spec.json'))['seeds'].items()})
        fin, dt = run_gen(G, P)
        if oat_used: json.dump(Q[OAT_PER_GEN:], open(qf, 'w'))
        spec = json.load(open(f'{G}/spec.json')); R, BT = eval_cand.gen_results(G.split('/')[-1]); E = eval_cand.expected(spec)
        rows = []
        for cid in cands:
            e = {pod: ks for pod, ks in E.get(cid, {}).items() if pod in fin}
            comp = eval_cand.score(cid, R, BT, e)
            rows.append(dict(gen=g, cid=cid, z=None if Z[cid] is None else [round(float(v), 4) for v in Z[cid]], vals=cands[cid], comp=comp, t=utc().strftime('%H:%M')))
        with open(os.path.join(D, 'evals.jsonl'), 'a') as f:
            for r in rows: f.write(json.dumps(r) + '\n')
        sc = {r['cid']: r['comp']['score'] for r in rows}
        c.tell([Z[f'g{g:03d}c{i:02d}'] for i in range(LAM)], [-sc[f'g{g:03d}c{i:02d}'] for i in range(LAM)]); c.save(os.path.join(ST, 'cma.json'))
        B = best_update([r for r in rows if r['cid'] != 'v183ms'])
        log('gen', g, 'done in %.0fs' % dt, 'fin', {k: round(v) for k, v in fin.items()}, 'best-of-gen', max(sc.items(), key=lambda kv: kv[1]),
            'mean', sc[f'g{g:03d}m'], 'overall best', B[0]['cid'], B[0]['comp']['score'])
if __name__ == '__main__':
    main()
