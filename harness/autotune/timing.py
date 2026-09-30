"""timing.py <pod-name> <cid> [...]: low-load peak-step check - each cid and v183ms play V183 on seeds 19901-19912 (seat = seed % 2),
8 processes at a time on one 32-vCPU pod (vs 26-32 during search/validation); prints per-build peak / p99 / n > 0.6 s."""
import sys, json, os, time
from common import *
import validate, driver
pn, cids = sys.argv[1], sys.argv[2:]
P = [p for p in pods() if p['name'] == pn]
G = 'gens/timing'; os.makedirs(G, exist_ok=True); jobs = []
for cid in ['v183ms'] + cids:
    for s in range(19901, 19913): jobs.append(dict(k='fresh', c=cand_path(cid), o=OPP['V183'], seed=s, seat=s % 2, out=f"{RD}/out/timing/{pn}/{cid}/f_V183_{s}_{s % 2}.json"))
json.dump({'build': {c: validate.cand_vals(c) for c in cids}, 'jobs': jobs}, open(f'{G}/jobs_{pn}.json', 'w'))
P[0]['w'] = 8; fin, dt = driver.run_gen(G, P, tmax=1800)
rsync_from(P[0], f"{RD}/out/timing/", 'out/timing/')
import glob
for cid in ['v183ms'] + cids:
    T = []; mx = []
    for f in glob.glob(f'out/timing/{pn}/{cid}/*.json'):
        d = json.load(open(f)); T += d['hs'] and []; mx.append(d['step']['max'])
        T.append(d['step'])
    print(cid, 'games', len(mx), 'peak max %.3f' % max(mx), 'median game max %.3f' % sorted(mx)[len(mx) // 2], 'n>0.6', sum(s['n_gt06'] for s in T), 'mean p99 %.3f' % (sum(s['p99'] for s in T) / len(T)))
