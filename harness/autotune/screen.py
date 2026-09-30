"""knob screen (phase A): every SCREEN knob at z=-1 and z=+1 (bools: flipped once), det mode (ops-bounded planning, reproducible),
vs V183 on seeds 20001/20002 seat 0; base (ms_slot unchanged) replicated on every pod. A knob is LIVE when both of its variants
change the candidate's per-step action digest vs the base on both seeds... (reported: first divergent step, n steps differing, margin delta).
  python screen.py make   -> gens/screen/jobs_<pod>.json ; python screen.py launch ; python screen.py pull ; python screen.py report"""
import os, sys, json
from common import *
import space
G = 'gens/screen'; SEEDS = (20001, 20002)
def variants():
    V = {'base': {}}
    EP, CP = space.effective()
    for k in space.SCREEN:
        n = k[0]; b = space.base_value(n, EP, CP)
        if k[3] == 'bool': V[f's_{n}_f'] = {n: space.decode(n, -1, b)}
        else:
            for tag, z in (('m', -1), ('p', 1)):
                v = space.decode(n, z, b)
                if v != b: V[f's_{n}_{tag}'] = {n: v}
    return V
def make():
    V = variants(); P = pods(); os.makedirs(G, exist_ok=True)
    jobs = {p['name']: [] for p in P}; builds = {p['name']: {} for p in P}
    names = [c for c in V if c != 'base']; wsum = sum(p['w'] for p in P)
    # base on every pod; the rest round-robin weighted
    for p in P:
        builds[p['name']]['base'] = {}
        for s in SEEDS: jobs[p['name']].append(dict(k='fresh', c=cand_path('base'), o=OPP['V183'], seed=s, seat=0, det=1, out=f"{RD}/out/screen/{p['name']}/base_{s}_0.json"))
    i = 0
    for c in names:
        p = P[i % len(P)] if True else None; i += 1
        builds[p['name']][c] = V[c]
        for s in SEEDS: jobs[p['name']].append(dict(k='fresh', c=cand_path(c), o=OPP['V183'], seed=s, seat=0, det=1, out=f"{RD}/out/screen/{p['name']}/{c}_{s}_0.json"))
    for p in P:
        json.dump({'build': builds[p['name']], 'jobs': jobs[p['name']]}, open(f"{G}/jobs_{p['name']}.json", 'w'))
        print(p['name'], len(jobs[p['name']]), 'jobs')
    json.dump(V, open(f'{G}/variants.json', 'w'), indent=0)
if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'make': make()
    elif a == 'launch':
        for p in pods(): print(p['name'], launch(p, f"{G}/jobs_{p['name']}.json").stdout.strip())
    elif a == 'status':
        for p in pods(): print(p['name'], done(p, f"{G}/jobs_{p['name']}.json"), ssh(p, f"ls {RD}/out/screen/{p['name']} 2>/dev/null | wc -l; uptime").stdout.split())
    elif a == 'pull':
        for p in pods(): print(p['name'], rsync_from(p, f"{RD}/out/screen/", 'out/screen/').returncode)
