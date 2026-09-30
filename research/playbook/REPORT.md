# final30/playbook — status (05:11 UTC)
- Role: specification only (no builds, no sims, no uploads). Deliverables: PLAYBOOK.md + playbook.json in this directory.
- 05:10 UTC note: coordinator message about "prefix build / handover triggers / RunPod / JUDGE_ME" reads as addressed to
  bundle/opening3; this agent does not build. The spec those agents need will be here: first cut by ~06:15, full by 07:00, update 08:30.
- Method: extract.py -> ev/<ep>.json per-step event logs (unit actions with tile, executed market orders with revenue, shed, prices)
  from the 117 fieldnow replays (pure JSON + engine price function, same lockstep as fieldnow/parse.py).
- 05:12 UTC: coordinator set HARD STOP 06:50 UTC. This agent runs no pod and no build; PLAYBOOK.md/playbook.json will be written by 06:40.
- 05:30 UTC: v1 delivered: PLAYBOOK.md (implementation spec, rules with numbers), playbook.json (345 KB: opening_hourly d0-d2 + d3-d10 per team,
  daily_mean d0-d29 per team, ledger, sell summary, rules), rules.json, tapes_all.json (raw action tapes of all 108 target farms), tab/*.
  Numbers: T3 = MMPQ 11 + DSM 15 + DECEM 11 farms; V183 28. Not determined: premium drip skip trigger, carrot trigger, early sheep release trigger.
