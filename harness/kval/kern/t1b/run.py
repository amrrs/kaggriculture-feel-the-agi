import subprocess, sys, os, glob, json, concurrent.futures
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'kaggle-environments==1.32.7'], check=False)
g = glob.glob('/kaggle/input/**/kaggriculture-kval2/kvgame.py', recursive=True)[0]; D = os.path.dirname(g)
print('ds', D, len(os.listdir(D)), 'cpus', os.cpu_count(), flush=True)
J = [['T1.py', 'lx3ms.py', 20117, 1], ['T1.py', 'lx3ms.py', 20118, 0], ['T1.py', 'lx3ms.py', 20119, 1], ['T1.py', 'lx3ms.py', 20120, 0], ['T1.py', 'lx3ms.py', 20121, 1], ['T1.py', 'lx3ms.py', 20122, 0], ['T1.py', 'lx3ms.py', 20123, 1], ['T1.py', 'lx3ms.py', 20124, 0], ['T1.py', 'lx3ms.py', 20125, 1], ['T1.py', 'lx3ms.py', 20126, 0], ['T1.py', 'lx3ms.py', 20127, 1], ['T1.py', 'lx3ms.py', 20128, 0], ['T1.py', 'lx3ms.py', 20129, 1], ['T1.py', 'lx3ms.py', 20130, 0], ['T1.py', 'lx3ms.py', 20131, 1], ['T1.py', 'lx3ms.py', 20132, 0], ['T1.py', 'g012m.py', 20117, 1], ['T1.py', 'g012m.py', 20118, 0], ['T1.py', 'g012m.py', 20119, 1], ['T1.py', 'g012m.py', 20120, 0], ['T1.py', 'g012m.py', 20121, 1], ['T1.py', 'g012m.py', 20122, 0], ['T1.py', 'g012m.py', 20123, 1], ['T1.py', 'g012m.py', 20124, 0], ['T1.py', 'g012m.py', 20125, 1], ['T1.py', 'g012m.py', 20126, 0], ['T1.py', 'g012m.py', 20127, 1], ['T1.py', 'g012m.py', 20128, 0], ['T1.py', 'g012m.py', 20129, 1], ['T1.py', 'g012m.py', 20130, 0], ['T1.py', 'g012m.py', 20131, 1], ['T1.py', 'g012m.py', 20132, 0]]
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
