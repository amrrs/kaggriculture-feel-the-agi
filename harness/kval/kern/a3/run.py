import subprocess, sys, os, glob, json, concurrent.futures, time
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'kaggle-environments==1.32.7'], check=False)
g = glob.glob('/kaggle/input/**/kvgame.py', recursive=True)[0]; D = os.path.dirname(g)
print('ds', D, os.listdir(D), 'cpus', os.cpu_count(), flush=True)
J = [(20009, 1), (20010, 0), (20011, 1), (20012, 0)]; CAND, OPP = 'lx3ms.py', 'lx3.py'
env = dict(os.environ, MPLBACKEND='Agg', OMP_NUM_THREADS='1')
out = open('/kaggle/working/res.jsonl', 'w')
def run(j):
    seed, seat = j; t = time.time()
    try:
        r = subprocess.run([sys.executable, g, f'{D}/{CAND}', f'{D}/{OPP}', str(seed), str(seat)], capture_output=True, text=True, env=env, timeout=1500)
        line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else json.dumps({'seed': seed, 'seat': seat, 'error': 'noout rc=%d %s' % (r.returncode, r.stderr[-800:])})
    except subprocess.TimeoutExpired:
        line = json.dumps({'seed': seed, 'seat': seat, 'error': 'harness timeout'})
    out.write(line + '\n'); out.flush(); print(line[:400], flush=True); return line
with concurrent.futures.ThreadPoolExecutor(min(len(J), os.cpu_count() or 4)) as ex: list(ex.map(run, J))
print('DONE', flush=True)
