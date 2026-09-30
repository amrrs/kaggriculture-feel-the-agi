"""python mkvar.py <base_src> '<json {tag: {param: value}}>'  -> build/<tag>/main.py = base source + P.update(...) (+ META.json)
The appended statement keeps `agent` the last callable (Kaggle loader rule); autotune can use the same mechanism."""
import sys, json, os, hashlib
src = open(sys.argv[1]).read(); V = json.loads(sys.argv[2])
for tag, ov in V.items():
    os.makedirs(f'build/{tag}', exist_ok=True)
    s = src + ('\nP.update(%r)\n' % (ov,) if ov else '')
    open(f'build/{tag}/main.py', 'w').write(s)
    json.dump(dict(base=sys.argv[1], P=ov, sha256=hashlib.sha256(s.encode()).hexdigest()), open(f'build/{tag}/META.json', 'w'))
    print(tag, hashlib.sha256(s.encode()).hexdigest()[:12], ov)
