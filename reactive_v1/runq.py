"""pod job runner: python runq.py <jobs.txt> <out_dir> <workers> [cpu_list e.g. 0-15 or 0,2,4]
jobs.txt lines: tag cand_path opp_tag opp_path seed seat. One process per game, each pinned (taskset) to its own logical CPU
(a CPU is handed to one game at a time). Resumable (skips existing JSONs)."""
import os, sys, subprocess, time, threading, queue
jobs_f, out, W = sys.argv[1], sys.argv[2], int(sys.argv[3])
def cpus(s):
    r = []
    for p in s.split(','):
        if '-' in p: a, b = p.split('-'); r += list(range(int(a), int(b) + 1))
        else: r.append(int(p))
    return r
C = cpus(sys.argv[4]) if len(sys.argv) > 4 else sorted(os.sched_getaffinity(0))
os.makedirs(out, exist_ok=True)
H = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable
Q = queue.Queue()
for ln in open(jobs_f):
    f = ln.split()
    if len(f) < 6: continue
    tag, cp, ot, op, sd, se = f[:6]
    fn = f'{out}/{tag}_vs_{ot}_{sd}_{se}.json'
    if not os.path.exists(fn): Q.put((cp, op, sd, se, fn))
free = queue.Queue()
for c in C[:W]: free.put(c)
print(Q.qsize(), 'jobs on cpus', C[:W], flush=True)
def worker():
    while True:
        try: j = Q.get_nowait()
        except queue.Empty: return
        c = free.get()
        try:
            subprocess.run(['taskset', '-c', str(c), PY, os.path.join(H, 'game.py'), *j], env=dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1'))
        finally: free.put(c)
T = [threading.Thread(target=worker) for _ in range(W)]
for t in T: t.start()
for t in T: t.join()
print('done', flush=True)
