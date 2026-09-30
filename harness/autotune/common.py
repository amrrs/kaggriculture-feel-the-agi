"""shared paths / pod helpers for the autotune harness (local side)."""
import os, json, subprocess, time
D = os.path.dirname(os.path.abspath(__file__))
R = '/work/kaggriculture'                                   # repo root on the pods
RD = R + '/research/claude/2900/agents/final30/autotune'    # this dir on the pods
LOCAL_ROOT = '/Users/1littlecoder/kaggriculture'
OPP = {'V183': R + '/research/codex/2026-09-05/v179-gate-loader/build/dated_gate/main.py',
       'v183ms': R + '/research/claude/2900/agents/micro/build/v183ms/main.py',
       'lx3': R + '/research/claude/2900/agents/lateexec/build/lx3/main.py',
       'ms_slot': R + '/research/claude/2900/agents/final30/newexec/build/ms_slot/main.py'}
HOLDOUT_SEEDS = list(range(19001, 19049))
def cand_path(cid): return OPP[cid] if cid in OPP else f'{RD}/cands/{cid}/main.py'
def pods():
    P = []
    for ln in open(os.path.join(D, os.environ.get('PODS_FILE', 'pods.txt'))):
        f = ln.split()
        if len(f) >= 3 and not ln.startswith('#'): P.append(dict(name=f[0], ip=f[1], port=f[2], w=int(f[3]) if len(f) > 3 else 26))
    return P
def ssh(p, cmd, timeout=120):
    return subprocess.run(['ssh', '-o', 'ConnectTimeout=20', '-o', 'ServerAliveInterval=15', '-o', 'StrictHostKeyChecking=accept-new', '-i',
                           os.path.expanduser('~/.ssh/id_ed25519'), '-p', p['port'], 'root@' + p['ip'], cmd],
                          capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
def rsync_to(p, local, remote):
    e = f"ssh -o ConnectTimeout=20 -i {os.path.expanduser('~/.ssh/id_ed25519')} -p {p['port']}"
    ex = ['--exclude', '__pycache__', '--exclude', 'out/', '--exclude', 'cands/', '--exclude', '*.log', '--exclude', 'build/', '--exclude', '*.jsonl']
    return subprocess.run(['rsync', '-a', '-e', e, *ex, local, f"root@{p['ip']}:{remote}"], capture_output=True, text=True, timeout=300)
def rsync_from(p, remote, local):
    e = f"ssh -o ConnectTimeout=20 -i {os.path.expanduser('~/.ssh/id_ed25519')} -p {p['port']}"
    os.makedirs(local, exist_ok=True)
    return subprocess.run(['rsync', '-a', '-e', e, '--exclude', '*.tmp', '--exclude', '*.err', f"root@{p['ip']}:{remote}", local], capture_output=True, text=True, timeout=600)
def launch(p, jobs_rel, w=None):
    """push the harness code + a jobs file and start pod_run.py in the background on pod p."""
    rsync_to(p, D + '/', RD + '/')  # small: code + gens/ spec files (out/ excluded below)
    return ssh(p, f"cd {RD} && (setsid nohup /opt/venv/bin/python pod_run.py {jobs_rel} {w or p['w']} > {jobs_rel}.log 2>&1 </dev/null &) ; echo started")
def done(p, jobs_rel):
    r = ssh(p, f"test -f {RD}/{jobs_rel}.done && echo yes || (ls {RD}/{os.path.dirname(jobs_rel)}/out 2>/dev/null | wc -l)")
    return r.stdout.strip()
