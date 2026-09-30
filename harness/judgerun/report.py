"""report.py crashok|crashfail|tapes|full|rebuild <tag> : judgerun bookkeeping (REPORT.md = header + summary table + append-only log.md)."""
import json, glob, os, sys, math, time
H = os.path.dirname(os.path.abspath(__file__)); R = f'{H}/results'
def now(): return time.strftime('%H:%M UTC', time.gmtime())
def J(p):
    try: return json.load(open(p))
    except Exception: return None
def ms(x):
    n = len(x); m = sum(x) / n if n else 0
    return m, (math.sqrt(sum((v - m) ** 2 for v in x) / (n - 1) / n) if n > 1 else 0)
def tapes(tag, base='v183ms'):
    def ld(t):
        D = {}
        for f in glob.glob(f'{H}/tj/out/{t}/*.json'):
            r = J(f)
            if r and r.get('margin') is not None: D[(r['ep'], r['cand_seat'])] = r
        return D
    C, B = ld(tag), ld(base)
    if not C: return dict(n=0)
    mg = [r['margin'] for r in C.values()]; m, se = ms(mg); it = [r for r in C.values() if r['intact']]; mi, sei = ms([r['margin'] for r in it]) if it else (0, 0)
    ks = sorted(k for k in C if k in B); d = [C[k]['margin'] - B[k]['margin'] for k in ks]; pm, pse = ms(d)
    ki = [k for k in ks if C[k]['intact'] and B[k]['intact']]; pi, psei = ms([C[k]['margin'] - B[k]['margin'] for k in ki]) if ki else (0, 0)
    return dict(n=len(C), wins=sum(x > 0 for x in mg), margin=round(m), se=round(se), intact=len(it), intact_margin=round(mi), intact_se=round(sei),
                intact_wins=sum(r['margin'] > 0 for r in it), paired=round(pm), paired_se=round(pse), better=sum(x > 0 for x in d), worse=sum(x < 0 for x in d),
                bi_n=len(ki), bi_paired=round(pi), bi_se=round(psei), base_wins=sum(B[k]['margin'] > 0 for k in ks), cand_wins=sum(C[k]['margin'] > 0 for k in ks),
                base_intact=sum(B[k]['intact'] for k in ks), peak=max(r['step']['max'] or 0 for r in C.values()), n_gt06=sum(r['step']['n_gt06'] for r in C.values()),
                nondone=sum(r['status'][r['cand_seat']] != 'DONE' for r in C.values()))
def crash_bad(c):
    why = []
    if not c or c.get('n', 0) < c.get('expected', 4): why.append(f"only {c and c.get('n')} of 4 games produced a result")
    if c:
        if c.get('errs'): why.append(f"{c['errs']} games wrote stderr: {c.get('err_tail')}")
        if c.get('bad'): why.append(f"non-DONE status {c['bad']}")
        if c.get('peak', 0) > 0.9: why.append(f"peak step {c['peak']:.3f} s > 0.9")
    return why
def fl(x, k, f='{:+d}'):
    return f.format(x[k]) if x and k in x else '-'
def verdict(m):
    fV, fM, tj = m.get('fV'), m.get('fM'), m.get('tj')
    if not (fV and fM and tj and 'margin' in fM and tj.get('n')): return 'INCOMPLETE', []
    worst = min(fV['worst'], fM['worst'], *( [m['fV2']['worst'], m['fM2']['worst']] if m.get('fV2') and m.get('fM2') and 'worst' in m['fM2'] else []))
    peak = max(fV['peak'], fM['peak'], tj['peak'])
    z = fM['margin'] / max(1, fM['se'])
    c = [(f"h2h vs v183ms {fM['margin']:+d} (z {z:.1f}) >= +1k & z>=2", fM['margin'] >= 1000 and z >= 2),
         (f"vs V183 {fV['winrate']}% >= 60%", fV['winrate'] >= 60),
         (f"judge paired {tj['paired']:+d} >= +1k", tj['paired'] >= 1000),
         (f"worst {worst:+d} > -15k", worst > -15000),
         (f"peak {peak:.3f} s < 0.6", peak < 0.6)]
    return ('PASS' if all(ok for _, ok in c) else 'FAIL'), c
def load_all(tag):
    m = J(f'{R}/{tag}.meta.json') or {'tag': tag}
    for k in ('crash', 'fV', 'fM', 'tj', 'fV2', 'fM2', 'fL', 'fVall', 'fMall'): m[k] = J(f'{R}/{tag}.{k}.json')
    return m
def fresh_line(x, lab):
    if not x or 'margin' not in x: return f'- {lab}: no result'
    s = (f"- {lab} (seeds {x['seeds']} both seats): n={x['n']} (distinct {x['distinct']}), W/D/L {x['wins']}/{x['draws']}/{x['losses']} = **{x['winrate']}%**, "
         f"margin **{x['margin']:+d}** (se {x['se']}, z {x['margin'] / max(1, x['se']):.1f}; se over seed-means {x['se_seed']}), worst {x['worst']:+d} at seed/seat {x['worst_at']}, "
         f"peak step {x['peak']:.3f} s, max p99 {x['p99max']:.3f} s, steps>0.6 s {x['n_gt06']}, errors {x['errs']}, non-DONE {len(x['bad'])}")
    if 'paired' in x: s += (f"\n  - paired d vs v183ms's own games vs {x['opp']} (same seed/seat): **{x['paired']:+d}** (se {x['paired_se']}, z {x['paired'] / max(1, x['paired_se']):.1f}), "
                            f"better/worse {x['better']}/{x['worse']}; v183ms there: {x['base_winrate']}% / {x['base_margin']:+d}")
    s += '\n  - revenue own/opp per game: ' + ', '.join(f"{k.lower()} {v[0] / 1000:.1f}/{v[1] / 1000:.1f}k" for k, v in x['prod'].items())
    if x.get('prod_d'): s += '\n  - revenue delta vs v183ms own/opp: ' + ', '.join(f"{k.lower()} {v[0]:+d}/{v[1]:+d}" for k, v in x['prod_d'].items())
    return s
def block(tag):
    m = load_all(tag); v, c = verdict(m); tj = m.get('tj') or {}
    L = [f"\n### {tag} — {now()} (seen {m.get('seen')} UTC){' FINAL' if m.get('final') == 'FINAL' else ''}", f"- path {m.get('dir')}/main.py, sha256 {m.get('sha')}"]
    cr = m.get('crash') or {}
    L.append(f"- crash check (4 games vs V183, 17801-17802): OK, margins {cr.get('margin', 0):+d} avg, peak {cr.get('peak', 0):.3f} s")
    L.append(fresh_line(m.get('fM'), 'H2H vs v183ms')); L.append(fresh_line(m.get('fV'), 'vs V183'))
    if m.get('fM2'): L.append(fresh_line(m.get('fM2'), 'H2H vs v183ms, 2nd block')); L.append(fresh_line(m.get('fV2'), 'vs V183, 2nd block'))
    if m.get('fL'): L.append(fresh_line(m.get('fL'), 'H2H vs lx1'))
    if m.get('fMall'): L.append(fresh_line(m.get('fMall'), 'POOLED H2H vs v183ms (both blocks)')); L.append(fresh_line(m.get('fVall'), 'POOLED vs V183 (both blocks)'))
    if tj.get('n'):
        L.append(f"- tape judge (n={tj['n']}): paired vs v183ms **{tj['paired']:+d}** (se {tj['paired_se']}), better/worse {tj['better']}/{tj['worse']}, wins {tj['base_wins']}->{tj['cand_wins']}; "
                 f"both-intact n={tj['bi_n']} **{tj['bi_paired']:+d}** (se {tj['bi_se']}); intact {tj['intact']}/{tj['n']} (v183ms {tj['base_intact']}), intact-only margin {tj['intact_margin']:+d} "
                 f"(se {tj['intact_se']}) wins {tj['intact_wins']}; peak step {tj['peak']:.3f} s, steps>0.6 {tj['n_gt06']}, non-DONE {tj['nondone']}")
    L.append(f"- **VERDICT: {v}** — " + '; '.join(f"{'ok' if ok else 'MISS'} {t}" for t, ok in c))
    return '\n'.join(L)
def row(tag):
    m = load_all(tag); fM, fV, tj = m.get('fM') or {}, m.get('fV') or {}, m.get('tj') or {}
    if m.get('crash') is not None and crash_bad(m['crash']): return f"| {tag} | {m.get('seen')} | CRASH/TIMEOUT | - | - | - | - | - | **FAIL (crash check)** |"
    v, _ = verdict(m); w = [x['worst'] for x in (fM, fV, m.get('fV2'), m.get('fM2')) if x and 'worst' in x]
    pk = [x['peak'] for x in (fM, fV, tj) if x and 'peak' in x]
    s = (f"| {tag}{' FINAL' if m.get('final') == 'FINAL' else ''} | {m.get('seen')} | {fl(fM, 'margin')} ({fM.get('se', '-')}) d{fM.get('distinct', '-')} | {fV.get('winrate', '-')}% / {fl(fV, 'paired')} ({fV.get('paired_se', '-')}) | "
         f"{fl(tj, 'paired')} ({tj.get('paired_se', '-')}) / bi {fl(tj, 'bi_paired')} | {tj.get('cand_wins', '-')} | {min(w) if w else '-'} | {max(pk) if pk else 0:.3f} | **{v}** |")
    if m.get('fM2') and 'margin' in m['fM2']:
        s += f"\n| {tag} 2nd block 17841-64 | | {m['fM2']['margin']:+d} ({m['fM2']['se']}) d{m['fM2']['distinct']} | {m['fV2']['winrate']}% / {fl(m['fV2'], 'paired')} ({m['fV2'].get('paired_se')}) | | | {min(m['fM2']['worst'], m['fV2']['worst'])} | {max(m['fM2']['peak'], m['fV2']['peak']):.3f} | |"
    return s
def rebuild():
    hdr = open(f'{H}/header.md').read() if os.path.exists(f'{H}/header.md') else '# final30/judgerun\n'
    tags = [os.path.basename(f)[:-10] for f in sorted(glob.glob(f'{R}/*.meta.json'), key=os.path.getmtime)]
    extra = open(f'{H}/baseline_rows.md').read() if os.path.exists(f'{H}/baseline_rows.md') else ''
    T = ['## Summary (updated ' + now() + ')', 'Pass bar: H2H vs v183ms >= +1k (z >= 2), >= 60% vs V183, judge paired >= +1k, worst > -15k, peak step < 0.6 s. Fresh seeds 17811-17834 both seats (48 games per pair); d = distinct games.', '',
         '| candidate | seen UTC | H2H vs v183ms margin (se) | vs V183 win% / paired d vs v183ms (se) | judge paired vs v183ms (se) / both-intact | judge wins /123 | worst | peak step s | verdict |', '|---|---|---|---|---|---|---|---|---|']
    T += [extra.strip()] if extra.strip() else []
    T += [row(t) for t in tags]
    log = open(f'{H}/log.md').read() if os.path.exists(f'{H}/log.md') else ''
    open(f'{H}/REPORT.md.tmp', 'w').write(hdr.rstrip() + '\n\n' + '\n'.join(T) + '\n\n## Log (append-only, newest last)\n' + log)
    os.replace(f'{H}/REPORT.md.tmp', f'{H}/REPORT.md')
def app(s): open(f'{H}/log.md', 'a').write(s.rstrip() + '\n')
if __name__ == '__main__':
    cmd = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == 'crashok': sys.exit(1 if crash_bad(J(f'{R}/{tag}.crash.json')) else 0)
    if cmd == 'crashfail':
        m = load_all(tag); app(f"\n### {tag} — {now()} (seen {m.get('seen')} UTC) — **CRASH/TIMEOUT CHECK FAILED, rest skipped**\n- path {m.get('dir')}/main.py sha256 {m.get('sha')}\n- " + '; '.join(crash_bad(m['crash']))); rebuild()
    if cmd == 'tapes': print(json.dumps(tapes(tag)))
    if cmd == 'full': app(block(tag)); rebuild()
    if cmd == 'final': app(block(tag).replace(' FINAL', ' FINAL (2nd block + lx1 added; verdict on block 1)', 1)); rebuild()
    if cmd == 'rebuild': rebuild()
