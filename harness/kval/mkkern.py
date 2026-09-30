"""mkkern.py <name> <cand> <opp> <seed:seat,...>: write kern/<name>/{run.py,kernel-metadata.json}"""
import sys, json, os
name, cand, opp, jobs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
J = [(int(a), int(b)) for a, b in (x.split(':') for x in jobs.split(','))]
d = f'kern/{name}'; os.makedirs(d, exist_ok=True)
json.dump({"id": f"nulldata/kaggriculture-kval-{name}", "title": f"kaggriculture-kval-{name}", "code_file": "run.py", "language": "python",
           "kernel_type": "script", "is_private": True, "enable_gpu": False, "enable_internet": True,
           "dataset_sources": ["nulldata/kaggriculture-kval"], "competition_sources": [], "kernel_sources": []}, open(f'{d}/kernel-metadata.json', 'w'))
open(f'{d}/run.py', 'w').write(f'''import subprocess, sys, os, glob, json, concurrent.futures, time
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'kaggle-environments==1.32.7'], check=False)
g = glob.glob('/kaggle/input/**/kvgame.py', recursive=True)[0]; D = os.path.dirname(g)
print('ds', D, os.listdir(D), 'cpus', os.cpu_count(), flush=True)
J = {J!r}; CAND, OPP = {cand!r}, {opp!r}
env = dict(os.environ, MPLBACKEND='Agg', OMP_NUM_THREADS='1')
out = open('/kaggle/working/res.jsonl', 'w')
def run(j):
    seed, seat = j; t = time.time()
    try:
        r = subprocess.run([sys.executable, g, f'{{D}}/{{CAND}}', f'{{D}}/{{OPP}}', str(seed), str(seat)], capture_output=True, text=True, env=env, timeout=1500)
        line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else json.dumps({{'seed': seed, 'seat': seat, 'error': 'noout rc=%d %s' % (r.returncode, r.stderr[-800:])}})
    except subprocess.TimeoutExpired:
        line = json.dumps({{'seed': seed, 'seat': seat, 'error': 'harness timeout'}})
    out.write(line + '\\n'); out.flush(); print(line[:400], flush=True); return line
with concurrent.futures.ThreadPoolExecutor(min(len(J), os.cpu_count() or 4)) as ex: list(ex.map(run, J))
print('DONE', flush=True)
''')
