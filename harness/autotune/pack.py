"""python pack.py <tag> <cid>: build/<tag>/main.py from the cid's knob values (evals.jsonl) on the ms_slot base, then
build/submission-<tag>.tar.gz (main.py only, mtime 0, uid/gid 0, like micro/build/submission-v183ms.tar.gz); prints both sha256."""
import sys, os, tarfile, hashlib, io, gzip, json
import build_cand
tag, cid = sys.argv[1], sys.argv[2]; D = os.path.dirname(os.path.abspath(__file__))
vals = next(json.loads(l)['vals'] for l in open(os.path.join(D, 'evals.jsonl')) if json.loads(l)['cid'] == cid)
d = os.path.join(D, 'build', tag); build_cand.build(d, vals)
src = os.path.join(d, 'main.py'); data = open(src, 'rb').read()
out = os.path.join(D, 'build', f'submission-{tag}.tar.gz'); buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w') as tf:
    ti = tarfile.TarInfo('main.py'); ti.size = len(data); ti.mtime = 0; ti.uid = ti.gid = 0; ti.mode = 0o644; tf.addfile(ti, io.BytesIO(data))
with open(out, 'wb') as f:
    with gzip.GzipFile(fileobj=f, mode='wb', mtime=0, filename='') as g: g.write(buf.getvalue())
json.dump({'cid': cid, 'vals': vals}, open(os.path.join(d, 'AUTOTUNE.json'), 'w'), indent=1)
print(out, 'archive sha256', hashlib.sha256(open(out, 'rb').read()).hexdigest(), 'main.py sha256', hashlib.sha256(data).hexdigest())
