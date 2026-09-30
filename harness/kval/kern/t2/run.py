import subprocess, sys, os, glob, json, concurrent.futures
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'kaggle-environments==1.32.7'], check=False)
g = glob.glob('/kaggle/input/**/kaggriculture-kval2/kvgame.py', recursive=True)[0]; D = os.path.dirname(g)
print('ds', D, len(os.listdir(D)), 'cpus', os.cpu_count(), flush=True)
J = [['T2.py', 'lx3ms.py', 20101, 1], ['T2.py', 'lx3ms.py', 20102, 0], ['T2.py', 'lx3ms.py', 20103, 1], ['T2.py', 'lx3ms.py', 20104, 0], ['T2.py', 'lx3ms.py', 20105, 1], ['T2.py', 'lx3ms.py', 20106, 0], ['T2.py', 'lx3ms.py', 20107, 1], ['T2.py', 'lx3ms.py', 20108, 0], ['T2.py', 'lx3ms.py', 20109, 1], ['T2.py', 'lx3ms.py', 20110, 0], ['T2.py', 'lx3ms.py', 20111, 1], ['T2.py', 'lx3ms.py', 20112, 0], ['T2.py', 'lx3ms.py', 20113, 1], ['T2.py', 'lx3ms.py', 20114, 0], ['T2.py', 'lx3ms.py', 20115, 1], ['T2.py', 'lx3ms.py', 20116, 0], ['T2.py', 'g012m.py', 20101, 1], ['T2.py', 'g012m.py', 20102, 0], ['T2.py', 'g012m.py', 20103, 1], ['T2.py', 'g012m.py', 20104, 0], ['T2.py', 'g012m.py', 20105, 1], ['T2.py', 'g012m.py', 20106, 0], ['T2.py', 'g012m.py', 20107, 1], ['T2.py', 'g012m.py', 20108, 0], ['T2.py', 'g012m.py', 20109, 1], ['T2.py', 'g012m.py', 20110, 0], ['T2.py', 'g012m.py', 20111, 1], ['T2.py', 'g012m.py', 20112, 0], ['T2.py', 'g012m.py', 20113, 1], ['T2.py', 'g012m.py', 20114, 0], ['T2.py', 'g012m.py', 20115, 1], ['T2.py', 'g012m.py', 20116, 0]]
env = dict(os.environ, MPLBACKEND='Agg', OMP_NUM_THREADS='1')
out = open('/kaggle/working/res.jsonl', 'w')
def run(j):
    c, o, seed, seat = j
    try:
        r = subprocess.run([sys.executable, g, f'{D}/{c}', f'{D}/{o}', str(seed), str(seat)], capture_output=True, text=True, env=env, timeout=1500)
        line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else json.dumps({'cand': c, 'opp': o, 'seed': seed, 'seat': seat, 'error': 'noout rc=%d %s' % (r.returncode, r.stderr[-800:])})
    except subprocess.TimeoutExpired:
        line = json.dumps({'cand': c, 'opp': o, 'seed': seed, 'seat': seat, 'error': 'harness timeout'})
    out.write(line + '\n'); out.flush(); print(line[:300], flush=True); return line
with concurrent.futures.ThreadPoolExecutor(os.cpu_count() or 4) as ex: list(ex.map(run, J))
print('DONE', flush=True)
