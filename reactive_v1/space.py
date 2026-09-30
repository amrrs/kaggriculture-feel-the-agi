"""rx parameter space for CMA-ES (z in [-1,1], 0 = current P value). kind: lin | log | int.
Edit KNOBS to add/remove dimensions; decode(z) -> {param: value} for mkvar.py / P.update."""
import math
KNOBS = [  # (name, kind, lo, hi) around the current default
    ('LAM', 'log', 15.0, 45.0), ('VCAP', 'log', 120.0, 320.0), ('URG_B', 'log', 120.0, 500.0), ('ADMIT_K', 'lin', 0.45, 0.8),
    ('FEED_V', 'log', 30.0, 150.0), ('CARE_K', 'lin', 0.6, 1.5), ('HV_K', 'lin', 0.3, 1.0), ('COL_K', 'lin', 0.5, 1.2),
    ('EFF', 'lin', 0.75, 1.05), ('A_L', 'lin', 3.0, 5.5), ('C_L', 'lin', 1.4, 2.5), ('W_L', 'lin', 1.5, 2.8),
    ('HC0', 'lin', 3.0, 7.0), ('HS0', 'lin', 2.0, 5.0), ('HG0', 'lin', 1.5, 6.0), ('HERD_MIN', 'log', 200.0, 1500.0),
    ('W_MIN', 'int', 0, 36), ('S10_0', 'lin', 10.0, 22.0), ('T0', 'lin', 5.0, 16.0), ('CAR_K', 'lin', 0.8, 1.4),
    ('DROP_MIN', 'log', 40.0, 300.0), ('DROP_K', 'log', 0.05, 0.4), ('W_RES', 'lin', 0.0, 1.0), ('FEED_URG_H', 'int', 10, 20),
]
def decode(z, P0):
    out = {}
    for (name, kind, lo, hi), v in zip(KNOBS, z):
        b = P0[name]; v = max(-1.0, min(1.0, float(v)))
        tgt = hi if v > 0 else lo; a = abs(v)
        if kind == 'log' and b > 0 and tgt > 0: x = math.exp(math.log(b) + a * (math.log(tgt) - math.log(b)))
        else: x = b + a * (tgt - b)
        out[name] = int(round(x)) if kind == 'int' else round(x, 4)
    return out
