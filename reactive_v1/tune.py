"""CMA-ES over rx's P (space.py), paired vs the base build on fresh seeds vs V183 (and optionally v183ms), run on the pod.
  python tune.py init <run> [sigma=0.3] [lam=10]
  python tune.py gen <run> <seed0> <nseeds>     # one generation: build, push, run on pod (blocking), pull, score, tell
Objective (maximise): mean paired margin vs the base (same seed/seat, same opponent) in coins; crashes = -20000.
State: tune/<run>/cma.json, tune/<run>/evals.jsonl. Requires pod.sh / push.sh / pull.sh pointing at a live pod."""
import sys, os, json, subprocess, importlib.util, glob, math
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
from cma import CMA
import space
spec = importlib.util.spec_from_file_location('rxm', os.path.join(H, 'rx.py')); rxm = importlib.util.module_from_spec(spec); spec.loader.exec_module(rxm)
P0 = dict(rxm.P)
cmd, run = sys.argv[1], sys.argv[2]; D = f'tune/{run}'; os.makedirs(D, exist_ok=True)
if cmd == 'init':
    sig = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3; lam = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    CMA(len(space.KNOBS), sigma=sig, lam=lam).save(f'{D}/cma.json'); print('init', run, len(space.KNOBS), 'dims'); sys.exit()
s0, ns = int(sys.argv[3]), int(sys.argv[4]); opps = (sys.argv[5] if len(sys.argv) > 5 else 'V183')
c = CMA.load(f'{D}/cma.json'); X = c.ask(); g = c.g
cands = {f't{run}g{g}c{i}': space.decode(x, P0) for i, x in enumerate(X)}
cands[f't{run}g{g}m'] = space.decode(c.m, P0); cands[f't{run}g{g}b'] = {}
subprocess.run(['python3', 'mkvar.py', 'rx.py', json.dumps(cands)], check=True, stdout=subprocess.DEVNULL)
subprocess.run(['python3', 'mkjobs.py', f'{D}/jobs_g{g}.txt', str(s0), str(ns), opps] + list(cands), check=True)
subprocess.run(['bash', 'push.sh'], check=True)
R = '/work/kaggriculture/research/claude/2900/agents/reactive_v1'
subprocess.run(['bash', 'pod.sh', f'cd {R} && /opt/venv/bin/python runq.py {D}/jobs_g{g}.txt out/{run}_g{g} 30 > out/{run}_g{g}.log 2>&1'], check=True)
subprocess.run(['bash', 'pull.sh', f'{run}_g{g}'], check=True)
res = {}
for f in glob.glob(f'out/{run}_g{g}/*.json'):
    r = json.load(open(f)); tag, rest = os.path.basename(f)[:-5].split('_vs_')
    res.setdefault(tag, {})[rest] = r['margin'] if r.get('margin') is not None and not (r.get('nxerr') or [0])[0] else -20000
base = res.get(f't{run}g{g}b', {})
def score(tag):
    d = [res.get(tag, {}).get(k, -20000) - base[k] for k in base]
    return sum(d) / len(d) if d else -20000
F = [score(f't{run}g{g}c{i}') for i in range(len(X))]
c.tell(X, [-f for f in F]); c.save(f'{D}/cma.json')
with open(f'{D}/evals.jsonl', 'a') as fo:
    for i, x in enumerate(X): fo.write(json.dumps(dict(g=g, tag=f't{run}g{g}c{i}', score=F[i], P=cands[f't{run}g{g}c{i}'])) + '\n')
    fo.write(json.dumps(dict(g=g, tag=f't{run}g{g}m', score=score(f't{run}g{g}m'), P=cands[f't{run}g{g}m'])) + '\n')
print('gen', g, 'scores', [round(f) for f in F], 'mean-cand', round(score(f't{run}g{g}m')), 'sigma', round(c.sigma, 3))
