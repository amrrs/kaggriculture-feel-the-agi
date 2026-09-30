import subprocess, sys, os, glob, json, concurrent.futures
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'kaggle-environments==1.32.7'], check=False)
g = glob.glob('/kaggle/input/**/kaggriculture-kval2/kvgame.py', recursive=True)[0]; D = os.path.dirname(g)
print('ds', D, len(os.listdir(D)), 'cpus', os.cpu_count(), flush=True)
J = [['lx3ms.py', 'lx3ms.py', 20101, 1], ['lx3ms.py', 'lx3ms.py', 20101, 1], ['K_HIRE_DOWN_W.py', 'lx3ms.py', 20101, 1], ['K_HAND_W.py', 'lx3ms.py', 20101, 1], ['K_SQ_W.py', 'lx3ms.py', 20101, 1], ['K_SQ_DECAY.py', 'lx3ms.py', 20101, 1], ['K_SQ_SPLIT.py', 'lx3ms.py', 20101, 1], ['K_SQ_START_DAY.py', 'lx3ms.py', 20101, 1], ['K_SELL0_MAX.py', 'lx3ms.py', 20101, 1], ['K_CARE_W.py', 'lx3ms.py', 20101, 1], ['K_FERT_WHEAT_MAXP.py', 'lx3ms.py', 20101, 1], ['K_WHEAT_BUFFER.py', 'lx3ms.py', 20101, 1], ['K_OVERFLOW_TARGET.py', 'lx3ms.py', 20101, 1], ['K_LATE_HARVEST_W.py', 'lx3ms.py', 20101, 1], ['K_AH_V.py', 'lx3ms.py', 20101, 1], ['K_ALLOC_MARGIN.py', 'lx3ms.py', 20101, 1], ['K_STRAW_AB_x.py', 'lx3ms.py', 20101, 1], ['K_LATE_START.py', 'lx3ms.py', 20101, 1], ['K_TOM_OPP_MARGIN.py', 'lx3ms.py', 20101, 1], ['K_AMAX_TOM.py', 'lx3ms.py', 20101, 1]]
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
