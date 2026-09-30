# Kaggriculture — team "feel the agi"

Agents, evaluation harness and research notes from the Kaggle **Kaggriculture** simulation competition (July–September 2026).
Start with [WRITEUP.md](WRITEUP.md).

## Layout
- `agent/g012m/`, `agent/g010c04/` — the two final submissions (`main.py` + the exact `submission-*.tar.gz` uploaded). Single file, standard library + numpy.
- `agent/base/` — the parent builds they were tuned from (`v183ms_main.py`) and the earlier lx3 line (`lx3_main.py`).
- `harness/autotune/` — CMA-ES parameter search: `space.py` (knob space), `eval_cand.py` (objective), `cma.py`, `run_gen.sh`, `evals.jsonl` (every evaluated vector), `REPORT.md` (landscape + validation tables).
- `harness/tapejudge/`, `harness/judgerun/`, `harness/kval/` — the top-field tape judge (recorded top-team games replayed against a candidate, paired), the fresh-seed bench with per-step timing, and the Kaggle-kernel runner used on the last day.
- `harness/micro/` — the route-optimisation ("micro") execution layer: design, results, optimiser.
- `research/` — reports: `playbook/` (exact policy of the top-3 teams extracted from their replays), `fieldnow/` (coin-by-coin ledger of the current top field vs our builds), and the negative results (`bundle/`, `newexec/`, `microstructure/`, `race/`, `opening3/`, `pairselect/`, `outside/`), plus the day-by-day lab notebooks (`claudefindings.md`, `codexfindings.md`, `COLLABORATION.md`).
- `reactive_v1/` — the start of a fully reactive controller (no recorded opening) with its own shop-pinned bench; day-one state and next steps in its `REPORT.md`.

## Running
```
pip install "kaggle-environments==1.32.7" numpy
python -c "from kaggle_environments import make; env=make('kaggriculture'); env.run(['agent/g012m/main.py','agent/g010c04/main.py']); print([s.reward for s in env.steps[-1]])"
```
The harness scripts assume a 32-vCPU Linux box (they were run on RunPod pods and Kaggle kernels); paths inside them are relative to this layout.

## License and credits
Apache-2.0 (see `LICENSE`, `NOTICE`). Opening library derived from public replays of top agents; early lineage from yhay81's *Three-Day Shop Router* (Apache-2.0); executor base by Codex (same team); order-book slot mechanic after thomastschinkel's *The 2945 Farm*; RNG analysis after leoprovorov. Built with Claude and Codex as coding agents.
