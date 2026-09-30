"""build_cand.py: candidate main.py = base main.py + appended override block (no code change).
  python build_cand.py <out_dir> '<json {knob: value}>' [base]      -> <out_dir>/main.py, prints sha256
The block updates the ctrl P['XC_P'] (applied to the executor at step 0 by agent()) and the ctrl P; get_last_callable still
returns agent (assignments add no callable)."""
import os, sys, json, hashlib
import space
def text(vals, base=space.BASE, EP=None, CP=None):
    xo, co = space.overrides(vals, EP, CP)
    src = open(space.BASES[base]).read().rstrip('\n') + '\n'
    blk = '\n# ---- autotune overrides (final30/autotune) ----\n'
    blk += 'AUTOTUNE = %r\n' % ({k: vals[k] for k in sorted(vals)},)
    if xo: blk += "P['XC_P'] = dict(P['XC_P'], **%r)\n" % (xo,)
    if co: blk += 'P.update(%r)\n' % (co,)
    return src + blk if vals else src
def build(out_dir, vals, base=space.BASE, EP=None, CP=None):
    os.makedirs(out_dir, exist_ok=True); t = text(vals, base, EP, CP)
    compile(t, 'main.py', 'exec')
    open(os.path.join(out_dir, 'main.py'), 'w').write(t)
    return hashlib.sha256(t.encode()).hexdigest()
if __name__ == '__main__':
    print(build(sys.argv[1], json.loads(sys.argv[2]), *(sys.argv[3:4] or [space.BASE])))
