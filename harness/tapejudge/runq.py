"""pod runner: python runq.py <cand main.py> <out_dir> [set=tapes|check|all] [workers] [cpu_list]
One tj_game.py process per game, each pinned (taskset) to its own logical CPU. Resumable (skips existing JSONs)."""
import os, sys, subprocess, threading, queue, json
H = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable
cand, out = sys.argv[1], sys.argv[2]; which = sys.argv[3] if len(sys.argv) > 3 else 'tapes'
C = sorted(os.sched_getaffinity(0)); W = int(sys.argv[4]) if len(sys.argv) > 4 else len(C)
if len(sys.argv) > 5:
    C = []
    for p in sys.argv[5].split(','):
        a, _, b = p.partition('-'); C += list(range(int(a), int(b or a) + 1))
rows = []
if which in ('tapes', 'all'): rows += json.load(open(f'{H}/tapes.json'))
if which in ('check', 'all'): rows += json.load(open(f'{H}/check.json'))
os.makedirs(out, exist_ok=True); Q = queue.Queue(); seen = set()
for r in rows:
    k = (r['ep'], r['cand_seat'])
    if k in seen: continue
    seen.add(k); fn = f"{out}/{r['ep']}_{r['cand_seat']}.json"
    if not os.path.exists(fn): Q.put((str(r['ep']), str(r['cand_seat']), fn))
free = queue.Queue()
for c in C[:W]: free.put(c)
print(Q.qsize(), 'jobs on', W, 'cpus', flush=True)
def worker():
    while True:
        try: j = Q.get_nowait()
        except queue.Empty: return
        c = free.get()
        try:
            with open(j[2] + '.err', 'w') as ef:
                subprocess.run(['taskset', '-c', str(c), PY, os.path.join(H, 'tj_game.py'), j[0], j[1], cand, j[2]], stderr=ef, stdout=subprocess.DEVNULL,
                               env=dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1'))
            if os.path.exists(j[2]) and os.path.getsize(j[2] + '.err') == 0: os.remove(j[2] + '.err')
        finally: free.put(c)
T = [threading.Thread(target=worker) for _ in range(W)]
for t in T: t.start()
for t in T: t.join()
print('done', flush=True)
