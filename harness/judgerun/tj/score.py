"""score.py <tag> [base_tag] [--set tapes|check]: score a tape-judge run (out/<tag>/*.json).
Prints: n, wins, mean margin (cand - recorded top agent) with se, own/opp coins, intact rate (tape keeps >= 90% of its recorded coins),
step-time peak; with a base tag: paired delta (cand margin - base margin on the same tape) with se, better/worse, wins base->cand,
on ALL games and on BOTH-INTACT games; per-team rows; worst games. Bias: a tape cannot react (see REPORT.md)."""
import json, glob, os, sys, math, collections
H = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith('--')]; SET = 'tapes'
if '--set' in sys.argv: SET = sys.argv[sys.argv.index('--set') + 1]
META = {}
for r in json.load(open(f'{H}/tapes.json')): META[(r['ep'], r['cand_seat'])] = dict(team=r['team'], rank=r['rank'], set='tapes')
for r in json.load(open(f'{H}/check.json')): META.setdefault((r['ep'], r['cand_seat']), dict(team=r['opp_team'], rank=99, set='check', group=r['group']))
def load(tag):
    R = {}
    for f in glob.glob(f'{H}/out/{tag}/*.json'):
        try: r = json.load(open(f))
        except Exception: continue
        k = (r['ep'], r['cand_seat'])
        if r.get('margin') is None or META.get(k, {}).get('set') != SET: continue
        R[k] = r
    return R
def ms(x):
    n = len(x); m = sum(x) / n if n else 0
    se = math.sqrt(sum((v - m) ** 2 for v in x) / (n - 1) / n) if n > 1 else 0
    return m, se
def summ(label, R):
    rows = list(R.values()); n = len(rows)
    if not n: print(label, 'n=0'); return
    mg = [r['margin'] for r in rows]; m, se = ms(mg); it = [r for r in rows if r['intact']]; mi, sei = ms([r['margin'] for r in it]) if it else (0, 0)
    tmax = max(r['step']['max'] or 0 for r in rows); n06 = sum(r['step']['n_gt06'] for r in rows); bad = sum(r['status'][r['cand_seat']] != 'DONE' for r in rows)
    print(f"{label}: n={n} wins {sum(x > 0 for x in mg)} ({100 * sum(x > 0 for x in mg) / n:.0f}%) margin {m:+.0f} (se {se:.0f}) own {sum(r['own'] for r in rows) / n:.0f} opp {sum(r['opp'] for r in rows) / n:.0f} "
          f"| intact {len(it)}/{n} ({100 * len(it) / n:.0f}%) intact-only margin {mi:+.0f} (se {sei:.0f}) wins {sum(r['margin'] > 0 for r in it)} "
          f"| peak step {tmax:.3f}s, steps>0.6s {n06}, non-DONE {bad}" + (f" | parity {sum(r['parity'] for r in rows)}/{n}" if SET == 'check' else ''))
C = load(args[0]); summ(args[0], C)
B = load(args[1]) if len(args) > 1 else None
if B is not None:
    summ(args[1], B)
    ks = sorted(k for k in C if k in B)
    d = [C[k]['margin'] - B[k]['margin'] for k in ks]; m, se = ms(d)
    ki = [k for k in ks if C[k]['intact'] and B[k]['intact']]; di = [C[k]['margin'] - B[k]['margin'] for k in ki]; mi, sei = ms(di) if di else (0, 0)
    do = [C[k]['own'] - B[k]['own'] for k in ks]; dp = [C[k]['opp'] - B[k]['opp'] for k in ks]
    print(f"PAIRED {args[0]} - {args[1]}: n={len(ks)} delta {m:+.0f} (se {se:.0f}) better/worse {sum(x > 0 for x in d)}/{sum(x < 0 for x in d)} "
          f"wins {sum(B[k]['margin'] > 0 for k in ks)}->{sum(C[k]['margin'] > 0 for k in ks)} | own {sum(do) / max(1, len(do)):+.0f} opp {sum(dp) / max(1, len(dp)):+.0f} "
          f"| both-intact n={len(ki)} delta {mi:+.0f} (se {sei:.0f})")
    print(f"  paired worst 5: {[(C[k]['margin'] - B[k]['margin'], k[0], META[k]['team'][:14]) for k in sorted(ks, key=lambda k: C[k]['margin'] - B[k]['margin'])[:5]]}")
by = collections.defaultdict(list)
for k in C: by[(META[k]['rank'], META[k]['team'])].append(k)
print(f"  {'rank team':34s} {'n':>3s} {'wins':>4s} {'margin':>7s} {'intact':>6s}" + (f" {'paired':>7s} {'b-int':>6s}" if B is not None else ''))
for (rk, tm), kk in sorted(by.items()):
    mg = [C[k]['margin'] for k in kk]
    s = f"  {rk:>2d} {tm[:30]:30s} {len(kk):3d} {sum(x > 0 for x in mg):4d} {sum(mg) / len(mg):+7.0f} {sum(C[k]['intact'] for k in kk):6d}"
    if B is not None:
        kb = [k for k in kk if k in B]
        if kb:
            s += f" {sum(C[k]['margin'] - B[k]['margin'] for k in kb) / len(kb):+7.0f}"
            ki = [k for k in kb if C[k]['intact'] and B[k]['intact']]
            s += f" {sum(C[k]['margin'] - B[k]['margin'] for k in ki) / len(ki):+6.0f}" if ki else '      -'
    print(s)
print(f"  worst 5 margins: {[(C[k]['margin'], k[0], META[k]['team'][:14], 'I' if C[k]['intact'] else 'x') for k in sorted(C, key=lambda k: C[k]['margin'])[:5]]}")
print(f"  lowest tape keep (opp_frac): {[(C[k]['opp_frac'], k[0], META[k]['team'][:14]) for k in sorted(C, key=lambda k: C[k]['opp_frac'] or 0)[:5]]}")
