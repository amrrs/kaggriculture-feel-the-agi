"""mktapes.py: build the tape set from final30/fieldnow (JSON parsing only).
For every replay in fieldnow/replays: data/live_pairs/{ep}_s{seat}.json (recorded actions of that seat, seed, team, bank) for both seats,
data/live_meta/{ep}.json (seed, teams, rewards, recorded shop order). Index tapes.json = one row per TOP-12 farm (tape seat = that farm,
candidate plays the other seat). check.json = our own V183 / v183ms / lx3 games (candidate seat = ours, tape = opponent) for parity checks."""
import json, glob, os
from pathlib import Path
H = Path(__file__).resolve().parent; FN = H.parent / 'fieldnow'; D = H / 'data'
F = json.load(open(FN / 'field_subs_now.json')); top = {v['name']: v['rank'] for v in F.values() if v['rank'] <= 12}
tapes, check = [], []
for g in sorted(glob.glob(str(FN / 'games' / '*.json'))):
    G = json.load(open(g)); ep = G['ep']; m = G['meta']
    lp = [D / 'live_pairs' / f'{ep}_s{s}.json' for s in (0, 1)]; lm = D / 'live_meta' / f'{ep}.json'
    if not (lm.exists() and all(p.exists() for p in lp)):
        d = json.load(open(FN / 'replays' / f'episode-{ep}-replay.json')); info = d['info']; steps = d['steps']
        for s in (0, 1):
            acts = [steps[t][s]['action'] for t in range(1, len(steps))]
            json.dump({'actions': acts, 'seed': info['seed'], 'seat': s, 'team': info['TeamNames'][s], 'bank': d['rewards'][s]}, open(lp[s], 'w'))
        shops = list(steps[-1][0]['observation']['town']['unlocked_shops'])
        json.dump({'seed': info['seed'], 'TeamNames': info['TeamNames'], 'rewards': d['rewards'], 'shops': shops, 'id': d.get('id'), 'n_steps': len(steps)}, open(lm, 'w'))
        del d, steps
    teams, rw = G['teams'], G['rewards']
    for s in (0, 1):
        if teams[s] in top:
            tapes.append(dict(ep=ep, tape_seat=s, cand_seat=1 - s, team=teams[s], rank=top[teams[s]], rec=rw[s], rec_opp=rw[1 - s],
                              rec_opp_team=teams[1 - s], t=m.get('t'), group=m.get('group')))
    if 'feel the agi' in teams:
        s = teams.index('feel the agi')
        check.append(dict(ep=ep, cand_seat=s, tape_seat=1 - s, group=m.get('group'), sub=m.get('sub'), rec=rw[s], rec_opp=rw[1 - s], opp_team=teams[1 - s]))
json.dump(tapes, open(H / 'tapes.json', 'w'), indent=0); json.dump(check, open(H / 'check.json', 'w'), indent=0)
print('tapes', len(tapes), 'check', len(check))
