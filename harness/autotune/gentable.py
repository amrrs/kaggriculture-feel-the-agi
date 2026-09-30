"""gentable.py [gen ...]: per-generation table with the base control (g{g}b = ms_slot unchanged) offsets: rel = score - control score."""
import json, sys
rows = [json.loads(l) for l in open('evals.jsonl')]
gens = [int(g) for g in sys.argv[1:]] or sorted({r['gen'] for r in rows})
for g in gens:
    R = [r for r in rows if r['gen'] == g]; b = next((r for r in R if r['cid'].endswith('b')), None)
    bs = b['comp']['score'] if b else float('nan')
    print(f'--- gen {g}  control score {bs:+.2f}')
    for r in sorted(R, key=lambda r: -r['comp']['score']):
        c = r['comp']; tag = r['vals'] if ('o' in r['cid'] or r['cid'].endswith(('m', 'b'))) and len(r['vals'] or {}) < 3 else len(r['vals'] or {})
        print('%-9s sc %+.2f rel %+.2f | T %+5.0f(%3.0f) TB %+5.0f TW %+2d | FV %+5.0f(%4.0f) WV %+.2f | WH %+.2f MH %+5.0f(%4.0f) | bad %d pk %.2f' % (
            r['cid'], c['score'], c['score'] - bs, c['T'], c['T_se'], c['TB'], c['TW'], c['FV'], c['FV_se'], c['WV'], c['WH'], c['MH'], c['MH_se'], c['bad'], c['pk95']), tag)
