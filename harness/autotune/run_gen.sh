#!/bin/bash
# autotune harness entry point (local side; every game runs on the pods listed in pods.txt: "name ip port workers").
#   ./run_gen.sh pod-setup <ip> <port>        arm the in-pod self-destruct (14000 s) FIRST, install kaggle-environments 1.32.7, rsync code
#   ./run_gen.sh screen                        knob screen: det-mode digests for every SCREEN knob at z=-1/+1 (screen.py make/launch/pull; screen_report.py)
#   ./run_gen.sh init                          CMA-ES state (state/cma.json) over space_final.json, mean = base, sigma driver.SIGMA0
#   ./run_gen.sh run [HH:MM]                   generations (objective v1: eval_cand.score) until HH:MM UTC -> evals.jsonl, state/best.json
#   ./run_gen.sh band-init | band [HH:MM]      band objective (driver_band.py) with holdout rounds every 2 generations
#   ./run_gen.sh validate <tag> <cid>...       holdout validation (validate.py; VAL_SEEDS=a-b VAL_TAPES=0 PODS_FILE=... optional)
#   ./run_gen.sh report <gen>...               per-generation table (gentable.py); ./run_gen.sh landscape [min_gen]
#   ./run_gen.sh pack <tag> <cid>              build/<tag>/main.py + build/submission-<tag>.tar.gz (then loader test on a pod: hybrid/loadtest.py)
set -e
cd "$(dirname "$0")"; source /Users/1littlecoder/kaggriculture/.venv/bin/activate
case "$1" in
  pod-setup) bash setup_pod.sh "$2" "$3" 14000 && ssh -o ConnectTimeout=20 -i ~/.ssh/id_ed25519 -p "$3" root@"$2" '/opt/venv/bin/pip install -q "kaggle-environments==1.32.7" numpy scipy; /opt/venv/bin/python -c "import kaggle_environments as k;print(k.__version__)"' ;;
  screen) python screen.py make && python screen.py launch && echo "poll: python screen.py status; then python screen.py pull && python screen_report.py" ;;
  init) python driver.py init ;;
  run) nohup python driver.py run "${2:-15:00}" >> state/driver.out 2>&1 & echo "driver running; tail -f state/driver.out" ;;
  band-init) python driver_band.py init ;;
  band) nohup python driver_band.py run "${2:-15:00}" >> state/driver_band.out 2>&1 & echo "band driver running; tail -f state/driver_band.out" ;;
  validate) shift; python validate.py "$@" ;;
  report) shift; python gentable.py "$@" ;;
  landscape) python landscape.py "${2:-0}" ;;
  pack) python pack.py "$2" "$3" ;;
  *) sed -n '2,13p' "$0" ;;
esac
