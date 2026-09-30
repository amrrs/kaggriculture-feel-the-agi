"""mkjobs.py <cand_tag> <opp_tag> <seed_lo> <seed_hi> [...more cand opp lo hi] > jobs.txt   (both seats; pod paths /work/jr/cands/<tag>/main.py)"""
import sys
a = sys.argv[1:]
for i in range(0, len(a), 4):
    c, o, lo, hi = a[i], a[i + 1], int(a[i + 2]), int(a[i + 3])
    for s in range(lo, hi + 1):
        for se in (0, 1): print(c, f'/work/jr/cands/{c}/main.py', o, f'/work/jr/cands/{o}/main.py', s, se)
