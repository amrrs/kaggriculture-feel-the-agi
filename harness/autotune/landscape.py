"""landscape.py: which knobs mattered. Linear ridge fit of each objective component on the z vector over every evaluated
candidate in evals.jsonl (bool knobs enter as their flip indicator), coefficients = effect of moving a knob from z=0 to z=+1
(se from the residual). Also prints the top candidates.  python landscape.py [min_gen]"""
import json, sys, numpy as np
knobs = json.load(open('space_final.json'))['knobs']
rows = [json.loads(l) for l in open('evals.jsonl')]
rows = [r for r in rows if r['z'] is not None and r['gen'] >= (int(sys.argv[1]) if len(sys.argv) > 1 else 0)]
X = np.array([[(-1.0 if (k == 'MS_SLOT' and z < -0.5) else (0.0 if k == 'MS_SLOT' else z)) for k, z in zip(knobs, r['z'])] for r in rows])
print('n candidates', len(rows))
for comp in ('score', 'T', 'WV', 'WH', 'TW', 'FV', 'MH'):
    y = np.array([r['comp'][comp] for r in rows], float)
    A = np.hstack([np.ones((len(X), 1)), X]); lam = 1.0 * np.eye(A.shape[1]); lam[0, 0] = 0
    beta = np.linalg.solve(A.T @ A + lam, A.T @ y); res = y - A @ beta
    dof = max(1, len(y) - A.shape[1]); s2 = res @ res / dof; cov = s2 * np.linalg.inv(A.T @ A + lam)
    se = np.sqrt(np.diag(cov)); order = np.argsort(-np.abs(beta[1:] / se[1:]))
    print(f'\n[{comp}] intercept {beta[0]:+.3f}  resid sd {np.sqrt(s2):.3f}  (effect of z 0 -> +1; MS_SLOT: effect of switching it OFF = -coef)')
    print('   ' + '  '.join(f'{knobs[i]} {beta[i+1]:+.2f}({se[i+1]:.2f})' for i in order[:10]))
rows.sort(key=lambda r: -r['comp']['score'])
print('\nTOP 10')
for r in rows[:10]:
    c = r['comp']; print(r['cid'], 'score %+.2f' % c['score'], 'T %+.0f(%.0f)' % (c['T'], c['T_se']), 'TW %+d' % c['TW'], 'WV %+.2f WH %+.2f' % (c['WV'], c['WH']),
                         'FV %+.0f(%.0f) MH %+.0f(%.0f)' % (c['FV'], c['FV_se'], c['MH'], c['MH_se']), 'pk %.2f bad %d' % (c['pk95'], c['bad']), r['vals'])
