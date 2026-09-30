# final30/tapejudge — top-field tape judge (REPORT; updated 05:17 UTC 30 Sep)

## Numbers first (123 tapes = every top-12 farm in fieldnow's 117 current replays; candidate plays the other seat live)
Pod n01rdll9gsx3cx (cpu5c 32 vCPU), one pinned process per game, env.run (actTimeout 1 s + overage as Kaggle). A full run = 123 games, ~1.5 min.

| build | n | wins | margin all (se) | intact | margin intact-only (se) | wins intact | paired vs V183 all (se) | paired both-intact (se) | peak step |
|---|---|---|---|---|---|---|---|---|---|
| V183 (80d3cfc8) | 123 | 62 (50%) | +18530 (3868) | 86/123 (70%) | **-1663 (1882)** | 28/86 | - | - | 0.363 s |
| v183ms (cba37327) | 123 | 64 (52%) | +19215 (3849) | 84/123 (68%) | **-1937 (1689)** | 28/84 | **+686 (85)**, better/worse 101/22 | **+747 (98)**, n=84 | 0.434 s |

v183ms - V183 per team (paired, all / both-intact): MMPQ +718/+1259, DSM +741/+687, DECEM +232/+268, Vadim +679/+679, Victor +698/+899,
Mother-Goose +1031/+710, Anton +1295/+2224, Yizhou +586/+475, Majkel +548/+412, tetsuya +712/+792, monsaraida +549/+528, Zenith +496/+580.
Paired worst: -2596 (115390459 MMPQ), -1574 (Majkel), -1348 (DSM). Worst raw margins (both builds): MMPQ 115430340 -30k/-33k (intact), MMPQ -20k/-21k.
Consistent with the earlier +823/game on 141 top-tier tapes (micro/RESULTS.txt). Full per-team tables: out/V183.score, out/v183ms_vs_V183.score.

## Bundle builds vs v183ms (05:26 UTC; all 123 tapes; paired = same tape, candidate margin - v183ms margin)
| build (bundle flags) | paired all (se) | better/worse | both-intact paired (se), n=84 | intact | intact-only margin | wins | own / opp coins vs v183ms | peak step |
|---|---|---|---|---|---|---|---|---|
| bz (all off = parity) | -6 (3) | 0/5 | -9 (5) | 68% | -1947 | 64 | -5 / +1 | 0.426 |
| bl (LAND4) | **-4100 (463)** | 21/102 | -4231 (515) | 72% | -5464 | 56 | -2445 / +1654 | **0.729 (2 steps > 0.6 s)** |
| bt (TOM+FEED) | **-9401 (547)** | 2/121 | -8375 (563) | 72% | -9000 | 50 | -4895 / +4506 | 0.405 |
| blt (LAND4+TOM+FEED) | **-14940 (809)** | 2/121 | -14474 (1019) | 73% | -15068 | 45 | -8376 / +6565 | 0.414 |
| bltf (+FERT0) | **-15468 (778)** | 1/122 | -14867 (925) | 73% | -15472 | 42 | -8640 / +6828 | 0.589 |
| bc (05:27) | -72 (64) | 52/55 | -17 (73) | 69% | -1786 | 64 | +2 / +75 | 0.405 |
| ball (+HAND+1 +CAR) | **-16642 (879)** | 0/123 | -16322 (1116) | 73% | -16745 | 41 | -10647 / +5996 | 0.553 |
bz reproduces v183ms (judge noise floor: 5/123 games move by a few coins through the 0.35 s wall cap). Every bundle flag set loses to v183ms
against the top field on every team row (see blocks below); the tape side GAINS coins (+1.7..+6.8k) as our pressure on the shared markets drops,
and intact rate rises (68% -> 72-73%), i.e. the bias here runs AGAINST the bundle only mildly and cannot explain -4..-17k.
Poller: poll.sh re-runs judge_bundle.sh every 5 min until 08:55 UTC; any new or changed bundle/build/*/main.py (keyed by SHA-256) is scored
and appended below automatically.

## Pipeline verification (exact reproduction)
- Local 2-3 game check (allowed): V183 replayed its own live games 115421746 (s0), 115432929 (s1), 114763214 (s1, vs Anton): rewards == recorded exactly in 3/3.
- On the pod, V183 on all 28 of its own live games in the set (56641767 + 56686499): **25/28 exact**, 3 off by 1-7 coins
  (114817723 103869 vs 103871; 114841133 129445/153121 vs 129446/153119; 114887589 opp 140540 vs 140533). 43/43 intact.
- v183ms on its own 13 live games: 8/13 exact, the rest off by 2..455 coins (its 0.35 s wall cap makes plans CPU-speed dependent). 43/43 intact.
=> the tape/seed/shop pinning reproduces live play; residual 1-coin drifts are negligible.

## KNOWN BIAS — read before using the all-games number
A tape cannot react. The recorded agent replays its actions blindly; when the candidate changes the shared market (prices it sells/buys at),
the tape's cash path changes, a purchase fails and the recorded plan cascades (tiles never planted, animals not bought).
- 37/123 (V183) and 39/123 (v183ms) tapes keep < 90% of their recorded coins (mean kept 68%; three Anton tapes collapse to 0-21%).
  Those games show margins of +65k on average: **the all-games margin (+18.5k) is meaningless as a strength estimate**. Use intact-only
  (the top field beats V183 by ~1.7k/game on intact tapes, 28/86 wins) and the PAIRED deltas.
- A candidate that floods a market the recorded agent also sells into (or buys what it buys) will break more tapes: its intact rate drops
  and its all-games margin RISES spuriously. Always compare intact rate against the baseline; a paired gain that comes with a lower intact
  rate is suspect. Both-intact paired is the conservative number (it drops the games where either run broke the tape).
- The top agents' reactions to our play are absent both ways (they cannot punish or exploit a change). Tapes are from 28-30 Sep active subs;
  11 of the 123 top-12 farms come from our own V183 games of 28 Sep (older opponent subs).
- Weed RNG: shared per night across both farms (seat 0 drawn first), so a seat-0 candidate changes the tape's weeds; intact rate by tape seat
  is the same (tape s0 69%, s1 71%), so this is not the main break source.

## Files
mktapes.py (tapes from fieldnow/replays -> data/, tapes.json 123 rows, check.json 49 own games), tj_game.py (one game; autopsy_tf-derived),
runq.py (pod runner, taskset-pinned), run_judge.sh <cand main.py> <tag> [tapes|check|all] (push, run, pull, score vs $BASE default v183ms),
score.py <tag> [base] [--set check], judge_bundle.sh (scores every bundle/build/*/main.py by SHA, appends here), setup_pod.sh, mkpod.sh, podip.sh.

## NOT done
- No fresh-seed games; no reaction model for the tapes; weeds not pinned for the tape farm; no uploads.

## Bundle builds (appended automatically, paired vs v183ms)

### b_ball_11ee82b0f7b2  (05:19 UTC) bundle/build/ball/main.py sha256 11ee82b0f7b22ff68c87e43896d0d643e21d6f0b99bdb87e610a8cb8b9855903
```
11ee82b0f7b22ff68c87e43896d0d643e21d6f0b99bdb87e610a8cb8b9855903  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/ball/main.py
123 jobs on 32 cpus
done
b_ball_11ee82b0f7b2: n=123 wins 41 (33%) margin +2573 (se 3731) own 109291 opp 106719 | intact 90/123 (73%) intact-only margin -16745 (se 1937) wins 9 | peak step 0.553s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_ball_11ee82b0f7b2 - v183ms: n=123 delta -16642 (se 879) better/worse 0/123 wins 64->41 | own -10647 opp +5996 | both-intact n=84 delta -16322 (se 1116)
  paired worst 5: [(-54826, 115431833, 'tetsuya & yuan'), (-43670, 115416427, 'tetsuya & yuan'), (-41422, 115418160, 'Vadim Vasilenk'), (-40612, 115429680, 'Zenith'), (-40546, 114944321, 'tetsuya & yuan')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2  -10051      8  -11677 -12206
   2 DSM                             15    4   -3535     12  -13438 -12780
   3 DECEM                           11    8  +34083      5  -16365 -15080
   4 Vadim Vasilenko                 11    3   -4104      8  -16751 -15399
   5 Victor @ Tufa Labs              11    4   -3252      9  -14168 -13703
   6 Unknown Mother-Goose            12    0  -23793     12  -15370 -15540
   7 Anton Tikhonov                   7    6  +83575      2  -21058 -13066
   8 Yizhou                           7    6  +30339      1  -14012 -26326
   9 Majkel1337                       9    2     -48      8  -14959 -16026
  10 tetsuya & yuanzhe & guoqin      11    2  -18755     10  -23861 -21831
  11 monsaraida                       7    2   +2705      6  -19510 -18845
  12 Zenith                          11    2  -12552      9  -21209 -22937
  worst 5 margins: [(-57173, 115431833, 'tetsuya & yuan', 'I'), (-56845, 114944321, 'tetsuya & yuan', 'I'), (-47028, 115430340, 'M & M & P & Q', 'I'), (-42146, 115429680, 'Zenith', 'I'), (-41969, 115426593, 'tetsuya & yuan', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0835, 115422295, 'Anton Tikhonov'), (0.2134, 115423940, 'Anton Tikhonov'), (0.4405, 115425513, 'Zenith'), (0.5, 115430326, 'Anton Tikhonov')]
```

### b_bl_74fb447925c7  (05:20 UTC) bundle/build/bl/main.py sha256 74fb447925c75e621d5a61431c71764636a34e0cf4d42b9ad2367d2f8205f356
```
74fb447925c75e621d5a61431c71764636a34e0cf4d42b9ad2367d2f8205f356  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bl/main.py
123 jobs on 32 cpus
done
b_bl_74fb447925c7: n=123 wins 56 (46%) margin +15115 (se 4017) own 117493 opp 102377 | intact 89/123 (72%) intact-only margin -5464 (se 1955) wins 23 | peak step 0.729s, steps>0.6s 2, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bl_74fb447925c7 - v183ms: n=123 delta -4100 (se 463) better/worse 21/102 wins 64->56 | own -2445 opp +1654 | both-intact n=84 delta -4231 (se 515)
  paired worst 5: [(-15257, 115390715, 'Victor @ Tufa '), (-14561, 115430326, 'Unknown Mother'), (-13354, 115428697, 'Majkel1337'), (-11899, 115428903, 'Yizhou'), (-11251, 115390715, 'Unknown Mother')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -4000      8   -5625  -6027
   2 DSM                             15    6   +4965     12   -4939  -4612
   3 DECEM                           11    8  +48218      5   -2229  -5827
   4 Vadim Vasilenko                 11    7   +8289      8   -4357  -2819
   5 Victor @ Tufa Labs              11    6   +8037      9   -2879  -2701
   6 Unknown Mother-Goose            12    1  -15012     12   -6590  -6246
   7 Anton Tikhonov                   7    6 +103563      2   -1071  -7840
   8 Yizhou                           7    7  +38359      1   -5992  +5210
   9 Majkel1337                       9    3   +9510      8   -5401  -5069
  10 tetsuya & yuanzhe & guoqin      11    4   +2263      9   -2844  -2376
  11 monsaraida                       7    4  +20706      6   -1509  -2962
  12 Zenith                          11    2   +4547      9   -4110  -3832
  worst 5 margins: [(-35687, 115430340, 'M & M & P & Q', 'I'), (-30672, 115408974, 'M & M & P & Q', 'I'), (-29050, 115431962, 'Unknown Mother', 'I'), (-26407, 115425958, 'M & M & P & Q', 'I'), (-25973, 115413582, 'M & M & P & Q', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0762, 115422295, 'Anton Tikhonov'), (0.209, 115423940, 'Anton Tikhonov'), (0.4185, 115425513, 'Zenith'), (0.4824, 115430326, 'Anton Tikhonov')]
```

### b_blt_a7bd597220a3  (05:22 UTC) bundle/build/blt/main.py sha256 a7bd597220a31c19ce772fe26bce2b49139d1dc9cfe3a76fc40e4f124ad66935
```
a7bd597220a31c19ce772fe26bce2b49139d1dc9cfe3a76fc40e4f124ad66935  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/blt/main.py
123 jobs on 32 cpus
done
b_blt_a7bd597220a3: n=123 wins 45 (37%) margin +4275 (se 3763) own 111562 opp 107287 | intact 90/123 (73%) intact-only margin -15068 (se 1927) wins 13 | peak step 0.414s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_blt_a7bd597220a3 - v183ms: n=123 delta -14940 (se 809) better/worse 2/121 wins 64->45 | own -8376 opp +6565 | both-intact n=84 delta -14474 (se 1019)
  paired worst 5: [(-45977, 115431833, 'tetsuya & yuan'), (-42081, 115416427, 'tetsuya & yuan'), (-38208, 115425513, 'Unknown Mother'), (-37693, 115429680, 'Zenith'), (-31864, 115427468, 'Zenith')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -9955      8  -11581 -11784
   2 DSM                             15    5   -2425     12  -12329 -11275
   3 DECEM                           11    8  +35727      5  -14721 -11994
   4 Vadim Vasilenko                 11    4    -236      8  -12882 -11685
   5 Victor @ Tufa Labs              11    4    -753      9  -11669 -11736
   6 Unknown Mother-Goose            12    0  -23760     12  -15337 -15290
   7 Anton Tikhonov                   7    6  +87913      2  -16721 -13334
   8 Yizhou                           7    6  +29383      1  -14967 -23670
   9 Majkel1337                       9    2   +1109      8  -13801 -14804
  10 tetsuya & yuanzhe & guoqin      11    2  -16897     10  -22004 -19925
  11 monsaraida                       7    4   +7536      6  -14679 -14197
  12 Zenith                          11    2  -11204      9  -19861 -20526
  worst 5 margins: [(-57010, 115430340, 'M & M & P & Q', 'I'), (-48324, 115431833, 'tetsuya & yuan', 'I'), (-47788, 114944321, 'tetsuya & yuan', 'I'), (-39227, 115429680, 'Zenith', 'I'), (-34731, 115430340, 'DSM', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0821, 115422295, 'Anton Tikhonov'), (0.2141, 115423940, 'Anton Tikhonov'), (0.4397, 115425513, 'Zenith'), (0.4985, 115430326, 'Anton Tikhonov')]
```

### b_bltf_43ebabcd4c90  (05:23 UTC) bundle/build/bltf/main.py sha256 43ebabcd4c90a4c2c49be05040d64a4e15f80219f86b421b1b7d025ac0451498
```
43ebabcd4c90a4c2c49be05040d64a4e15f80219f86b421b1b7d025ac0451498  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bltf/main.py
123 jobs on 32 cpus
done
b_bltf_43ebabcd4c90: n=123 wins 42 (34%) margin +3747 (se 3708) own 111298 opp 107550 | intact 90/123 (73%) intact-only margin -15472 (se 1869) wins 10 | peak step 0.589s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bltf_43ebabcd4c90 - v183ms: n=123 delta -15468 (se 778) better/worse 1/122 wins 64->42 | own -8640 opp +6828 | both-intact n=84 delta -14867 (se 925)
  paired worst 5: [(-46551, 115416427, 'tetsuya & yuan'), (-40770, 115427468, 'Zenith'), (-36562, 115387712, 'monsaraida'), (-35518, 115431833, 'tetsuya & yuan'), (-34458, 115429680, 'Zenith')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2  -10527      8  -12153 -11620
   2 DSM                             15    5   -3673     12  -13577 -13459
   3 DECEM                           11    8  +34933      5  -15514 -13582
   4 Vadim Vasilenko                 11    4   -2425      8  -15071 -13951
   5 Victor @ Tufa Labs              11    4   -2801      9  -13717 -12233
   6 Unknown Mother-Goose            12    0  -22802     12  -14379 -14134
   7 Anton Tikhonov                   7    5  +85133      2  -19500 -15252
   8 Yizhou                           7    6  +31567      1  -12783 -19762
   9 Majkel1337                       9    2   +1849      8  -13062 -14006
  10 tetsuya & yuanzhe & guoqin      11    2  -14868     10  -19974 -17305
  11 monsaraida                       7    2   +5811      6  -16404 -16020
  12 Zenith                          11    2  -12000      9  -20657 -22078
  worst 5 margins: [(-51057, 115430340, 'M & M & P & Q', 'I'), (-47814, 114944321, 'tetsuya & yuan', 'I'), (-43363, 115427468, 'Zenith', 'I'), (-37865, 115431833, 'tetsuya & yuan', 'I'), (-37629, 115430340, 'DSM', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0832, 115422295, 'Anton Tikhonov'), (0.2114, 115423940, 'Anton Tikhonov'), (0.4404, 115425513, 'Zenith'), (0.4987, 115430326, 'Anton Tikhonov')]
```

### b_bt_3691c8a6ef57  (05:24 UTC) bundle/build/bt/main.py sha256 3691c8a6ef570fd9b036332f325e96eb6ba2c72d127736ae352ef853153e4ae6
```
3691c8a6ef570fd9b036332f325e96eb6ba2c72d127736ae352ef853153e4ae6  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bt/main.py
123 jobs on 32 cpus
done
b_bt_3691c8a6ef57: n=123 wins 50 (41%) margin +9814 (se 3645) own 115042 opp 105229 | intact 89/123 (72%) intact-only margin -9000 (se 1858) wins 18 | peak step 0.405s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bt_3691c8a6ef57 - v183ms: n=123 delta -9401 (se 547) better/worse 2/121 wins 64->50 | own -4895 opp +4506 | both-intact n=84 delta -8375 (se 563)
  paired worst 5: [(-26704, 115430326, 'Anton Tikhonov'), (-26384, 114944321, 'tetsuya & yuan'), (-25669, 115392457, 'DECEM'), (-25568, 115430340, 'DSM'), (-24276, 115416427, 'tetsuya & yuan')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -7187      8   -8813  -9867
   2 DSM                             15    5    -317     12  -10220 -10021
   3 DECEM                           11    8  +37023      5  -13425  -8782
   4 Vadim Vasilenko                 11    6   +4631      8   -8015  -8293
   5 Victor @ Tufa Labs              11    5   +3684      9   -7232  -6418
   6 Unknown Mother-Goose            12    0  -15583     12   -7161  -6887
   7 Anton Tikhonov                   7    6  +89906      2  -14727  -4922
   8 Yizhou                           7    6  +37533      1   -6818 -12188
   9 Majkel1337                       9    3   +6912      8   -7998  -7499
  10 tetsuya & yuanzhe & guoqin      11    3   -6010     10  -11116  -9164
  11 monsaraida                       7    4  +12108      6  -10107  -9518
  12 Zenith                          11    2    +569      8   -8088  -7935
  worst 5 margins: [(-52508, 115430340, 'M & M & P & Q', 'I'), (-43324, 115430340, 'DSM', 'I'), (-42683, 114944321, 'tetsuya & yuan', 'I'), (-29683, 115425958, 'M & M & P & Q', 'I'), (-28845, 115431962, 'Unknown Mother', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0813, 115422295, 'Anton Tikhonov'), (0.2105, 115423940, 'Anton Tikhonov'), (0.4332, 115425513, 'Zenith'), (0.497, 115430326, 'Anton Tikhonov')]
```

### b_bz_b252f65ba786  (05:26 UTC) bundle/build/bz/main.py sha256 b252f65ba7863e45d4994e9e8f125679ed6d43add86a5803866091efd0ca8d3c
```
b252f65ba7863e45d4994e9e8f125679ed6d43add86a5803866091efd0ca8d3c  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bz/main.py
123 jobs on 32 cpus
done
b_bz_b252f65ba786: n=123 wins 64 (52%) margin +19209 (se 3850) own 119933 opp 100724 | intact 84/123 (68%) intact-only margin -1947 (se 1689) wins 28 | peak step 0.426s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bz_b252f65ba786 - v183ms: n=123 delta -6 (se 3) better/worse 0/5 wins 64->64 | own -5 opp +1 | both-intact n=84 delta -9 (se 5)
  paired worst 5: [(-274, 115427458, 'tetsuya & yuan'), (-229, 115390479, 'Victor @ Tufa '), (-217, 115427326, 'Zenith'), (-23, 115428247, 'Majkel1337'), (-19, 115425939, 'Unknown Mother')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   +1626      8      +0     +0
   2 DSM                             15    8   +9904     12      +0     +0
   3 DECEM                           11    8  +50447      4      +0     +0
   4 Vadim Vasilenko                 11    7  +12647      7      +0     +0
   5 Victor @ Tufa Labs              11    6  +10895      9     -21    -25
   6 Unknown Mother-Goose            12    1   -8424     11      -2     -2
   7 Anton Tikhonov                   7    7 +104633      2      +0     +0
   8 Yizhou                           7    7  +44350      1      +0     +0
   9 Majkel1337                       9    8  +14908      7      -3     -3
  10 tetsuya & yuanzhe & guoqin      11    4   +5082      9     -25    -30
  11 monsaraida                       7    4  +22215      6      +0     +0
  12 Zenith                          11    2   +8637      8     -20    -27
  worst 5 margins: [(-30211, 115430340, 'M & M & P & Q', 'I'), (-20417, 115408974, 'M & M & P & Q', 'I'), (-18673, 115431962, 'Unknown Mother', 'x'), (-18098, 115422937, 'Vadim Vasilenk', 'I'), (-17869, 115425958, 'M & M & P & Q', 'I')]
  lowest tape keep (opp_frac): [(0.0018, 115427471, 'Anton Tikhonov'), (0.0831, 115422295, 'Anton Tikhonov'), (0.2088, 115423940, 'Anton Tikhonov'), (0.4309, 115425513, 'Zenith'), (0.4859, 115430326, 'Anton Tikhonov')]
```

### b_bc_7a936f5a592c  (05:27 UTC) bundle/build/bc/main.py sha256 7a936f5a592c5c34cc6d9e5136fb2c7034388c46503898d982ba518cf446cb8a
```
7a936f5a592c5c34cc6d9e5136fb2c7034388c46503898d982ba518cf446cb8a  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bc/main.py
123 jobs on 32 cpus
done
b_bc_7a936f5a592c: n=123 wins 64 (52%) margin +19143 (se 3840) own 119940 opp 100797 | intact 85/123 (69%) intact-only margin -1786 (se 1674) wins 29 | peak step 0.405s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bc_7a936f5a592c - v183ms: n=123 delta -72 (se 64) better/worse 52/55 wins 64->64 | own +2 opp +75 | both-intact n=84 delta -17 (se 73)
  paired worst 5: [(-2593, 115381978, 'DECEM'), (-2379, 115422937, 'Vadim Vasilenk'), (-1932, 115423940, 'Anton Tikhonov'), (-1910, 115424138, 'Unknown Mother'), (-1732, 115430326, 'Anton Tikhonov')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   +1998      8    +372   +235
   2 DSM                             15    8   +9834     12     -70   -102
   3 DECEM                           11    8  +50351      4     -96   +386
   4 Vadim Vasilenko                 11    7  +12435      8    -211   -204
   5 Victor @ Tufa Labs              11    6  +10650      9    -266   -239
   6 Unknown Mother-Goose            12    1   -8613     11    -190   -140
   7 Anton Tikhonov                   7    7 +104136      2    -497    -65
   8 Yizhou                           7    7  +44316      1     -34  +1033
   9 Majkel1337                       9    8  +15207      7    +297   +364
  10 tetsuya & yuanzhe & guoqin      11    4   +5055      9     -51    -38
  11 monsaraida                       7    4  +22276      6     +61    +94
  12 Zenith                          11    2   +8460      8    -197   -270
  worst 5 margins: [(-30196, 115430340, 'M & M & P & Q', 'I'), (-20487, 115408974, 'M & M & P & Q', 'I'), (-20477, 115422937, 'Vadim Vasilenk', 'I'), (-19415, 115431962, 'Unknown Mother', 'x'), (-18284, 115381978, 'DSM', 'I')]
  lowest tape keep (opp_frac): [(0.0019, 115427471, 'Anton Tikhonov'), (0.0834, 115422295, 'Anton Tikhonov'), (0.209, 115423940, 'Anton Tikhonov'), (0.4305, 115425513, 'Zenith'), (0.4849, 115430326, 'Anton Tikhonov')]
```

### b_bf_00eaf94d10e7  (05:29 UTC) bundle/build/bf/main.py sha256 00eaf94d10e7d85a1ba4b10cb7efbd022a1c869af020b541ab1e8594967c136d
```
00eaf94d10e7d85a1ba4b10cb7efbd022a1c869af020b541ab1e8594967c136d  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bf/main.py
123 jobs on 32 cpus
done
b_bf_00eaf94d10e7: n=123 wins 52 (42%) margin +12459 (se 3740) own 116797 opp 104338 | intact 90/123 (73%) intact-only margin -6706 (se 1858) wins 20 | peak step 0.421s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bf_00eaf94d10e7 - v183ms: n=123 delta -6756 (se 373) better/worse 1/122 wins 64->52 | own -3141 opp +3615 | both-intact n=84 delta -6182 (se 384)
  paired worst 5: [(-22791, 115430340, 'DSM'), (-19918, 115392457, 'DECEM'), (-18915, 115428651, 'Anton Tikhonov'), (-17409, 115416427, 'tetsuya & yuan'), (-16627, 115430340, 'M & M & P & Q')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -4220      8   -5846  -6337
   2 DSM                             15    6   +1647     12   -8257  -7889
   3 DECEM                           11    8  +42198      5   -8249  -5810
   4 Vadim Vasilenko                 11    7   +5697      8   -6950  -6591
   5 Victor @ Tufa Labs              11    5   +5071      9   -5845  -5715
   6 Unknown Mother-Goose            12    0  -14179     12   -5756  -5322
   7 Anton Tikhonov                   7    6  +94894      2   -9740  -7824
   8 Yizhou                           7    6  +38254      1   -6096 -11705
   9 Majkel1337                       9    3   +9507      8   -5403  -5319
  10 tetsuya & yuanzhe & guoqin      11    3   -1226     10   -6333  -5492
  11 monsaraida                       7    4  +15140      6   -7075  -6032
  12 Zenith                          11    2   +2877      9   -5781  -5542
  worst 5 margins: [(-46838, 115430340, 'M & M & P & Q', 'I'), (-40547, 115430340, 'DSM', 'I'), (-29214, 115431962, 'Unknown Mother', 'I'), (-25877, 115427458, 'tetsuya & yuan', 'I'), (-24284, 114817142, 'Unknown Mother', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.08, 115422295, 'Anton Tikhonov'), (0.2102, 115423940, 'Anton Tikhonov'), (0.4322, 115425513, 'Zenith'), (0.4876, 115430326, 'Anton Tikhonov')]
```

### b_bf2_8c55f6fb4362  (05:30 UTC) bundle/build/bf2/main.py sha256 8c55f6fb4362748f2dec440925035d269a541f0105ee637f95b2543fdce27ef5
```
8c55f6fb4362748f2dec440925035d269a541f0105ee637f95b2543fdce27ef5  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bf2/main.py
123 jobs on 32 cpus
done
b_bf2_8c55f6fb4362: n=123 wins 61 (50%) margin +18018 (se 3798) own 119202 opp 101184 | intact 85/123 (69%) intact-only margin -2114 (se 1891) wins 26 | peak step 0.772s, steps>0.6s 1, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bf2_8c55f6fb4362 - v183ms: n=123 delta -1197 (se 236) better/worse 23/65 wins 64->61 | own -736 opp +461 | both-intact n=84 delta -1047 (se 237)
  paired worst 5: [(-10948, 115392457, 'DECEM'), (-10825, 115430340, 'DSM'), (-10160, 115430340, 'M & M & P & Q'), (-9399, 115423940, 'Anton Tikhonov'), (-7691, 115427468, 'monsaraida')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2    +562      8   -1064  -1578
   2 DSM                             15    8   +8214     12   -1689  -1628
   3 DECEM                           11    8  +48521      5   -1927   -929
   4 Vadim Vasilenko                 11    7  +11246      7   -1400  -1341
   5 Victor @ Tufa Labs              11    5   +9630      9   -1286  -1414
   6 Unknown Mother-Goose            12    0   -9086     11    -663   -723
   7 Anton Tikhonov                   7    7 +102351      2   -2282   -482
   8 Yizhou                           7    7  +43832      1    -519  -2405
   9 Majkel1337                       9    8  +15112      7    +202   +298
  10 tetsuya & yuanzhe & guoqin      11    3   +4423      9    -683  -1077
  11 monsaraida                       7    4  +20129      6   -2086  -1152
  12 Zenith                          11    2   +7607      8   -1050   -517
  worst 5 margins: [(-40371, 115430340, 'M & M & P & Q', 'I'), (-28581, 115430340, 'DSM', 'I'), (-20417, 115408974, 'M & M & P & Q', 'I'), (-20103, 115427458, 'tetsuya & yuan', 'I'), (-18673, 115431962, 'Unknown Mother', 'x')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0795, 115422295, 'Anton Tikhonov'), (0.2089, 115423940, 'Anton Tikhonov'), (0.4275, 115425513, 'Zenith'), (0.4818, 115430326, 'Anton Tikhonov')]
```

### b_bf2c_8397eee245ce  (05:31 UTC) bundle/build/bf2c/main.py sha256 8397eee245ceea297dd744b6c5a63f7f90ae43d4971a88965f54768904443821
```
8397eee245ceea297dd744b6c5a63f7f90ae43d4971a88965f54768904443821  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bf2c/main.py
123 jobs on 32 cpus
done
b_bf2c_8397eee245ce: n=123 wins 63 (51%) margin +18104 (se 3800) own 119305 opp 101200 | intact 85/123 (69%) intact-only margin -1978 (se 1897) wins 28 | peak step 0.401s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bf2c_8397eee245ce - v183ms: n=123 delta -1111 (se 244) better/worse 48/72 wins 64->63 | own -633 opp +477 | both-intact n=84 delta -910 (se 235)
  paired worst 5: [(-10664, 115430340, 'DSM'), (-10375, 115392457, 'DECEM'), (-10047, 115430340, 'M & M & P & Q'), (-9479, 115381978, 'DECEM'), (-8045, 115423940, 'Anton Tikhonov')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2    +922      8    -704  -1320
   2 DSM                             15    8   +8362     12   -1541  -1430
   3 DECEM                           11    8  +48403      5   -2045   -677
   4 Vadim Vasilenko                 11    7  +11167      7   -1480  -1377
   5 Victor @ Tufa Labs              11    5   +9762      9   -1154  -1207
   6 Unknown Mother-Goose            12    1   -9164     11    -741   -639
   7 Anton Tikhonov                   7    7 +102637      2   -1996     +4
   8 Yizhou                           7    7  +44340      1     -10    -99
   9 Majkel1337                       9    8  +15168      7    +258   +380
  10 tetsuya & yuanzhe & guoqin      11    4   +4424      9    -682  -1081
  11 monsaraida                       7    4  +20326      6   -1889  -1003
  12 Zenith                          11    2   +7480      8   -1178   -662
  worst 5 margins: [(-40258, 115430340, 'M & M & P & Q', 'I'), (-28420, 115430340, 'DSM', 'I'), (-20538, 115431962, 'Unknown Mother', 'x'), (-20487, 115408974, 'M & M & P & Q', 'I'), (-20483, 115427458, 'tetsuya & yuan', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0802, 115422295, 'Anton Tikhonov'), (0.209, 115423940, 'Anton Tikhonov'), (0.4275, 115425513, 'Zenith'), (0.4817, 115430326, 'Anton Tikhonov')]
```

### b_bh_11c9a08a89ff  (05:32 UTC) bundle/build/bh/main.py sha256 11c9a08a89ffb6cff856d10088575492c43beb528cddd4aaf8310445d289a111
```
11c9a08a89ffb6cff856d10088575492c43beb528cddd4aaf8310445d289a111  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bh/main.py
123 jobs on 32 cpus
done
b_bh_11c9a08a89ff: n=123 wins 60 (49%) margin +17764 (se 3861) own 118293 opp 100529 | intact 84/123 (68%) intact-only margin -2515 (se 1919) wins 24 | peak step 0.392s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bh_11c9a08a89ff - v183ms: n=123 delta -1451 (se 110) better/worse 10/113 wins 64->60 | own -1645 opp -194 | both-intact n=83 delta -1399 (se 119)
  paired worst 5: [(-6691, 115431962, 'Unknown Mother'), (-4772, 115425957, 'Unknown Mother'), (-4258, 115424138, 'Unknown Mother'), (-4153, 115416427, 'tetsuya & yuan'), (-4097, 115425958, 'M & M & P & Q')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2      -6      8   -1632  -2162
   2 DSM                             15    7   +8498     12   -1406  -1205
   3 DECEM                           11    8  +49522      5    -926  -1088
   4 Vadim Vasilenko                 11    7  +11358      7   -1288   -939
   5 Victor @ Tufa Labs              11    5   +9499      9   -1417  -1474
   6 Unknown Mother-Goose            12    1  -10777     11   -2354  -1960
   7 Anton Tikhonov                   7    6 +102520      2   -2113  -2054
   8 Yizhou                           7    7  +43117      1   -1233   -832
   9 Majkel1337                       9    7  +13723      6   -1187  -1316
  10 tetsuya & yuanzhe & guoqin      11    4   +3862      9   -1245   -833
  11 monsaraida                       7    4  +20738      6   -1477  -1317
  12 Zenith                          11    2   +7466      8   -1192  -1296
  worst 5 margins: [(-33498, 115430340, 'M & M & P & Q', 'I'), (-25364, 115431962, 'Unknown Mother', 'x'), (-21966, 115425958, 'M & M & P & Q', 'I'), (-21312, 115408974, 'M & M & P & Q', 'I'), (-19631, 115430334, 'M & M & P & Q', 'I')]
  lowest tape keep (opp_frac): [(0.0018, 115427471, 'Anton Tikhonov'), (0.0828, 115422295, 'Anton Tikhonov'), (0.2079, 115423940, 'Anton Tikhonov'), (0.4307, 115425513, 'Zenith'), (0.4838, 115430326, 'Anton Tikhonov')]
```

### b_blc_8e7bb5375c4e  (05:34 UTC) bundle/build/blc/main.py sha256 8e7bb5375c4e7003e691dafe6f390d2c8ccb222c05b9967c0d2abccc16ae6757
```
8e7bb5375c4e7003e691dafe6f390d2c8ccb222c05b9967c0d2abccc16ae6757  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/blc/main.py
123 jobs on 32 cpus
done
b_blc_8e7bb5375c4e: n=123 wins 57 (46%) margin +15428 (se 4023) own 117740 opp 102313 | intact 88/123 (72%) intact-only margin -6015 (se 1775) wins 23 | peak step 0.592s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_blc_8e7bb5375c4e - v183ms: n=123 delta -3788 (se 470) better/worse 24/99 wins 64->57 | own -2198 opp +1590 | both-intact n=84 delta -3974 (se 517)
  paired worst 5: [(-15257, 115390715, 'Victor @ Tufa '), (-14317, 115430326, 'Unknown Mother'), (-13354, 115428697, 'Majkel1337'), (-12160, 115428903, 'Yizhou'), (-12084, 115428651, 'Anton Tikhonov')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -3327      8   -4953  -5614
   2 DSM                             15    6   +5177     12   -4727  -4451
   3 DECEM                           11    8  +48794      4   -1654  -6169
   4 Vadim Vasilenko                 11    8   +8558      8   -4089  -2354
   5 Victor @ Tufa Labs              11    6   +8491      9   -2425  -2398
   6 Unknown Mother-Goose            12    1  -14520     12   -6097  -5796
   7 Anton Tikhonov                   7    6 +103063      2   -1570  -7314
   8 Yizhou                           7    7  +38640      1   -5710  +4850
   9 Majkel1337                       9    3  +10103      8   -4807  -4646
  10 tetsuya & yuanzhe & guoqin      11    4   +2529      9   -2578  -2052
  11 monsaraida                       7    4  +20801      6   -1414  -2894
  12 Zenith                          11    2   +4566      9   -4091  -3864
  worst 5 margins: [(-37457, 115430340, 'M & M & P & Q', 'I'), (-29191, 115408974, 'M & M & P & Q', 'I'), (-28078, 115431962, 'Unknown Mother', 'I'), (-26316, 115413582, 'M & M & P & Q', 'I'), (-25652, 115425958, 'M & M & P & Q', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0777, 115422295, 'Anton Tikhonov'), (0.2093, 115423940, 'Anton Tikhonov'), (0.4197, 115425513, 'Zenith'), (0.4826, 115430326, 'Anton Tikhonov')]
```

### b_blt2_14002e125051  (05:35 UTC) bundle/build/blt2/main.py sha256 14002e125051616b47393b380a88d706808664016cb1e74d04aa03fc958f0ba3
```
14002e125051616b47393b380a88d706808664016cb1e74d04aa03fc958f0ba3  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/blt2/main.py
123 jobs on 32 cpus
done
b_blt2_14002e125051: n=123 wins 53 (43%) margin +12873 (se 3811) own 115967 opp 103094 | intact 88/123 (72%) intact-only margin -7222 (se 1928) wins 19 | peak step 0.455s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_blt2_14002e125051 - v183ms: n=123 delta -6342 (se 606) better/worse 12/111 wins 64->53 | own -3971 opp +2371 | both-intact n=84 delta -6194 (se 806)
  paired worst 5: [(-35585, 115431833, 'tetsuya & yuan'), (-29652, 115387712, 'monsaraida'), (-25567, 115429680, 'Zenith'), (-21511, 115430326, 'Anton Tikhonov'), (-20945, 115418160, 'Zenith')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -1563      8   -3189  -3003
   2 DSM                             15    7   +6298     12   -3606  -3109
   3 DECEM                           11    8  +45257      5   -5190  -6240
   4 Vadim Vasilenko                 11    6   +7723      8   -4923  -3458
   5 Victor @ Tufa Labs              11    5   +6958      9   -3958  -3575
   6 Unknown Mother-Goose            12    0  -15368     12   -6945  -7023
   7 Anton Tikhonov                   7    6  +94859      2   -9774  -4792
   8 Yizhou                           7    7  +38420      1   -5931  -6984
   9 Majkel1337                       9    4  +12287      7   -2624  -2446
  10 tetsuya & yuanzhe & guoqin      11    2   -7272      9  -12379 -11774
  11 monsaraida                       7    4  +13586      6   -8629  -9753
  12 Zenith                          11    2   -2494      9  -11151 -12779
  worst 5 margins: [(-37932, 115431833, 'tetsuya & yuan', 'I'), (-36051, 114944321, 'tetsuya & yuan', 'I'), (-32694, 115430340, 'M & M & P & Q', 'I'), (-29130, 115418160, 'Zenith', 'I'), (-27101, 115429680, 'Zenith', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0817, 115422295, 'Anton Tikhonov'), (0.2115, 115423940, 'Anton Tikhonov'), (0.4322, 115425513, 'Zenith'), (0.4956, 115430326, 'Anton Tikhonov')]
```

### b_bn_fcfc6dae095b  (05:37 UTC) bundle/build/bn/main.py sha256 fcfc6dae095bf08bb248e747e7c7bb7f8565736ad2b3572ebd0341d4ceb3d815
```
fcfc6dae095bf08bb248e747e7c7bb7f8565736ad2b3572ebd0341d4ceb3d815  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bn/main.py
123 jobs on 32 cpus
done
b_bn_fcfc6dae095b: n=123 wins 63 (51%) margin +18659 (se 3847) own 119625 opp 100966 | intact 86/123 (70%) intact-only margin -1006 (se 1981) wins 28 | peak step 0.589s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bn_fcfc6dae095b - v183ms: n=123 delta -556 (se 99) better/worse 36/87 wins 64->63 | own -313 opp +244 | both-intact n=84 delta -615 (se 115)
  paired worst 5: [(-3145, 115427326, 'Vadim Vasilenk'), (-2942, 115423940, 'Anton Tikhonov'), (-2843, 115430340, 'M & M & P & Q'), (-2707, 115422295, 'Anton Tikhonov'), (-2581, 115387741, 'DECEM')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2    +934      8    -692   -836
   2 DSM                             15    8   +9395     12    -509   -656
   3 DECEM                           11    8  +50257      5    -191   -856
   4 Vadim Vasilenko                 11    7  +12017      7    -629   -669
   5 Victor @ Tufa Labs              11    5  +10237      9    -679   -810
   6 Unknown Mother-Goose            12    1   -8927     11    -504   -394
   7 Anton Tikhonov                   7    7 +103545      2   -1088   -441
   8 Yizhou                           7    7  +43869      1    -482  -1222
   9 Majkel1337                       9    7  +14357      7    -553   -548
  10 tetsuya & yuanzhe & guoqin      11    4   +4493     10    -614   -665
  11 monsaraida                       7    4  +21673      6    -542   -298
  12 Zenith                          11    3   +8283      8    -374   -456
  worst 5 margins: [(-33054, 115430340, 'M & M & P & Q', 'I'), (-20394, 115431962, 'Unknown Mother', 'x'), (-20149, 115408974, 'M & M & P & Q', 'I'), (-19701, 115430340, 'DSM', 'I'), (-19566, 115425958, 'M & M & P & Q', 'I')]
  lowest tape keep (opp_frac): [(0.0018, 115427471, 'Anton Tikhonov'), (0.0831, 115422295, 'Anton Tikhonov'), (0.21, 115423940, 'Anton Tikhonov'), (0.4311, 115425513, 'Zenith'), (0.4855, 115430326, 'Anton Tikhonov')]
```

### b_bt0_2f0daffb2320  (05:38 UTC) bundle/build/bt0/main.py sha256 2f0daffb2320ba5119928154f5a346aafd530851beeb911da4e48619b10223bf
```
2f0daffb2320ba5119928154f5a346aafd530851beeb911da4e48619b10223bf  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bt0/main.py
123 jobs on 32 cpus
done
b_bt0_2f0daffb2320: n=123 wins 56 (46%) margin +13447 (se 3740) own 116668 opp 103221 | intact 87/123 (71%) intact-only margin -5657 (se 1935) wins 23 | peak step 0.625s, steps>0.6s 1, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bt0_2f0daffb2320 - v183ms: n=123 delta -5768 (se 431) better/worse 3/120 wins 64->56 | own -3270 opp +2498 | both-intact n=84 delta -5378 (se 465)
  paired worst 5: [(-21093, 115424138, 'Unknown Mother'), (-19958, 115430326, 'Anton Tikhonov'), (-17446, 115381978, 'DECEM'), (-17266, 114944321, 'tetsuya & yuan'), (-16939, 115422295, 'Anton Tikhonov')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -3021      8   -4647  -5480
   2 DSM                             15    7   +4932     12   -4972  -4850
   3 DECEM                           11    8  +44099      5   -6348  -4227
   4 Vadim Vasilenko                 11    7   +7626      8   -5021  -4256
   5 Victor @ Tufa Labs              11    5   +5878      9   -5038  -3944
   6 Unknown Mother-Goose            12    0  -13562     11   -5140  -5210
   7 Anton Tikhonov                   7    6  +96036      2   -8597  -3067
   8 Yizhou                           7    7  +42198      1   -2152  -1467
   9 Majkel1337                       9    5  +10148      7   -4763  -4954
  10 tetsuya & yuanzhe & guoqin      11    3   -3399     10   -8505  -7791
  11 monsaraida                       7    4  +13661      6   -8554  -8638
  12 Zenith                          11    2   +2288      8   -6370  -5747
  worst 5 margins: [(-36519, 115430340, 'M & M & P & Q', 'I'), (-33565, 114944321, 'tetsuya & yuan', 'I'), (-26254, 115425958, 'M & M & P & Q', 'I'), (-25482, 115430334, 'M & M & P & Q', 'I'), (-24671, 115420975, 'DSM', 'I')]
  lowest tape keep (opp_frac): [(0.0019, 115427471, 'Anton Tikhonov'), (0.0825, 115422295, 'Anton Tikhonov'), (0.2087, 115423940, 'Anton Tikhonov'), (0.4348, 115425513, 'Zenith'), (0.4933, 115430326, 'Anton Tikhonov')]
```

### b_bt2_9013154d431b  (05:39 UTC) bundle/build/bt2/main.py sha256 9013154d431b4ee5447f7b627fe96af9d061f338bb41c010f887feacfbe5c340
```
9013154d431b4ee5447f7b627fe96af9d061f338bb41c010f887feacfbe5c340  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bt2/main.py
123 jobs on 32 cpus
done
b_bt2_9013154d431b: n=123 wins 55 (45%) margin +14271 (se 3709) own 117400 opp 103129 | intact 87/123 (71%) intact-only margin -4513 (se 1985) wins 22 | peak step 0.413s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bt2_9013154d431b - v183ms: n=123 delta -4944 (se 468) better/worse 9/114 wins 64->55 | own -2538 opp +2406 | both-intact n=84 delta -4097 (se 496)
  paired worst 5: [(-21985, 115428651, 'Anton Tikhonov'), (-21695, 115430340, 'DSM'), (-21133, 115392457, 'DECEM'), (-21015, 114944321, 'tetsuya & yuan'), (-17605, 115387741, 'DECEM')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -3995      8   -5620  -6892
   2 DSM                             15    6   +4530     12   -5373  -5531
   3 DECEM                           11    8  +41549      5   -8898  -4184
   4 Vadim Vasilenko                 11    7   +9054      8   -3592  -2649
   5 Victor @ Tufa Labs              11    5   +7419      9   -3497  -2970
   6 Unknown Mother-Goose            12    0  -11334     11   -2912  -3002
   7 Anton Tikhonov                   7    6  +95306      2   -9328  -1449
   8 Yizhou                           7    7  +42163      1   -2188  -4438
   9 Majkel1337                       9    5  +10777      7   -4134  -3668
  10 tetsuya & yuanzhe & guoqin      11    3    -523     10   -5629  -4646
  11 monsaraida                       7    4  +16791      6   -5424  -4699
  12 Zenith                          11    2   +5274      8   -3383  -3078
  worst 5 margins: [(-47276, 115430340, 'M & M & P & Q', 'I'), (-39451, 115430340, 'DSM', 'I'), (-37314, 114944321, 'tetsuya & yuan', 'I'), (-30223, 115425958, 'M & M & P & Q', 'I'), (-24585, 115430334, 'M & M & P & Q', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0805, 115422295, 'Anton Tikhonov'), (0.2082, 115423940, 'Anton Tikhonov'), (0.4275, 115425513, 'Zenith'), (0.4909, 115430326, 'Anton Tikhonov')]
```

### b_bx_b6687a421a0b  (05:40 UTC) bundle/build/bx/main.py sha256 b6687a421a0b36677d1db23453832fb5a90f3e16f06da29fdf4de43c9e68b924
```
b6687a421a0b36677d1db23453832fb5a90f3e16f06da29fdf4de43c9e68b924  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bx/main.py
123 jobs on 32 cpus
done
b_bx_b6687a421a0b: n=123 wins 55 (45%) margin +16210 (se 3905) own 118281 opp 102071 | intact 86/123 (70%) intact-only margin -3851 (se 2045) wins 21 | peak step 0.387s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bx_b6687a421a0b - v183ms: n=123 delta -3005 (se 189) better/worse 4/119 wins 64->55 | own -1657 opp +1348 | both-intact n=84 delta -3481 (se 242)
  paired worst 5: [(-11597, 115430340, 'M & M & P & Q'), (-11468, 115430340, 'DSM'), (-7974, 115387741, 'Unknown Mother'), (-7811, 115413553, 'DSM'), (-7475, 114944321, 'tetsuya & yuan')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -1620      8   -3246  -4386
   2 DSM                             15    6   +6057     12   -3847  -4278
   3 DECEM                           11    8  +47858      5   -2590  -3720
   4 Vadim Vasilenko                 11    7  +10147      7   -2499  -3025
   5 Victor @ Tufa Labs              11    5   +7679      9   -3237  -3472
   6 Unknown Mother-Goose            12    0  -11991     11   -3568  -3537
   7 Anton Tikhonov                   7    6 +101550      2   -3084  -3376
   8 Yizhou                           7    7  +42619      1   -1732  -3919
   9 Majkel1337                       9    5  +12564      7   -2346  -2306
  10 tetsuya & yuanzhe & guoqin      11    3   +2530     10   -2577  -2840
  11 monsaraida                       7    4  +19348      6   -2867  -2721
  12 Zenith                          11    2   +5155      8   -3502  -3888
  worst 5 margins: [(-41808, 115430340, 'M & M & P & Q', 'I'), (-29224, 115430340, 'DSM', 'I'), (-23774, 114944321, 'tetsuya & yuan', 'I'), (-23210, 115425958, 'M & M & P & Q', 'I'), (-22773, 115381978, 'DSM', 'I')]
  lowest tape keep (opp_frac): [(0.0018, 115427471, 'Anton Tikhonov'), (0.0838, 115422295, 'Anton Tikhonov'), (0.2085, 115423940, 'Anton Tikhonov'), (0.4342, 115425513, 'Zenith'), (0.4875, 115430326, 'Anton Tikhonov')]
```

### b_bz_72fd4924c944  (05:42 UTC) bundle/build/bz/main.py sha256 72fd4924c9445a2877a390b1252be8cf98560652c4fe1401db46ca95e6fb65df
```
72fd4924c9445a2877a390b1252be8cf98560652c4fe1401db46ca95e6fb65df  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bz/main.py
123 jobs on 32 cpus
done
b_bz_72fd4924c944: n=123 wins 64 (52%) margin +19213 (se 3849) own 119938 opp 100725 | intact 84/123 (68%) intact-only margin -1942 (se 1689) wins 28 | peak step 0.384s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bz_72fd4924c944 - v183ms: n=123 delta -3 (se 3) better/worse 3/7 wins 64->64 | own +0 opp +3 | both-intact n=84 delta -5 (se 4)
  paired worst 5: [(-229, 115390479, 'Victor @ Tufa '), (-217, 115427326, 'Zenith'), (-74, 115417660, 'Vadim Vasilenk'), (-24, 115411632, 'Vadim Vasilenk'), (-23, 115428247, 'Majkel1337')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   +1626      8      +0     +0
   2 DSM                             15    8   +9904     12      +0     +0
   3 DECEM                           11    8  +50447      4      +0     +0
   4 Vadim Vasilenko                 11    7  +12638      7      -9    -11
   5 Victor @ Tufa Labs              11    6  +10904      9     -12    -15
   6 Unknown Mother-Goose            12    1   -8424     11      -2     -2
   7 Anton Tikhonov                   7    7 +104651      2     +18     +0
   8 Yizhou                           7    7  +44350      1      +0     +0
   9 Majkel1337                       9    8  +14908      7      -3     -3
  10 tetsuya & yuanzhe & guoqin      11    4   +5111      9      +4     +5
  11 monsaraida                       7    4  +22215      6      +0     +0
  12 Zenith                          11    2   +8637      8     -20    -27
  worst 5 margins: [(-30211, 115430340, 'M & M & P & Q', 'I'), (-20417, 115408974, 'M & M & P & Q', 'I'), (-18673, 115431962, 'Unknown Mother', 'x'), (-18098, 115422937, 'Vadim Vasilenk', 'I'), (-17869, 115425958, 'M & M & P & Q', 'I')]
  lowest tape keep (opp_frac): [(0.0018, 115427471, 'Anton Tikhonov'), (0.0831, 115422295, 'Anton Tikhonov'), (0.2088, 115423940, 'Anton Tikhonov'), (0.4309, 115425513, 'Zenith'), (0.4859, 115430326, 'Anton Tikhonov')]
```

### b_bd_ac3ee2b1a55e  (05:54 UTC) bundle/build/bd/main.py sha256 ac3ee2b1a55e77d3d596b8d47989be2a778a258d0d1127a73956af13604d93bd
```
ac3ee2b1a55e77d3d596b8d47989be2a778a258d0d1127a73956af13604d93bd  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bd/main.py
123 jobs on 32 cpus
done
b_bd_ac3ee2b1a55e: n=123 wins 57 (46%) margin +17402 (se 3888) own 121791 opp 104390 | intact 87/123 (71%) intact-only margin -3085 (se 1862) wins 23 | peak step 1.363s, steps>0.6s 1722, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bd_ac3ee2b1a55e - v183ms: n=123 delta -1813 (se 171) better/worse 15/108 wins 64->57 | own +1854 opp +3667 | both-intact n=84 delta -2177 (se 193)
  paired worst 5: [(-8720, 115413553, 'DSM'), (-8143, 115425958, 'DSM'), (-6273, 115428247, 'Unknown Mother'), (-5822, 115423940, 'Anton Tikhonov'), (-5457, 115430340, 'M & M & P & Q')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2     -93      8   -1719  -2262
   2 DSM                             15    6   +6761     12   -3143  -3361
   3 DECEM                           11    8  +49870      5    -578  -1522
   4 Vadim Vasilenko                 11    7  +10497      8   -2150  -1673
   5 Victor @ Tufa Labs              11    5  +10019      9    -897  -1385
   6 Unknown Mother-Goose            12    0  -11253     11   -2831  -3205
   7 Anton Tikhonov                   7    7 +102163      2   -2471  -1608
   8 Yizhou                           7    7  +43631      1    -719  -2702
   9 Majkel1337                       9    6  +13329      7   -1581  -1773
  10 tetsuya & yuanzhe & guoqin      11    3   +3772      9   -1335  -1443
  11 monsaraida                       7    4  +20441      6   -1774  -1698
  12 Zenith                          11    2   +6885      9   -1772  -2177
  worst 5 margins: [(-35668, 115430340, 'M & M & P & Q', 'I'), (-22069, 115425958, 'M & M & P & Q', 'I'), (-20522, 115381978, 'DSM', 'I'), (-20066, 115408974, 'M & M & P & Q', 'I'), (-19314, 115430340, 'DSM', 'I')]
  lowest tape keep (opp_frac): [(0.0018, 115427471, 'Anton Tikhonov'), (0.0841, 115422295, 'Anton Tikhonov'), (0.2118, 115423940, 'Anton Tikhonov'), (0.4362, 115425513, 'Zenith'), (0.4925, 115430326, 'Anton Tikhonov')]
```

### b_bdf_178f99f8ebda  (06:00 UTC) bundle/build/bdf/main.py sha256 178f99f8ebdaf01830fde0edadd2928e0b5f23bba1a34761eb7506ec85621e35
```
178f99f8ebdaf01830fde0edadd2928e0b5f23bba1a34761eb7506ec85621e35  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bdf/main.py
123 jobs on 32 cpus
done
b_bdf_178f99f8ebda: n=123 wins 57 (46%) margin +16044 (se 3804) own 120755 opp 104711 | intact 88/123 (72%) intact-only margin -3594 (se 1898) wins 24 | peak step 1.442s, steps>0.6s 1415, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bdf_178f99f8ebda - v183ms: n=123 delta -3171 (se 303) better/worse 14/109 wins 64->57 | own +817 opp +3988 | both-intact n=84 delta -3234 (se 288)
  paired worst 5: [(-17521, 115417660, 'DECEM'), (-12799, 115423940, 'Anton Tikhonov'), (-12003, 115430340, 'DSM'), (-11802, 115430340, 'M & M & P & Q'), (-10941, 115392457, 'DECEM')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -1693      8   -3319  -3569
   2 DSM                             15    6   +5456     12   -4448  -4629
   3 DECEM                           11    8  +46755      5   -3693  -3036
   4 Vadim Vasilenko                 11    7   +9000      8   -3646  -3373
   5 Victor @ Tufa Labs              11    5   +8279      9   -2637  -2961
   6 Unknown Mother-Goose            12    0  -11440     11   -3017  -3408
   7 Anton Tikhonov                   7    7  +99835      2   -4798  -1670
   8 Yizhou                           7    7  +43433      1    -917  -3705
   9 Majkel1337                       9    6  +13073      7   -1837  -2142
  10 tetsuya & yuanzhe & guoqin      11    3   +2472     10   -2634  -3088
  11 monsaraida                       7    4  +18792      6   -3423  -2714
  12 Zenith                          11    2   +5803      9   -2854  -2698
  worst 5 margins: [(-42013, 115430340, 'M & M & P & Q', 'I'), (-29759, 115430340, 'DSM', 'I'), (-23648, 115427458, 'tetsuya & yuan', 'I'), (-22069, 115425958, 'M & M & P & Q', 'I'), (-20522, 115381978, 'DSM', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0808, 115422295, 'Anton Tikhonov'), (0.2116, 115423940, 'Anton Tikhonov'), (0.4317, 115425513, 'Zenith'), (0.4877, 115430326, 'Anton Tikhonov')]
```

### b_blt3_30560e432c14  (06:02 UTC) bundle/build/blt3/main.py sha256 30560e432c1413da8fd0252a8db3033fbeba23bf2e6efaeefc009dfc841b3ea4
```
30560e432c1413da8fd0252a8db3033fbeba23bf2e6efaeefc009dfc841b3ea4  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/blt3/main.py
123 jobs on 32 cpus
done
b_blt3_30560e432c14: n=123 wins 56 (46%) margin +15931 (se 3906) own 118243 opp 102313 | intact 88/123 (72%) intact-only margin -4394 (se 1846) wins 22 | peak step 0.681s, steps>0.6s 1, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_blt3_30560e432c14 - v183ms: n=123 delta -3284 (se 352) better/worse 20/103 wins 64->56 | own -1694 opp +1590 | both-intact n=84 delta -3232 (se 396)
  paired worst 5: [(-12516, 115425957, 'DSM'), (-11192, 115430326, 'Unknown Mother'), (-10608, 115381978, 'DECEM'), (-9942, 115425957, 'Unknown Mother'), (-9406, 115428924, 'DECEM')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -1204      8   -2830  -3003
   2 DSM                             15    7   +6272     12   -3631  -3141
   3 DECEM                           11    8  +45697      5   -4750  -6361
   4 Vadim Vasilenko                 11    7  +10811      8   -1836   +246
   5 Victor @ Tufa Labs              11    6   +8539      9   -2377  -2760
   6 Unknown Mother-Goose            12    1  -12746     12   -4323  -4163
   7 Anton Tikhonov                   7    6 +101940      2   -2693  -4792
   8 Yizhou                           7    7  +39919      1   -4431  +4883
   9 Majkel1337                       9    4  +12278      7   -2632  -2458
  10 tetsuya & yuanzhe & guoqin      11    2   +1548      9   -3559  -3609
  11 monsaraida                       7    4  +19711      6   -2504  -5118
  12 Zenith                          11    2   +5232      9   -3426  -3793
  worst 5 margins: [(-32694, 115430340, 'M & M & P & Q', 'I'), (-24843, 115408974, 'M & M & P & Q', 'I'), (-24764, 115431962, 'Unknown Mother', 'I'), (-23428, 115425958, 'M & M & P & Q', 'I'), (-22051, 115413582, 'M & M & P & Q', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0812, 115422295, 'Anton Tikhonov'), (0.2105, 115423940, 'Anton Tikhonov'), (0.4301, 115425513, 'Zenith'), (0.4891, 115430326, 'Anton Tikhonov')]
```

### b_bt3_c9019e891263  (06:03 UTC) bundle/build/bt3/main.py sha256 c9019e8912635067c0cc87f97ff356d6d405320cf9282b2c0fef1f8479c39a1e
```
c9019e8912635067c0cc87f97ff356d6d405320cf9282b2c0fef1f8479c39a1e  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bt3/main.py
123 jobs on 32 cpus
done
b_bt3_c9019e891263: n=123 wins 55 (45%) margin +14688 (se 3717) own 117735 opp 103047 | intact 87/123 (71%) intact-only margin -4140 (se 1974) wins 22 | peak step 0.449s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bt3_c9019e891263 - v183ms: n=123 delta -4527 (se 450) better/worse 10/113 wins 64->55 | own -2203 opp +2324 | both-intact n=84 delta -3751 (se 463)
  paired worst 5: [(-21985, 115428651, 'Anton Tikhonov'), (-21695, 115430340, 'DSM'), (-21133, 115392457, 'DECEM'), (-17605, 115387741, 'DECEM'), (-17065, 115430340, 'M & M & P & Q')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -3730      8   -5356  -6892
   2 DSM                             15    6   +4519     12   -5384  -5545
   3 DECEM                           11    8  +41400      5   -9048  -4184
   4 Vadim Vasilenko                 11    7   +9394      8   -3252  -2099
   5 Victor @ Tufa Labs              11    5   +7472      9   -3444  -2971
   6 Unknown Mother-Goose            12    0  -11233     11   -2811  -2892
   7 Anton Tikhonov                   7    6  +96420      2   -8213  -1449
   8 Yizhou                           7    7  +42212      1   -2139  -4473
   9 Majkel1337                       9    5  +10777      7   -4134  -3668
  10 tetsuya & yuanzhe & guoqin      11    3   +2442     10   -2665  -2449
  11 monsaraida                       7    4  +16750      6   -5465  -4446
  12 Zenith                          11    2   +5661      8   -2996  -2713
  worst 5 margins: [(-47276, 115430340, 'M & M & P & Q', 'I'), (-39451, 115430340, 'DSM', 'I'), (-30223, 115425958, 'M & M & P & Q', 'I'), (-24585, 115430334, 'M & M & P & Q', 'I'), (-23767, 115413582, 'M & M & P & Q', 'I')]
  lowest tape keep (opp_frac): [(0.0, 115427471, 'Anton Tikhonov'), (0.0804, 115422295, 'Anton Tikhonov'), (0.2089, 115423940, 'Anton Tikhonov'), (0.4275, 115425513, 'Zenith'), (0.492, 115430326, 'Anton Tikhonov')]
```

### b_bt3n_016a0cc722ce  (06:04 UTC) bundle/build/bt3n/main.py sha256 016a0cc722cee2790db24737b2fc0704564f505361a490ed8ebd012ccef603b9
```
016a0cc722cee2790db24737b2fc0704564f505361a490ed8ebd012ccef603b9  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/bt3n/main.py
123 jobs on 32 cpus
done
b_bt3n_016a0cc722ce: n=123 wins 56 (46%) margin +14730 (se 3762) own 117623 opp 102893 | intact 87/123 (71%) intact-only margin -4386 (se 1943) wins 23 | peak step 0.392s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_bt3n_016a0cc722ce - v183ms: n=123 delta -4485 (se 331) better/worse 4/119 wins 64->56 | own -2315 opp +2170 | both-intact n=84 delta -4138 (se 346)
  paired worst 5: [(-17788, 115381978, 'DECEM'), (-16369, 115387741, 'DECEM'), (-14176, 115422295, 'Anton Tikhonov'), (-12662, 115418160, 'Vadim Vasilenk'), (-12615, 115431863, 'monsaraida')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2   -3154      8   -4780  -5480
   2 DSM                             15    7   +4932     12   -4972  -4850
   3 DECEM                           11    8  +44252      5   -6195  -4228
   4 Vadim Vasilenko                 11    7   +8968      8   -3679  -2552
   5 Victor @ Tufa Labs              11    5   +6750      9   -4166  -3796
   6 Unknown Mother-Goose            12    0  -12246     11   -3824  -3775
   7 Anton Tikhonov                   7    6  +97817      2   -6816  -3067
   8 Yizhou                           7    7  +42294      1   -2057  -1174
   9 Majkel1337                       9    5  +10148      7   -4763  -4954
  10 tetsuya & yuanzhe & guoqin      11    3   +1784     10   -3323  -3539
  11 monsaraida                       7    4  +16290      6   -5925  -5854
  12 Zenith                          11    2   +4912      8   -3745  -3272
  worst 5 margins: [(-36519, 115430340, 'M & M & P & Q', 'I'), (-26254, 115425958, 'M & M & P & Q', 'I'), (-25482, 115430334, 'M & M & P & Q', 'I'), (-24671, 115420975, 'DSM', 'I'), (-23856, 115430340, 'DSM', 'I')]
  lowest tape keep (opp_frac): [(0.0019, 115427471, 'Anton Tikhonov'), (0.0824, 115422295, 'Anton Tikhonov'), (0.2086, 115423940, 'Anton Tikhonov'), (0.4342, 115425513, 'Zenith'), (0.4921, 115430326, 'Anton Tikhonov')]
```

### b_mo3d_8deb5fbe54d0  (06:06 UTC) bundle/build/mo3d/main.py sha256 8deb5fbe54d0c9f2aeaff193957ee3246d80f1d804a19d47658c308eecda172a
```
8deb5fbe54d0c9f2aeaff193957ee3246d80f1d804a19d47658c308eecda172a  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/mo3d/main.py
123 jobs on 32 cpus
done
b_mo3d_8deb5fbe54d0: n=123 wins 24 (20%) margin -509 (se 3050) own 106667 opp 107176 | intact 105/123 (85%) intact-only margin -10718 (se 1634) wins 8 | peak step 0.507s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_mo3d_8deb5fbe54d0 - v183ms: n=123 delta -19724 (se 4709) better/worse 26/97 wins 64->24 | own -13271 opp +6453 | both-intact n=76 delta -8763 (se 1864)
  paired worst 5: [(-200303, 115422295, 'Anton Tikhonov'), (-174473, 115430326, 'Anton Tikhonov'), (-173880, 115423940, 'Anton Tikhonov'), (-145560, 115427471, 'Anton Tikhonov'), (-137137, 115425513, 'Zenith')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    0  -16237     10  -17863   +465
   2 DSM                             15    2   -9028     15  -18932  -6836
   3 DECEM                           11    4   +8991      9  -41457 -25956
   4 Vadim Vasilenko                 11    2   +2108     10  -10539  +2002
   5 Victor @ Tufa Labs              11    2   -4448      9  -15364 -13123
   6 Unknown Mother-Goose            12    0  -14508     12   -6086  -5672
   7 Anton Tikhonov                   7    1  -18107      6 -122740 -25244
   8 Yizhou                           7    2    +774      5  -43576      -
   9 Majkel1337                       9    2    +700      8  -14211  -9788
  10 tetsuya & yuanzhe & guoqin      11    3  +15473      8  +10366 -10784
  11 monsaraida                       7    3  +29397      5   +7182 -22261
  12 Zenith                          11    3   +8314      8    -343  -8268
  worst 5 margins: [(-32948, 115430326, 'Anton Tikhonov', 'I'), (-29693, 115428651, 'Anton Tikhonov', 'I'), (-29308, 115431962, 'Unknown Mother', 'I'), (-27824, 115425939, 'Anton Tikhonov', 'I'), (-27655, 115422295, 'Anton Tikhonov', 'I')]
  lowest tape keep (opp_frac): [(0.2047, 114937790, 'monsaraida'), (0.4624, 115422656, 'Zenith'), (0.471, 114944321, 'tetsuya & yuan'), (0.4943, 115431756, 'tetsuya & yuan'), (0.5033, 115413576, 'Zenith')]
```

### b_mo3d0_72948575b172  (06:07 UTC) bundle/build/mo3d0/main.py sha256 72948575b172ebf9613a0ddd8907ce5ea0fcfeabd79f85c6ea8441b30678ed0f
```
72948575b172ebf9613a0ddd8907ce5ea0fcfeabd79f85c6ea8441b30678ed0f  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/mo3d0/main.py
123 jobs on 32 cpus
done
b_mo3d0_72948575b172: n=123 wins 26 (21%) margin -1932 (se 3086) own 104974 opp 106906 | intact 104/123 (85%) intact-only margin -13258 (se 1463) wins 7 | peak step 0.659s, steps>0.6s 1, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_mo3d0_72948575b172 - v183ms: n=123 delta -21147 (se 4677) better/worse 23/100 wins 64->26 | own -14964 opp +6184 | both-intact n=74 delta -12033 (se 1347)
  paired worst 5: [(-198468, 115422295, 'Anton Tikhonov'), (-171427, 115423940, 'Anton Tikhonov'), (-169069, 115430326, 'Anton Tikhonov'), (-143430, 115427471, 'Anton Tikhonov'), (-137775, 115390459, 'M & M & P & Q')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    0  -18465     11  -20091  -1883
   2 DSM                             15    2  -11072     14  -20975 -11646
   3 DECEM                           11    4   +8384      9  -42064 -26225
   4 Vadim Vasilenko                 11    2      +4      9  -12642 -14072
   5 Victor @ Tufa Labs              11    2   -6473      9  -17389 -15133
   6 Unknown Mother-Goose            12    0  -17160     12   -8737  -7836
   7 Anton Tikhonov                   7    1  -17571      6 -122205 -26271
   8 Yizhou                           7    2    -398      5  -44748      -
   9 Majkel1337                       9    3     +89      8  -14821 -10838
  10 tetsuya & yuanzhe & guoqin      11    3  +15061      8   +9954 -10854
  11 monsaraida                       7    3  +29153      5   +6938 -23638
  12 Zenith                          11    4   +6515      8   -2142  -9055
  worst 5 margins: [(-37325, 115431962, 'Unknown Mother', 'I'), (-35711, 115428651, 'Anton Tikhonov', 'I'), (-27544, 115430326, 'Anton Tikhonov', 'I'), (-26513, 115428924, 'DSM', 'I'), (-25820, 115422295, 'Anton Tikhonov', 'I')]
  lowest tape keep (opp_frac): [(0.2034, 114937790, 'monsaraida'), (0.4635, 115422656, 'Zenith'), (0.4642, 114944321, 'tetsuya & yuan'), (0.4694, 115431756, 'tetsuya & yuan'), (0.5018, 115413576, 'Zenith')]
```

### b_mo3e_45861b58ec25  (06:09 UTC) bundle/build/mo3e/main.py sha256 45861b58ec25d7b683a0c64174816644af430997dd21afd3f782c29016a516e2
```
45861b58ec25d7b683a0c64174816644af430997dd21afd3f782c29016a516e2  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/mo3e/main.py
123 jobs on 32 cpus
done
b_mo3e_45861b58ec25: n=123 wins 36 (29%) margin +2293 (se 2729) own 112016 opp 109723 | intact 107/123 (87%) intact-only margin -6039 (se 1758) wins 21 | peak step 0.446s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_mo3e_45861b58ec25 - v183ms: n=123 delta -16922 (se 4064) better/worse 29/94 wins 64->36 | own -7921 opp +9001 | both-intact n=80 delta -3112 (se 1849)
  paired worst 5: [(-183294, 115422295, 'Anton Tikhonov'), (-160109, 115430326, 'Anton Tikhonov'), (-156343, 115423940, 'Anton Tikhonov'), (-146859, 115390459, 'M & M & P & Q'), (-146020, 115427471, 'Anton Tikhonov')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2  -11010     11  -12635  +9843
   2 DSM                             15    4   -2703     15  -12606  -1983
   3 DECEM                           11    6  +31529      7  -18919  -3729
   4 Vadim Vasilenko                 11    5   -1038     10  -13685  +1469
   5 Victor @ Tufa Labs              11    5   +9001      9   -1915  -2747
   6 Unknown Mother-Goose            12    0  -13843     12   -5421  -4805
   7 Anton Tikhonov                   7    1   -6573      6 -111207 -12998
   8 Yizhou                           7    1   -4200      6  -48550      -
   9 Majkel1337                       9    2   -1558      8  -16469 -16128
  10 tetsuya & yuanzhe & guoqin      11    2   -7120     10  -12226  -5798
  11 monsaraida                       7    7  +62772      3  +40557  +6157
  12 Zenith                          11    1   -8751     10  -17408  -6134
  worst 5 margins: [(-41620, 115417660, 'Vadim Vasilenk', 'I'), (-30861, 115431962, 'Unknown Mother', 'I'), (-28321, 115416427, 'Majkel1337', 'I'), (-26484, 115413582, 'M & M & P & Q', 'I'), (-24889, 115428893, 'Yizhou', 'I')]
  lowest tape keep (opp_frac): [(0.4425, 114937790, 'monsaraida'), (0.5403, 115427408, 'monsaraida'), (0.5512, 115431863, 'monsaraida'), (0.6396, 115428414, 'Victor @ Tufa '), (0.6653, 115419249, 'Victor @ Tufa ')]
```

### b_mo3e0_904ef103fa66  (06:10 UTC) bundle/build/mo3e0/main.py sha256 904ef103fa666ab3b0741ef73df08553d65b89b43da0c70c41e92812b1c72fca
```
904ef103fa666ab3b0741ef73df08553d65b89b43da0c70c41e92812b1c72fca  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/mo3e0/main.py
123 jobs on 32 cpus
done
b_mo3e0_904ef103fa66: n=123 wins 32 (26%) margin -1153 (se 2804) own 109255 opp 110408 | intact 106/123 (86%) intact-only margin -9902 (se 1793) wins 16 | peak step 0.532s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_mo3e0_904ef103fa66 - v183ms: n=123 delta -20368 (se 4165) better/worse 22/101 wins 64->32 | own -10682 opp +9685 | both-intact n=79 delta -7000 (se 1858)
  paired worst 5: [(-194073, 115422295, 'Anton Tikhonov'), (-164261, 115430326, 'Anton Tikhonov'), (-161765, 115423940, 'Anton Tikhonov'), (-148321, 115390459, 'M & M & P & Q'), (-144209, 115427471, 'Anton Tikhonov')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    2  -12229     11  -13855  +9405
   2 DSM                             15    4   -2690     14  -12594  -4127
   3 DECEM                           11    6  +30698      7  -19750  -3566
   4 Vadim Vasilenko                 11    4   -5810     10  -18457  -5524
   5 Victor @ Tufa Labs              11    3   +7805      9   -3111  -4559
   6 Unknown Mother-Goose            12    0  -16149     12   -7726  -7115
   7 Anton Tikhonov                   7    1  -11056      6 -115690 -16300
   8 Yizhou                           7    1   -7957      6  -52308      -
   9 Majkel1337                       9    2   -3488      8  -18398 -18446
  10 tetsuya & yuanzhe & guoqin      11    1  -16493     10  -21600 -14103
  11 monsaraida                       7    7  +54323      3  +32108  -5967
  12 Zenith                          11    1  -15189     10  -23847 -13007
  worst 5 margins: [(-49562, 115416427, 'tetsuya & yuan', 'I'), (-40523, 115417660, 'Vadim Vasilenk', 'I'), (-34021, 115428697, 'Majkel1337', 'I'), (-33770, 115427468, 'Zenith', 'I'), (-33126, 115431962, 'Unknown Mother', 'I')]
  lowest tape keep (opp_frac): [(0.4205, 114937790, 'monsaraida'), (0.5488, 115431863, 'monsaraida'), (0.5563, 115427408, 'monsaraida'), (0.6448, 115428414, 'Victor @ Tufa '), (0.6653, 115419249, 'Victor @ Tufa ')]
```

### b_op_n5d_8dbfc703107d  (06:11 UTC) bundle/build/op_n5d/main.py sha256 8dbfc703107d95d20a590f3618b192f66c263b6562a62d537366bfdb42454c5d
```
8dbfc703107d95d20a590f3618b192f66c263b6562a62d537366bfdb42454c5d  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/op_n5d/main.py
123 jobs on 32 cpus
done
b_op_n5d_8dbfc703107d: n=123 wins 26 (21%) margin +2289 (se 2993) own 108138 opp 105849 | intact 107/123 (87%) intact-only margin -8014 (se 1523) wins 10 | peak step 0.388s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_op_n5d_8dbfc703107d - v183ms: n=123 delta -16926 (se 4658) better/worse 33/90 wins 64->26 | own -11800 opp +5127 | both-intact n=76 delta -6256 (se 1654)
  paired worst 5: [(-195171, 115422295, 'Anton Tikhonov'), (-169965, 115430326, 'Anton Tikhonov'), (-167687, 115423940, 'Anton Tikhonov'), (-139203, 115390459, 'DECEM'), (-138471, 115390459, 'M & M & P & Q')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    0  -14511     11  -16137  +2143
   2 DSM                             15    2   -5651     14  -15555  -6904
   3 DECEM                           11    4  +11371      9  -39076 -20736
   4 Vadim Vasilenko                 11    2   +3471     10   -9176  +2360
   5 Victor @ Tufa Labs              11    2    -992      9  -11908  -9661
   6 Unknown Mother-Goose            12    1  -11754     12   -3331  -2555
   7 Anton Tikhonov                   7    1  -13473      6 -118107 -21810
   8 Yizhou                           7    1   +1711      6  -42639      -
   9 Majkel1337                       9    3   +3832      9  -11078  -6646
  10 tetsuya & yuanzhe & guoqin      11    4  +20172      8  +15066  -7245
  11 monsaraida                       7    3  +30865      5   +8650 -17610
  12 Zenith                          11    3  +11318      8   +2661  -4907
  worst 5 margins: [(-32327, 115390459, 'DECEM', 'I'), (-31402, 115428651, 'Anton Tikhonov', 'I'), (-30537, 115431962, 'Unknown Mother', 'I'), (-28871, 115422436, 'M & M & P & Q', 'I'), (-28440, 115430326, 'Anton Tikhonov', 'I')]
  lowest tape keep (opp_frac): [(0.2037, 114937790, 'monsaraida'), (0.4666, 115422656, 'Zenith'), (0.4672, 114944321, 'tetsuya & yuan'), (0.5025, 115431756, 'tetsuya & yuan'), (0.5231, 115413576, 'Zenith')]
```

### b_op_nd_ca751018801f  (06:13 UTC) bundle/build/op_nd/main.py sha256 ca751018801ffe1b1438ab7f44bcf8b864fdfc0be063645a3e9ac0cfc9ca032c
```
ca751018801ffe1b1438ab7f44bcf8b864fdfc0be063645a3e9ac0cfc9ca032c  /Users/1littlecoder/kaggriculture/research/claude/2900/agents/final30/bundle/build/op_nd/main.py
123 jobs on 32 cpus
done
b_op_nd_ca751018801f: n=123 wins 29 (24%) margin +2091 (se 2965) own 108173 opp 106083 | intact 106/123 (86%) intact-only margin -7726 (se 1605) wins 13 | peak step 0.391s, steps>0.6s 0, non-DONE 0
v183ms: n=123 wins 64 (52%) margin +19215 (se 3849) own 119938 opp 100723 | intact 84/123 (68%) intact-only margin -1937 (se 1689) wins 28 | peak step 0.434s, steps>0.6s 0, non-DONE 0
PAIRED b_op_nd_ca751018801f - v183ms: n=123 delta -17124 (se 4652) better/worse 32/91 wins 64->29 | own -11764 opp +5360 | both-intact n=77 delta -6010 (se 1773)
  paired worst 5: [(-198468, 115422295, 'Anton Tikhonov'), (-171427, 115423940, 'Anton Tikhonov'), (-169069, 115430326, 'Anton Tikhonov'), (-143430, 115427471, 'Anton Tikhonov'), (-140212, 115425513, 'Zenith')]
  rank team                            n wins  margin intact  paired  b-int
   1 M & M & P & Q                   11    0  -13171     10  -14797  +3776
   2 DSM                             15    2   -6638     15  -16542  -4879
   3 DECEM                           11    4  +12030      9  -38417 -22688
   4 Vadim Vasilenko                 11    2   +3343     10   -9304  +1768
   5 Victor @ Tufa Labs              11    2   -2292      9  -13208  -9943
   6 Unknown Mother-Goose            12    1  -11674     12   -3252  -2469
   7 Anton Tikhonov                   7    1  -14709      6 -119342 -20164
   8 Yizhou                           7    3   +6078      5  -38272      -
   9 Majkel1337                       9    3   +3416      9  -11495  -6048
  10 tetsuya & yuanzhe & guoqin      11    3  +19167      8  +14061  -7634
  11 monsaraida                       7    3  +30044      5   +7829 -18358
  12 Zenith                          11    5   +9670      8   +1013  -6082
  worst 5 margins: [(-30537, 115431962, 'Unknown Mother', 'I'), (-27887, 115428651, 'Anton Tikhonov', 'I'), (-27544, 115430326, 'Anton Tikhonov', 'I'), (-25820, 115422295, 'Anton Tikhonov', 'I'), (-23643, 115431833, 'DECEM', 'I')]
  lowest tape keep (opp_frac): [(0.2072, 114937790, 'monsaraida'), (0.4672, 114944321, 'tetsuya & yuan'), (0.4689, 115422656, 'Zenith'), (0.498, 115431756, 'tetsuya & yuan'), (0.5383, 115413576, 'Zenith')]
```
