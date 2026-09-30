"""pod job runner: python pod_run.py <jobs.json> <workers>
jobs.json = {"build": {cid: {knob: value}}, "jobs": [{"k": "fresh"|"tape", "c": cand main.py, ...}]}
Builds every candidate main.py from its knob values (build_cand.py, on the pod), then runs one game process per job
(fresh: at_game.py cand opp seed seat out [det]; tape: tapejudge/tj_game.py ep seat cand out), <workers> at a time.
Resumable: jobs whose output JSON exists are skipped. Writes <jobs.json>.done when finished."""
import os, sys, json, subprocess, threading, queue, time
H = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable
TJ = os.path.join(H, '..', 'tapejudge', 'tj_game.py')
sys.path.insert(0, H)
import space, build_cand
spec = json.load(open(sys.argv[1])); W = int(sys.argv[2])
EP, CP = space.effective()
for cid, vals in spec.get('build', {}).items():
    d = os.path.join(H, 'cands', cid)
    build_cand.build(d, vals, spec.get('base', space.BASE), EP, CP)   # always rebuild (ids can be reused after a restart)
Q = queue.Queue(); n = 0
for j in spec['jobs']:
    if os.path.exists(j['out']): continue
    os.makedirs(os.path.dirname(j['out']), exist_ok=True); Q.put(j); n += 1
print(n, 'jobs,', W, 'workers', time.strftime('%H:%M:%S'), flush=True)
env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
def worker():
    while True:
        try: j = Q.get_nowait()
        except queue.Empty: return
        if j['k'] == 'fresh': cmd = [PY, os.path.join(H, 'at_game.py'), j['c'], j['o'], str(j['seed']), str(j['seat']), j['out']] + (['det'] if j.get('det') else [])
        else: cmd = [PY, TJ, str(j['ep']), str(j['seat']), j['c'], j['out']]
        with open(j['out'] + '.err', 'w') as ef: subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=ef, env=env)
        try:
            if os.path.exists(j['out']) and os.path.getsize(j['out'] + '.err') == 0: os.remove(j['out'] + '.err')
        except OSError: pass
T = [threading.Thread(target=worker) for _ in range(W)]
for t in T: t.start()
for t in T: t.join()
open(sys.argv[1] + '.done', 'w').write(time.strftime('%H:%M:%S'))
print('done', time.strftime('%H:%M:%S'), flush=True)
