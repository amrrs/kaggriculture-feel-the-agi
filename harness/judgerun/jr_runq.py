"""pod job runner (judgerun; = bundle/runq.py + per-game stderr capture): python jr_runq.py <jobs.txt> <out_dir> [workers] [cpu_list]
jobs.txt lines: tag cand_path opp_tag opp_path seed seat. One game.py process per game, each pinned (taskset) to its own logical CPU.
Resumable (skips existing JSONs). stderr of each game kept in <json>.err when non-empty (agent exceptions / tracebacks)."""
import os, sys, subprocess, threading, queue
jobs_f, out = sys.argv[1], sys.argv[2]
def cpus(s):
    r = []
    for p in s.split(','):
        a, _, b = p.partition('-'); r += list(range(int(a), int(b or a) + 1))
    return r
C = cpus(sys.argv[4]) if len(sys.argv) > 4 else sorted(os.sched_getaffinity(0))
W = int(sys.argv[3]) if len(sys.argv) > 3 else len(C)
os.makedirs(out, exist_ok=True)
G = '/work/kaggriculture/research/claude/2900/agents/final30/bundle/game.py'; PY = '/opt/venv/bin/python'
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
            with open(j[4] + '.err', 'w') as ef:
                subprocess.run(['taskset', '-c', str(c), PY, G, *j], stderr=ef, stdout=subprocess.DEVNULL,
                               env=dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1'))
            if os.path.exists(j[4]) and os.path.getsize(j[4] + '.err') == 0: os.remove(j[4] + '.err')
        finally: free.put(c)
T = [threading.Thread(target=worker) for _ in range(W)]
for t in T: t.start()
for t in T: t.join()
print('done', flush=True)
