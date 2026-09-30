"""python mkjobs.py <out_jobs> <seed0> <nseeds> <opp[,opp...]> tag[:path] ...   (both seats)
opps: V183, v183ms, at12m, self (= the candidate itself), random"""
import sys
W = '/work/kaggriculture/research'
OPP = {'V183': W + '/codex/2026-09-05/v179-gate-loader/build/dated_gate/main.py',
       'v183ms': W + '/claude/2900/agents/micro/build/v183ms/main.py',
       'at12m': W + '/claude/2900/agents/final30/autotune/build/at12m/main.py'}
out, s0, n, opps = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4].split(',')
L = []
for tg in sys.argv[5:]:
    tag, _, p = tg.partition(':')
    p = p or f'build/{tag}/main.py'
    for op in opps:
        opath = p if op == 'self' else OPP[op]
        for sd in range(s0, s0 + n):
            for se in (0, 1): L.append(f'{tag} {p} {op} {opath} {sd} {se}')
open(out, 'w').write('\n'.join(L) + '\n'); print(len(L), 'jobs')
